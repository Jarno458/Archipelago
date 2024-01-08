from dataclasses import dataclass
from Options import PerGameCommonOptions, DeathLink, Range, Toggle, OptionList, StartInventoryPool, NamedRange

class ElevatorTier(NamedRange):
    """Ship these Space Elevator packages to finish"""
    display_name = "Goal: Space Elevator shipment"
    default = 2
    range_start = 0
    range_end = 4
    special_range_names = {
        "disabled": 0,
        "one package (tiers 1-2)": 1,
        "two packages (tiers 1-4)": 2,
        "three packages (tiers 1-6)": 3,
        "four packages (tiers 7-8)": 4,
    }

class ResourceSinkPoints(NamedRange):
    """Sink an amount of items totalling this amount of points to finish.

    In the base game, it takes 208 coupons to unlock every unique crafting recipe, or 1813 coupons to purchase every non-producible item.

    Use the TFIT mod or the Satisfactory wiki to find out how many points items are worth.

    If you have Free Samples enabled, consider setting this higher so that you can't reach the goal just by sinking your Free Samples."""
    display_name = "Goal: AWESOME Sink points"
    default = 0
    range_start = 0
    range_end = 18436379500
    special_range_names = {
        "disabled": 0,
        "50 coupons (~2M points)": 2166000,
        "100 coupons (~18M points)": 17804500,
        "150 coupons (~61M points)": 60787500,
        "200 coupons (~145M points)": 145053500,
        "250 coupons (~284M points)": 284442000,
        "300 coupons (~493M points)": 492825000,
        "350 coupons (~784M points)": 784191000,
        "400 coupons (~1,2B points)": 1172329500,
        "450 coupons (~1,7B points)": 1671112500,
        "500 coupons (~2B points)": 2294578500,
        "550 coupons (~3B points)": 3056467000,
        "600 coupons (~4B points)": 3970650000,
        "650 coupons (~5B points)": 5051216000,
        "700 coupons (~6B points)": 6311854500,
        "750 coupons (~8B points)": 7766437500,
        "800 coupons (~9B points)": 9429103500,
        "850 coupons (~11B points)": 11313492000,
        "900 coupons (~13B points)": 13433475000,
        "950 coupons (~16B points)": 15803241000,
        "1000 coupons (~18B points)": 18436379500
    }

class AllowDroppodProgression(Toggle):
    """Allow hard drive Gacha to contain progression items."""
    display_name = "Allow Hard-drive Progression"

# class TechTreeInformation(Choice):
#     """TODO Implement me
#     How much information should be displayed in the tech tree.

#     None: No indication what a technology unlocks or who it is for
#     Advancement: Indicates which technologies unlock items that are considered logical advancements
#     Player: Indicates what player will receive something when a technology is unlocked
#     Player and Advancement: Indicates which technologies unlock items that are considered logical advancements, and who they are for
#     Full: Labels with exact names and recipients of unlocked items; all technologies are prefilled into the !hint command.
#     """
#     display_name = "Technology Information"
#     option_none = 0
#     option_advancement = 1
#     option_player = 2
#     option_player_and_advancement = 3
#     option_full = 4
#     default = 4

class FreeSampleEquipment(Range):
    """How many free sample items of Equipment items should be given when they are unlocked.
    (ex. Jetpack, Rifle)"""
    display_name = "Free Samples: Equipment"
    default = 1
    range_start = 0
    range_end = 10


class FreeSampleBuildings(Range):
    """How many copies of a Building's construction cost to give as a free sample when they are unlocked.
    Space Elevator is always excluded.
    (ex. Packager, Constructor, Smelter)"""
    display_name = "Free Samples: Buildings"
    default = 5
    range_start = 0
    range_end = 10


class FreeSampleParts(NamedRange):
    """How free sample items of general crafting components should be given when a recipe for them is unlocked.
    Space Elevator Project Parts are always excluded.
    Negative numbers mean that fraction of a full stack.

    If you want samples of radioactive parts, you must manually enable that in the Free Samples mod configuration in-game.
    (ex. Iron Plate, Packaged Turbofuel, Reinforced Modular Frame)"""
    display_name = "Free Samples: Parts"
    default = -1
    range_start = -5
    range_end = 500
    special_range_names = {
        "disabled": 0,
        "half_stack": -2,
        "one_stack": -1,
        "1": 1,
        "50": 50,
        "100": 100,
        "200": 200,
        "500": 500,
    }

class FreeSampleRadioactive(Toggle):
    """Allow free samples to be Radioactive."""
    display_name = "Free Samples: Radioactive"

class TrapChance(Range):
    """Chance of traps in the item pool.
    Traps will only replace filler items such as parts and resources"""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10

class Traps(OptionList):
    """List of traps that may be in the item pool to find"""
    display_name = "Traps Types"
    valid_keys = { 
        "Doggo Pulse Nobelisk", 
        "Doggo Nuke Nobelisk", 
        "Doggo Gas Nobelisk", 
        "Hog Basic",
        "Hog Alpha",
        "Hog Cliff",
        "Hog Cliff Nuclear",
        "Hog Johnny",
        "Hatcher",
        "Stinger Small",
        "Stinger Elite",
        "Stinger Gas",
        "Spore Flower",
        "Spitter Forest",
        "Spitter Forest Alpha",
        "Not The Bees",
        "Nuclear Waste (ground)",
        "Plutonium Waste (ground)",

        # Radioactive parts
        "Uranium",
        "Uranium Fuel Rod",
        "Uranium Waste (item)",
        "Plutonium Fuel Rod",
        "Plutonium Pellet",
        "Plutonium Waste (item)",
        "Non-fissile Uranium",
    }
    default = [ 
        "Doggo Pulse Nobelisk", 
        "Hog Basic",
        "Spitter Forest"
    ]

class EnergyLink(Toggle):
    """Allow sending energy to other worlds. 25% of the energy is lost in the transfer."""
    display_name = "EnergyLink"

@dataclass
class SatisfactoryOptions(PerGameCommonOptions):
    final_elevator_tier: ElevatorTier
    final_resource_sink_points: ResourceSinkPoints
    # tech_tree_information: TechTreeInformation # TODO: NYI
    # allow_droppod_progression: AllowDroppodProgression #TODO: NYI
    free_sample_equipment: FreeSampleEquipment
    free_sample_buildings: FreeSampleBuildings
    free_sample_parts: FreeSampleParts
    free_sample_radioactive: FreeSampleRadioactive
    trap_chance: TrapChance
    traps: Traps
    death_link: DeathLink
    energy_link: EnergyLink
    start_inventory_from_pool: StartInventoryPool
