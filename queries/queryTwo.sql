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

INSERT INTO Occupies(OccupiesID, ReservationID, HotelID, RoomNumber, StartDateTime, EndDateTime)
VALUES (20, 1, 1, 10, CURRENT_TIMESTAMP, NULL );

INSERT INTO Occupant (OccupantID, OccupiesID, Name)
VALUES ((SELECT MAX(OccupantID) + 1 FROM Occupant), 20, 'Mrs. Smith');

INSERT INTO Occupant (OccupantID, OccupiesID, Name)
VALUES ((SELECT MAX(OccupantID) + 1 FROM Occupant), 20, 'Mr. Smith');
