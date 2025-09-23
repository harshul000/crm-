import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from urllib.parse import quote_plus
from datetime import datetime
from twilio.rest import Client

app = Flask(__name__)

# --- Logging Configuration ---
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Admin Dashboard application starting up...')

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db_user = 'admin_user'
db_pass_raw = 'Str0ngP@ssw0rd!_2025'
db_pass_encoded = quote_plus(db_pass_raw)
db_name = 'admin_dashboard_db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass_encoded}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key'

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'AC435bf8efd9e006d217974626ad79289a')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '04d269df3a1b10c899877a76ad6fef1b')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
ADMIN_WHATSAPP_TO = os.environ.get('ADMIN_WHATSAPP_TO', 'whatsapp:+917023145266')
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

db = SQLAlchemy(app)

# --- Database Models ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    advance_paid = db.Column(db.Float, nullable=False)
    amount_remaining = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.Date, nullable=True)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_whatsapp_alert(order):
    app.logger.info(f"Attempting to send WhatsApp alert for Order ID: {order.id} to {ADMIN_WHATSAPP_TO}")
    try:
        product_name = order.product.name
        customer = order.customer_name
        total = order.total_amount
        advance = order.advance_paid
        message_body = (
            f"🎉 *New Order Alert!* 🎉\n\n"
            f"*Product:* {product_name}\n"
            f"*Customer:* {customer}\n"
            f"*Total Amount:* ₹{total:,.2f}\n"
            f"*Advance Paid:* ₹{advance:,.2f}\n\n"
            f"Check the dashboard for more details."
        )
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            body=message_body,
            to=ADMIN_WHATSAPP_TO
        )
        app.logger.info(f"WhatsApp alert sent successfully for Order ID: {order.id}. Message SID: {message.sid}")
        flash('Order created and WhatsApp alert sent!', 'success')
    except Exception as e:
        app.logger.error(f"Failed to send WhatsApp alert for Order ID: {order.id}. Error: {e}", exc_info=True)
        flash('Order created, but failed to send WhatsApp alert. Check logs for details.', 'danger')

# --- Routes ---
@app.route('/')
def index():
    orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    total_orders = Order.query.count()
    total_advance = db.session.query(db.func.sum(Order.advance_paid)).scalar() or 0
    total_remaining = db.session.query(db.func.sum(Order.amount_remaining)).scalar() or 0
    return render_template('index.html', orders=orders, total_orders=total_orders, total_advance=total_advance, total_remaining=total_remaining)

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        if 'product_image' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['product_image']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product = Product(
                name=request.form['product_name'],
                price=float(request.form['product_price']),
                image_filename=filename
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        else:
            flash('Allowed image types are png, jpg, jpeg, gif', 'danger')
            return redirect(request.url)

    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)
    associated_orders = Order.query.filter_by(product_id=product_to_delete.id).count()
    if associated_orders > 0:
        flash(f'Cannot delete "{product_to_delete.name}" because it is used in {associated_orders} order(s). Please remove associated orders first.', 'danger')
        return redirect(url_for('products'))
    try:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product_to_delete.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        app.logger.info(f"Deleted image file for product: {product_to_delete.name}")
    except Exception as e:
        app.logger.error(f"Error deleting image file for product ID {product_to_delete.id}: {e}")
        flash('Error removing the product image file, but the database record will be deleted.', 'warning')
    db.session.delete(product_to_delete)
    db.session.commit()
    app.logger.info(f"Deleted product from database: {product_to_delete.name}")
    flash(f'Product "{product_to_delete.name}" was successfully deleted!', 'success')
    return redirect(url_for('products'))

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        product_id = request.form['product_id']
        total_amount = float(request.form['total_amount'])
        advance_paid = float(request.form['advance_paid'])
        delivery_date_str = request.form.get('delivery_date')
        delivery_date_obj = None
        if delivery_date_str:
            delivery_date_obj = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        new_order = Order(
            product_id=product_id,
            customer_name=request.form['customer_name'],
            total_amount=total_amount,
            advance_paid=advance_paid,
            amount_remaining=total_amount - advance_paid,
            delivery_date=delivery_date_obj
        )
        db.session.add(new_order)
        db.session.commit()
        send_whatsapp_alert(new_order)
        return redirect(url_for('orders'))
    all_products = Product.query.all()
    all_orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('orders.html', products=all_products, orders=all_orders)

# NEW (DELETE ORDER): This new route handles deleting an order from the database.
@app.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order_to_delete = Order.query.get_or_404(order_id)
    db.session.delete(order_to_delete)
    db.session.commit()
    flash(f'Order #{order_to_delete.id} has been successfully deleted.', 'success')
    # This will redirect back to the page the user was on (either index or orders)
    return redirect(request.referrer or url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/api/orders')
def api_orders():
    orders = Order.query.all()
    events = []
    for order in orders:
        if order.delivery_date:
            events.append({
                'title': order.customer_name,
                'start': order.delivery_date.isoformat(),
                'allDay': True,
                'extendedProps': {
                    'productName': order.product.name,
                    'totalAmount': f'{order.total_amount:.2f}'
                },
                'backgroundColor': '#3b82f6',
                'borderColor': '#3b82f6'
            })
    return jsonify(events)

@app.route('/logs')
def view_logs():
    try:
        with open('app.log', 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "Log file not found."
    return render_template('logs.html', log_content=log_content)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

