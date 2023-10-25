from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location, CollectionState
from .Locations import LocationData
from .GameLogic import GameLogic
from .Rules import StateLogic

def create_regions_and_return_locations(world: MultiWorld, player: int, 
            game_logic: GameLogic, state_logic: StateLogic, locations: Tuple[LocationData, ...]):
    locations_per_region = get_locations_per_region(locations)
    
    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Overworld"),
        create_region(world, player, locations_per_region, "Gas Area"),
        create_region(world, player, locations_per_region, "Radioactive Area"),
        create_region(world, player, locations_per_region, "Hub Tier 1"),
        create_region(world, player, locations_per_region, "Hub Tier 2"),
        create_region(world, player, locations_per_region, "Hub Tier 3"),
        create_region(world, player, locations_per_region, "Hub Tier 4"),
        create_region(world, player, locations_per_region, "Hub Tier 5"),
        create_region(world, player, locations_per_region, "Hub Tier 6"),
        create_region(world, player, locations_per_region, "Hub Tier 7"),
        create_region(world, player, locations_per_region, "Hub Tier 8"),
        create_region(world, player, locations_per_region, "Mam"),
        create_region(world, player, locations_per_region, "AWESOME Shop")
    ]

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        for minestone, _ in enumerate(milestones_per_hub_tier, 1):
            regions.append(create_region(world, player, locations_per_region, f"Hub {hub_tier}-{minestone}"))

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())
        
    world.regions += regions

    connect(world, player, "Menu", "Overworld")
    connect(world, player, "Overworld", "Hub Tier 1")
    connect(world, player, "Overworld", "Hub Tier 2")
    connect(world, player, "Overworld", "Hub Tier 3", lambda state: state.has("Elevator Tier 1", player))
    connect(world, player, "Overworld", "Hub Tier 4", lambda state: state.has("Elevator Tier 1", player))
    connect(world, player, "Overworld", "Hub Tier 5", lambda state: state.has("Elevator Tier 2", player))
    connect(world, player, "Overworld", "Hub Tier 6", lambda state: state.has("Elevator Tier 2", player))
    connect(world, player, "Overworld", "Hub Tier 7", lambda state: state.has("Elevator Tier 3", player))
    connect(world, player, "Overworld", "Hub Tier 8", lambda state: state.has("Elevator Tier 3", player))
    connect(world, player, "Overworld", "Gas Area", lambda state: state.has("Gas Mask", player))
    connect(world, player, "Overworld", "Radioactive Area", lambda state: state.has("Hazmat Suit", player))
    connect(world, player, "Overworld", "Mam") # should prob require mam building and seperated tree"s
    connect(world, player, "Overworld", "AWESOME Shop") # should prob require AWESOME shop building

    def can_produce_all_allowing_handcrafting(parts: Tuple[str, ...]) -> Callable[[CollectionState], bool]:
        def logic_rule(state: CollectionState):
            return state_logic._satisfactory_can_produce_all_allowing_handcrafting(state, game_logic, parts)

        return logic_rule

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        for minestone, parts_per_milestone in enumerate(milestones_per_hub_tier, 1):
            connect(world, player, f"Hub Tier {hub_tier}", f"Hub {hub_tier}-{minestone}", 
                can_produce_all_allowing_handcrafting(parts_per_milestone.keys()))


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions:
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


def connect(world: MultiWorld, player: int, source: str, target: str, 
        rule: Optional[Callable[[CollectionState], bool]] = None):

    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

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
