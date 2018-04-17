
#Steam
-------
###A few notes
* `[ ]` indicates an ID, not a literal string i.e. `User:[userID]:Friend` in which [userID] is a user's ID


##User
--

### User has
* id
* inventory
* library
* balance
* friends
* acheievements
* buy orders
* sell orders
* incoming trade offers
* outgoing trade offers
* past trades
* past transactions


## A user's inventory

```
User:[userID]:inventory -> List([itemID])
```

## A user's Game Library

```
user:[userID]:library -> Set([gameID])
user:[userID]:library:[gameID]:achievements -> List([achievementID])
user:[userID]:library:[gameID]:hours -> Numeric

```
## A user's balance

```
user:[userID]:balance -> Numeric
```
## A user's friends
```
user:[userID]:friendList -> Set([userID])
```
## A user's messages
```
user:[userID]:friend:[friendID]:messages -> List([messageID])
```
## A user's orders
```
user:[userID]:buy -> List([orderID])
user:[userID]:sell -> List([orderID])
```

## A user's trade offers
```
user:[userID]:trades:incoming -> List([tradeID])
user:[userID]:trades:outgoing -> List([tradeID])
```

## A user's trade history
```
user:[userID]:trades:completed -> List([tradeID])
```

## A user's transcations
```
user:[userID]:transactions -> List([transactionID])
```

## A user's orders
```
user:[userID]:order:buy/sell -> List([orderID])
```

## A user's transcations
```
user:[userID]:transactions -> List([transactionID])
```
---------

##Game
--
### Game has
* id
* title
* genre
* price
* description
* achievements

## A game's title

```
game:[gameID]:title -> string
```
## A game's genre

```
game:[gameID]:genre -> string
```
## A game's price

```
game:[gameID]:price -> numeric
```
## A game's description

```
game:[gameID]:desc -> string
```
## A game's achievements

```
game:[gameID]:achievements -> Set([achievementID])
```
-----


##Item
--
### An item has
* id
* name
* gameID
* desc
* image link?
* marketOrders
* transactions

## An item's name
```
item:[itemID]:name -> string
```
## An item's gameID
```
item:[itemID]:game -> [gameID]
```
## An item's description
```
item:[itemID]:desc -> string
```
## An item's image link (if we have time)
```
item:[itemID]:image -> string
```


## An item's orders
```
item:[itemID]:buy -> List([orderID])
item:[itemID]:sell -> List([orderID])
```
## An item's transactions
```
item:[itemID]:transactions -> List([transactionID])
```
-----
##Transaction
--
### A transaction has
* id
* from
* to
* item
* timestamp
* price

## A transaction's from
```
message:[transactionID]:from -> [userID]
```

## A transaction's to
```
message:[transactionID]:to -> [userID]
```


## A transaction's item
```
message:[transactionID]:item -> [itemID]
```

## A transaction's date
```
message:[transactionID]:timestamp -> timestamp
```

## A transaction's message
```
message:[transactionID]:price -> int
```

-----


##Message
--
### A message has
* id
* from
* to
* message
* timestamp

## A message's from
```
message:[messageID]:from -> [userID]
```

## A message's to
```
message:[messageID]:to -> [userID]
```


## A message's message
```
message:[messageID]:message -> string
```

## A message's timestamp
```
message:[messageID]:timestamp -> string
```


-----

##Achievement
--
### Achievement has
* id
* title
* description

## An achievement's title

```
achievement:[achievementID]:title -> string
```
## An achievement's description

```
achievement:[achievementID]:desc -> string
```
----


##Genre
--
### A genre has
* id
* type

## A genre's type
```
genre:[genreID]:type -> string
```
-----

##Order
--
### An order has
* id
* type
* price
* poster
* timestamp

## An order's type
```
order:[orderID]:type -> string
```

## An order's price
```
order:[orderID]:price -> numeric
```

## An order's poster
```
order:[orderID]:poster -> [userID]
```

## An order's timestamp
```
order:[orderID]:timestamp -> string
```

## Order Matching Algorithm

The order of execution will prioritize a first in first out system. Given a sell order A of $9 posted at t = 1 and another sell order B of $10 posted at t = 2, if a buy order C of $11 is posted at t = 3, the sell order ... and buy order C will be matched and a transaction will be completed for a price of $...

Similarly, given a buy order A of $10 posted at t = 1 and another buy order B of $9 posted at t = 2, a sell order C of $8 posted at t = 3 will cause the sell order C to be matched with the buy order ... at a price of $...

-----


##Trade
--
### A trade has
* tradeID
* userFrom
* userTo
* offerItems
* forItems

## A trade's userFrom
```
trade:[tradeID]:from -> [userID]
```
## A trade's userTo
```
trade:[tradeID]:to -> [userID]
```
## A trade's offerItems
```
trade:[tradeID]:offer -> List([itemID])
```
## A trade's forItems
```
trade:[tradeID]:for -> List([itemID])
```
-----


![]()