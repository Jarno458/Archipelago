from typing import Tuple, Optional, Set, Iterable
from BaseClasses import CollectionState
from .GameLogic import GameLogic, Recipe, PowerInfrastructureLevel
from .Options import SatisfactoryOptions

EventId: Optional[int] = None

part_event_prefix = "Can Produce: "
building_event_prefix = "Can Build: "

class StateLogic:
    player: int
    options: SatisfactoryOptions
    initial_unlocked_items: Set[str]

    def __init__(self, player: int, options: SatisfactoryOptions, initial_unlocked_items: Set[str]):
        self.player = player
        self.options = options
        self.initial_unlocked_items = initial_unlocked_items

    def has_recipe(self, state: CollectionState, recipe: Recipe):
        return recipe.implicitly_unlocked \
            or recipe.name in self.initial_unlocked_items \
            or state.has(recipe.name, self.player)
    
    def can_build(self, state: CollectionState, building_name: Optional[str]) -> bool:
        return building_name is None or state.has(building_event_prefix + building_name, self.player)

    def can_produce(self, state: CollectionState, part_name: Optional[str]) -> bool:
        return part_name is None or state.has(part_event_prefix + part_name, self.player)
    
    def can_power(self, state: CollectionState, power_level: Optional[PowerInfrastructureLevel]) -> bool:
        return power_level is None or state.has(building_event_prefix +  str(power_level), self.player)

    def can_produce_all(self, state: CollectionState, parts: Optional[Iterable[str]]) -> bool:
        return parts is None or \
            state.has_all({part_event_prefix + part_name for part_name in parts}, self.player)

    def can_produce_all_allowing_handcrafting(self, state: CollectionState, logic: GameLogic, 
            parts: Optional[Tuple[str, ...]]) -> bool:
        
        def can_handcraft_part(part: str) -> bool:
            if part == "Coal":
                debugger="attach"

            if state.has(part_event_prefix + part, self.player):
                return True
            elif part not in logic.handcraftable_recipes:
                return False

            recipe: Recipe = logic.handcraftable_recipes[part]

            return self.has_recipe(state, recipe) \
                and (not recipe.inputs or 
                     self.can_produce_all_allowing_handcrafting(state, logic, recipe.inputs))

        return not parts or all(self.can_produce(state, part) or can_handcraft_part(part) for part in parts)

    def can_produce_specific_recipe_for_part(self, state: CollectionState, recipe: Recipe) -> bool:
        #TODO, check if we got enough belt through put, check if pipes are needed
        return self.has_recipe(state, recipe) \
            and self.can_build(state, recipe.building) \
            and self.can_produce_all(state, recipe.inputs)



