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