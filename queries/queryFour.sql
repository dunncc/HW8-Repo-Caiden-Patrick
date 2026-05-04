SELECT name
FROM Occupies
JOIN Occupant on Occupies.OccupiesID = Occupant.OccupiesID
WHERE HotelID = 1   --Replace as desired
AND RoomNumber = 1  --Replace as desired
AND '03/10/2025' BETWEEN StartDateTime AND EndDateTime --Change string/datetime as desired.