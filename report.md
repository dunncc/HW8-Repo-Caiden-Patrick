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
This query finds all available room types in a specific hotel for a given date range and calculates the average nightly cost based on seasonal pricing, day of the week rates, and guest discounts. It only selects rooms not currently occupied during the requested dates.

### Query Two - [queryTwo.sql](./queries/queryTwo.sql)
This query selects all currently unoccupied rooms of a specific room type in a hotel at the time of check in.

### Query Three - 

### Query Four - [queryFour.sql](./queries/queryFour.sql)
This query selects the names of all Occupants, and selects the names of all Guests.
Guests count as both, so they'll show up twice.


### Query Five - [queryFive.sql](./queries/queryFive.sql)
This query selects the sums of the totalAmount in Invoice a given guest has.
Also gives the GuestID so you know who its about.
