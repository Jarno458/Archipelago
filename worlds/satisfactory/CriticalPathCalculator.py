from random import Random
from typing import Optional
from collections.abc import Iterable
from venv import logger
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions
import logging


class CriticalPathCalculator:
    logic: GameLogic
    random: Random
    final_elevator_phase: int
    randomize_starter_recipes: bool
    ficsmas: bool

    required_parts: set[str]
    required_buildings: set[str]
    required_item_names: set[str]
    required_power_level: int

    __potential_required_belt_speed: int

    parts_to_exclude: set[str]
    recipes_to_exclude: set[str]
    buildings_to_exclude: set[str]

    implicitly_unlocked: set[str]
    handcraftable_parts: dict[str, list[Recipe]]
    tier_0_recipes: set[str]

    progression_calculation_passes: int
    progression_recipe_per_part: dict[str, Recipe]

    def __init__(self, logic: GameLogic, seed: float, options: SatisfactoryOptions):
        self.logic = logic
        self.random = Random(seed)
        self.final_elevator_phase = options.final_elevator_phase.value
        self.randomize_starter_recipes = bool(options.randomize_starter_recipes.value)
        self.ficsmas = "Erect a FICSMAS Tree" in options.goal_selection

    def calculate(self) -> None:
        self.required_parts = set[str]()
        self.required_buildings = set[str]()
        self.required_item_names = set[str]()
        self.required_power_level: int = 1

        self.__potential_required_belt_speed = 1

        self.progression_recipe_per_part = {}

        self.configure_implicitly_unlocked_and_handcraftable_parts()

        self.select_starter_recipes()

        self.select_minimal_required_parts_for(
            self.logic.space_elevator_phases[self.final_elevator_phase-1].keys(), context=f"Initial selection: Space Elevator Parts phase {self.final_elevator_phase}")

        for tree_name, tree in self.logic.man_trees.items():
            if tree_name == "Ficsmas" and not self.ficsmas:
                continue

            self.select_minimal_required_parts_for(tree.access_items, context=f"Initial selection: {tree_name} Access Items")

            for node in tree.nodes:
                if node.minimal_phase > self.final_elevator_phase:
                    continue

                self.select_minimal_required_parts_for(node.unlock_cost, context=f"Initial selection: {node.name} Unlock Cost")

                if node.requires_items:
                    self.required_item_names.update(node.requires_items)

        self.select_minimal_required_parts_for_building("MAM", context="Initial selection: MAM")
        self.select_minimal_required_parts_for_building("AWESOME Sink", context="Initial selection: AWESOME Sink")
        self.select_minimal_required_parts_for_building("AWESOME Shop", context="Initial selection: AWESOME Shop")
        self.select_minimal_required_parts_for_building("Space Elevator", context="Initial selection: Space Elevator")
        self.select_minimal_required_parts_for_building("Conveyor Splitter", context="Initial selection: Conveyor Splitter")
        self.select_minimal_required_parts_for_building("Conveyor Merger", context="Initial selection: Conveyor Merger")
        self.select_minimal_required_parts_for_building("Equipment Workshop", context="Initial selection: Equipment Workshop")
        self.select_minimal_required_parts_for_building("Foundation", context="Initial selection: Foundation")
        self.select_minimal_required_parts_for_building("Walls Orange", context="Initial selection: Walls Orange")
        self.select_minimal_required_parts_for_building("Power Storage", context="Initial selection: Power Storage")
        self.select_minimal_required_parts_for_building("Miner Mk.2", context="Initial selection: Miner Mk.2")
        self.select_minimal_required_parts_for_building("Pipes Mk.1", context="Initial selection: Pipes Mk.1")
        self.select_minimal_required_parts_for_building("Pipes Mk.2", context="Initial selection: Pipes Mk.2")
        self.select_minimal_required_parts_for_building("Pipeline Pump Mk.1", context="Initial selection: Pipeline Pump Mk.1")
        self.select_minimal_required_parts_for_building("Pipeline Pump Mk.2", context="Initial selection: Pipeline Pump Mk.2")

        if self.ficsmas:
            self.select_minimal_required_parts_for(("FICSMAS Wonder Star", ), context="Initial selection: FICSMAS Wonder Star")

        if self.logic.recipes["Uranium"][0].minimal_phase <= self.final_elevator_phase:
            self.select_minimal_required_parts_for(("Hazmat Suit", "Iodine-Infused Filter"), context="Initial selection: Hazmat Suit & Iodine-Infused Filter")

        for i in range(1, self.__potential_required_belt_speed + 1):
            self.select_minimal_required_parts_for_building(f"Conveyor Mk.{i}", context=f"Initial selection: Conveyor Mk.{i}")

        for i in range(1, self.required_power_level + 1):
            power_recipe = self.random.choice(self.logic.requirement_per_powerlevel[i])
            self.select_minimal_required_parts_for(power_recipe.inputs, context=f"Power Recipe for {power_recipe.name}")
            self.select_minimal_required_parts_for_building(power_recipe.building, context=f"Power Recipe for {power_recipe.name}")

        self.progression_calculation_passes = 0
        self.select_progression_recipes()

        self.required_item_names.update({
            recipe.name
            for part in self.required_parts
            for recipe in self.logic.recipes[part]
            if recipe.minimal_phase <= self.final_elevator_phase
        })

        self.required_item_names.update({"Building: " + building for building in self.required_buildings})

        self.calculate_excluded_things()

    def select_minimal_required_parts_for_building(self, building: str, context: Optional[str] = None) -> None:
        self.select_minimal_required_parts_for(self.logic.buildings[building].inputs, context)
        self.required_buildings.add(building)


    ######################
    ### NEW CODE START    
    ######################


    # so lets think this through
    # we select 1 recipe for each space elevator part we need
    # for those recipes we need to make sure we have all the required parts to build thier buildings and the parts to produce them
    def select_minimal_required_parts_for(self, parts: Optional[Iterable[str]], context: Optional[str] = None) -> None:
        if parts is None:
            return

        for part in parts:
            if part in self.required_parts:
                continue

            recipes_per_part = self.logic.recipes[part]
            if any(recipe.name in self.implicitly_unlocked or recipe.name in self.tier_0_recipes for recipe in recipes_per_part):
                continue

            self.required_parts.add(part)

            selected_recipe = self.random.choice(recipes_per_part)
            self.progression_recipe_per_part[part] = selected_recipe

            logging.info(f"Selected progression recipe for {part}: {selected_recipe.name}, context: {context}")

            if not context:
                context = f"Selected recipe for {part}: {selected_recipe.name}"

            self.select_minimal_required_parts_for(selected_recipe.inputs, context)
            self.select_minimal_required_parts_for_building(selected_recipe.building, context)


    def select_progression_recipes(self) -> None:
        self.progression_calculation_passes += 1

        if (self.progression_calculation_passes > 10):
            raise RuntimeError("Exceeded maximum number of progression calculation passes.")

        # select progression recipes for each required part
        #for part in self.required_parts:
        #    if part in self.progression_recipe_per_part:
        #        continue

        #    recipes_per_part = self.logic.recipes[part]
        #    if any(recipe.name in self.implicitly_unlocked or recipe.name in self.tier_0_recipes for recipe in recipes_per_part):
        #        continue

        #    self.progression_recipe_per_part[part] = self.random.choice(recipes_per_part)

        ### todo remove
        #for part, recipe in self.progression_recipe_per_part.items():
        #    logging.info(f"Selected progression recipe for {part}: {recipe.name} (building: {recipe.building})")

        logging.warning("Beatable check")
        ###

        # beatability check
        available_parts = {
            part
            for part, recipes_per_part in self.logic.recipes.items()
            if any(recipe.name in self.implicitly_unlocked or recipe.name in self.tier_0_recipes for recipe in recipes_per_part)
        }

        # todo fixme, available_parts likely contains a few raw resources at this point that arent in required parts

        previous_count = len(available_parts)
        while len(available_parts) < len(self.required_parts):
            for part, recipe_per_part in self.progression_recipe_per_part.items():
                if part in available_parts:
                    continue

                if part == "Steel Ingot":
                    Debug = True

                if part == "Steel Beam":
                    Debug = True 

                if not recipe_per_part.inputs or all(
                    input in available_parts and all(
                        building_input in available_parts for building_input in self.logic.buildings[recipe_per_part.building].inputs
                    ) for input in recipe_per_part.inputs):

                    available_parts.add(part)

            if len(available_parts) == previous_count:
                # Try again
                missing = self.required_parts - available_parts
                logging.warning(f"Missing parts: {missing}, Trying again")    

                self.select_progression_recipes()
            
            previous_count = len(available_parts)

        logging.warning("Beatable check complete")


    ######################
    ### NEW CODE END     
    ######################



    def select_minimal_required_parts_for_oldge(self, parts: Optional[Iterable[str]], context: Optional[str] = None) -> None:
        if parts is None:
            return

        for part in parts:
            if part in self.required_parts:
                continue

            if context is None:
                context = f"Selecting minimal required parts for {part}"
            logger.info(f"Adding required part '{part}' for context: '{context}'")

            self.required_parts.add(part)

            for recipe in self.logic.recipes[part]:
                if recipe.minimal_phase > self.final_elevator_phase:
                    continue

                self.__potential_required_belt_speed = \
                    max(self.__potential_required_belt_speed, recipe.minimal_belt_speed)

                self.select_minimal_required_parts_for(recipe.inputs, context=f"Recipe for {part}")

                if recipe.building:
                    self.select_minimal_required_parts_for(self.logic.buildings[recipe.building].inputs, context=f"Building {recipe.building} for {part}")
                    self.required_buildings.add(recipe.building)

                    if self.logic.buildings[recipe.building].power_requirement:
                        self.required_power_level = \
                            max(self.required_power_level,
                                self.logic.buildings[recipe.building].power_requirement)

    def calculate_excluded_things(self) -> None:
        self.parts_to_exclude = set[str]()
        self.buildings_to_exclude = set[str]()
        self.recipes_to_exclude = {
            recipe.name
            for part in self.logic.recipes
            for recipe in self.logic.recipes[part]
            if recipe.minimal_phase > self.final_elevator_phase
        }

        excluded_count = len(self.recipes_to_exclude)
        while True:
            for part in self.logic.recipes:
                if part in self.parts_to_exclude:
                    continue

                for recipe in self.logic.recipes[part]:
                    if recipe.name in self.recipes_to_exclude:
                        continue

                    if recipe.inputs and any(input in self.parts_to_exclude for input in recipe.inputs):
                        self.recipes_to_exclude.add(recipe.name)

                if all(r.name in self.recipes_to_exclude for r in self.logic.recipes[part]):
                    self.parts_to_exclude.add(part)

                new_buildings_to_exclude = {
                    building_name
                    for building_name, building in self.logic.buildings.items()
                    if building_name not in self.buildings_to_exclude
                    and building.inputs and any(input in self.parts_to_exclude for input in building.inputs)
                }

                self.recipes_to_exclude.update({
                    recipe_per_part.name
                    for recipes_per_part in self.logic.recipes.values()
                    for recipe_per_part in recipes_per_part
                    if recipe_per_part.building in new_buildings_to_exclude
                })

                self.buildings_to_exclude.update(new_buildings_to_exclude)

            new_length = len(self.recipes_to_exclude)
            if new_length == excluded_count:
                break
            excluded_count = new_length

    def configure_implicitly_unlocked_and_handcraftable_parts(self) -> None:
        self.implicitly_unlocked: set[str] = {
            recipe.name
            for recipes_per_part in self.logic.recipes.values()
            for recipe in recipes_per_part if recipe.implicitly_unlocked
        }
        self.implicitly_unlocked.update({
            building.name
            for building in self.logic.buildings.values() if building.implicitly_unlocked
        })

        self.handcraftable_parts: dict[str, list[Recipe]] = {}
        for part, recipes_per_part in self.logic.recipes.items():
            for recipe in recipes_per_part:
                if recipe.handcraftable:
                    self.handcraftable_parts.setdefault(part, []).append(recipe)

    def select_starter_recipes(self) -> None:
        # cable is left unaffected as all its alternative recipes require refinery
        if not self.randomize_starter_recipes:
            self.tier_0_recipes = {
                "Recipe: Iron Ingot",
                "Recipe: Iron Plate",
                "Recipe: Iron Rod",
                "Recipe: Copper Ingot",
                "Recipe: Wire",
                "Recipe: Concrete",
                "Recipe: Screw",
                "Recipe: Reinforced Iron Plate"
            }
        else:
            # we only allow basic parts to be made without the need of refineries
            # could be made more based of GameLogic rather than hardcoded but this is likely faster
            # would likely need to be based of GameLogic when we add mod support
            self.tier_0_recipes = set()

            self.tier_0_recipes.add(self.random.choice(
                ("Recipe: Iron Ingot", "Recipe: Basic Iron Ingot", "Recipe: Iron Alloy Ingot")))

            selected_recipe = self.random.choice(
                ("Recipe: Iron Plate", "Recipe: Iron Plate", "Recipe: Iron Plate", "Recipe: Steel Cast Plate"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Cast Plate":
                self.add_steel_ingot_to_starter_recipes()

            selected_recipe = self.random.choice(
                ("Recipe: Iron Rod", "Recipe: Iron Rod", "Recipe: Iron Rod", "Recipe: Steel Rod"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Rod":
                self.add_steel_ingot_to_starter_recipes()

            self.tier_0_recipes.add(self.random.choice(("Recipe: Copper Ingot", "Recipe: Copper Alloy Ingot")))

            selected_recipe = self.random.choice(
                ("Recipe: Wire", "Recipe: Caterium Wire", "Recipe: Fused Wire", "Recipe: Iron Wire"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe in {"Recipe: Caterium Wire", "Recipe: Fused Wire"}:
                # add Caterium Ingot
                self.tier_0_recipes.add("Recipe: Caterium Ingot")

            selected_recipe = self.random.choice(("Recipe: Concrete", "Recipe: Fine Concrete"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Fine Concrete":
                # add Silica
                self.tier_0_recipes.add(self.random.choice(("Recipe: Silica", "Recipe: Cheap Silica")))

            selected_recipe = self.random.choice(
                ("Recipe: Screw", "Recipe: Screw", "Recipe: Cast Screw", "Recipe: Cast Screw", "Recipe: Steel Screw"))

            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Screw":
                # add Steel Beam and steel Ingot
                self.add_steel_ingot_to_starter_recipes()
                self.tier_0_recipes.add(self.random.choice(("Recipe: Steel Beam", "Recipe: Molded Beam")))

            self.tier_0_recipes.add(self.random.choice(
                ("Recipe: Reinforced Iron Plate", "Recipe: Bolted Iron Plate", "Recipe: Stitched Iron Plate")))

        for part, recipes in self.logic.recipes.items():
            for recipe in recipes:
                if recipe.name in self.tier_0_recipes:
                    if part in self.handcraftable_parts:
                        self.handcraftable_parts[part].append(recipe)
                    else:
                        self.handcraftable_parts[part] = [recipe]
                    self.tier_0_recipes.add(self.logic.buildings[recipe.building].name)

        self.implicitly_unlocked.update(self.tier_0_recipes)

    def add_steel_ingot_to_starter_recipes(self) -> None:
        if "Recipe: Steel Ingot" not in self.tier_0_recipes \
                and "Recipe: Compacted Steel Ingot" not in self.tier_0_recipes \
                and "Recipe: Solid Steel Ingot" not in self.tier_0_recipes:

            selected_recipe = self.random.choice(
                ("Recipe: Steel Ingot", "Recipe: Compacted Steel Ingot", "Recipe: Solid Steel Ingot"))

            self.tier_0_recipes.add(selected_recipe)

            if selected_recipe == "Recipe: Compacted Steel Ingot":
                self.tier_0_recipes.add("Recipe: Compacted Coal")
