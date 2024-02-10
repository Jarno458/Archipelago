# Satisfactory

<!-- Spellchecker config - cspell:ignore FICSIT Nobelisk Zoop -->

## Where is the settings page?

The [player settings page for this game](../player-settings)
contains all the options you need to configure and export a config file.

## What does randomization do to this game?

In Satisfactory, the HUB Milestones and MAM Research Nodes are shuffled,
causing technologies to be obtained in a non-standard order.
The costs of unlocking these technologies are also shuffled.

TODO Hard Drive scanning results are also optionally shuffled,
meaning that scanning a Hard Drive will result in a selection between 3 random items.

## What is the goal of Satisfactory?

The player can choose from a number of goals using their YAML settings:

- Complete a certain [Space Elevator](https://satisfactory.wiki.gg/wiki/Space_Elevator) tier with optionally randomized required items
- Supply items to the [AWESOME Sink](https://satisfactory.wiki.gg/wiki/AWESOME_Sink) totalling a configurable amount of points to finish.

## What Satisfactory items can appear in other players' worlds?

Satisfactory's technologies are removed from the HUB and MAM and placed into other players' worlds.
When those technologies are found, they are sent back to Satisfactory
along with, optionally, free samples of those technologies.

<!-- TODO Other players' worlds may have Resource Packs of building materials, ammunition, or FICSIT Coupons. -->

## What is a free sample?

A free sample is a package of items in Satisfactory granted by a technology received from another world.
For equipment and component crafting recipes, this is the output product.
For buildings, this is the ingredients for the building.
For example, receiving the [Nobelisk Detonator MAM Node](https://satisfactory.wiki.gg/wiki/Nobelisk_Detonator#Unlocking)
would give you one Nobelisk Detonator and 50 Nobelisk,
receiving the [Jump Pads Milestone](https://satisfactory.wiki.gg/wiki/Milestones#Tier_2)
would give you the ingredients to construct 5 Jump Pads and 5 U-Jelly Landing Pads, etc.

TODO FreeSamples implements this but AP needs config for it:
You can separately configure how many samples to receive for buildings, equipment, and crafting components.

## What does another world's item look like in Satisfactory?

In Satisfactory, items which need to be sent to other worlds appear in the HUB and MAM as info cards
in a similar manner to the base game's building and recipe unlocks. They have the Archipelago category icon.
You can hover over them to read a description
Their icons are color coded to indicate what Archipelago progression type they are.

![TODO screenshot](/static/generated/docs/Satisfactory/HUB-screenshot.png)

Upon successful unlock of the technology, the item will be sent to its home world.

## When the player receives an item, what happens?

When the player receives a technology, it is instantly unlocked and able to be crafted or constructed.
A message will appear in the chat to notify the player,
and if free samples are enabled the player may also receive some items delivered directly to their inventory.

## What is EnergyLink?

TODO not fully implemented

EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld.
In Satisfactory, if enabled in the player settings, Archipelago Portal buildings can be crafted and placed, which allow
depositing excess energy and supplementing energy deficits, much like [Power Storage](https://satisfactory.wiki.gg/wiki/Power_Storage) buildings.

Each placed EnergyLink Bridge provides TODO MW of throughput. The shared storage has unlimited capacity, but TODO% of energy
is lost during depositing, and a conversion ratio of TODO is applied when sending energy across different games (ex. Satisfactory to Factorio). The amount of energy currently in the shared storage is displayed in the Archipelago client.
It can also be queried by typing `/TODO` in-game.

## What is the Archipelago Portal?

TODO not implemented

The Archipelago Portal is a building that allows players to transfer items between multiple Satisfactory worlds.

## What is a Trap?

You can optionally enable that some Traps be mixed into the item pool.
Traps are items will instantly trigger some sort of surprise on the player when received.
Their severity varies from annoyance to killing the player.

## Where do I run Archipelago commands?

You can use the game's build-in chat menu.
Check the game's keybinding options to see how to open it.

## Multiplayer and Dedicated Servers

You cannot play an Archipelago Slot in multiplayer at the moment.
The team hopes to add this feature in the future,
but research must still be performed to assess its viability.

The Satisfactory modding toolkit does not yet support dedicated servers,
so neither does the Archipelago mod.

## Mods

It is possible to load other Satisfactory mods in tandem with the Archipelago Satisfactory mod.
However, no guarantee is made that any mods, except those listed below, will work correctly,
especially if they affect game progression, recipes, or add unlocks to base-game technologies.
Use other mods at your own risk, support will not be offered.

The following mods are **required dependencies** of the Archipelago mod and **will automatically be installed for you**
when you install it using the Satisfactory Mod Manager:

- [ContentLib](https://ficsit.app/mod/ContentLib) - Runtime content generation
- [Free Samples](https://ficsit.app/mod/FreeSamples) - Used to implement the Free Samples options
- [MAM Enhancer](https://ficsit.app/mod/MAMTips) - Allows viewing MAM research nodes in detail. Enables you to hover over the items/unlocks of a node to see more info, especially important when their names get long

The following mods are known to work with Archipelago:

<!-- Nog's Chat currently broken -->
<!-- - [Nog's Chat](https://ficsit.app/mod/NogsChat) - Easily repeat past chat messages, improving the user experience of running Archipelago commands in the game's chat window. -->
- [The FICSIT Information Tool](https://ficsit.app/mod/TFIT) - View how many Sink Points items are worth and how points-profitable recipes are. Helpful for the AWESOME Points goal.
- [Faster Manual Crafting Redux](https://ficsit.app/mod/FasterManualCraftingRedux) - Reduce the early game manual crafting grind with a manual crafting speed that ramps up as you craft larger batches at once.

<!-- TODO Test these  -->
<!-- - [Infinite Zoop](https://ficsit.app/mod/InfiniteZoop) - Adds a research tree in the MAM where you can improve your Zoop capacity. Also enables multi-row & column Wall and Foundation construction.  -->
<!-- - [Nog's Research](https://ficsit.app/mod/NogsResearch/) - Queue Milestones and MAM Nodes for automatic research in the style of Factorio's research queue. Queue type might need to be changed to soft class reference to save CL schematics. -->
