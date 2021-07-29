from faker import Faker
fake = Faker()
import random
import numpy as np
from datetime import datetime
import hashlib
import json
import string

script= open('fake_data.sql','w')


_file1 = open('cardataset.json','r')
result = json.loads(_file1.read())

_file1 = open('address.json','r')
result1 = json.loads(_file1.read())

password = "password123"
hashpass = hashlib.md5(password.encode())


for d in range(1):
    adminid = d+1
    name = fake.name().split(" ")
    fname = name[0]
    lname= name[1]
    username = fname+str.upper(lname[0])
    password = hashpass.hexdigest()
    addadmin = f"INSERT INTO Admin(Id,Username,Password) VALUES ('{adminid}','{username}','{password}');"
    script.write(addadmin+'\n'+'\n')

for d in range(5):
    userid = d+1
    name = fake.name().split(" ")
    fname = name[0]
    lname= name[1]
    username = fname+str.upper(lname[0])
    password = hashpass.hexdigest()
    adduser = f"INSERT INTO Officer(Id,Username,Password) VALUES ('{userid}','{username}','{password}');"
    script.write(adduser+'\n'+'\n')

for i in range(8):
    lower_upper_alphabet = string.ascii_uppercase
    random_letter = random.choice(lower_upper_alphabet)+random.choice(lower_upper_alphabet)
    trn = random.randint(100000000,999999999)
    name = fake.name().split(" ")
    fname = name[0]
    lname= name[1]
    mname = random.choice(['Arden','Belle','Bowie','Claire','Jude','Nash','Orion','River'])
    v = random.randint(0,18)
    q = random.randint(1,90)
    address = str(q)+" "+ result1[v]['street']+" "+ result1[v]['state'] +" "+ result1[v]['parish']
    email = 'testable876@gmail.com'
    dob = str(random.randint(1961,2005))+"-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
    gender = random.choice(['Male','Female'])
    listofplates = ['9518JK','8424GR','DEPMED','2445GX','1206FQ','6606HW','3840GF','4737HA']
    licplate = listofplates[i]
    country = 'Jamaica'
    parish = random.choice(['St. Catherine','St. Mary','St. Ann','Manchester','Clarendon','Hanover','Westmoreland','St. James','Trelawny','St. Elizabeth','Kingston','St. Andrew','Portland','St. Thomas'])
    licensein = 'Jamaica'
    expdate = str(random.randint(2021,2025))+"-"+str(fake.month())+"-"+str(random.randint(1,28))
    licensetype = random.choice(['General','Private'])
    addowner = f"INSERT INTO VehicleOwner(TRN,Fname,Lname,Mname,Address,Country,Parish,Email,DOB,Gender,LicensePlate,LicenseIn,ExpDate,LicenseType) VALUES ('{trn}','{fname}','{lname}','{mname}','{address}','{country}','{parish}','{email}','{dob}','{gender}','{licplate}','{licensein}','{expdate}','{licensetype}');"
    
    x = random.randint(0, len(result))
    make = result[x]['make']
    model = result[x]['model']
    colour = random.choice(['Black','Silver','Red','Blue'])
    year = result[x]['year']
    transmission = random.choice(['Standard','Automatic'])
    cartype = random.choice(['Sedan','Coupe','Hatchback','SUV'])
    licensediscno = fake.bothify(text='??######')
    expdate2 = str(2022)+"-"+str(fake.month())+"-"+str(random.randint(1,28))
    addcar = f"INSERT INTO Vehicle(LicensePlate,Make,Model,Colour,Year,LicenseDiscNo,Cartype,ExpDate) VALUES ('{licplate}','{make}','{model}','{colour}',{year},'{licensediscno}','{cartype}','{expdate2}');"
    script.write(addcar+'\n'+'\n')
    script.write(addowner+'\n'+'\n')

fine1 = 5000
fine2 =7000
points1 =8
points2 =12
offence1 = f"INSERT INTO Offence(Code,Description,Fine, Points) VALUES ('F100','Failure to obey traffic signal','{fine1}','{points1}');"
offence2 = f"INSERT INTO Offence(Code,Description,Fine, Points) VALUES ('E200','Exceeding the speed limit','{fine2}','{points2}');"
script.write(offence1+'\n')
script.write(offence2+'\n')

location1 = f"INSERT INTO Location(Description,Parish) VALUES ('27 Constant Spring Road, Kingston 3', 'Kingston');"
location2 = f"INSERT INTO Location(Description,Parish) VALUES ('48 Old Hope Road, Kingston 7', 'Kingston');"
location3 = f"INSERT INTO Location(Description,Parish) VALUES ('9 Darling Street, Kingston 13', 'Kingston');"
location4 = f"INSERT INTO Location(Description,Parish) VALUES ('31B Mona Road, Kingston 5', 'Kingston');"
location5 = f"INSERT INTO Location(Description,Parish) VALUES ('3 Molynes Road, Kingston 4', 'Kingston');"
script.write(location1+'\n')
script.write(location2+'\n')
script.write(location3+'\n')
script.write(location4+'\n')
script.write(location5+'\n')

for i in range(8):
    curtime = datetime.today().strftime('%H:%M:%S')
    curdate = datetime.today().strftime('%Y-%m-%d')
    locationid = random.choice([1,2,3,4,5])
    offenceid = random.choice(['F100','E200'])
    images=['flagged.png','ja.jpg','ja2.jpg','ja3.jpg','ja4.jpg','ja5.jpeg','ja6.jpeg','ja7.jpeg']
    image= images[i]
    addincident = f"INSERT INTO Incident(Date,Time,LocationID,OffenceID,Image) VALUES ('{curdate}','{curtime}','{locationid}','{offenceid}','{image}');"
    script.write(addincident+'\n')
script.close()

