from typing import List, Optional, Callable, Tuple, Dict, Iterable
from BaseClasses import CollectionState
from .GameLogic import GameLogic, Recipe, Building, PowerInfrastructureLevel
from .StateLogic import StateLogic, EventId, part_event_prefix, building_event_prefix
from .Items import Items


class LocationData():
    region: str
    name: str
    event_name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]]

    def __init__(self, region: str, name: str, code: Optional[int], event_name: Optional[str] = None,
                 rule: Optional[Callable[[CollectionState], bool]] = None):
        self.region = region
        self.name = name
        self.code = code
        self.rule = rule
        self.event_name = event_name or name


class Part(LocationData):
    @staticmethod
    def get_parts(state_logic: StateLogic, recipes: Tuple[Recipe, ...], name: str, items: Items) -> List[LocationData]:
        recipes_per_region: Dict[str, List[Recipe]] = {}

        for recipe in recipes:
            recipes_per_region.setdefault(recipe.building or "Overworld", []).append(recipe)

        return [Part(state_logic, region, recipes_for_region, name, items) 
                for region, recipes_for_region in recipes_per_region.items()]

    def __init__(self, state_logic: StateLogic, region: str, recipes: Iterable[Recipe], name: str, items: Items):
        super().__init__(region, part_event_prefix + name + region, EventId, part_event_prefix + name,
            self.can_produce_any_recipe_for_part(state_logic, recipes, name, items))

    def can_produce_any_recipe_for_part(self, state_logic: StateLogic, recipes: Tuple[Recipe, ...], 
                                        name: str, items: Items) -> Callable[[CollectionState], bool]:
        def can_build_by_any_recipe(state: CollectionState) -> bool:
            if name == "Water":
                debugger="attach"
            return any(state_logic.can_produce_specific_recipe_for_part(state, recipe) for recipe in recipes)

        def can_build_by_precalculated_recipe(state: CollectionState) -> bool:
            return state_logic.can_produce_specific_recipe_for_part( 
                state, items.precalculated_progression_recipes[name])

        if items.precalculated_progression_recipes:
            return can_build_by_precalculated_recipe
        else:
            return can_build_by_any_recipe


class EventBuilding(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, building_name: str, building: Building):
        super().__init__("Overworld", building_event_prefix + building_name, EventId, 
            self.can_create_building(game_logic, state_logic, building))

    def can_create_building(self, game_logic: GameLogic, state_logic: StateLogic, building: Building
            ) -> Callable[[CollectionState], bool]:

        def can_build(state: CollectionState) -> bool:
            return state_logic.has(state, building.name) and \
                state_logic.can_produce_all_allowing_handcrafting(state, game_logic, building.inputs)

        return can_build


class PowerInfrastructure(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, 
                 powerLevel: PowerInfrastructureLevel, recipes: Tuple[Recipe, ...]):
        super().__init__("Overworld", building_event_prefix + str(powerLevel), EventId, 
            self.can_create_power_infrastructure(game_logic, state_logic, powerLevel, recipes))

    def can_create_power_infrastructure(self, game_logic: GameLogic, state_logic: StateLogic, 
                                        powerLevel: PowerInfrastructureLevel, recipes: Tuple[Recipe, ...]
            ) -> Callable[[CollectionState], bool]:

        def can_power(state: CollectionState) -> bool:
            if powerLevel == PowerInfrastructureLevel.Simpel:
                debugger="attach"

            return any(state_logic.can_build(state, recipe.building) and 
                       state_logic.can_produce_all_allowing_handcrafting(state, game_logic, recipe.inputs) 
                for recipe in recipes)

        return can_power


class ElevatorTier(LocationData):
    def __init__(self, tier: int, state_logic: StateLogic, game_logic: GameLogic):
        super().__init__("Overworld", f"Elevator Tier {tier + 1}", EventId,
            lambda state: state_logic.can_produce_all(state, game_logic.space_elevator_tiers[tier].keys()))


class HubSlot(LocationData):
    def __init__(self, name: str, slot: int, locationId: int):
        super().__init__(name, f"{name}, item {slot}", locationId)


class MamSlot(LocationData):
    def __init__(self, name: str, slot: int, locationId: int):
        super().__init__(name, f"{name}, item {slot}", locationId)


class Droppod(LocationData):
    def __init__(self, x: int, y: int, z: int, unlocked_by: str, state_logic: Optional[StateLogic],
            locationId: int, needs_power: Optional[bool] = False, gassed: Optional[bool] = False,
            radioactive: Optional[bool] = False):

        def get_region(gassed: bool, radioactive: bool) -> str:
            if radioactive:
                return "Radioactive Area"
            elif gassed:
                return "Gas Area"
            else:
                return "Overworld"

        def get_rule(unlocked_by: str, needs_power: bool) -> Callable[[CollectionState], bool]:
            #TODO handle power

            def logic_rule(state: CollectionState):
                return state_logic and state_logic.can_produce(state, unlocked_by)

            return logic_rule

        super().__init__(get_region(gassed, radioactive), f"Crash Site ({x}, {y}, {z})", locationId,
                get_rule(unlocked_by, needs_power))


class Locations():
    game_logic: Optional[GameLogic]
    state_logic: Optional[StateLogic]
    items: Optional[Items]

    hub_location: int = 1338000
    max_tiers: int = 10
    max_milestones: int = 5
    max_slots: int = 10

    def __init__(self, game_logic: Optional[GameLogic] = None, 
                 state_logic: Optional[StateLogic] = None, items: Optional[Items] = None):
        self.game_logic = game_logic
        self.state_logic = state_logic
        self.items = items

    def get_base_location_table(self) -> List[LocationData]:
        return [
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),
        ]

    def get_all_location_ids_by_name(self) -> Dict[str, int]:
        location_table = self.get_base_location_table()

        # All possible locations
        for tier in range(1, self.max_tiers + 1):
            for milestone in range(1, self.max_milestones + 1):
                for slot in range(1, self.max_slots + 1):
                    location_table.append(HubSlot(f"Hub {tier}-{milestone}", slot, self.hub_location))
                    self.hub_location += 1

        # TODO mam slots
        # location_table.append(MamSlot(f"Mam TODO"))

        location_table.append(LocationData("Overworld", "UpperBound", 1338999))

        return {location.name: location.code for location in location_table}

    def get_locations(self) -> List[LocationData]:
        if not self.game_logic or not self.state_logic or not self.items:
            raise Exception("Locations need to be initialized with logic and items before using this method")

        location_table = self.get_base_location_table()

        # Only used locations
        for tier in range(1, self.max_tiers + 1):
            for milestone in range(1, self.max_milestones + 1):
                for slot in range(1, self.max_slots + 1):
                    if tier <= len(self.game_logic.hub_layout) \
                            and milestone <= len(self.game_logic.hub_layout[tier - 1]) \
                            and slot <= self.game_logic.slots_per_milestone:
                        location_table.append(HubSlot(f"Hub {tier}-{milestone}", slot, self.hub_location))

                    self.hub_location += 1

        # TODO mam slots
        # location_table.append(MamSlot(f"Mam TODO"))

        location_table.extend(self.get_logical_event_locations())

        return location_table


    def get_logical_event_locations(self) -> List[LocationData]:
        location_table: List[LocationData] = []

        location_table.extend(
            ElevatorTier(index, self.state_logic, self.game_logic) 
            for index, parts in enumerate(self.game_logic.space_elevator_tiers))
        location_table.extend(
            part 
            for part_name, recipes in self.game_logic.recipes.items() 
            for part in Part.get_parts(self.state_logic, recipes, part_name, self.items))
        location_table.extend(
            EventBuilding(self.game_logic, self.state_logic, name, building) 
            for name, building in self.game_logic.buildings.items())
        location_table.extend(
            PowerInfrastructure(self.game_logic, self.state_logic, power_level, recipes) 
            for power_level, recipes in self.game_logic.requirement_per_powerlevel.items())

        return location_table