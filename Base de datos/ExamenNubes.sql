-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.29 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para examennube
CREATE DATABASE IF NOT EXISTS `examennube` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `examennube`;

-- Volcando estructura para tabla examennube.curso
CREATE TABLE IF NOT EXISTS `curso` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `credito` int NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla examennube.curso: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` (`codigo`, `nombre`, `credito`) VALUES
	('C001', 'Matematica basica', 2),
	('C002', 'algebra', 2),
	('C003', 'Calculo diferencial', 4);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;

-- Volcando estructura para tabla examennube.escuela
CREATE TABLE IF NOT EXISTS `escuela` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `duracion` int NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla examennube.escuela: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `escuela` DISABLE KEYS */;
INSERT INTO `escuela` (`codigo`, `nombre`, `duracion`) VALUES
	('E0001', 'Ing. Informatica Y sistemas', 10),
	('E002', 'Inicial', 10),
	('E003', 'CIVIL', 10),
	('E004', 'ING. MINAS', 10),
	('E005', 'ING. Agroindustrial', 10);
/*!40000 ALTER TABLE `escuela` ENABLE KEYS */;

-- Volcando estructura para tabla examennube.estudiante
CREATE TABLE IF NOT EXISTS `estudiante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `DNI` varchar(10) NOT NULL,
  `apellidos` varchar(200) NOT NULL,
  `nombres` varchar(200) NOT NULL,
  `feNacimiento` varchar(30) NOT NULL,
  `sexo` varchar(1) NOT NULL,
  `codEscuela` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codEscuela` (`codEscuela`),
  CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`codEscuela`) REFERENCES `escuela` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla examennube.estudiante: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `estudiante` DISABLE KEYS */;
INSERT INTO `estudiante` (`id`, `DNI`, `apellidos`, `nombres`, `feNacimiento`, `sexo`, `codEscuela`) VALUES
	(4, '60015283', 'huamani aiquipa', 'Cielo', '2022-09-30', 'F', 'E0001'),
	(5, '55524269', 'peres', 'DAYSi', '2022-08-31', 'F', 'E002'),
	(7, '55524286', 'torres', 'LENIN', '2022-09-04', 'M', 'E002'),
	(9, '85452454', 'chacon', 'kimy', '2022-09-17', 'F', 'E003'),
	(10, '09926637', 'retamozo', 'pedro', '2022-10-02', 'M', 'E003');
/*!40000 ALTER TABLE `estudiante` ENABLE KEYS */;

-- Volcando estructura para tabla examennube.matricula
CREATE TABLE IF NOT EXISTS `matricula` (
  `codigo` varchar(10) NOT NULL,
  `codEstudiante` int DEFAULT NULL,
  `codCurso` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codigo`),
  KEY `codEstudiante` (`codEstudiante`),
  KEY `codCurso` (`codCurso`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`codEstudiante`) REFERENCES `estudiante` (`id`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`codCurso`) REFERENCES `curso` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla examennube.matricula: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `matricula` DISABLE KEYS */;
INSERT INTO `matricula` (`codigo`, `codEstudiante`, `codCurso`) VALUES
	('M002', 4, 'C001'),
	('M003', 5, 'C001'),
	('M006', 10, 'C003');
/*!40000 ALTER TABLE `matricula` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
