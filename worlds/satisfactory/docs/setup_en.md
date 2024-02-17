# Satisfactory Setup Guide

<!-- Spellchecker config - cspell:ignore FICSIT Randomizer Plando -->

## Required Software

- [Satisfactory (Steam)](https://store.steampowered.com/app/526870/Satisfactory/)
  or [Satisfactory (Epic)](https://www.epicgames.com/store/en-US/product/satisfactory/home)
- Latest version of **Satisfactory Mod Manager**: [Satisfactory Mod Manager GitHub Releases](https://github.com/satisfactorymodding/SatisfactoryModManager/releases/latest/)

## Overview

This guide will walk you through installing the Satisfactory Archipelago mod via the Mod Manager
and entering Archipelago server connection details in the mod configuration options.
The server will send the required data to the game client and create the content required by the seed at runtime.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them.
Satisfactory player settings page: [Satisfactory Settings Page](/games/Satisfactory/player-settings)

### Verifying Your Config File

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page.
YAML
Validator page: [Yaml Validation Page](/mysterycheck)

### Advanced Configuration

TODO link to Advanced Settings page and Plando

## Prepare to Host Your Own Satisfactory Game

In Archipelago, multiple Satisfactory worlds may be played simultaneously.
Each of these worlds must be hosted by a Satisfactory game client, each of which is connected to the Archipelago Server.

- **Satisfactory Client** - The Satisfactory instance which will be used to host, and play, the game.
- **Archipelago Server** - The central Archipelago server, which connects all games to each other.

It is important to note that the Satisfactory Archipelago mod is not yet compatible with dedicated servers or in-game multiplayer.
Each Satisfactory world must be hosted and played by an individual player.

## Installing Satisfactory

Purchase and install Satisfactory via one the sources linked [above](#required-software).
Launch the game at least once to ensure that the Mod Manager can detect the game's install location.

Make sure that you are running the correct branch of the game (Early Access or Experimental) that Archipelago supports.
Learn how to switch branches here:
[Satisfactory Modding Documentation FAQ: Switching Branches](https://docs.ficsit.app/satisfactory-modding/latest/faq.html#_how_do_i_get_the_experimental_or_early_access_branch_of_the_game)

## Installing Satisfactory Mod Manager

The Mod Manager is used to install and manage mods for Satisfactory.
It automatically detects your game install location and automatically handles mod dependencies for you.

Download the Mod Manager here:
[Satisfactory Mod Manager GitHub Releases](https://github.com/satisfactorymodding/SatisfactoryModManager/releases/latest/)

Directions for setting up the Mod Manager can be found here:
[Satisfactory Modding Documentation FAQ: Installing the Mod Manager](https://docs.ficsit.app/satisfactory-modding/latest/ForUsers/SatisfactoryModManager.html)

## Installing the Archipelago Mod

Once the Mod Manager is installed you can install mods directly in the manager or via the Satisfactory Mod Repository website.

Inside the Mod Manager, search for and install the "Archipelago Multi-World Randomizer".
Alternatively, visit the mod page: [Archipelago Multi-World Randomizer on Ficsit.app](https://ficsit.app/mod/Archipelago).
Once on the mod page, click the "Install" link in the Latest Versions card.

The Mod Manager will install all required dependency mods for you with no additional action required.

As soon as you have the relevant mods installed, you do not need to launch the game through the Mod Manager - desktop shortcuts, Steam, Epic. etc. will all launch the game with mods still loaded.

TODO for development time only: Here is a link to the manual install directions in case the Archipelago mod developers send you a custom version for testing: <https://docs.ficsit.app/satisfactory-modding/latest/ManualInstallDirections.html>

## Installing Additional Mods

You may also wish to install some of the suggested mods mentioned on the
[Archipelago Info page for Satisfactory](/games/Satisfactory/info/en#additional-mods).

## Entering Connection Details

After you have installed the mods, launch the game via the Mod Manager or via your preferred method.
Once the game has launched, click on the 'Mods' button on the main menu and open the Archipelago entry.

Next, enter the connection details in the relevant fields.
You can hover over the fields in the menu for more information and example values.

- **URI**: Archipelago Server URI and port, for example, `archipelago.gg:49236`
- **Username**: The name you entered as your Player Name when you created your config file. It's also listed in the Name column of your room page.
- **Password**: The password for your slot, blank if you did not assign one.
- **Archipelago Enabled**: Make sure this is checked, otherwise no server connection will be attempted.
- **Debug Mode**: Don't enable it unless the developers ask you to when reporting problems.
- **Force override settings in save**: When loading a save, will use the `URI`, `Username` and `Password` provided here rather than the values stored in the save (usefull when the server changed ports)

Note that the Satisfactory Client does _not_ need a copy of your config file.
The mod communicates with the Archipelago Server, which already has your config file,
to generate the required content at runtime.

## Creating a New World

Once you have entered connection details, create a new world using the game's New Game menu.
Make sure to check 'Skip Intro' if you don't want to deal with the game's tutorial sequence.
Consider enabling Advanced Game Settings to allow dealing with bugs that may arise.
You may also wish to switch the "Keep Inventory" setting to "Keep Everything" to avoid dropping items when you die,
although this will never lock you out of progression.

## Verifying Connection Success

Once connected to the AP server,
you can issue the `/help` command in the game's chat to list available commands like `!hint`.
For more information about the commands you can use, see the [Commands Guide](/tutorial/Archipelago/commands/en) and
[Other Settings](#other-settings).
Note that Archipelago commands are not prefixed with `!` for Satisfactory.

## Other Settings

TODO implement filter_item_sends and bridge_chat_out mentioned in the Factorio guide?

## Troubleshooting

TODO what is the scope of this section? How much do we help with vs. sending people somewhere else

- If you are having trouble connecting to the Archipelago server,
  make sure you have entered the correct server address and port.
- If you are having trouble using the Satisfactory Mod Manager, join the Satisfactory Modding Discord for support.
  Discord: [Satisfactory Modding Discord](https://discord.gg/xkVJ73E)
- If you encounter a game crash, please report it to the Satisfactory Modding Discord.
  Please explain what you were doing when the crash occurred and generate a debug zip following the directions below.
  Discord: [Satisfactory Modding Discord](https://discord.gg/xkVJ73E)
  Generating a debug zip: [Satisfactory Modding Documentation FAQ](https://docs.ficsit.app/satisfactory-modding/latest/faq.html#_where_can_i_find_the_games_log_files)

## Additional Resources

- Satisfactory Wiki: [Satisfactory Official Wiki](https://satisfactory.wiki.gg/wiki/)
- Satisfactory Modding FAQ page: [Satisfactory Modding Documentation FAQ](https://docs.ficsit.app/satisfactory-modding/latest/faq.html)
