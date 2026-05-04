select sum(TotalAmount)
FROM Invoice
JOIN Reservation as r1 on Reservation.ReservationID = Invoice.ReservationID
WHERE EXISTS (SELECT 1 FROM Reservation as r2 WHERE
r1.HotelID!=r2.HotelID AND r1.GuestID = r2.GuestID)
WHERE GuestID = 1--Change as desired.
GROUP BY GuestID --NOTE: if the guest has not made reservations for 2 different hotels, they will not show anything.
