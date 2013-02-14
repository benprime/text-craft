TextCraft
=========

TextCraft is a text adventure game creator.  It differs from other text adventure engines, in that you create the game while playing it.

Here is an example of map creation:

```Entryway
This is the grand entryway where all adventurers start.
Exits: None
> create room north

Entryway
This is the grand entryway where all adventurers start.
Exits: North
> n

default title
default desc
Exits: South
> set title Armory

Armory
default desc
Exits: South
> set desc Weapons o' plenty line the walls of the Hestinfold Armory.

Armory
Weapons o' plenty line the walls of the Hestinfold Armory.
Exits: South
>
