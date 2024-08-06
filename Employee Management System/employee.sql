-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: employee
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignment` (
  `assignmentId` varchar(10) NOT NULL,
  `requestId` varchar(10) NOT NULL,
  `employeeId` varchar(10) DEFAULT NULL,
  `projectId` varchar(10) DEFAULT NULL,
  `assigned` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`assignmentId`),
  UNIQUE KEY `assignmentId` (`assignmentId`),
  KEY `requestId` (`requestId`),
  KEY `employeeId` (`employeeId`),
  KEY `projectId` (`projectId`),
  CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`requestId`) REFERENCES `request` (`requestId`),
  CONSTRAINT `assignment_ibfk_2` FOREIGN KEY (`employeeId`) REFERENCES `employee` (`employeeId`),
  CONSTRAINT `assignment_ibfk_3` FOREIGN KEY (`projectId`) REFERENCES `project` (`projectId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
INSERT INTO `assignment` VALUES ('ASSG001','REQ005','EMP001','PROJ002',1),('ASSG002','REQ002','EMP002','PROJ001',0);
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `departmentId` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `managerId` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`departmentId`),
  KEY `fk_manager` (`managerId`),
  CONSTRAINT `fk_manager` FOREIGN KEY (`managerId`) REFERENCES `employee` (`employeeId`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES ('DEPT001','Devlopment','MGR001'),('DEPT002','Quality Assurance','MGR001'),('DEPT003','Testing','MGR002');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `employeeId` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  `role` varchar(50) NOT NULL,
  `is_assigned` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`employeeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('ADM001','anupam.pandey@company.com','Anupam Pandey ',20000000.00,'CEO',0),('EMP001','john.doe@company.com','John Doe',80000.00,'Software Engineer',1),('EMP002','jane.smith@company.com','Jane Smith',95000.00,'Team Lead',0),('EMP003','michael.jones@company.com','Michael Jones',70000.00,'Quality Assurance Analyst',0),('EMP004','olivia.williams@company.com','Olivia Williams',65000.00,'Junior Developer',0),('EMP005','putlkit.pandey@company.com','pulkit',100000.00,'senior software engineer',0),('EMP006','anupam.pandey@company.com','anupam pandey',3000.00,'SDE',0),('MGR001','Nehal.Pandey@company.com','Nehal Pandey',600000.00,'Senior Devloper',0),('MGR002','Bharat.Pandey@company.com','Bharat Kumar Pandey',10000000.00,'CTO',0);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employeeskill`
--

DROP TABLE IF EXISTS `employeeskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeeskill` (
  `employeeId` varchar(10) NOT NULL,
  `skillId` varchar(10) NOT NULL,
  PRIMARY KEY (`employeeId`,`skillId`),
  KEY `skillId` (`skillId`),
  CONSTRAINT `employeeskill_ibfk_1` FOREIGN KEY (`employeeId`) REFERENCES `employee` (`employeeId`),
  CONSTRAINT `employeeskill_ibfk_2` FOREIGN KEY (`skillId`) REFERENCES `skillset` (`skillId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeeskill`
--

LOCK TABLES `employeeskill` WRITE;
/*!40000 ALTER TABLE `employeeskill` DISABLE KEYS */;
INSERT INTO `employeeskill` VALUES ('EMP001','SKILL001'),('EMP003','SKILL001'),('EMP004','SKILL001'),('EMP001','SKILL002'),('EMP002','SKILL002'),('EMP004','SKILL002'),('EMP005','SKILL002'),('EMP001','SKILL003'),('EMP002','SKILL003'),('EMP004','SKILL003'),('EMP003','SKILL004'),('EMP004','SKILL004');
/*!40000 ALTER TABLE `employeeskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `managerId` varchar(10) NOT NULL,
  `employeeId` varchar(10) NOT NULL,
  PRIMARY KEY (`managerId`,`employeeId`),
  CONSTRAINT `fk_manager_manager` FOREIGN KEY (`managerId`) REFERENCES `employee` (`employeeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES ('MGR001','EMP001'),('MGR001','EMP002'),('MGR002','EMP003');
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `projectId` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `managerId` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`projectId`),
  KEY `fk_project_manager` (`managerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES ('PROJ001','E-commerce Platform','Development of an online store platform.','MGR001'),('PROJ002','CRM System','Implementation of a customer relationship management system.','MGR001'),('PROJ003','Mobile App','Design and development of a mobile application for the company.','MGR002'),('PROJ004','OTT App','Create a mobile app to stream web series','MGR002');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `requestId` varchar(10) NOT NULL,
  `projectId` varchar(10) DEFAULT NULL,
  `skillId` varchar(10) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`requestId`),
  KEY `projectId` (`projectId`),
  KEY `skillId` (`skillId`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `project` (`projectId`),
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`skillId`) REFERENCES `skillset` (`skillId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES ('REQ001','PROJ002','SKILL003','Close'),('REQ002','PROJ001','SKILL002','Open'),('REQ003','PROJ003','SKILL001','Close'),('REQ004','PROJ004','SKILL003','Open'),('REQ005','PROJ002','SKILL001','Close');
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skillset`
--

DROP TABLE IF EXISTS `skillset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skillset` (
  `skillId` varchar(10) NOT NULL,
  `skillName` varchar(50) NOT NULL,
  PRIMARY KEY (`skillId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skillset`
--

LOCK TABLES `skillset` WRITE;
/*!40000 ALTER TABLE `skillset` DISABLE KEYS */;
INSERT INTO `skillset` VALUES ('SKILL001','Java Development'),('SKILL002','Python Programming'),('SKILL003','SQL'),('SKILL004','Software Testing'),('SKILL005','C++'),('SKILL006','C#');
/*!40000 ALTER TABLE `skillset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` char(64) NOT NULL,
  `role` enum('admin','manager','user') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin_user','6d4525c2a21f9be1cca9e41f3aa402e0765ee5fcc3e7fea34a169b1730ae386e','admin'),(2,'manager_user','a69ae21824e5590ce83123122c2c9f4c5855c696c289627f8f4a55741d218c37','manager'),(3,'regular_user','7ae2e2473bdcf762e98ff6d1386013eb455cfa54aa19e150c87e22af222daf5a','user'),(6,'EMP001','0c0eed7f7ab5877b2623ed2335e9d69c576bfea25c63fd86e0b4c5afc7028c45','user'),(7,'MGR001','461f30dbcd4ce3b00b8a60f978d699e847b47de1f5095a63a29e91c1866f8cdd','manager'),(8,'EMP006','11c55b5f15948387cd1759bd4b86bc003e0faed3ab8f65e37b1b9295b015f2eb','user'),(15,'ADM001','4e55c6070b838b51dd595ec16c36b8eb95ad6dbca3e012bd0fb5f8f8cb3370b5','admin'),(19,'EMP002','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8','user'),(20,'EMP003','35142c7708234c2e764b7ea2e5eb20d7d2883c335947309c46f043e2a88cda28','user'),(21,'EMP004','82fe72589300e72f63de75f4c0f1ffe7a0ce7140977eeb2b82a87641ab24f6cc','user'),(22,'EMP005','861f3c5ea597d90bb454ff7956fcaa1aafee256900c770c90fbd9780c350b125','user'),(23,'MGR002','e4d76e6ba901386b55dc081412388111f3cfb4fdfd85cdc0858663b3ebbc22f4','manager');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-31  7:35:11
