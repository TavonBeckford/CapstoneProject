INSERT INTO Admin(Id,Username,Password) VALUES ('1','EricE','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Officer(Id,Username,Password) VALUES ('1','GregoryM','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Officer(Id,Username,Password) VALUES ('2','JoelM','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Officer(Id,Username,Password) VALUES ('3','DianaB','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Officer(Id,Username,Password) VALUES ('4','RickyR','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Officer(Id,Username,Password) VALUES ('5','CassandraF','482c811da5d5b4bc6d497ffa98491e38');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('9518JK','CAN-AM','COMMANDER 1000 LTD','Red',2012,'kL073355','Sedan','2022-06-20');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('430946954','Travis','Lee','Arden','41 Hummingbird Cluster Ocho Rios St.Ann','Jamaica','Manchester','testable876@gmail.com','1992-1-19','Female','9518JK','Jamaica','2023-02-4','General');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('8424GR','AUDI','A3 QUATTRO','Black',2007,'QZ090041','Sedan','2022-04-1');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('666948837','Sarah','Cunningham','River','79 Hummingbird Cluster Ocho Rios St.Ann','Jamaica','Kingston','testable876@gmail.com','1987-1-24','Female','8424GR','Jamaica','2021-08-28','General');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('DEPMED','BMW','ALPINA B7L','Red',2014,'YP288107','Sedan','2022-03-20');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('891739538','Elizabeth','Pacheco','Belle','69 Hummingbird Cluster Ocho Rios St.Ann','Jamaica','St. Mary','testable876@gmail.com','1964-11-14','Female','DEPMED','Jamaica','2021-01-13','Private');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('2445GX','FORD','CROWN VICTORIA','Black',2011,'cb156478','Coupe','2022-09-23');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('368842259','Ricky','Shelton','Claire','62 Constant Spring Rd Kingston 5 Kingston','Jamaica','Hanover','testable876@gmail.com','1984-7-15','Male','2445GX','Jamaica','2023-03-13','Private');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('1206FQ','HONDA','NSS250AS REFLEX SPORT ABS','Blue',2006,'Pi139762','Hatchback','2022-10-19');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('589141377','Amanda','Jensen','River','69 Lismore Ave May Pen Clarendon','Jamaica','Portland','testable876@gmail.com','1978-11-27','Female','1206FQ','Jamaica','2025-05-28','Private');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('6606HW','KAWASAKI','ZX600 NINJA ZX-6R','Blue',2008,'su777496','Coupe','2022-11-16');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('902920400','Jose','Stanton','Belle','6 West St Port Antonie Port Antonio','Jamaica','St. Thomas','testable876@gmail.com','1989-12-1','Female','6606HW','Jamaica','2024-02-22','General');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('3840GF','PETERBILT','337','Black',2011,'yx885195','SUV','2022-02-24');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('172411570','John','Valdez','Claire','15 Manch Rd Kingston 5 Mandeville','Jamaica','St. Catherine','testable876@gmail.com','1987-5-28','Female','3840GF','Jamaica','2022-05-1','General');

INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('4737HA','MASERATI','COUPE','Silver',2004,'PC391286','Coupe','2022-03-6');

INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('437299793','Dominique','Clark','Nash','56 John Pringle Dr Hopewell Hanover','Jamaica','Manchester','testable876@gmail.com','1981-10-17','Male','4737HA','Jamaica','2023-09-3','Private');

INSERT INTO Offence(Code,Description,Fine, Points) VALUES ('F100','Failure to obey traffic signal','5000','8');
INSERT INTO Offence(Code,Description,Fine, Points) VALUES ('E200','Exceeding the speed limit','7000','12');
INSERT INTO Location(Description,Parish) VALUES ('27 Constant Spring Road, Kingston 3', 'Kingston');
INSERT INTO Location(Description,Parish) VALUES ('48 Old Hope Road, Kingston 7', 'Kingston');
INSERT INTO Location(Description,Parish) VALUES ('9 Darling Street, Kingston 13', 'Kingston');
INSERT INTO Location(Description,Parish) VALUES ('31B Mona Road, Kingston 5', 'Kingston');
INSERT INTO Location(Description,Parish) VALUES ('3 Molynes Road, Kingston 4', 'Kingston');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','5','F100','flagged.png');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','3','E200','ja.jpg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','3','E200','ja2.jpg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','4','E200','ja3.jpg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','2','E200','ja4.jpg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','5','F100','ja5.jpeg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','2','F100','ja6.jpeg');
INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('2021-07-15','17:45:06','5','F100','ja7.jpeg');
