SELECT name
FROM Occupies
JOIN Occupant on Occupies.OccupiesID = Occupant.OccupiesID
WHERE HotelID = 1   --Replace as desired
AND RoomNumber = 1  --Replace as desired
AND '03/10/2025' BETWEEN StartDateTime AND EndDateTime --Change string/datetime as desired.
UNION --constants in the below need to be changed to match the above if they are changed.
SELECT name
FROM Occupies
JOIN Occupant on Occupies.OccupiesID = Occupant.OccupiesID
JOIN Reservation on Reservation.ReservationID = Occupies.ReservationID
WHERE HotelID = 1   --Replace as desired
AND RoomNumber = 1  --Replace as desired
AND '03/10/2025' BETWEEN StartDateTime AND EndDateTime --Change string/datetime as desired.
AND GuestID IS NOT NULL