
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
game:[gameID]:genre -> [genreID]
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
-----

##Message
--
### A message has
* id
* from
* to
* message

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