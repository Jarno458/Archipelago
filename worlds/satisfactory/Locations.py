from typing import List, Tuple, Optional, Callable
from BaseClasses import CollectionState
from .GameLogic import GameLogic
from .Rules import StateLogic, LocationData, EventId, get_logical_event_locations
from .Items import Items

class ElevatorTier(LocationData):
    def __init__(self, name: str, state_logic: Optional[StateLogic], ingredients: Tuple[str, ...]):
        super().__init__("Overworld", name, EventId,
            lambda state: state_logic and state_logic._satisfactory_can_produce_all(state, ingredients))


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
                return state_logic and state_logic._satisfactory_can_produce(state, unlocked_by)

            return logic_rule

        super().__init__(get_region(gassed, radioactive), f"Crash Site ({x}, {y}, {z})", locationId,
                get_rule(unlocked_by, needs_power))


def get_locations(game_logic: Optional[GameLogic], state_logic: Optional[StateLogic], items: Optional[Items]) \
        -> List[LocationData]:
    
    location_table: List[LocationData] = [
        ElevatorTier("Elevator Tier 1", state_logic, game_logic.space_elevator_tiers[0].keys()),
        ElevatorTier("Elevator Tier 2", state_logic, game_logic.space_elevator_tiers[1].keys()),
        ElevatorTier("Elevator Tier 3", state_logic, game_logic.space_elevator_tiers[2].keys()),
        ElevatorTier("Elevator Tier 4", state_logic, game_logic.space_elevator_tiers[3].keys()),
        #Droppod(0, 0, 0, "Motor", state_logic, 1337605)),
        #Droppod(0, 0, 0, "Motor", state_logic, 1337605)),
        #Droppod(0, 0, 0, "Motor", state_logic, 1337605)),
    ]

    hub_location: int = 1338000
    max_tiers: int = 10
    max_milestones: int = 5
    max_slots: int = 10

    if game_logic:
        # Only used locations
        for tier in range(1, max_tiers + 1):
            for milestone in range(1, max_milestones + 1):
                for slot in range(1, max_slots + 1):
                    if tier <= len(game_logic.hub_layout) \
                            and milestone <= len(game_logic.hub_layout[tier - 1]) \
                            and slot <= game_logic.slots_per_milestone:
                        location_table.append(HubSlot(f"Hub {tier}-{milestone}", slot, hub_location))

                    hub_location += 1

        # TODO mam slots
        # location_table.append(MamSlot(f"Mam TODO"))

        if state_logic and items:
            location_table.extend(get_logical_event_locations(game_logic, state_logic, items))
        
    else:
        # All possible locations
        for tier in range(1, max_tiers + 1):
            for milestone in range(1, max_milestones + 1):
                for slot in range(1, max_slots + 1):
                    location_table.append(HubSlot(f"Hub {tier}-{milestone}", slot, hub_location))
                    hub_location += 1

        # TODO mam slots
        # location_table.append(MamSlot(f"Mam TODO"))

        location_table.append(LocationData("Overworld", "UpperBound", 1338999))
 
    return location_table
