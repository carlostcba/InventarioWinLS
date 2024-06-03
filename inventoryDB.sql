CREATE DATABASE IF NOT EXISTS inventoryDB;

USE inventoryDB;

CREATE TABLE `inventoryls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nameOS` varchar(255) NOT NULL,
  `tipoOS` varchar(50) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `processor` varchar(255) DEFAULT NULL,
  `motherboard` varchar(255) NOT NULL,
  `totalRAM` varchar(20) NOT NULL,
  `bank1` varchar(255) DEFAULT NULL,
  `bank2` varchar(255) DEFAULT NULL,
  `bank3` varchar(255) DEFAULT NULL,
  `bank4` varchar(255) DEFAULT NULL,
  `disk1_model` varchar(255) DEFAULT NULL,
  `disk1_capacity` varchar(255) DEFAULT NULL,
  `disk2_model` varchar(255) DEFAULT NULL,
  `disk2_capacity` varchar(255) DEFAULT NULL,
  `disk3_model` varchar(255) DEFAULT NULL,
  `disk3_capacity` varchar(255) DEFAULT NULL,
  `disk4_model` varchar(255) DEFAULT NULL,
  `disk4_capacity` varchar(255) DEFAULT NULL,
  `mac1` varchar(17) DEFAULT NULL, 
  `mac2` varchar(17) DEFAULT NULL, 
  `mac3` varchar(17) DEFAULT NULL, 
  `mac4` varchar(17) DEFAULT NULL, 
  `ip_principal` varchar(15),
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
