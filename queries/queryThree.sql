--INSERT query
INSERT INTO ServiceUsage
VALUES (1,1,1,10.0)--In order: ReversationID (So the smiths' reversationID), serviceID, quantity, and priceCharged

--SELECT query
SELECT CheckInDate, CheckOutDate, Room.TypeID, sum(ServiceUsage.priceCharged*quantity) + RoomPrice.price * GuestCategory.DiscountPercent as TotalAmount
FROM Reservation
--TODO: the rest.

--Insert/update query

--TODO: 
--UPDATE EndDateTime for both occupies
--INSERT a new invoice for this reservation, total amount for that invoice should be about what the last statement in the select is.