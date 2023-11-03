from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location, CollectionState
from .Locations import LocationData
from .GameLogic import GameLogic
from .Rules import StateLogic

def create_regions_and_return_locations(world: MultiWorld, player: int, 
            game_logic: GameLogic, state_logic: StateLogic, locations: Tuple[LocationData, ...]):
    
    region_names: List[str] = [
        "Menu",
        "Overworld",
        "Gas Area",
        "Radioactive Area",
        "Mam",
        "AWESOME Shop"
    ]

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        region_names.append(f"Hub Tier {hub_tier}")

        for minestone, _ in enumerate(milestones_per_hub_tier, 1):
            region_names.append(f"Hub {hub_tier}-{minestone}")

    locations_per_region: Dict[str, LocationData] = get_locations_per_region(locations)
    regions: Dict[str, Region] = create_regions(world, player, locations_per_region, region_names)

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())
        
    world.regions += regions.values()

    connect(player, regions, "Menu", "Overworld")
    connect(player, regions, "Overworld", "Hub Tier 1")
    connect(player, regions, "Overworld", "Hub Tier 2")
    connect(player, regions, "Overworld", "Hub Tier 3", lambda state: state.has("Elevator Tier 1", player))
    connect(player, regions, "Overworld", "Hub Tier 4", lambda state: state.has("Elevator Tier 1", player))
    connect(player, regions, "Overworld", "Hub Tier 5", lambda state: state.has("Elevator Tier 2", player))
    connect(player, regions, "Overworld", "Hub Tier 6", lambda state: state.has("Elevator Tier 2", player))
    connect(player, regions, "Overworld", "Hub Tier 7", lambda state: state.has("Elevator Tier 3", player))
    connect(player, regions, "Overworld", "Hub Tier 8", lambda state: state.has("Elevator Tier 3", player))
    connect(player, regions, "Overworld", "Gas Area", lambda state: state.has("Gas Mask", player))
    connect(player, regions, "Overworld", "Radioactive Area", lambda state: state.has("Hazmat Suit", player))
    connect(player, regions, "Overworld", "Mam") # should prob require mam building and seperated tree"s
    connect(player, regions, "Overworld", "AWESOME Shop") # should prob require AWESOME shop building

    def can_produce_all_allowing_handcrafting(parts: Tuple[str, ...]) -> Callable[[CollectionState], bool]:
        def logic_rule(state: CollectionState):
            return state_logic.can_produce_all_allowing_handcrafting(state, game_logic, parts)

        return logic_rule

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        for minestone, parts_per_milestone in enumerate(milestones_per_hub_tier, 1):
            connect(player, regions, f"Hub Tier {hub_tier}", f"Hub {hub_tier}-{minestone}", 
                can_produce_all_allowing_handcrafting(parts_per_milestone.keys()))


def throwIfAnyLocationIsNotAssignedToARegion(regions: Dict[str, Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions.values():
        existingRegions.add(region.name)

    if (regionNames - existingRegions):
        raise Exception(f"Satisfactory: the following regions are used in locations: {regionNames - existingRegions}, but no such region exists")


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Location(player, location_data.name, location_data.code, region)

    if (location_data.rule):
        location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    return location


def create_region(world: MultiWorld, player: int, 
        locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:

    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def create_regions(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                    region_names: List[str]) -> Dict[str, Region]:

    regions: Dict[str, Region] = {}

    for name in region_names:
        regions[name] = create_region(world, player, locations_per_region, name)

    return regions


def connect(player: int, regions: Dict[str, Region], source: str, target: str, 
        rule: Optional[Callable[[CollectionState], bool]] = None):

    sourceRegion = regions[source]
    targetRegion = regions[target]

    connection = Entrance(player, target, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
