from typing import Tuple, Optional, List, Callable, Dict
from BaseClasses import MultiWorld, CollectionState
from enum import Enum
from .Options import is_option_enabled
from .GameLogic import GameLogic, Recipe, Building, PowerLevel
from .Items import Items

EventId: Optional[int] = None

part_event_prefix = "Can Produce: "
building_event_prefix = "Can Build: "

class StateLogic:
    player: int

    def __init__(self, world: MultiWorld, player: int):
        self.player = player


    def has(self, state: CollectionState, item_name: str):
        return state.has(item_name, self.player)


    def _satisfactory_can_produce(self, state: CollectionState, part_name: str) -> bool:
        return state.has(part_event_prefix + part_name, self.player)


    def _satisfactory_can_produce_all(self, state: CollectionState, parts: Optional[Tuple[str, ...]]) -> bool:
        return parts is None or \
            state.has_all({part_event_prefix + part_name for part_name in parts}, self.player)


    def _satisfactory_can_produce_all_allowing_handcrafting(self, state: CollectionState, logic: GameLogic, 
            parts: Optional[Tuple[str, ...]]) -> bool:

        def can_handcraft_part(part: str) -> bool:
            if state.has(part_event_prefix + part, self.player):
                return True
            elif part not in logic.handcraftable_recipes:
                return False

            recipe: Recipe = logic.handcraftable_recipes[part]

            return state.has(recipe.name, self.player) \
                and self._satisfactory_can_produce_all_allowing_handcrafting(state, logic, recipe.inputs)

        return self._satisfactory_can_produce_all(state, parts) or all(can_handcraft_part(part) for part in parts)


    def _satisfactory_can_produce_specific_recipe_for_part(self, state: CollectionState, recipe: Recipe) -> bool:
        #TODO, check if we got enough belt through put, check if pipes are needed, check if advanced power infrastructure is needed
        return state.has(recipe.name, self.player) \
            and (recipe.building is None or state.has(building_event_prefix + recipe.building, self.player)) \
            and self._satisfactory_can_produce_all(state, recipe.inputs)


class LocationData():
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]]

    def __init__(self, region: str, name: str, code: Optional[int], 
                 rule: Optional[Callable[[CollectionState], bool]] = None):
        self.region = region
        self.name = name
        self.code = code
        self.rule = rule


class Part(LocationData):
    def __init__(self, state_logic: StateLogic, recipes: Tuple[Recipe, ...], name: str, items: Items):
        super().__init__("Overworld", part_event_prefix + name, EventId,
            self.can_produce_any_recipe_for_part(state_logic, recipes, name, items))


    def can_produce_any_recipe_for_part(self, state_logic: StateLogic, recipes: Tuple[Recipe, ...], 
                                        name: str, items: Items) -> Callable[[CollectionState], bool]:
        
        def logic_rule(state: CollectionState) -> bool:
            return any(state_logic._satisfactory_can_produce_specific_recipe_for_part(state, recipe) 
                for recipe in recipes)

        def specific_logic_rule(state: CollectionState) -> bool:
            return state_logic._satisfactory_can_produce_specific_recipe_for_part(state, items.selected_recipes[name])
        
        return logic_rule if not items.selected_recipes else specific_logic_rule


class EventBuilding(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, building_name: str, building: Building):
        super().__init__("Overworld", building_event_prefix + building_name, EventId, 
            self.can_create_building(game_logic, state_logic, building))


    def can_create_building(self, game_logic: GameLogic, state_logic: StateLogic, name: str
            ) -> Callable[[CollectionState], bool]:

        def logic_rule(state: CollectionState) -> bool:
            recipe = game_logic.buildings[name].recipe
            return state_logic.has(state, "Building: " + name) and \
                state_logic._satisfactory_can_produce_all_allowing_handcrafting(state, game_logic, recipe.inputs)

        return logic_rule
    
class PowerInfrastructure(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, 
                 powerLevel: PowerLevel, recipes: Tuple[Recipe, ...]):
        super().__init__("Overworld", building_event_prefix + powerLevel, EventId, 
            self.can_create_power_infrastructure(game_logic, state_logic, powerLevel, recipes))

    def can_create_power_infrastructure(self, game_logic: GameLogic, state_logic: StateLogic, 
                                        powerLevel: PowerLevel, recipes: Tuple[Recipe, ...]
            ) -> Callable[[CollectionState], bool]:

        def logic_rule(state: CollectionState) -> bool:
            return any(state_logic._satisfactory_can_produce_specific_recipe_for_part(state, recipe) 
                for recipe in recipes)

        return logic_rule


def get_logical_event_locations(game_logic: GameLogic, state_logic: StateLogic, items: Items) -> List[LocationData]:
    location_table: List[LocationData] = []
    location_table.extend(
        Part(state_logic, recipes, part, items) for part, recipes in game_logic.recipes.items())
    location_table.extend(
        EventBuilding(game_logic, state_logic, name, building) for name, building in game_logic.buildings.items())
    location_table.extend(
        PowerInfrastructure(game_logic, state_logic, power_level, recipes) for power_level, recipes in 
        game_logic.requirement_per_powerlevel.items())


    return location_table
