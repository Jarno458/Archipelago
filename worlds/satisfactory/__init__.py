from typing import Dict, List, Set, Tuple, TextIO, Optional, ClassVar
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .GameLogic import GameLogic
from .Items import Items
from .Locations import get_locations, LocationData
from .Rules import EventId, StateLogic
from .Options import SatisfactoryOptions
from .Regions import create_regions_and_return_locations
from ..AutoWorld import World, WebWorld


class SatisfactoryWebWorld(WebWorld):
    theme = "dirt"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Satisfactory Archipelago mod and connect it to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Robb", "Jarno"]
    )
    tutorials = [setup]


class SatisfactoryWorld(World):
    """
    Satisfactory is a first-person open-world factory building game with a dash of exploration and combat.
    Explore an alien planet, create multi-story factories, and enter conveyor belt heaven!
    """

    game = "Satisfactory"
    options_dataclass = SatisfactoryOptions
    options: SatisfactoryOptions
    topology_present = False
    data_version = 0
    web = SatisfactoryWebWorld()

    item_name_to_id = Items.item_names_and_ids
    location_name_to_id = {location.name: location.code for location in get_locations(None, None, None)}
    item_name_groups = Items.get_item_names_per_category()

    game_logic: ClassVar[GameLogic] = GameLogic()
    state_logic: StateLogic
    items: Items
    
    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)


    def generate_early(self) -> None:
        self.state_logic = StateLogic(self.player, self.options)
        self.items = Items(self.player, self.game_logic, self.random)

        if self.options.final_elevator_tier <= 0 and self.options.final_resource_sink_points <= 0:
                raise Exception("""Satisfactory: player {} needs to choose a goal,
                    both FinalElevatorTier and FinalResourceSinkPoints are set to off"""
                    .format(self.multiworld.player_name[self.player]))


    def create_regions(self) -> None:
        locations: Tuple[LocationData, ...] = get_locations(self.game_logic, self.state_logic, self.items)
        create_regions_and_return_locations(
            self.multiworld, self.player, self.game_logic, self.state_logic, locations)


    def create_items(self) -> None:
        self.create_initial_unlocked_items()
        self.setup_events()

        excluded_items = set() #self.get_excluded_items()

        self.multiworld.itempool += self.items.build_item_pool(self.random, excluded_items, 
            len(self.multiworld.get_unfilled_locations(self.player)))


    def set_rules(self) -> None:
        last_elevator_tier: int = \
            len(self.game_logic.space_elevator_tiers) if self.options.final_resource_sink_points > 0 \
                else self.options.final_elevator_tier

        required_parts = self.game_logic.space_elevator_tiers[last_elevator_tier - 1]
        self.multiworld.completion_condition[self.player] = \
            lambda state: self.state_logic._satisfactory_can_produce_all(state, required_parts)


    def fill_slot_data(self) -> Dict[str, object]:
        hub_layout: List[List[Dict[str, int]]] = []

        for tier, milestones in enumerate(self.game_logic.hub_layout, 1):
            hub_layout.append([])
            for milestone, parts in enumerate(milestones, 1):
                 hub_layout[tier - 1].append({})
                 for part, amount in parts.items():
                     self.item_name_to_id[part]
                     hub_layout[tier - 1][milestone - 1][f"{self.item_name_to_id[part]}"] = amount

        return {
            "Data": {
                "HubLayout": hub_layout,
                "SlotsPerMilestone": self.game_logic.slots_per_milestone,
                "Options": {
                    "ElevatorTier": int(self.options.final_elevator_tier),
                    "ResourceSinkPoints": int(self.options.final_resource_sink_points),
                    "AllowDroppodProgression": bool(self.options.allow_droppod_progression),
                    "FreeSampleEquipment": int(self.options.free_sample_equipment),
                    "FreeSampleBuildings": int(self.options.free_sample_buildings),
                    "FreeSampleParts": int(self.options.free_sample_parts),
                    "FreeSampleRadioactive": bool(self.options.free_sample_radioactive),
                    "DeathLink": bool(self.options.death_link),
                    "EnergyLink": bool(self.options.energy_link)
                }
            }
        }


    def write_spoiler(self, spoiler_handle: TextIO):
        self.items.write_progression_chain(self.multiworld, spoiler_handle)
        pass


    def get_filler_item_name(self) -> str:
        return self.items.get_filler_item_name(self.random, self.options)


    def setup_events(self):
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item = Item(location.name, ItemClassification.progression, EventId, self.player)

                location.place_locked_item(item)
                location.show_in_spoiler = False


    def create_item(self, name: str) -> Item:
        return self.items.create_item(name)


    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in self.item_name_groups['Parts']:
                excluded_items.add(item.name)

        return excluded_items


    def create_initial_unlocked_items(self) -> None:
        initial_unlocked_items: Tuple[str, ...] = (
            #Tier 0 rewards
            "Building: Constructor",
            "Building: Miner Mk.1",
            "Building: Smelter",

            "Recipe: Limestone",
            "Recipe: Raw Quartz",
            "Recipe: Iron Ore",
            "Recipe: Copper Ore",
            "Recipe: Coal",
            "Recipe: Sulfur",
            "Recipe: Caterium Ore",
            "Recipe: Water",

            "Recipe: Iron Ingot",
            "Recipe: Copper Ingot",

            "Recipe: Concrete",
            "Recipe: Iron Plate",
            "Recipe: Iron Rod",

            "Recipe: Reinforced Iron Plate",
            "Recipe: Screw",
            "Recipe: Wire",
            "Recipe: Cable"
        )

        for item_name in initial_unlocked_items:
            self.multiworld.push_precollected(self.create_item(item_name))