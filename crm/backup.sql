-- MySQL dump 10.13  Distrib 8.4.6, for Linux (x86_64)
--
-- Host: localhost    Database: admin_dashboard_db
-- ------------------------------------------------------
-- Server version	8.4.6-0ubuntu0.25.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `customer_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_amount` float NOT NULL,
  `advance_paid` float NOT NULL,
  `amount_remaining` float NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `customer_mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (49,30,'Sanidhya ',1200,1200,0,'Pending','2025-09-22 07:35:04',NULL,NULL),(70,35,' Nisha ',1000,500,500,'Pending','2025-10-10 13:01:16','2025-11-28','6375179296'),(72,29,'Nisha',1000,0,1000,'Pending','2025-10-13 10:35:03','2025-11-30','6375179296'),(74,37,'Nisha',2000,0,2000,'Pending','2025-10-19 11:29:15','2025-11-28',''),(76,27,'Nisha ',1700,1000,700,'Pending','2025-10-19 11:31:57','2025-11-30',''),(77,38,'Anu',1900,1000,900,'Pending','2025-10-26 06:52:11','2025-11-28','9358448600'),(78,39,'Tanisha ',1250,1250,0,'Pending','2025-10-26 06:56:46','2025-12-09','7357573127'),(79,30,'Tanisa',1000,1000,0,'Pending','2025-10-26 07:17:18','2025-12-10','-'),(80,40,'Garima ',1700,500,1200,'Pending','2025-10-28 07:18:58','2025-11-30','8058854189'),(81,34,'Teju',1600,0,1600,'Pending','2025-10-28 13:52:15','2025-11-23','8279240017'),(82,30,'Teju',1300,0,1300,'Pending','2025-10-28 13:52:58','2025-11-23',''),(84,43,'Kinni',1400,0,1400,'Pending','2025-10-28 14:00:11','2025-11-30',''),(85,42,'Kinni',1400,0,1400,'Pending','2025-10-28 14:01:37','2025-11-30',''),(86,36,'Kinni',1400,0,1400,'Pending','2025-10-28 14:03:18','2025-12-11','855755424'),(87,30,'Divya dangi',1500,500,1000,'Pending','2025-10-29 13:28:59','2025-11-29','9696944298'),(88,44,'Divya dangi ',2000,500,1500,'Pending','2025-10-29 13:31:41','2025-11-29',''),(89,44,'Jigyasa',2500,1000,1500,'Pending','2025-11-03 11:25:35','2025-11-30','8005529985'),(90,45,'Priyanka',1500,500,1000,'Pending','2025-11-03 11:28:31','2025-11-30','800548381'),(92,34,'Gouri ',1400,500,900,'Pending','2025-11-06 08:08:40','2025-11-30','7878007646'),(93,46,'Gouri',1300,500,800,'Pending','2025-11-06 08:11:39','2025-11-29','7878007646'),(94,34,'Namrata',1700,500,1200,'Pending','2025-11-06 11:14:55','2025-11-28','8769446043'),(95,21,'Himanshi',1300,1300,0,'Pending','2025-11-06 11:20:23','2025-12-02','7976414028'),(96,6,'Nisha',1700,1000,700,'Pending','2025-11-06 11:23:18','2025-11-30','9588911831'),(97,9,'Mumal',1500,0,1500,'Pending','2025-11-06 14:01:31','2025-12-02','6358128452'),(98,40,'Mumal ',2500,0,2500,'Pending','2025-11-06 14:02:41','2025-12-02',''),(99,36,'Mumal',1500,0,1500,'Pending','2025-11-06 14:05:31','2025-12-04',''),(100,47,'Anshu sister',1800,0,1800,'Pending','2025-11-08 12:50:27','2025-12-05',''),(101,48,'Karishma',1000,1000,0,'Pending','2025-11-09 10:36:21','2025-11-24','8824268488'),(105,49,'Nikita',1800,500,1300,'Pending','2025-11-11 14:00:20','2025-11-30','894980196'),(106,50,'Yuktika 10,11,12,',1300,500,800,'Pending','2025-11-12 08:30:30','2025-12-10','9672520020'),(107,51,'Priyanka',1400,500,900,'Pending','2025-11-12 12:47:33','2025-11-21','9352196616'),(108,34,'Dolly ',1700,500,1200,'Pending','2025-11-12 13:55:04','2025-12-04','9251168031'),(109,41,'Dolly',1000,500,500,'Pending','2025-11-12 14:03:55','2025-12-02',''),(110,30,'Dolly',1000,500,500,'Pending','2025-11-13 05:19:12',NULL,''),(112,27,'Tina',1400,500,900,'Pending','2025-11-14 11:32:46','2025-11-17','7240195920 '),(113,30,'Bhoik 7,8,9',1300,600,700,'Pending','2025-11-14 12:16:24','2025-12-07','8233093928'),(114,39,'Harshita 27 ,28',0,0,0,'Pending','2025-11-14 12:22:20','2025-11-27','7300408679'),(115,52,'Harshita ',0,0,0,'Pending','2025-11-14 12:24:18','2025-11-30',''),(116,35,'Namrata ',900,500,400,'Pending','2025-11-14 12:44:12','2025-11-22','9257416442'),(117,50,'Namrata',1500,500,1000,'Pending','2025-11-14 12:49:35','2025-11-22',''),(119,8,'Preeti ',800,400,400,'Pending','2025-11-15 11:28:43','2025-12-02','8854905759'),(120,9,'Divya ',1000,250,750,'Pending','2025-11-16 12:11:01','2025-12-10','9352418512'),(121,35,'Divya',1000,250,750,'Pending','2025-11-16 12:11:41','2025-12-14','9352418512'),(122,52,'Seema ',2000,0,2000,'Pending','2025-11-16 13:09:12','2025-11-21','8949457260'),(123,53,'Harshita ',800,400,400,'Pending','2025-11-17 08:22:31','2025-11-23','9588270829'),(124,50,'Komal',1000,0,1000,'Pending','2025-11-18 04:19:15','2025-11-23','8209348900'),(125,50,'Aaishi',1250,500,750,'Pending','2025-11-20 13:09:54','2025-11-25','7357479168');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` float NOT NULL,
  `image_filename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (6,'Yellow gown kodi ',700,'IMG_9100.png'),(7,'Bhavi lehariya ',400,'IMG_9014.jpeg'),(8,'Levander ',900,'IMG_9122.jpeg'),(9,'Blue mirror ',1000,'IMG_9101.png'),(10,'Black tie end dye ',700,'IMG_9194.png'),(12,'Black new ',1000,'IMG_8540.png'),(13,'Black old',800,'IMG_9102.png'),(14,'Black and red',800,'984a01ed-4d0f-4e9d-9587-c2c7010dba90.jpeg'),(15,'Black and mehrun (kotti)',1000,'d38815e1-1ca5-4125-babd-eaa38005e6cb.jpeg'),(16,'Red golden ',700,'IMG_9020.jpeg'),(17,'Colourfull old',800,'IMG_9142.jpeg'),(18,'Plane black ',500,'IMG_9071.jpeg'),(19,'Blue new lehriya',1500,'BBBA6DF2-DFFD-4A43-B0D2-41164C14B1DF.jpeg'),(20,'White red ne ',700,'IMG_8885.png'),(21,'White Anarkali (lehnga)',1700,'IMG_9099.png'),(22,'White bhavi',1000,'IMG_2287.jpeg'),(23,'Blue plane old ',600,'IMG_9026.jpeg'),(24,'Black and colourful ',900,'IMG_8942.jpeg'),(25,'White and colourful old',800,'IMG_9195.jpeg'),(27,'Pink rajputi heavy',2000,'IMG_4843.jpeg'),(28,'Orange new',2000,'IMG_9168.jpeg'),(29,'Red Net',1000,'IMG_9198.jpeg'),(30,'Pink and green ',1000,'IMG_0473.jpeg'),(31,'Black banarasi',500,'IMG_9207.jpeg'),(32,'Red old old ',400,'image.jpg'),(33,'White old plan ',600,'image.jpg'),(34,'Brown old',1500,'IMG_0055.png'),(35,'Green. Zigzag ',1000,'IMG_0056.jpeg'),(36,'Light pink heavy colourful poshak ',1500,'IMG_0057.png'),(37,'Of white pecock',2000,'IMG_0314.png'),(38,'Blue gown',2000,'IMG_0059.jpeg'),(39,'Sky blue and pink ',1500,'BE05CA4E-E522-40CF-A8AB-F7D8584D63C6.jpeg'),(40,'Black gown',2000,'IMG_0060.jpeg'),(41,'Velvet blue old',1400,'IMG_0062.jpeg'),(42,'Velvet blue old',1400,'IMG_0062.jpeg'),(43,'Light pista green old',1500,'IMG_0063.png'),(44,'Diwali white ',2000,'IMG_0314.png'),(45,'Purple velvet',1500,'IMG_0069.jpeg'),(46,'Sky blue',1500,'IMG_0070.jpeg'),(47,'Blue net new',30000,'IMG_0074.jpeg'),(48,'Red banarasi',1000,'IMG_0075.png'),(49,'Purple new ',1800,'IMG_0076.jpeg'),(50,'Green Banarasi ',1500,'IMG_0077.jpeg'),(51,'Orange new ',1500,'IMG_0078.jpeg'),(52,'Heavy cream new',3000,'IMG_0080.jpeg'),(53,'Pink cream ',800,'IMG_0081.png');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-21  5:13:20
