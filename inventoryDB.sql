CREATE DATABASE IF NOT EXISTS inventoryDB;

USE inventoryDB;

CREATE TABLE `inventoryls` (
  `id` int(11) NOT NULL,
  `nameOS` varchar(255) NOT NULL,
  `tipoOS` varchar(50) NOT NULL,
  `hostname` varchar(255) NOT NULL,
  `motherboard` varchar(255) NOT NULL,
  `processor` varchar(255) DEFAULT NULL,
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
  `mac1` VARCHAR(17), 
  `mac2` VARCHAR(17), 
  `mac3` VARCHAR(17), 
  `mac4` VARCHAR(17), 
  `ip_principal` VARCHAR(15);
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
