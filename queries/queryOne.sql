SELECT RoomType.TypeID, RoomType.Name, AVG(RoomPrice.Price * (1 - GuestCategory.DiscountPercent / 100.0)) AS AvgPriceANight
FROM RoomType
JOIN Room ON Room.TypeID = RoomType.TypeID
JOIN RoomPrice ON RoomPrice.TypeID = RoomType.TypeID
JOIN Season ON Season.SeasonID = RoomPrice.SeasonID
JOIN GuestCategory ON GuestCategory.CategoryID = 1
LEFT JOIN Occupies ON Occupies.HotelID = Room.HotelID AND Occupies.RoomNumber = Room.RoomNumber
AND (
    Occupies.StartDateTime < DATE '2025-07-17'
    AND (Occupies.EndDateTime IS NULL OR Occupies.EndDateTime > DATE '2025-07-15')
)
WHERE Room.HotelID = 1 
AND DATE '2025-07-15' BETWEEN Season.StartDate 
AND Season.EndDate 
AND RoomPrice.DayOfWeek IN ('Tuesday','Wednesday') 
AND Occupies.OccupiesID IS NULL
GROUP BY RoomType.TypeID, RoomType.Name;

INSERT INTO Guest (GuestUID, IdentificationType, IdentificationNumber, Address, HomePhone, MobilePhone, CategoryID)
VALUES (1000, 'SSN', '111-99-4545', '6767 Epic Rd', '804-2650', '111-2222', 1);

INSERT INTO ReservationRoomRequest (RequestID, ReservationID, TypeID, Quantity)
VALUES (3000, 5, 2, 1);
