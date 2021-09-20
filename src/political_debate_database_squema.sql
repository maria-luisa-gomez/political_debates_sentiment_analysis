-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema political_debates
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema political_debates
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `political_debates` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema political_debates
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema political_debates
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `political_debates` DEFAULT CHARACTER SET utf8 ;
USE `political_debates` ;

-- -----------------------------------------------------
-- Table `political_debates`.`speakers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `political_debates`.`speakers` (
  `speakerid` INT NOT NULL AUTO_INCREMENT,
  `speaker` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`speakerid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `political_debates`.`speeches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `political_debates`.`speeches` (
  `sentenceid` INT NOT NULL AUTO_INCREMENT,
  `minute` TIME NOT NULL,
  `sentence` LONGTEXT NOT NULL,
  `tokens` LONGTEXT NOT NULL,
  `speakers_speakerid` INT NULL DEFAULT NULL,
  `debate` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`sentenceid`),
  INDEX `fk_speeches_speakers_idx` (`speakers_speakerid` ASC) VISIBLE,
  CONSTRAINT `fk_speeches_speakers`
    FOREIGN KEY (`speakers_speakerid`)
    REFERENCES `political_debates`.`speakers` (`speakerid`))
ENGINE = InnoDB;

USE `political_debates` ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
