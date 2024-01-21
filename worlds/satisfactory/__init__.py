from typing import Dict, List, Set, TextIO, ClassVar, Tuple
from BaseClasses import Item, MultiWorld, ItemClassification
from .GameLogic import GameLogic
from .Items import Items
from .Locations import Locations, LocationData
from .StateLogic import EventId, StateLogic
from .Options import SatisfactoryOptions
from .Regions import SatisfactoryLocation, create_regions_and_return_locations
from .Web import SatisfactoryWebWorld
from ..AutoWorld import World


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
    location_name_to_id = Locations().get_all_location_ids_by_name()
    item_name_groups = Items.get_item_names_per_category()

    game_logic: ClassVar[GameLogic] = GameLogic()
    state_logic: StateLogic
    items: Items

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.items = None

    def generate_early(self) -> None:
        initial_unlocked_items = self.get_initial_unlocked_items()
        self.state_logic = StateLogic(self.player, self.options, initial_unlocked_items)
        self.items = Items(self.player, self.game_logic, self.random)

        if self.options.final_elevator_tier.value <= 0 and self.options.final_resource_sink_points.value <= 0:
                raise Exception("""Satisfactory: player {} needs to choose a goal,
                    both FinalElevatorTier and FinalResourceSinkPoints are set to off"""
                    .format(self.multiworld.player_name[self.player]))


    def create_regions(self) -> None:
        locations: List[LocationData] = Locations(self.game_logic, self.state_logic, self.items).get_locations()
        create_regions_and_return_locations(self.multiworld, self.player, self.game_logic, self.state_logic, locations)


    def create_items(self) -> None:
        self.setup_events()

        number_of_locations: int = len(self.multiworld.get_unfilled_locations(self.player))

        self.multiworld.itempool += self.items.build_item_pool(self.random, self.options, number_of_locations)


    def set_rules(self) -> None:
        last_elevator_tier: int = \
            len(self.game_logic.space_elevator_tiers) if self.options.final_resource_sink_points.value > 0 \
                else self.options.final_elevator_tier.value

        required_parts: Set[str] = set(self.game_logic.space_elevator_tiers[last_elevator_tier - 1].keys())

        if self.options.final_resource_sink_points > 0:
            required_parts.union(self.game_logic.buildings["AWESOME Sink"].inputs)

        required_parts_tuple: Tuple[str, ...] = tuple(required_parts)

        self.multiworld.completion_condition[self.player] = \
            lambda state: self.state_logic.can_produce_all(state, required_parts_tuple)


    def fill_slot_data(self) -> Dict[str, object]:
        hub_layout: List[List[Dict[str, int]]] = []

        for tier, milestones in enumerate(self.game_logic.hub_layout, 1):
            hub_layout.append([])
            for milestone, parts in enumerate(milestones, 1):
                 hub_layout[tier - 1].append({})
                 for part, amount in parts.items():
                    hub_layout[tier - 1][milestone - 1][f"{self.item_name_to_id[part]}"] = amount

        return {
            "Data": {
                "HubLayout": hub_layout,
                "SlotsPerMilestone": self.game_logic.slots_per_milestone,
                "Options": {
                    "FinalElevatorTier": self.options.final_elevator_tier.value,
                    "FinalResourceSinkPoints": self.options.final_resource_sink_points.value,
                    #"AllowDroppodProgression": bool(self.options.allow_droppod_progression),
                    "FreeSampleEquipment": self.options.free_sample_equipment.value,
                    "FreeSampleBuildings": self.options.free_sample_buildings.value,
                    "FreeSampleParts": self.options.free_sample_parts.value,
                    "FreeSampleRadioactive": bool(self.options.free_sample_radioactive),
                    "EnergyLink": bool(self.options.energy_link)
                }
            },
            "DeathLink": bool(self.options.death_link)
        }


    def write_spoiler(self, spoiler_handle: TextIO):
        self.items.write_progression_chain(self.multiworld, spoiler_handle)


    def get_filler_item_name(self) -> str:
        return self.items.get_filler_item_name(self.random, self.options)


    def setup_events(self):
        location: SatisfactoryLocation
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item_name = location.event_name

                item = Item(item_name, ItemClassification.progression, EventId, self.player)

                location.place_locked_item(item)
                location.show_in_spoiler = False


    def create_item(self, name: str) -> Item:
        return Items.create_item(self.items, name, self.player)


    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in self.item_name_groups['Parts']:
                excluded_items.add(item.name)

        return excluded_items


    def get_initial_unlocked_items(self) -> Set[str]:
        return {
            # Unlocked as part of core starting recipes
            # /Game/FactoryGame/Schematics/Schematic_StartingRecipes.Schematic_StartingRecipes
            "Recipe: Iron Ingot",
            "Recipe: Iron Plate",
            "Recipe: Iron Rod",
            "Building: The HUB",
            "Recipe: Xeno-Zapper",
            "Building: Craft Bench",
            # (Iron Ore scanning)

            # Tier 0 rewards
            # HUB 0-1
            "Building: Equipment Workshop",
            "Recipe: Portable Miner",
            # (3 Inventory slots)

            # HUB 0-2
            "Building: Smelter",
            "Building: Power Line",
            "Recipe: Copper Ingot",
            "Recipe: Wire",
            "Recipe: Cable",
            # (Copper Ore scanning)

            # HUB 0-3
            "Building: Constructor",
            "Building: Power Pole Mk.1",
            "Recipe: Concrete",
            "Recipe: Screw",
            "Recipe: Reinforced Iron Plate",
            # (Limestone scanner)

            # HUB 0-4
            "Building: Conveyor Pole",
            "Building: Conveyor Mk.1",
            # (3 Inventory slots)

            # HUB 0-5
            "Building: Miner Mk.1",
            "Building: Storage Container",
            # (3 Inventory slots)

            # HUB 0-6
            "Building: Space Elevator", # TODO do we want to leave this here or remove it?
            "Building: Biomass Burner",
            "Recipe: Biomass (Leaves)", # TODO do we want to leave this here or remove it?
            "Recipe: Biomass (Wood)", # TODO do we want to leave this here or remove it?
        }
