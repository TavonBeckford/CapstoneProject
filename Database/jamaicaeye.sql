DROP DATABASE IF EXISTS jamaicaeye;
CREATE DATABASE jamaicaeye;
USE jamaicaeye;


create table Admin(
	Id int not null unique auto_increment,
	Username varchar(30),
	Password varchar(255),
	primary key(AdminId)
);

create table User(
	Id int not null unique auto_increment,
	Username varchar(30),
	Password varchar(255),
	primary key(UserId)
);

create table Vehicle(
    LicensePlate varchar(20) not null,
    Make varchar(60),
    Model varchar(60),
    Colour varchar(60),
    Year int,
    LicenseDiscNo varchar(60),
    Cartype varchar(60),
    ExpDate date, 
    primary key (LicensePlate)
);


create table VehicleOwner(
	TRN int not null unique,
	Fname varchar(25),
	Lname varchar(25),
	Mname varchar(25),
	Address varchar(100),
	Country varchar(10),
	Parish varchar(30),
	Email varchar(60),
	DOB datetime,
	Gender varchar(8),
	LicensePlate varchar(20) not null,
	LicenseIn varchar (10),
	ExpDate date,
	primary key(TRN),
	foreign key(LicensePlate) references Vehicle(LicensePlate) on delete cascade on update cascade
);

create table OffenceLoc(
	LocationId int not null auto_increment,
	Location varchar (14),
	Parish varchar(14),
	primary key (LocationId)
);

create table Offence(
	OffenceId int not null unique auto_increment,
	Description varchar (30),
	Code int not null,
	Fine varchar (100),
	Points int not null,
	primary key(OffenceId)
);

create table Ticket(
	TicketId int not null unique auto_increment,
	TRN int not null,
	OffenceId int not null,
	LocationId int not null, 
	DateSent datetime,
	Status varchar(30),
	Snapshot varchar (50),
	primary key(TicketId,TRN),
	foreign key(TRN) references VehicleOwner(TRN) on delete cascade on update cascade
);



/*Stored Procedure To Get Vehicles Owners details associated with License Plate*/
delimiter //
Create procedure getOwnerInfo()
	Begin
	SELECT VehicleOwner.Fname, VehicleOwner.Lname, VehicleOwner.LicensePlate,
	Vehicle.Make,Vehicle.Model, Vehicle.Colour, Vehicle.Year, Vehicle.Transmission, Vehicle.Cartype
	FROM VehicleOwner
	INNER JOIN Vehicle
	ON VehicleOwner.LicensePlate = Vehicle.LicensePlate;
end //
DELIMITER ;



delimiter //
Create procedure getCars()
	Begin
	SELECT * 
	FROM Vehicle;
end //
DELIMITER ;


/*
ALTER TABLE Vehicle
ADD CONSTRAINT UQ_Plates UNIQUE (LicensePlate);
*/
