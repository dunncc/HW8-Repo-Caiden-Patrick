# CS374 Hotel Database Final Report
*Patrick Buehlmann & Caiden Dunn*

## ER Model: 
![Hotel EER](./images/HotelEER.drawio.png)

## Relational Model:
![Hotel EER](./images/HotelRelationshipMode.png)

## Database Creation:
- Drop tables: [drop.sql](./database/drop.sql)
- Create tables: [create.sql](./database/alter.sql)
- Add constraints to tables: [alter.sql](./database/alter.sql)

## Data:
- Add some data from using Python and faker: [generate.py](./data/generate.py)

## Queries: 
### Query One - [queryOne.sql](./queries/queryOne.sql)
This query finds all available room types in a specific hotel for a given date range and calculates the average nightly cost based on seasonal pricing, day of the week rates, and guest discounts. It only selects rooms not currently occupied during the requested dates. We used dates July 15th to July 17th (according to directions), HotelID of 1, days of Tuesday and Wednesday, unoccupied rooms, and guests with a category of 1 (gold customers). The first INSERT query adds a new guest to the Guest database with values 1000 (GuestID), 'SSN' (IdentificationType), '111-99-4545' (IdentificationNumber), '6767 Epic Rd' (Address), '804-2650' (HomePhone), '111-2222' (NormalPhone), and 1 (GuestCategory). The second INSERT query adds a reservation request to the ReservationRoomRequest database, with values 3000 (RequestID), 5 (ReservationID), 2 (TypeID), and 1 (Quantity).

### Query Two - [queryTwo.sql](./queries/queryTwo.sql)
This first query selects all currently unoccupied rooms of a specific room type in a hotel at the time of check in. We looked for a room from Hotel #2, with a double room room type, that is NOT OCCUPIED. Our query returned room numbers 16 and 17. The first INSERT query insert into the Occupies database, adding a row including the OccupiedID (Unique), ReservationID (Unique), HotelID used in the select query, the RoomNumber returned from the previous query, CURRENT_TIMESTAMP for the StartDateTime, and NULL for the EndDateTime. The second and third INSERT query add Mrs. Smith and Mr. Smith into the Occupant database, both using a unique OccupantID, the same OccupiesID from the previous query, and their names.

### Query Three - [queryThreee.sql](./queries/queryThree.sql)
The first query (An insert) inserts a row into ServiceUsage for Service with the ID of 1, and charges them 10$ for that one Usage of it. This charge is currently set to be assigned to reservation 1, changing the first number inside the () would change which reservation this charge is assigned to.

Second query Selects The checkout and checkin dates for the reservation, the roomID, and finally gets the total charge for that reservation. The total charge is the sum of all serviceUsage charges, plus the roomPrices, the guestCategory discount ONLY gets applied to the roomPrice, this is consistent with when the database was made. The reason so many joins are done is mostly because there is some difficult getting from reservation to Room.

The rest of the queries are designed to checkout a reservation. It then adds an invoice for the reservation to Invoice table. The Update adds the EndDateTime to the guests' rows in the Occupies table.

### Query Four - [queryFour.sql](./queries/queryFour.sql)
This query selects the names of all Occupants for (currently) room 1 of hotel ID 1, for which the date '03/10/2025' (m/d/y) is between the start and end date of that Occupant Occupying that room. The output is just the names of everyone who occupied that room. It will give back at least 2 for any reservation that had more than 2 occupants, but only those.


### Query Five - [queryFive.sql](./queries/queryFive.sql)
This query selects the sums of the totalAmount in Invoice a given guest has. The WHERE clause makes sure that the person has had a reservation at at least 2 hotels. Output is GuestID, followed by the sum of all invoices that Guest has. Currently it is set to get the invoices for guestID 1.