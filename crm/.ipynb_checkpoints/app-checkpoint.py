import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from urllib.parse import quote_plus
from datetime import datetime
from twilio.rest import Client

# PRODUCTION CHANGE: The Flask app instance needs to be easily importable.
# We create it at the top level.
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

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'AC435bf8efd9e006d217974626ad79289a')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'd147526963dd674c7bc5ba891b8e4952')
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
    customer_mobile = db.Column(db.String(20), nullable=True)
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
        message_body = (f"🎉 *New Order Alert!* 🎉\n\n"
                        f"*Product:* {order.product.name}\n"
                        f"*Customer:* {order.customer_name}\n"
                        f"*Total Amount:* ₹{order.total_amount:,.2f}\n"
                        f"*Advance Paid:* ₹{order.advance_paid:,.2f}\n\n")
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM, body=message_body, to=ADMIN_WHATSAPP_TO)
        app.logger.info(f"WhatsApp alert sent successfully for Order ID: {order.id}. Message SID: {message.sid}")
    except Exception as e:
        app.logger.error(f"Failed to send WhatsApp alert for Order ID: {order.id}. Error: {e}", exc_info=True)

# --- Routes (Unchanged) ---
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
            new_product = Product(name=request.form['product_name'], price=float(request.form['product_price']), image_filename=filename)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)
    if product_to_delete.orders:
        flash('Cannot delete product because it has existing orders. Please delete the associated orders first.', 'danger')
        return redirect(url_for('products'))
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product_to_delete.image_filename))
    except OSError:
        pass
    db.session.delete(product_to_delete)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('products'))

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        delivery_date_str = request.form.get('delivery_date')
        new_order = Order(
            product_id=request.form['product_id'],
            customer_name=request.form['customer_name'],
            customer_mobile=request.form.get('customer_mobile'),
            total_amount=float(request.form['total_amount']),
            advance_paid=float(request.form['advance_paid']),
            amount_remaining=float(request.form['total_amount']) - float(request.form['advance_paid']),
            delivery_date=datetime.strptime(delivery_date_str, '%Y-%m-%d').date() if delivery_date_str else None
        )
        db.session.add(new_order)
        db.session.commit()
        send_whatsapp_alert(new_order)
        flash('Order created successfully and notification sent!', 'success')
        return redirect(url_for('orders'))
    all_orders = Order.query.order_by(Order.order_date.desc()).all()
    products_for_dropdown = Product.query.all()
    return render_template('orders.html', orders=all_orders, products=products_for_dropdown)

@app.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order_to_delete = Order.query.get_or_404(order_id)
    db.session.delete(order_to_delete)
    db.session.commit()
    flash('Order deleted successfully.', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/api/orders')
def api_orders():
    orders = Order.query.all()
    events = []
    for order in orders:
        if order.delivery_date:
            events.append({'title': f"#{order.id}: {order.product.name}", 'start': order.delivery_date.isoformat(), 'description': f"Customer: {order.customer_name}<br>Total: ₹{order.total_amount}"})
    return jsonify(events)

@app.route('/logs')
def view_logs():
    try:
        with open('app.log', 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        log_content = "Log file not found."
    return render_template('logs.html', log_content=log_content)

# PRODUCTION CHANGE: The `if __name__ == '__main__':` block is removed.
# Gunicorn will start the app, so we no longer need this part for development.
# You can keep it if you want to switch between development and production,
# but it's cleaner to remove it for a production-only setup.

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, host='0.0.0.0', port=5000)

