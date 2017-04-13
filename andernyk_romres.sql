-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: mysql.stud.ntnu.no
-- Generation Time: 12. Apr, 2017 22:45 PM
-- Server-versjon: 5.5.54-0ubuntu0.12.04.1
-- PHP Version: 7.0.15-0ubuntu0.16.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `andernyk_romres`
--

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Booking`
--

CREATE TABLE `Booking` (
  `Id` int(11) NOT NULL,
  `FromTimeNumber` int(11) DEFAULT NULL,
  `ToTimeNumber` int(11) DEFAULT NULL,
  `Room_Id1` int(11) NOT NULL,
  `Room_Position_idPosition` int(11) NOT NULL,
  `User_Id` int(11) NOT NULL,
  `Confirmed` binary(1) DEFAULT '0',
  `Breached` binary(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `Booking`
--

INSERT INTO `Booking` (`Id`, `FromTimeNumber`, `ToTimeNumber`, `Room_Id1`, `Room_Position_idPosition`, `User_Id`, `Confirmed`, `Breached`) VALUES
(1, 1490947200, 1490954400, 1, 1, 1, NULL, NULL),
(2, 1490947200, 1490954400, 2, 2, 1, NULL, NULL),
(3, 1500648, 1490954400, 3, 3, 1, NULL, NULL),
(4, 1491473600, 1491625200, 1, 1, 1, 0x30, 0x30);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Building`
--

CREATE TABLE `Building` (
  `Id` int(11) NOT NULL,
  `CampusId` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `Building`
--

INSERT INTO `Building` (`Id`, `CampusId`, `Name`) VALUES
(1, 1, 'Realfagsbygget'),
(2, 1, 'Sentralbygg 1'),
(3, 1, 'Hovedbygget'),
(4, 1, 'Idrettsbygget'),
(5, 1, 'Gamle Kjemi'),
(6, 1, 'EL-bygget');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Campus`
--

CREATE TABLE `Campus` (
  `Id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `Campus`
--

INSERT INTO `Campus` (`Id`, `Name`) VALUES
(1, 'Gløshaugen');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Position`
--

CREATE TABLE `Position` (
  `idPosition` int(11) NOT NULL,
  `Floor` int(11) DEFAULT NULL,
  `Block` varchar(1) DEFAULT NULL,
  `NumberInFofB` int(11) DEFAULT NULL,
  `Building_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `Position`
--

INSERT INTO `Position` (`idPosition`, `Floor`, `Block`, `NumberInFofB`, `Building_Id`) VALUES
(1, 0, '1', 0, 1),
(2, 1, '1', 0, 1),
(3, 1, '2', 0, 6);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Room`
--

CREATE TABLE `Room` (
  `Id` int(11) NOT NULL,
  `Size` int(11) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Ammenities` longtext,
  `Position_idPosition` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `Room`
--

INSERT INTO `Room` (`Id`, `Size`, `Name`, `Ammenities`, `Position_idPosition`) VALUES
(1, 4, 'R90', NULL, 1),
(2, 5, 'R1', NULL, 2),
(3, 100, 'El101', NULL, 3);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `User`
--

CREATE TABLE `User` (
  `Id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `FullName` varchar(80) NOT NULL,
  `Administrator` binary(1) DEFAULT '0',
  `Password` varchar(45) NOT NULL,
  `Campus_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dataark for tabell `User`
--

INSERT INTO `User` (`Id`, `Name`, `FullName`, `Administrator`, `Password`, `Campus_Id`) VALUES
(1, 'anders', 'Anders Nykås', NULL, '1234', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Booking`
--
ALTER TABLE `Booking`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `fk_Booking_Room2_idx` (`Room_Id1`,`Room_Position_idPosition`),
  ADD KEY `fk_Booking_User1_idx` (`User_Id`);

--
-- Indexes for table `Building`
--
ALTER TABLE `Building`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Campus`
--
ALTER TABLE `Campus`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Position`
--
ALTER TABLE `Position`
  ADD PRIMARY KEY (`idPosition`),
  ADD KEY `fk_Position_Building1_idx` (`Building_Id`);

--
-- Indexes for table `Room`
--
ALTER TABLE `Room`
  ADD PRIMARY KEY (`Id`,`Position_idPosition`),
  ADD KEY `fk_Room_Position1_idx` (`Position_idPosition`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `Name_UNIQUE` (`Name`),
  ADD KEY `fk_User_Campus1_idx` (`Campus_Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Booking`
--
ALTER TABLE `Booking`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `Building`
--
ALTER TABLE `Building`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `Room`
--
ALTER TABLE `Room`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Begrensninger for dumpede tabeller
--

--
-- Begrensninger for tabell `Booking`
--
ALTER TABLE `Booking`
  ADD CONSTRAINT `fk_Booking_Room2` FOREIGN KEY (`Room_Id1`) REFERENCES `Room` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Booking_User1` FOREIGN KEY (`User_Id`) REFERENCES `User` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Begrensninger for tabell `Position`
--
ALTER TABLE `Position`
  ADD CONSTRAINT `fk_Position_Building1` FOREIGN KEY (`Building_Id`) REFERENCES `Building` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Begrensninger for tabell `Room`
--
ALTER TABLE `Room`
  ADD CONSTRAINT `fk_Room_Position1` FOREIGN KEY (`Position_idPosition`) REFERENCES `Position` (`idPosition`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Begrensninger for tabell `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `fk_User_Campus1` FOREIGN KEY (`Campus_Id`) REFERENCES `Campus` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
