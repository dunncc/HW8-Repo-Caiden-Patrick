import psycopg
import faker
import random
import datetime
fake = faker.Faker()
CONNSTR = "host=localhost port=5433 dbname=sp26 user=dunncc password=PurpleDog7"
__author__ = "Patrick Buehlmann & Caiden Dunn"
def connect(path):
    """Connect to the SQLite database file and return a cursor.

    This function defines the global variables con and cur, which
    you will use throughout the module.

    THE CODE IS ALREADY FINISHED; DO NOT EDIT THIS FUNCTION.

    Args:
        path (str): File system path to the SQLite database file.

    Returns:
        sqlite3.Cursor: An object for executing SQL statements.
    """
    global con, cur

    con = psycopg.connect(path)
    cur = con.cursor()
#SQL script that creates your tables (with no foreign key constraints):
def makeTables():
    global con, cur
    
    cur.execute('''
        CREATE TABLE Hotel (
            HotelID INTEGER PRIMARY KEY,
            Name VARCHAR NOT NULL,
            Address VARCHAR NOT NULL
        );

        CREATE TABLE HotelPhone (
            PhoneID INTEGER PRIMARY KEY,
            HotelID INTEGER NOT NULL,
            PhoneNumber VARCHAR NOT NULL,
            FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID)
        );

        CREATE TABLE Season (
            SeasonID INTEGER PRIMARY KEY,
            Name VARCHAR NOT NULL,
            StartDate DATE NOT NULL,
            EndDate DATE NOT NULL
        );

        CREATE TABLE RoomType (
            TypeID INTEGER PRIMARY KEY,
            Name VARCHAR NOT NULL,
            Size INTEGER NOT NULL,
            Capacity INTEGER NOT NULL
        );

        CREATE TABLE FeatureType (
            FeatureID INTEGER PRIMARY KEY,
            Name VARCHAR NOT NULL
        );

        CREATE TABLE RoomTypeFeature (
            TypeID INTEGER NOT NULL,
            FeatureID INTEGER NOT NULL,
            PRIMARY KEY (TypeID, FeatureID),
            FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID),
            FOREIGN KEY (FeatureID) REFERENCES FeatureType(FeatureID)
        );

        CREATE TABLE Room (
            HotelID INTEGER NOT NULL,
            RoomNumber INTEGER NOT NULL,
            TypeID INTEGER NOT NULL,
            Floor INTEGER NOT NULL,
            PRIMARY KEY (HotelID, RoomNumber),
            FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID),
            FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID)
        );

        CREATE TABLE RoomPrice (
            PriceID INTEGER PRIMARY KEY,
            TypeID INTEGER NOT NULL,
            SeasonID INTEGER NOT NULL,
            DayOfWeek VARCHAR NOT NULL,
            Price DECIMAL NOT NULL,
            FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID),
            FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID)
        );

        CREATE TABLE GuestCategory (
            CategoryID INTEGER PRIMARY KEY,
            Name VARCHAR NOT NULL,
            DiscountPercent DECIMAL NOT NULL
        );

        CREATE TABLE Guest (
            GuestUID INTEGER PRIMARY KEY,
            IdentificationType VARCHAR NOT NULL,
            IdentificationNumber VARCHAR NOT NULL,
            Address VARCHAR,
            HomePhone VARCHAR,
            MobilePhone VARCHAR,
            CategoryID INTEGER NOT NULL,
            FOREIGN KEY (CategoryID) REFERENCES GuestCategory(CategoryID)
        );

        CREATE TABLE Reservation (
            ReservationID INTEGER PRIMARY KEY,
            GuestUID INTEGER NOT NULL,
            HotelID INTEGER NOT NULL,
            CheckInDate DATE NOT NULL,
            CheckOutDate DATE,
            FOREIGN KEY (GuestUID) REFERENCES Guest(GuestUID),
            FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID)
        );

        CREATE TABLE ReservationRoomRequest (
            RequestID INTEGER PRIMARY KEY,
            ReservationID INTEGER NOT NULL,
            TypeID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
            FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID)
        );

        CREATE TABLE Occupies (
            OccupiesID INTEGER PRIMARY KEY,
            ReservationID INTEGER NOT NULL,
            HotelID INTEGER NOT NULL,
            RoomNumber INTEGER NOT NULL,
            StartDateTime TIMESTAMP NOT NULL,
            EndDateTime TIMESTAMP,
            FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
            FOREIGN KEY (HotelID, RoomNumber) REFERENCES Room(HotelID, RoomNumber)
        );

        CREATE TABLE Occupant (
            OccupantID INTEGER PRIMARY KEY,
            OccupiesID INTEGER NOT NULL,
            Name VARCHAR NOT NULL,
            FOREIGN KEY (OccupiesID) REFERENCES Occupies(OccupiesID)
        );

        CREATE TABLE Service (
            ServiceID INTEGER PRIMARY KEY,
            HotelID INTEGER NOT NULL,
            Name VARCHAR NOT NULL,
            Price DECIMAL NOT NULL,
            FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID)
        );

        CREATE TABLE ServiceUsage (
            ReservationID INTEGER NOT NULL,
            ServiceID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            PriceCharged DECIMAL NOT NULL,
            PRIMARY KEY (ReservationID, ServiceID),
            FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
            FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
        );

        CREATE TABLE Invoice (
            InvoiceID INTEGER PRIMARY KEY,
            ReservationID INTEGER NOT NULL,
            IssueDate DATE NOT NULL,
            TotalAmount DECIMAL NOT NULL,
            FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
        );

    ''')
    # cur.execute('''
    #     CREATE TABLE "Hotel" (
    #         HotelID int PRIMARY KEY,
    #         Name text,
    #         Address text
    #     );
    #     CREATE TABLE "FeatureType" (
    #         FeatureID int PRIMARY KEY,
    #         Name text
    #     );
    #     CREATE TABLE "HotelPhone" (
    #         PhoneID int PRIMARY KEY,
    #         HotelID int,
    #         PhoneNumber text
    #     );
    #     CREATE TABLE "Season" (
    #         SeasonID int PRIMARY KEY,
    #         Name text,
    #         StartDate date,
    #         EndDate date
    #     );
    #     CREATE TABLE "RoomType" (
    #         TypeID int PRIMARY KEY,
    #         Name text,
    #         Size int,
    #         Capacity int
    #     );
    #     CREATE TABLE "RoomTypeFeature" (
    #         TypeID int,
    #         FeatureID int
    #     );
    #     CREATE TABLE "Room" (
    #         RoomNumber int PRIMARY KEY,
    #         HotelID int,
    #         TypeID int,
    #         Floor int
    #     );
    #     CREATE TABLE "RoomPrice" (
    #         PriceID int PRIMARY KEY,
    #         TypeID int,
    #         SeasonID int,
    #         DayOfWeek text,
    #         Price decimal
    #     );
    #     CREATE TABLE "GuestCategory" (
    #         CategoryID int PRIMARY KEY,
    #         Name text,
    #         DiscountPercent decimal
    #     );
    #     CREATE TABLE "Guest" (
    #         GuestUID int PRIMARY KEY,
    #         IdentificationType text,
    #         IdentificationNumber text,
    #         Address text,
    #         HomePhone text,
    #         MobilePhone text,
    #         CategoryID int
    #     );
    #     CREATE TABLE "Reservation" (
    #         ReservationID int PRIMARY KEY,
    #         GuestUID int,
    #         HotelID int,
    #         CheckInDate date,
    #         CheckOutDate date
    #     );
    #     CREATE TABLE "ReservationRoomRequest" (
    #         RequestID int PRIMARY KEY,
    #         ReservationID int,
    #         RoomNumber int,
    #         TypeID int,
    #         Quantity int
    #     );
    #     CREATE TABLE "RoomAssignment" (
    #         AssignmentID int PRIMARY KEY,
    #         ReservationID int,
    #         RoomNumber int,
    #         StartDateTime date,
    #         EndDateTime date
    #     );
    #     CREATE TABLE "Occupant" (
    #         OccupantID int PRIMARY KEY,
    #         AssignmentID int,
    #         Name text
    #     );
    #     CREATE TABLE "Service" (
    #         ServiceID int PRIMARY KEY,
    #         HotelID int,
    #         Name text,
    #         Price decimal
    #     );
    #     CREATE TABLE "ServiceUsage" (
    #         UsageID int PRIMARY KEY,
    #         ReservationID int,
    #         ServiceID int,
    #         Quantity int,
    #         PriceCharged decimal
    #     );
    #     CREATE TABLE "Invoice" (
    #         InvoiceID int PRIMARY KEY,
    #         ReservationID int,
    #         IssueDate date,
    #         TotalAmount decimal
    #     );
    #     CREATE TABLE Occupies (
    #         OccupiesID INTEGER PRIMARY KEY,
    #         ReservationID INTEGER NOT NULL,
    #         HotelID INTEGER NOT NULL,
    #         RoomNumber INTEGER NOT NULL,
    #         StartDateTime TIMESTAMP NOT NULL,
    #         EndDateTime TIMESTAMP,
    #         FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
    #         FOREIGN KEY (HotelID, RoomNumber) REFERENCES Room(HotelID, RoomNumber)
    #     );

    # ''')
    con.commit()
#Here's the one that drops it:
def dropTables():
    global con, cur
    #The CASCADE is not needed if the tables have no constraints.
    cur.execute('''
        DROP TABLE IF EXISTS Hotel CASCADE;
        DROP TABLE IF EXISTS FeatureType CASCADE;
        DROP TABLE IF EXISTS HotelPhone CASCADE;
        DROP TABLE IF EXISTS Season CASCADE;
        DROP TABLE IF EXISTS RoomTypeFeature CASCADE;
        DROP TABLE IF EXISTS Room CASCADE;
        DROP TABLE IF EXISTS RoomPrice CASCADE;
        DROP TABLE IF EXISTS Guest CASCADE;
        DROP TABLE IF EXISTS Reservation CASCADE;
        DROP TABLE IF EXISTS ReservationRoomRequest CASCADE;
        DROP TABLE IF EXISTS Occupies CASCADE;
        DROP TABLE IF EXISTS RoomAssignment CASCADE;
        DROP TABLE IF EXISTS Occupant CASCADE;
        DROP TABLE IF EXISTS Service CASCADE;
        DROP TABLE IF EXISTS ServiceUsage CASCADE;
        DROP TABLE IF EXISTS Invoice CASCADE;
        DROP TABLE IF EXISTS RoomType CASCADE;
        DROP TABLE IF EXISTS GuestCategory CASCADE;
    ''')
    con.commit()
#SQL script that adds the foreign key constraints:
def addKeyConstrants():
    global con, cur
    cur.execute('''
                ALTER TABLE HotelPhone ADD CONSTRAINT hotelphone_HotelID_fkey FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID);
                ALTER TABLE RoomTypeFeature ADD CONSTRAINT roomtypefeature_typeid_fkey FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID);
                ALTER TABLE RoomTypeFeature ADD CONSTRAINT roomtypefeature_featureid_fkey FOREIGN KEY (FeatureID) REFERENCES FeatureType(FeatureID);
                ALTER TABLE Room ADD CONSTRAINT room_HotelID_fkey FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID);
                ALTER TABLE Room ADD CONSTRAINT room_typeid_fkey FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID);
                ALTER TABLE RoomPrice ADD CONSTRAINT roomprice_typeid_fkey FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID);
                ALTER TABLE RoomPrice ADD CONSTRAINT roomprice_seasonid_fkey FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID);
                ALTER TABLE Guest ADD CONSTRAINT guest_categoryid_fkey FOREIGN KEY (CategoryID) REFERENCES GuestCategory(CategoryID);
                ALTER TABLE Reservation ADD CONSTRAINT reservation_guestuid_fkey FOREIGN KEY (GuestUID) REFERENCES Guest(GuestUID);
                ALTER TABLE Reservation ADD CONSTRAINT reservation_HotelID_fkey FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID);
                ALTER TABLE ReservationRoomRequest ADD CONSTRAINT reservationroomrequest_reservationid_fkey FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID);
                ALTER TABLE ReservationRoomRequest ADD CONSTRAINT reservationroomrequest_typeid_fkey FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID);
                ALTER TABLE Occupies ADD CONSTRAINT occupies_reservationid_fkey FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID);
                ALTER TABLE Occupies ADD CONSTRAINT occupies_HotelID_roomnumber_fkey FOREIGN KEY (HotelID, RoomNumber) REFERENCES Room(HotelID, RoomNumber);
                ALTER TABLE Occupant ADD CONSTRAINT occupant_occupiesid_fkey FOREIGN KEY (OccupiesID) REFERENCES Occupies(OccupiesID);
                ALTER TABLE Service ADD CONSTRAINT service_HotelID_fkey FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID);
                ALTER TABLE ServiceUsage ADD CONSTRAINT serviceusage_reservationid_fkey FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID);
                ALTER TABLE ServiceUsage ADD CONSTRAINT serviceusage_serviceid_fkey FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID);
                ALTER TABLE Invoice ADD CONSTRAINT invoice_reservationid_fkey FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID);
                ''')
    # cur.execute('''
    #     ALTER TABLE "HotelPhone" ADD CONSTRAINT FK_PhoneHotel FOREIGN KEY (HotelID) REFERENCES "Hotel" (HotelID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Room" ADD CONSTRAINT FK_RoomHotel FOREIGN KEY (HotelID) REFERENCES "Hotel" (HotelID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Room" ADD CONSTRAINT FK_RoomType FOREIGN KEY (TypeID) REFERENCES "RoomType" (TypeID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "RoomPrice" ADD CONSTRAINT FK_PriceType FOREIGN KEY (TypeID) REFERENCES "RoomType" (TypeID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "RoomPrice" ADD CONSTRAINT FK_PriceSeason FOREIGN KEY (SeasonID) REFERENCES "Season" (SeasonID) DEFERRABLE INITIALLY IMMEDIATE;
       
    #     ALTER TABLE "RoomTypeFeature" ADD CONSTRAINT FK_RoomFeatureType FOREIGN KEY (TypeID) REFERENCES "RoomType" (TypeID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "RoomTypeFeature" ADD CONSTRAINT FK_RoomFeatureFeature FOREIGN KEY (FeatureID) REFERENCES "FeatureType" (FeatureID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Guest" ADD CONSTRAINT FK_GuestCat FOREIGN KEY (CategoryID) REFERENCES "GuestCategory" (CategoryID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Reservation" ADD CONSTRAINT FK_ResGuest FOREIGN KEY (GuestUID) REFERENCES "Guest" (GuestUID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Reservation" ADD CONSTRAINT FK_ResHotel FOREIGN KEY (HotelID) REFERENCES "Hotel" (HotelID) DEFERRABLE INITIALLY IMMEDIATE;
        
    #     ALTER TABLE "ReservationRoomRequest" ADD CONSTRAINT FK_ResReqRes FOREIGN KEY (ReservationID) REFERENCES "Reservation" (ReservationID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "ReservationRoomRequest" ADD CONSTRAINT FK_ResReqType FOREIGN KEY (TypeID) REFERENCES "RoomType" (TypeID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "RoomAssignment" ADD CONSTRAINT FK_AssignRes FOREIGN KEY (ReservationID) REFERENCES "Reservation" (ReservationID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "RoomAssignment" ADD CONSTRAINT FK_AssignNum FOREIGN KEY (RoomNumber) REFERENCES "Room" (RoomNumber) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Occupant" ADD CONSTRAINT FK_OccAssign FOREIGN KEY (AssignmentID) REFERENCES "RoomAssignment" (AssignmentID) DEFERRABLE INITIALLY IMMEDIATE;
        
    #     ALTER TABLE "Service" ADD CONSTRAINT FK_ServiceHotel FOREIGN KEY (HotelID) REFERENCES "Hotel" (HotelID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "ServiceUsage" ADD CONSTRAINT FK_UsageRes FOREIGN KEY (ReservationID) REFERENCES "Reservation" (ReservationID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "ServiceUsage" ADD CONSTRAINT FK_UsageService FOREIGN KEY (ServiceID) REFERENCES "Service" (ServiceID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "Invoice" ADD CONSTRAINT FK_InRes FOREIGN KEY (ReservationID) REFERENCES "Reservation" (ReservationID) DEFERRABLE INITIALLY IMMEDIATE;
    #     ALTER TABLE "ReservationRoomRequest" ADD CONSTRAINT FK_ResReqRoom FOREIGN KEY (RoomNumber) REFERENCES "Room" (RoomNumber) DEFERRABLE INITIALLY IMMEDIATE;
    # ''')
    con.commit()
#SQL script that drops the foreign key constraints:
def dropConstrants():
    #I'm keeping the typo
    global con, cur
    cur.execute('''
                ALTER TABLE HotelPhone DROP CONSTRAINT IF EXISTS hotelphone_HotelID_fkey;
                ALTER TABLE RoomTypeFeature DROP CONSTRAINT IF EXISTS roomtypefeature_typeid_fkey;
                ALTER TABLE RoomTypeFeature DROP CONSTRAINT IF EXISTS roomtypefeature_featureid_fkey;
                ALTER TABLE Room DROP CONSTRAINT IF EXISTS room_HotelID_fkey;
                ALTER TABLE Room DROP CONSTRAINT IF EXISTS room_typeid_fkey;
                ALTER TABLE RoomPrice DROP CONSTRAINT IF EXISTS roomprice_typeid_fkey;
                ALTER TABLE RoomPrice DROP CONSTRAINT IF EXISTS roomprice_seasonid_fkey;
                ALTER TABLE Guest DROP CONSTRAINT IF EXISTS guest_categoryid_fkey;
                ALTER TABLE Reservation DROP CONSTRAINT IF EXISTS reservation_guestuid_fkey;
                ALTER TABLE Reservation DROP CONSTRAINT IF EXISTS reservation_HotelID_fkey;
                ALTER TABLE ReservationRoomRequest DROP CONSTRAINT IF EXISTS reservationroomrequest_reservationid_fkey;
                ALTER TABLE ReservationRoomRequest DROP CONSTRAINT IF EXISTS reservationroomrequest_typeid_fkey;
                ALTER TABLE Occupies DROP CONSTRAINT IF EXISTS occupies_reservationid_fkey;
                ALTER TABLE Occupies DROP CONSTRAINT IF EXISTS occupies_HotelID_roomnumber_fkey;
                ALTER TABLE Occupant DROP CONSTRAINT IF EXISTS occupant_occupiesid_fkey;
                ALTER TABLE Service DROP CONSTRAINT IF EXISTS service_HotelID_fkey;
                ALTER TABLE ServiceUsage DROP CONSTRAINT IF EXISTS serviceusage_reservationid_fkey;
                ALTER TABLE ServiceUsage DROP CONSTRAINT IF EXISTS serviceusage_serviceid_fkey;
                ALTER TABLE Invoice DROP CONSTRAINT IF EXISTS invoice_reservationid_fkey;
                ''')
    # cur.execute('''
    #     ALTER TABLE "HotelPhone" DROP CONSTRAINT FK_PhoneHotel;
    #     ALTER TABLE "Room" DROP CONSTRAINT FK_RoomHotel;
    #     ALTER TABLE "Room" DROP CONSTRAINT FK_RoomType;
    #     ALTER TABLE "RoomPrice" DROP CONSTRAINT FK_PriceType;
    #     ALTER TABLE "RoomPrice" DROP CONSTRAINT FK_PriceSeason;
                
    #     ALTER TABLE "RoomTypeFeature" DROP CONSTRAINT FK_RoomFeatureType;
    #     ALTER TABLE "RoomTypeFeature" DROP CONSTRAINT FK_RoomFeatureFeature;
    #     ALTER TABLE "Guest" DROP CONSTRAINT FK_GuestCat;
    #     ALTER TABLE "Reservation" DROP CONSTRAINT FK_ResGuest;
    #     ALTER TABLE "Reservation" DROP CONSTRAINT FK_ResHotel;
                
    #     ALTER TABLE "ReservationRoomRequest" DROP CONSTRAINT FK_ResReqRes;
    #     ALTER TABLE "ReservationRoomRequest" DROP CONSTRAINT FK_ResReqType;
    #     ALTER TABLE "RoomAssignment" DROP CONSTRAINT FK_AssignRes;
    #     ALTER TABLE "RoomAssignment" DROP CONSTRAINT FK_AssignNum;
    #     ALTER TABLE "Occupant" DROP CONSTRAINT FK_OccAssign;
                
    #     ALTER TABLE "Service" DROP CONSTRAINT FK_ServiceHotel;
    #     ALTER TABLE "ServiceUsage" DROP CONSTRAINT FK_UsageRes;
    #     ALTER TABLE "ServiceUsage" DROP CONSTRAINT FK_UsageService;
    #     ALTER TABLE "Invoice" DROP CONSTRAINT FK_InRes;
    #     ALTER TABLE "ReservationRoomRequest" DROP CONSTRAINT FK_ResReqRoom;
    # ''')
    con.commit()

def fakeHotels():
    toReturn=[]
    for i in range(0,5):
        hold = {
            "HotelID":i,
            "Name": fake.name(),
            "Address":fake.address()
        }
        toReturn.append(hold)
    return toReturn
roomTypes=["double","single"]
global counter

counter=0
def fakeRooms(hotel):
    global counter
    toReturn=[]
    for i in range(0,6):
        hold={
            "RoomNumber":counter,
            "HotelID":hotel["HotelID"],
            "TypeID":1 if i<3 else 2,
            "Floor":random.randint(1,2)
        }
        counter+=1
        toReturn.append(hold)
    return toReturn
def fakeFeatures(typ):
    global counter
    fTypes=[]
    rTF=[]
    for i in range(0,random.randint(2,4)):
        hold={
            "FeatureID":counter,
            "Name":fake.name()
        }
        fTypes.append(hold)
        hold={
            "FeatureID":counter,
            "TypeID":typ["TypeID"]
        }
        rTF.append(hold)
        counter+=1
        
    return (fTypes,rTF)
def fakePrices(typ):
    global counter
    toReturn=[]
    for i in range(1,3):
        for day in ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]:
            hold={
                "PriceID":counter,
                "TypeID":typ["TypeID"],
                "SeasonID":i,
                "DayOfWeek":day,
                "Price":random.randint(0,100)+random.random()
            }
            counter+=1
            toReturn.append(hold)
    return toReturn

def inSummer(dat):
    return dat >= datetime.datetime(dat.year,5,6) and dat <= datetime.datetime(dat.year,7,26)

def inSpring(dat):
    return dat >= datetime.datetime(dat.year,2,10) and dat <= datetime.datetime(dat.year,5,5)
def populateTable(hotels,phones,seasons,roomTypes,featureTypes,roomTypeFeatures,rooms,roomPrices,guestCategories,guests,reservations,reservationRoomRequests,occupants,services,serviceUsages,invoices,occupies):
    #TODO: ALL OF THIS!
    global con, cur
    # cur.execute(''' ''')
    for hotel in hotels:
        cur.execute('''INSERT INTO Hotel VALUES
                    (%s,%s,%s)''',(hotel["HotelID"],hotel["Name"],hotel["Address"]))
    for season in seasons:
        cur.execute('''INSERT INTO Season VALUES
                    (%s,%s,%s,%s)''',(season["SeasonID"],season["Name"],season["StartDate"],season["EndDate"]))
    for row in guestCategories:
        cur.execute('''INSERT INTO GuestCategory VALUES
                    (%s,%s,%s)''',(row["CategoryID"],row["Name"],row["DiscountPercent"]))
    for row in featureTypes:
        cur.execute('''INSERT INTO FeatureType VALUES
                    (%s,%s)''',(row["FeatureID"],row["Name"]))
    for row in roomTypes:
        cur.execute('''INSERT INTO RoomType VALUES
                    (%s,%s,%s,%s)''',(row["TypeID"],row["Name"],row["Size"],row["Capacity"]))
    for row in roomTypeFeatures:
        cur.execute('''INSERT INTO roomTypeFeature VALUES
                    (%s,%s)''',(row["TypeID"],row["FeatureID"]))
    for row in guests:
        cur.execute('''INSERT INTO Guest VALUES
                    (%s,%s,%s,%s,%s,%s,%s)''',(row["GuestUID"],row["IdentificationType"],row["IdentificationNumber"],row["Address"],row["HomePhone"],row["MobilePhone"],row["CategoryID"]))
    for row in rooms:
        cur.execute('''INSERT INTO Room VALUES
                    (%s,%s,%s,%s)''',(row["HotelID"],row["RoomNumber"],row["TypeID"],row["Floor"]))
    for row in roomPrices:
        cur.execute('''INSERT INTO RoomPrice VALUES
                    (%s,%s,%s,%s,%s)''',(row["PriceID"],row["TypeID"],row["SeasonID"],row["DayOfWeek"],row["Price"]))
    for row in services:
        cur.execute('''INSERT INTO Service VALUES
                    (%s,%s,%s,%s)''',(row["ServiceID"],row["HotelID"],row["Name"],row["Price"]))
    for row in phones:
        cur.execute('''INSERT INTO HotelPhone VALUES
                    (%s,%s,%s)''',(row["PhoneID"],row["HotelID"],row["PhoneNumber"]))
    print("insert reservations")
    for row in reservations:
        print(row["ReservationID"])
        cur.execute('''INSERT INTO Reservation VALUES
                    (%s,%s,%s,%s,%s)''',(row["ReservationID"],row["GuestUID"],row["HotelID"],row["CheckInDate"],row["CheckOutDate"]))
    for row in reservationRoomRequests:
        cur.execute('''INSERT INTO ReservationRoomRequest VALUES
                    (%s,%s,%s,%s)''',(row["RequestID"],row["ReservationID"],row["TypeID"],row["Quantity"]))
    for row in invoices:
        cur.execute('''INSERT INTO Invoice VALUES
                    (%s,%s,%s,%s)''',(row["InvoiceID"],row["ReservationID"],row["IssueDate"],row["TotalAmount"]))
    for row in serviceUsages:
        cur.execute('''INSERT INTO ServiceUsage VALUES
                    (%s,%s,%s,%s)''',(row["ReservationID"],row["ServiceID"],row["Quantity"],row["PriceCharged"]))
    for row in occupies:
        cur.execute('''INSERT INTO Occupies VALUES
                    (%s,%s,%s,%s,%s,%s)''',(row["OccupiesID"],row["ReservationID"],row["HotelID"],row["RoomNumber"],row["StartDateTime"],row["EndDateTime"]))
    for row in occupants:
        cur.execute('''INSERT INTO Occupant VALUES
                    (%s,%s,%s)''',(row["OccupantID"],row["OccupiesID"],row["Name"]))
    con.commit()

def invoiceAndUsage(guestCategory,reservations,services,roomPrices):
    counter=0
    usageCounter=0
    voices=[]
    usage=[]
    for res in reservations:
        if(not res["CheckOutDate"]):
            continue
        #usage:
        for serv in services:
            if(serv["HotelID"]!=res["HotelID"]):
                continue
            else:
                times=random.randint(1,9)
                hold={
                    "UsageID":usageCounter,
                    "ReservationID":res["ReservationID"],
                    "ServiceID":serv["ServiceID"],
                    "Quantity":times,
                    "PriceCharged":serv["Price"]*times
                }
                usageCounter+=1
                usage.append(hold)
        #invoice:
        cat=1 if res["GuestUID"]%2==0 else 2
        disCountPrecent=0
        for categ in guestCategory:
            if(categ["CategoryID"]==cat):
                disCountPrecent=categ["DiscountPercent"]
                break
        discount=disCountPrecent/100
        finalAmount=0

        startDay=datetime.datetime.strptime(res["CheckInDate"], "%m/%d/%Y")
        endDay = datetime.datetime.strptime(res["CheckOutDate"], "%m/%d/%Y")
        # pricesOfTheWeek={"Sunday":-1,"Monday":-1,"Tuesday":-1,"Wednesday":-1,"Thursday":-1,"Friday":-1,"Saturday":-1}
        pricesOfTheWeek=["",-1,-1,-1,-1,-1,-1,-1]
        namesOfTheWeek=["N/A","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        #NOTE: this code will not work if we end up moving between seasons.
        summer=False
        print(startDay)
        print(endDay)
        while startDay<=endDay:
            toAdd=0
            dayOfWeek=startDay.isoweekday()#monday==1, sunday==7
            if(inSummer(startDay)!=summer):
                summer=inSummer(startDay)
                pricesOfTheWeek=["",-1,-1,-1,-1,-1,-1,-1]#Clear this cause its now wrong.
            if(pricesOfTheWeek[dayOfWeek]>0):##optimization.
                toAdd+=pricesOfTheWeek[dayOfWeek]
            else:#1 is summer, 2 is spring
                if(inSummer(startDay)):#Going to assume it is spring until told otherwise.
                    summer=True
                for price in roomPrices:
                    if(summer and price["SeasonID"]==1) or ((not summer) and price["SeasonID"]==2):
                        #right season
                        if price["DayOfWeek"]==namesOfTheWeek[dayOfWeek]:
                            toAdd+=price["Price"]*discount
                            break
                        else:
                            continue
                    else:
                        continue
            #Now add it to the total
            startDay=startDay+datetime.timedelta(days=1)
            finalAmount+=toAdd
        hold={
            "InvoiceID":counter,
            "ReservationID":res["ReservationID"],
            "IssueDate":res["CheckOutDate"],
            "TotalAmount":finalAmount
        }
        counter+=1
        voices.append(hold)
    return (voices,usage)


def fakeData():
    hotels=fakeHotels()
    roomTypes=[{
        "TypeID":1,
        "Name":"Single",
        "Size":5,
        "Capacity":1
    },
    {
        "TypeID":2,
        "Name":"Double",
        "Size":10,
        "Capacity":2
    }]
    rooms=[]
    for hotel in hotels:
        rooms+=fakeRooms(hotel)
    RoomTypeFeature=[]
    FeatureType=[]
    counter=0#Reset this
    for typ in roomTypes:
        hold=fakeFeatures(typ)
        FeatureType+=hold[0]
        RoomTypeFeature+=hold[1]
    seasons=[#While it is stored with the year, most of the code ignores the year.
    {
        "SeasonID":1,
        "Name":"Summer",
        "StartDate":"2025-05-06",
        "EndDate":"2025-07-26",
    },
    {
        "SeasonID":2,
        "Name":"Spring",
        "StartDate":"2025-02-10",
        "EndDate":"2025-05-05"
    }
    ]
    counter=0
    roomPrices=[]
    for typ in roomTypes:
        roomPrices+=fakePrices(typ)
    counter=0
    phones=[]
    for hotel in hotels:
        phones.append({
            "PhoneID":counter,
            "HotelID":hotel["HotelID"],
            "PhoneNumber":fake.phone_number()
        })
        counter+=1
    guestCategory=[{
        "CategoryID":1,
        "Name":"gold",
        "DiscountPercent":random.random()*100,
    },{
        "CategoryID":2,
        "Name":"sliver",
        "DiscountPercent":random.random()*20,
    }]#Should generally result in sliver having worse discount.
    #billing information is ServiceUsage and Invoice
    serviceTypes=[{
        "Name":"RoomService",
        "Price":10.00
    },{
        "Name":"Food",
        "Price":15.00
    }]
    counter=0
    services=[]
    for hotel in hotels:
        hold=[{
            "ServiceID":counter,
            "HotelID":hotel["HotelID"],
            "Name":serviceTypes[0]["Name"],
            "Price":serviceTypes[0]["Price"]
        },{
            "ServiceID":counter+1,
            "HotelID":hotel["HotelID"],
            "Name":serviceTypes[1]["Name"],
            "Price":serviceTypes[1]["Price"]
        }]
        counter+=2
        services+=hold
    #Guests:
    counter=0
    guests=[]
    for i in range(0,12):
        guests.append({
            "GuestUID":i,
            "IdentificationType":"SSN",
            "IdentificationNumber":fake.ssn(),
            "Address":fake.address(),
            "HomePhone":fake.phone_number(),
            "MobilePhone":fake.phone_number(),
            "CategoryID": 1 if i%2==0 else 2#guest category
        })
    #Reservations:
    print("Construct reservations")
    reservations=[]
    for guest in guests:
        hold={
            "ReservationID": guest["GuestUID"],
            "GuestUID": guest["GuestUID"],
            "HotelID": hotels[random.randint(0,4)]["HotelID"],
        }
        startDate=fake.past_date("-4w")#hopefully this works.
        # endDate=fake.past_date(startDate)
        hold["CheckInDate"]=startDate.strftime("%Y/%m/%d")
        hold["CheckOutDate"]=None#Haven't checked out yet
        reservations.append(hold)
    #I'm just gonna assume the above gets me this:
    # At least 2 reservations should be multi-day

    #Gotta to specifically make sure this one happens though:
    # At least 2 reservations should be within a special season (fully within)
    hold={
        "ReservationID": 15,
        "GuestUID": 5,
        "HotelID": hotels[random.randint(0,4)]["HotelID"],
        "CheckInDate":"03/10/2025",
        "CheckOutDate":"03/20/2025"
    }
    reservations.append(hold)
    hold={
        "ReservationID": 16,
        "GuestUID": 7,
        "HotelID": hotels[random.randint(0,4)]["HotelID"],
        "CheckInDate":"05/10/2025",
        "CheckOutDate":"05/20/2025"
    }

    reservations.append(hold)
    #the above 2 and the following will also make sure this is done:
    #At least 3 guests should have already completed their stays in the past, so that billing information will exist for them
    hold={
        "ReservationID": 17,
        "GuestUID": 4,
        "HotelID": hotels[random.randint(0,4)]["HotelID"],
        "CheckInDate":"04/01/2025",
        "CheckOutDate":"04/20/2025"
    }
    reservations.append(hold)
    #ReservationRoomRequest:
    counter=0
    ResRoomRequests=[]
    for res in reservations:
        hoteldent=res["HotelID"]
        relevantRooms=[]
        for room in rooms:
            if(room["HotelID"]==hoteldent):
                relevantRooms.append(room)
        yourRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
        relevantRooms.remove(yourRoom)
        ResRoomRequests.append({
            "RequestID": counter,
            "ReservationID": res["ReservationID"],
            "RoomNumber": yourRoom["RoomNumber"],#Techically unneed now.
            "TypeID": yourRoom["TypeID"],
            "Quantity": 1 if yourRoom["TypeID"]==1 else 2
        })
        counter+=1
        # At least 2 reservations should include multiple rooms of the same type (ReservationRoomRequest)
        if(res["ReservationID"]==15):
            otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            while otherRoom["TypeID"] == yourRoom["TypeID"]:#this makes sure the above comment is true
                relevantRooms.remove(otherRoom)
                otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            ResRoomRequests.append({
                "RequestID": counter,
                "ReservationID": res["ReservationID"],
                "RoomNumber": otherRoom["RoomNumber"],
                "TypeID": otherRoom["TypeID"],
                "Quantity": 1 if otherRoom["TypeID"]==1 else 2
            })
            counter+=1 
        elif(res["ReservationID"]==16):
            otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            while otherRoom["TypeID"] == yourRoom["TypeID"]:
                relevantRooms.remove(otherRoom)
                otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            ResRoomRequests.append({
                "RequestID": counter,
                "ReservationID": res["ReservationID"],
                "RoomNumber": otherRoom["RoomNumber"],
                "TypeID": otherRoom["TypeID"],
                "Quantity": 1 if otherRoom["TypeID"]==1 else 2
            })
            counter+=1
        # At least 2 reservations should include multiple room types (ReservationRoomRequest)
        elif(res["ReservationID"]==4):
            otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            while otherRoom["TypeID"] != yourRoom["TypeID"]:#this makes sure the above comment is true
                relevantRooms.remove(otherRoom)
                otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            ResRoomRequests.append({
                "RequestID": counter,
                "ReservationID": res["ReservationID"],
                "RoomNumber": otherRoom["RoomNumber"],
                "TypeID": otherRoom["TypeID"],
                "Quantity": 1 if otherRoom["TypeID"]==1 else 2
            })
            counter+=1
        elif(res["ReservationID"]==9):
            otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            while otherRoom["TypeID"] != yourRoom["TypeID"]:
                relevantRooms.remove(otherRoom)
                otherRoom=relevantRooms[random.randint(0,len(relevantRooms)-1)]
            ResRoomRequests.append({
                "RequestID": counter,
                "ReservationID": res["ReservationID"],
                "RoomNumber": otherRoom["RoomNumber"],
                "TypeID": otherRoom["TypeID"],
                "Quantity": 1 if otherRoom["TypeID"]==1 else 2
            })
            counter+=1
    #Quantity for ReservationRoomRequest, is number of occupants
    #RoomAssignment and occupants:
    counter=0
    occIDs=0
    occupies=[]
    guestOccupants={
        -1:"TEMP",
    }
    occupants=[]
    for res in reservations:
        nums=[]
        for quest in ResRoomRequests:
            if(quest["ReservationID"]==res["ReservationID"]):
                nums.append((quest["RoomNumber"],quest["Quantity"]))
        for tup in nums:
            assignID=counter
            assign={
                "OccupiesID":assignID,
                "ReservationID":res["ReservationID"],
                "HotelID":res["HotelID"],
                "RoomNumber":tup[0],
                "StartDateTime":res["CheckInDate"],
                "EndDateTime":res["CheckOutDate"] if res["CheckOutDate"] else fake.future_date("+7d").strftime("%Y/%m/%d")
            }
            occupies.append(assign)
            counter+=1
            for i in range(0,tup[1]):#make an occupation for each person in the request.
                if(i==0):#Keep names consistent.
                    if not (res["GuestUID"] in guestOccupants.keys()):
                        guestOccupants[res["GuestUID"]]=fake.name()
                    occupants.append({
                        "OccupantID":occIDs,
                        "OccupiesID":assignID,
                        "Name":guestOccupants[res["GuestUID"]]
                    })
                else:
                    occupants.append({
                        "OccupantID":occIDs,
                        "OccupiesID":assignID,
                        "Name":fake.name()
                    })
                occIDs+=1
    #Quantity for services used is just how many times that service was used by a given reservation.
    #Invoice and ServiceUsage:
    counter=0
    usageCounter=0
    voices=[]
    usage=[]
    #comment these 3 lines out since they take awhile.
    hold=invoiceAndUsage(guestCategory,reservations,services,roomPrices)
    voices=hold[0]
    usage=hold[1]
    #now we have the data for every table, so now we gotta do something with it.
    #hotels,phones,seasons,roomtypes,featuretypes,roomtypefeatures,rooms,roomprices,guestcategories,guests,reservations,
    populateTable(hotels,phones,seasons,roomTypes,FeatureType,RoomTypeFeature,rooms,roomPrices,guestCategory,guests,reservations,ResRoomRequests,occupants,services,usage,voices,occupies)

if __name__ == "__main__":
  connect(CONNSTR)
  dropTables()
  makeTables()
#   addKeyConstrants()
  dropConstrants()
  addKeyConstrants()#Restore them.
  fakeData()#make the fake data
  

#"2 seasons per hotel" link chain: Season > RoomPrice > RoomType > Room > Hotel
#Not sure how to logically make that make sense, I guess every hotel has a 2 roomprices that link to different seasons?
#Hotels end up needing at least of 6 rooms.
#14 room price per hotel.
#That would work out to a min of 70 prices, except there's nothing stopping us from reusing room types between hotels.
#We can't get out of the min 30 hotel rooms, even if we could we'd probably end up having issues with guest data.
