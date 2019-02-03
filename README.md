A RPG bot, with a working inventory, market and economy, team setups and characters aswell. Each user has a server unique inventory and balance. Players may list items on a market for other users to buy. Users may create characters with teams from Pokemon in their storage box. Server administrators may add and give items to the server and its users. Pokemon boxes and server configurations.

Made by XxKingNovaXx#0416

Add to your server

Support Server


**Admin Commands**
Note: Start With N! eg N!character
Characters Commands
allchars
character
character create
character delete
character edit
character remattr
characters
Economy Commands
baltop
bid
economy
givemoney
lotto
lotto cancel
lotto enter
lotto new
market
market buy
market create
market remove
market search
pay
setbalance
shop
shop additem
shop buy
shop removeitem
shop sell
startbid
takemoney
Groups Commands
guild
guild create
guild delete
guild deposit
guild deposititems
guild info
guild invite
guild join
guild kick
guild leave
guild setdescription
guild seticon
guild setimage
guild setmod
guild toggleopen
guild transfer
guild withdraw
guild withdrawitems
guilds
Inventory Commands
craft
give
giveitem
inventory
lootbox
lootbox buy
lootbox create
lootbox delete
offer
recipe
recipe create
recipe delete
recipes
respond
takeitem
use
wipeinv
Mapping Commands
map
map buy
map check
map create
map delete
map down
map generate
map left
map right
map up
Misc Commands
donate
info
ping
rtd
source
totalcmds
Pokemon Commands
box
pokemon
pokemon create
pokemon info
pokemon release
pokemon trade
Salary Commands
salaries
salary
salary create
salary delete
salary payout
Settings Commands
currency
deleteafter
language
loaddnd
loaddndmagic
loaddndshop
loadmagicshop
loadpokemon
setstart
settings
settings additem
settings iteminfo
settings items
settings removeitem
unload
Team Commands
team
team add
team remove
User Commands
experience
experience add
experience disable
experience enable
experience setlevel
userinfo
Admin Commands
**Characters Commands**
allchars
Description: List all guild characters

Usage: N!allchars

character
Description: Get info on a character

Usage: N![character|c|char|personnage] <name>

character create
Description: Create a new character

Usage: N!character [create|new|nouveau|creer] <name> [user]

character delete
Description: Delete a character of the given name (you must be the owner)

Usage: N!character [delete|remove|supprimer] <name>

character edit
Description: Edit a character Usage: rp!character edit John description John likes bananas! Valid values for the [item] (second argument): name: the character's name description: the description of the character level: an integer representing the character's level meta: used like the additional info section when creating; can be used to edit/remove all attributes Anything else will edit single attributes in the additional info section

Usage: N!character edit <character> <attribute> <value>

character remattr
Description: Delete a character attribute Usage: rp!character remattr John hair color

Usage: N!character remattr <character> <attribute>

characters
Description: List all your characters

Usage: N![characters|chars|personnages] [user]

Economy Commands
Economy related commands: balance, market, etc
baltop
Description: Get the top 10 server balances

Usage: N!baltop

bid
Description: Place a bid on the current bidding item in the channel

Usage: N!bid

economy
Description: Check your or another users balance

Usage: N![economy|bal|balance|eco|e] [member]

givemoney
Description: Give the member's money (Moderators)

Usage: N!givemoney <amount> [members...]

lotto
Description: List the currently running lottos.

Usage: N![lotto|lottery]

lotto cancel
Description: Cancel a lottery

Usage: N!lotto [cancel|delete] <name>

lotto enter
Description: Enter the lottery with the given name.

Usage: N!lotto [enter|join] <name>

lotto new
Description: Create a new lotto, with jacpot payout lasting time in seconds

Usage: N!lotto [new|create] <name> <jackpot> <time>

market
Description: View the current market listings

Usage: N![market|m|pm]

market buy
Description: Buy a given amount of an item from the player market at the cheapest given price

Usage: N!market [buy|purchase|acheter] <id>

market create
Description: Create a new market listing

Usage: N!market [create|createlisting|new|listitem|list] <cost> <amount> <item>

market remove
Description: Remove an item from the market

Usage: N!market [remove|rm] <id>

market search
Description: Search the market for an item

Usage: N!market search <item>

pay
Description: Pay another user money

Usage: N!pay <amount> <member>

setbalance
Description: Set the balance of the given members to an amount

Usage: N![setbalance|set] <amount> [members...]

shop
Description: Get all items currently listed on the server shop

Usage: N!shop

shop additem
Description: Add an item to the server shop, to make an item unsaleable or unbuyable set their respective values to 0 pb!additem Pokeball -> 0 -> 10 Can be sold for 10 and cannot be bought. Must be an existing item! Requires Bot Moderator or Admin

Usage: N!shop [additem|add] <name>

shop buy
Description: Buy an item from the shop

Usage: N!shop buy <item> <amount>

shop removeitem
Description: Remove a listed item

Usage: N!shop removeitem <name>

shop sell
Description: Sell an item to the shop

Usage: N!shop sell <item> <amount>

startbid
Description: Start a bid for an item

Usage: N!startbid <item> <amount> <startbid>

takemoney
Description: Take the member's money (Moderators)

Usage: N!takemoney <amount> [members...]

Groups Commands
Commands for guild management
guild
Description: Get info on a member's guild. Subcommands for guild management

Usage: N![guild|g] [member]

guild create
Description: Create a new guild

Usage: N!guild create <name>

guild delete
Description: Delete your guild

Usage: N!guild delete [name]

guild deposit
Description: Deposit an amount of money into the guild bank

Usage: N!guild deposit <amount> [guild_name]

guild deposititems
Description: Deposit items into the guild's storage, uses {item}x{#} notation

Usage: N!guild deposititems [items...]

guild info
Description: Get info on a guild

Usage: N!guild info <name>

guild invite (OUTTA ORDER)
Description: Invite a user your closed guild

Usage: N!guild invite <user>

guild join
Description: Join a guild (if you have an invite for closed guilds)

Usage: N!guild join <name>

guild kick
Description: Kick a member from a guild

Usage: N!guild kick <user>

guild leave
Description: Leave your guild

Usage: N!guild leave

guild setdescription
Description: Set the guild's description

Usage: N!guild [setdescription|setdesc] <description>

guild seticon
Description: Set the guild's icon

Usage: N!guild seticon <url>

guild setimage
Description: Set the guild's image

Usage: N!guild setimage <url>

guild setmod
Description: Give the listed users mod for your guild (guild owner only)

Usage: N!guild setmod [members...]

guild toggleopen
Description: Toggle the Guilds open state

Usage: N!guild toggleopen

guild transfer
Description: Transfer ownership of a guild to someone else

Usage: N!guild transfer <user>

guild withdraw
Description: Take money from the guild bank

Usage: N!guild withdraw <amount>

guild withdrawitems
Description: Withdraw items from the guild (guild mods only)

Usage: N!guild withdrawitems [items...]

guilds
Description: List guilds

Usage: N!guilds

Inventory Commands
craft
Description: Craft a recipe with a given name from the available server recipes; e.g. rp!craft 5 Apple Pie

Usage: N!craft <number> <name>

give
Description: Give items ({item}x{#}) to a member; ie: rp!give @Henry#6174 Pokeballx3

Usage: N!give <other> [items...]

giveitem
Description: Give an item to a person (Not out of your inventory) Example: rp!giveitem Banana 32 @Henry#6174 @RPGBot#8700 @JoeShmoe#3012

Usage: N!giveitem <item> <num> [members...]

inventory
Description: Check your or another users inventory. Example: rp!inventory @Henry#6174 or just rp!inventory

Usage: N![inventory|i|inv] [member]

lootbox
Description: List the current lootboxes

Usage: N![lootbox|lb] [name]

lootbox buy
Description: Buy a lootbox of the given name

Usage: N!lootbox buy <name>

lootbox create
Description: Create a new lootbox, under the given name for the given cost Use {item}x{#} notation to add items with {#} weight Weight being an integer. For example: rp!lootbox create MyBox 500 bananax2 orangex3. The outcome of the box will be Random Choice[banana, banana, orange, orange, orange] The price can also be an item (or several items), for example rp!lootbox create MyBox Key bananax2 orangex3 or rp!lootbox create MyBox Keyx2 bananax3 orangex3

Usage: N!lootbox [create|new] <name> <cost> [items...]

lootbox delete
Description: Delete a lootbox with the given name

Usage: N!lootbox [delete|remove] <name>

offer
Description: Send a trade offer to another user. Usage: rp!inventory offer @Henry bananax3 applex1 --Format items as {item}x{#}

Usage: N!offer <other> [items...]

recipe
Description: Subcommands for recipes. See data on a specific recipe; e.g. rp!recipe Banana

Usage: N!recipe <name>

recipe create
Description: Create a new recipe; e.g. rp!recipe create Apple Pie

What items must be consumed to follow this recipe? e.g. Applex5 Breadx2 Applex5 Breadx15 "Pie Tinx1" What items will be given upon the completion of this recipe? e.g. "Apple Piex1" "Apple Piex1" "Pie Tinx1" Successfully created new recipe!

Usage: N!recipe create <name>

recipe delete
Description: Delete the recipe with the given name; e.g. rp!recipe delete Apple Pie

Usage: N!recipe delete <name>

recipes
Description: List all the available server recipes

Usage: rp!recipes

respond
Description: Respond to a trade offer by another user. Usage: rp!inventory respond @Henry grapex8 applex1 --Format items as {item}x{#}

Usage: rp!respond <other> [items...]

takeitem
Description: Remove an item from a person's inventory

Usage: rp![takeitem|take] <item> <num> [members...]

use
Description: Use an item. Example rp!use Banana or rp!use Banana 5 To make an item usable, you must put the key used: <message> when you are adding additional information for an item

Usage: rp!use <item> [number=1]

wipeinv
Description: Wipe all inventories. Must be administrator

Usage: rp!wipeinv [members...]

Mapping Commands
map
Description: See the server map

Usage: rp![map|carte] <name>

map buy
Description: Buy an item from the shop on the current tile

Usage: rp!map buy <mapname> <character> <amount> <itemname>

map check
Description: Inspect the current tile a character is on

Usage: rp!map [check|look|regarder|inspect|voir] <mapname> <character>

map create
Description: Create a map that will generate as it is explored. Set xmax and ymax to -1 for an infinite map ($5 Patrons only)

Usage: rp!map create <mapname> <xmax> <ymax>

map delete
Description: Delete a map

Usage: rp!map [delete|supprimer] <name>

map down
Description: Move south on a map

Usage: rp!map [down|south|sud] <mapname> <character>

map generate
Description: Create a custom map for the guild. Usage: rp!map create Earth 64 64 This will create a 64x64 map that will generate as the players explore it

Usage: rp!map [generate|creer|new|nouvelle] <name> <xsize> <ysize>

map left
Description: Move West on a map

Usage: rp!map [left|west|ouest|gauche] <mapname> <character>

map right
Description: Move East on a map

Usage: rp!map [right|east|est|droit] <mapname> <character>

map up
Description: Move North on a map

Usage: rp!map [up|north|nord] <mapname> <character>

Misc Commands
donate
Description: Donation information

Usage: rp!donate

info
Description: Bot Info

Usage: rp!info

ping
Description: Test the bot's connection ping

Usage: rp!ping

rtd
Description: Roll a number of dice with given sides (ndx notation) Example: rp!rtd 3d7 2d4 Optional Additions: Test for success by adding a >/<# Grab the top n rolls by adding ^n Add to the final roll by just adding a number (pos or neg)

Examples of all:
    rp!rtd 8d8 -12 15 ^4 >32
    
    -> Roll failed (30 > 32) ([8 + 7 + 6 + 6] + -12 + 15) (Grabbed top 4 out of 8)
Usage: rp![rtd|rollthedice|dice] [dice...]

source
Description: Displays my full source code or for a specific command. To display the source code of a subcommand you have to separate it by periods, e.g. tag.create for the create subcommand of the tag command.

Usage: rp!source [command]

totalcmds
Description: Get totals of commands and their number of uses

Usage: rp!totalcmds

Pokemon Commands
box
Description: Check the pokemon in your box

Usage: rp!box [member]

pokemon
Description: Subcommands for Pokemon management, see rp!help pokemon Same use as rp!box

Usage: rp![pokemon|p] [member]

pokemon create
Description: Create a new Pokemon to add to your box

Usage: rp!pokemon [create|new]

pokemon info
Description: Get info on a Pokemon

Usage: rp!pokemon info <id>

pokemon release
Description: Release a Pokemon from your box

Usage: rp!pokemon [release|delete|rm|remove] <id>

pokemon trade
Description: Offer a trade to a user. your_id is the ID of the Pokemon you want to give, their_id is the Pokemon you want from them. other being the user you want to trade with

Usage: rp!pokemon trade <your_id> <their_id> <other>

Salary Commands
Salary commands
salaries
Description: See guild salaries

Usage: rp!salaries

salary
Description: Get a role's salary. Also includes salary subcommands

Usage: rp![salary|sal] <role>

salary create
Description: Create a daily salary for a user with the given role. Roles are paid every day at 24:00, every user with the role will receive the amount specified. If a role with a salary is deleted, the salary will also be deleted. For example rp!salary create @Bot Creator 500 Will create a salary of $500 for a user daily rp!salary create @Bot Creator Bananax3 Orangex4 Will create a salary of 3 Bananas and 4 Oranges for a user daily

Usage: rp!salary create <role> [items_or_number...]

salary delete
Description: Remove a created salary

Usage: rp!salary delete <role>

salary payout
Description: Manually pay out salaries for a role or all roles

Usage: rp!salary payout [role]

Settings Commands
currency
Description: Set the guild currency

Usage: rp!currency <currency>

deleteafter
Description: Set a time for messages to be automatically deleted after running. rp!deleteafter 0 to make messages never be deleted

Usage: rp!deleteafter <time>

language
Description: Set the guild language or check the language

Usage: rp!language [language]

loaddnd
Description: This command will pre-load all D&D items and make them available to give

Usage: rp!loaddnd

loaddndmagic
Description: This command will pre-load all D&D Magic items and make them available to give

Usage: rp!loaddndmagic

loaddndshop
Description: This command will pre-load all D&D items and make them available in shop

Usage: rp!loaddndshop

loadmagicshop
Description: This command will pre-load all D&D Magic items and make them available in shop

Usage: rp!loadmagicshop

loadpokemon
Description: This command will pre-load all Pokemon items and make them available to give

Usage: rp!loadpokemon

setstart
Description: Set the money start amount for a guild

Usage: rp!setstart <amount>

settings
Description: Get the current server settings

Usage: rp![settings|s|configuration|conf]

settings additem
Description: Add a custom item. Custom keys that can be used for special additions: image Setting this to a URL will give that item a special thumbnail when info is viewed for it

Usage: rp!settings additem <name>

settings iteminfo
Description: Get info on a server item

Usage: rp!settings iteminfo <item>

settings items
Description: See all items for a guild

Usage: rp!settings items [letter]

settings removeitem
Description: Remove a custom item

Usage: rp!settings [removeitem|deleteitem] <name>

unload
Description: Unload Pokemon, D&D, or D&D Magic items. rp!unload pokemon rp!unload dnd rp!unload dndmagic

Usage: rp!unload <name>

Team Commands
team
Description: Check a character's team

Usage: rp!team <character>

team add
Description: Add a Pokemon to a character's team

Usage: rp!team [add|addmember] <character> <id>

team remove
Description: Remove a Pokemon from a character's team

Usage: rp!team [remove|removemember] <character> <id>

User Commands
Commands for guild management
experience
Description: Get your or another user's level information. Help on this command for experience subcommands EXP is calculated using a 0.1x^2+5x+4 where x is equal to the user's current level Spamming commands or messages will not earn more exp!

Usage: rp![experience|exp] [member]

experience add
Description: Give the given members an amount of experience

Usage: rp!experience add <amount> [members...]

experience disable
Description: Disable EXP settings for a guild

Usage: rp!experience disable

experience enable
Description: Enable EXP settings for a guild

Usage: rp!experience enable

experience setlevel
Description: Set the given members level

Usage: rp!experience [setlevel|set] <level> [members...]

userinfo
Description: Get info on a user

Usage: rp![userinfo|ui] [user]

