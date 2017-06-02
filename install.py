import db_connector

#install.py create database and initialised files etc
def createdb():
    db = db_connector.db_connector()

    db.cursor.execute_script("""
        --
        -- Table structure for table `Articles`
        --

        DROP TABLE IF EXISTS `Articles`;
        CREATE TABLE `Articles` (
        `AID` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `WriterUID` int(10) unsigned NOT NULL,
        `title` varchar(70) NOT NULL,
        `subtitle` varchar(140) DEFAULT NULL,
        `submitdate` datetime NOT NULL,
        `summary` varchar(500) DEFAULT NULL,
        `body` mediumtext NOT NULL,
        PRIMARY KEY (`AID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

        --
        -- Table structure for table `Files`
        --

        DROP TABLE IF EXISTS `Files`;
        CREATE TABLE `Files` (
        `FID` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `OwnerUID` int(10) unsigned NOT NULL,
        `extension` varchar(10) NOT NULL,
        `uploaddate` datetime NOT NULL,
        PRIMARY KEY (`FID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

        --
        -- Table structure for table `Links`
        --

        DROP TABLE IF EXISTS `Links`;
        CREATE TABLE `Links` (
        `ParentAID` int(10) unsigned NOT NULL,
        `ChildAID` int(10) unsigned NOT NULL,
        PRIMARY KEY (`ParentAID`,`ChildAID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

        --
        -- Table structure for table `Tags`
        --

        DROP TABLE IF EXISTS `Tags`;
        CREATE TABLE `Tags` (
        `AID` int(10) unsigned NOT NULL,
        `tag` varchar(64) NOT NULL,
        PRIMARY KEY (`AID`,`tag`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

        --
        -- Table structure for table `Users`
        --

        DROP TABLE IF EXISTS `Users`;
        CREATE TABLE `Users` (
        `UID` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `username` varchar(32) NOT NULL,
        `displayname` varchar(64) DEFAULT NULL,
        `regdate` datetime NOT NULL,
        `password` char(128) NOT NULL,
        `email` varchar(254) DEFAULT NULL,
        PRIMARY KEY (`UID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """)
