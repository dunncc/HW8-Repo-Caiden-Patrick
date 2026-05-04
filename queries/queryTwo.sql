SELECT Room.RoomNumber
FROM Room
JOIN RoomType ON Room.TypeID = RoomType.TypeID
LEFT JOIN Occupies ON Occupies.HotelID = Room.HotelID AND Occupies.RoomNumber = Room.RoomNumber
AND (
    Occupies.StartDateTime <= CURRENT_TIMESTAMP
    AND (Occupies.EndDateTime IS NULL OR Occupies.EndDateTime >= CURRENT_TIMESTAMP)
)
WHERE Room.HotelID = 2
AND RoomType.Name = 'Double'
AND Occupies.OccupiesID IS NULL;

INSERT INTO Occupies (OccupiesID, ReservationID, HotelID, RoomNumber, StartDateTime, EndDateTime)
VALUES (5000, 2000, 2, 101, CURRENT_TIMESTAMP, NULL);

INSERT INTO Occupant (OccupantID, OccupiesID, Name)
VALUES (6000, 5000, 'Mrs. Smith');

INSERT INTO Occupant (OccupantID, OccupiesID, Name)
VALUES (6001, 5000, 'Mr. Smith');
