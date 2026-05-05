--INSERT query
INSERT INTO ServiceUsage
VALUES (1,1,1,10.0)--In order: ReversationID (So the smiths' reversationID), serviceID, quantity, and priceCharged

--SELECT query
SELECT CheckInDate, CheckOutDate, Room.TypeID, sum(ServiceUsage.priceCharged*quantity) + RoomPrice.price * GuestCategory.DiscountPercent as TotalAmount
FROM Reservation

UPDATE Occupies
SET EndDateTime = CURRENT_TIMESTAMP
WHERE ReservationID = 5
AND EndDateTime IS NULL;

INSERT INTO Invoice (InvoiceID, ReservationID, IssueDate, TotalAmount)
VALUES((SELECT MAX(InvoiceID) + 1 FROM Invoice), 5, CURRENT_DATE,(SELECT SUM(RoomPrice.Price * (1 - GuestCategory.DiscountPercent / 100.0)) + COALESCE(SUM(ServiceUsage.PriceCharged), 0)
FROM Reservation
JOIN Guest ON Guest.GuestUID = Reservation.GuestUID
JOIN GuestCategory ON GuestCategory.CategoryID = Guest.CategoryID
JOIN Occupies ON Occupies.ReservationID = Reservation.ReservationID
JOIN Room ON Room.HotelID = Occupies.HotelID AND Room.RoomNumber = Occupies.RoomNumber
JOIN RoomType ON RoomType.TypeID = Room.TypeID
JOIN RoomPrice ON RoomPrice.TypeID = RoomType.TypeID
JOIN Season ON Season.SeasonID = RoomPrice.SeasonID
LEFT JOIN ServiceUsage ON ServiceUsage.ReservationID = Reservation.ReservationID
WHERE Reservation.ReservationID = 5 AND RoomPrice.DayOfWeek IN ('Tuesday','Wednesday')));
