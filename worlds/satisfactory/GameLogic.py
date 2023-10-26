from typing import Tuple, Optional, Dict
from enum import Enum

class PowerLevel(Enum):
    Simpel = 1
    Advanced = 2
    Complex = 3


class Recipe():
    name: str
    building: str
    inputs: Tuple[str, ...]
    needs_pipes: bool
    minimal_belt_speed: int
    handcraftable: bool
    additional_outputs: Tuple[str, ...]

    def __init__(self, name: str, building: str, inputs: Optional[Tuple[str, ...]] = None,
            needs_pipes: Optional[bool] = False, minimal_belt_speed: Optional[int] = 1,
            handcraftable: Optional[bool] = False, additional_outputs: Optional[Tuple[str, ...]] = None):
        self.name = "Recipe: " + name
        self.building = building
        self.inputs = inputs
        self.needs_pipes = needs_pipes
        self.minimal_belt_speed = minimal_belt_speed
        self.handcraftable = handcraftable
        self.additional_outputs = additional_outputs


class Building():
    recipe: Recipe
    power_requirement: Optional[PowerLevel]

    def __init__(self, recipe: Recipe, power_requirement: Optional[PowerLevel] = None):
        self.recipe = recipe
        self.power_requirement = power_requirement


class MamNode():
    unlock_cost: Dict[str, int]
    depends_on: Tuple[str, ...]

    def __init__(self, unlock_cost: Dict[str, int], depends_on: Tuple[str, ...]):
        self.unlock_cost = unlock_cost
        self.depends_on = depends_on


class MamTree():
    access_items: Tuple[str, ...]
    nodes: Tuple[str, ...]

    def __init__(self, access_items: Tuple[str, ...], nodes: Tuple[str, ...]):
        self.access_item = access_items
        self.nodes = nodes


class GameLogic:
    recipes: Dict[str, Tuple[Recipe, ...]]
    handcraftable_recipes: Dict[str, Recipe]
    buildings: Dict[str, Building]
    requirement_per_powerlevel: Dict[PowerLevel, Tuple[Recipe, ...]]
    free_recipes: Tuple[str]
    slots_per_milestone: int
    hub_layout: Tuple[Tuple[Dict[str, int], ...]]
    mam_layout: Dict[str, MamTree]
    slots_per_milestone: int
    space_elevator_tiers: Tuple[Dict[str, int], ...]
    mam_nodes_layout: Dict[str, MamNode]
    mam_trees_layout: Dict[str, MamTree]

    def __init__(self):
        self.recipes = {
            "Reinforced Iron Plate": (
                Recipe("Reinforced Iron Plate", "Assembler", ("Iron Plate", "Screw"), handcraftable=True),
                Recipe("Adhered Iron Plate", "Assembler", ("Iron Plate", "Rubber")),
                Recipe("Bolted Iron Plate", "Assembler", ("Iron Plate", "Screw"), minimal_belt_speed=3),
                Recipe("Stitched Iron Plate", "Assembler", ("Iron Plate", "Wire"))),
            "Rotor": (
                Recipe("Rotor", "Assembler", ("Iron Rod", "Screw"), minimal_belt_speed=2, handcraftable=True),
                Recipe("Copper Rotor", "Assembler", ("Copper Sheet", "Screw"), minimal_belt_speed=3),
                Recipe("Steel Rotor", "Assembler", ("Steel Pipe", "Wire"))),
            "Stator": (
                Recipe("Stator", "Assembler", ("Steel Pipe", "Wire"), handcraftable=True),
                Recipe("Quickwire Stator", "Assembler", ("Steel Pipe", "Quickwire"))),
            "Plastic": (
                Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue"), needs_pipes=True),
                Recipe("Residual Plastic", "Refinery", ("Polymer Resin", "Water"), needs_pipes=True),
                Recipe("Recycled Plastic", "Refinery", ("Rubber", "Fuel"), needs_pipes=True)),
            "Rubber": (
                Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue"), needs_pipes=True),
                Recipe("Residual Rubber", "Refinery", ("Polymer Resin", "Water"), needs_pipes=True),
                Recipe("Recycled Rubber", "Refinery", ("Plastic", "Fuel"), needs_pipes=True)),
            "Iron Plate": (
                Recipe("Iron Plate", "Constructor", ("Iron Ingot", ), handcraftable=True),
                Recipe("Coated Iron Plate", "Assembler", ("Iron Ingot", "Plastic"), minimal_belt_speed=2),
                Recipe("Steel Coated Plate", "Assembler", ("Steel Ingot", "Plastic"))),
            "Iron Rod": (
                Recipe("Iron Rod", "Constructor", ("Iron Ingot", ), handcraftable=True),
                Recipe("Steel Rod", "Constructor", ("Steel Ingot", ))),
            "Screw": (
                Recipe("Screw", "Constructor", ("Iron Rod", ), handcraftable=True),
                Recipe("Cast Screw", "Constructor", ("Iron Ingot", )),
                Recipe("Steel Screw", "Constructor", ("Steel Beam", ), minimal_belt_speed=3)),
            "Wire": (
                Recipe("Wire", "Constructor", ("Copper Ingot", ), handcraftable=True),
                Recipe("Fused Wire", "Assembler", ("Copper Ingot", "Caterium Ingot"), minimal_belt_speed=2),
                Recipe("Iron Wire", "Constructor", ("Iron Ingot", )),
                Recipe("Caterium Wire", "Constructor", ("Caterium Ingot", ), minimal_belt_speed=2)),
            "Cable": (
                Recipe("Cable", "Constructor", ("Wire", ), handcraftable= True),
                Recipe("Coated Cable", "Refinery", ("Wire", "Heavy Oil Residue"), needs_pipes=True, minimal_belt_speed=2),
                Recipe("Insulated Cable", "Assembler", ("Wire", "Rubber"), minimal_belt_speed=2),
                Recipe("Quickwire Cable", "Assembler", ("Quickwire", "Rubber"))),
            "Quickwire": (
                Recipe("Quickwire", "Constructor", ("Caterium Ingot", ), handcraftable=True),
                Recipe("Fused Quickwire", "Assembler", ("Caterium Ingot", "Copper Ingot"), minimal_belt_speed=2)),
            "Copper Sheet": (
                Recipe("Copper Sheet", "Constructor", ("Copper Ingot", ), handcraftable=True),
                Recipe("Steamed Copper Sheet", "Refinery", ("Copper Ingot", "Water"), needs_pipes=True)),
            "Steel Pipe": (
                Recipe("Steel Pipe", "Constructor", ("Steel Ingot", ), handcraftable=True), ),
            "Steel Beam": (
                Recipe("Steel Beam", "Constructor", ("Steel Ingot", ), handcraftable=True), ),
            "Crude Oil": (
                Recipe("Crude Oil", "Oil Extractor", None, needs_pipes=True), ),
            "Heavy Oil Residue": (
                Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", ), needs_pipes=True),
                Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Plastic", ), needs_pipes=True),
                Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Rubber", ), needs_pipes=True),
                Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", ), needs_pipes=True, minimal_belt_speed=3)),
            "Polymer Resin": (
                Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", ), needs_pipes=True),
                Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Fuel", ), needs_pipes=True),
                Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", ), needs_pipes=True, minimal_belt_speed=3)),
            "Fuel": (
                Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin"), needs_pipes=True),
                Recipe("Diluted Fuel (blender)", "Blender", ("Heavy Oil Residue", "Water"), needs_pipes=True),
                Recipe("Residual Fuel", "Refinery", ("Heavy Oil Residue", ), needs_pipes=True)),
            "Water": (
                Recipe("Water", "Water Extractor", None, needs_pipes=True), ),
            "Concrete": (
                Recipe("Concrete", "Constructor", ("Limestone", ), handcraftable= True),
                Recipe("Fine Concrete", "Assembler", ("Limestone", "Silica")),
                Recipe("Rubber Concrete", "Assembler", ("Limestone", "Rubber")),
                Recipe("Wet Concrete", "Refinery", ("Limestone", "Water"), needs_pipes=True, minimal_belt_speed=2)),
            "Silica": (
                Recipe("Alumina Solution", "Refinery", ("Bauxite", "Water"), additional_outputs=("Alumina Solution", ), needs_pipes=True, minimal_belt_speed=2),
                Recipe("Silica", "Constructor", ("Raw Quartz", ), handcraftable=True),
                Recipe("Cheap Silica", "Assembler", ("Raw Quartz", "Limestone"))),
            "Quartz Crystal": (
                Recipe("Quartz Crystal", "Constructor", ("Raw Quartz", ), handcraftable=True),
                Recipe("Pure Quartz Crystal", "Refinery", ("Raw Quartz", "Water"), needs_pipes=True, minimal_belt_speed=2)),
            "Iron Ingot": (
                Recipe("Iron Ingot", "Smelter", ("Iron Ore", ), handcraftable=True),
                Recipe("Pure Iron Ingot", "Refinery", ("Iron Ore", "Water"), needs_pipes=True, minimal_belt_speed=2),
                Recipe("Iron Alloy Ingot", "Foundry", ("Iron Ore", "Copper Ore"))),
            "Steel Ingot": (
                Recipe("Steel Ingot", "Foundry", ("Iron Ore", "Coal"), handcraftable=True),
                Recipe("Coke Steel Ingot", "Foundry", ("Iron Ore", "Petroleum Coke"), minimal_belt_speed=2),
                Recipe("Compacted Steel Ingot", "Foundry", ("Iron Ore", "Compacted Coal")),
                Recipe("Solid Steel Ingot", "Foundry", ("Iron Ingot", "Coal"))),
            "Copper Ingot": (
                Recipe("Copper Ingot", "Smelter", ("Copper Ore", ), handcraftable=True),
                Recipe("Copper Alloy Ingot", "Foundry", ("Copper Ore", "Iron Ore"), minimal_belt_speed=2),
                Recipe("Pure Copper Ingot", "Refinery", ("Copper Ore", "Water"), needs_pipes=True)),
            "Caterium Ingot": (
                Recipe("Caterium Ingot", "Smelter", ("Caterium Ore", ), handcraftable=True),
                Recipe("Pure Caterium Ingot", "Refinery", ("Caterium Ore", "Water"), needs_pipes=True)),
            "Limestone": (
                Recipe("Limestone", "Miner Mk.1", None, handcraftable=True), ),
            "Raw Quartz": (
                Recipe("Raw Quartz", "Miner Mk.1", None, handcraftable=True), ),
            "Iron Ore": (
                Recipe("Iron Ore", "Miner Mk.1", None, handcraftable=True), ),
            "Copper Ore": (
                Recipe("Copper Ore", "Miner Mk.1", None, handcraftable=True), ),
            "Coal": (
                Recipe("Coal", "Miner Mk.1", None, handcraftable=True), ),
            "Sulfur": (
                Recipe("Sulfur", "Miner Mk.1", None, handcraftable=True), ),
            "Caterium Ore": (
                Recipe("Caterium Ore", "Miner Mk.1", None, handcraftable=True), ),
            "Petroleum Coke": (
                Recipe("Petroleum Coke", "Refinery", ("Heavy Oil Residue", ), needs_pipes=True, minimal_belt_speed=2), ),
            "Compacted Coal": (
                Recipe("Compacted Coal", "Assembler", ("Coal", "Sulfur")), ),
            "Motor": (
                Recipe("Motor", "Assembler", ("Rotor", "Stator"), handcraftable=True),
                Recipe("Rigour Motor", "Manufacturer", ("Rotor", "Stator", "Crystal Oscillator")),
                Recipe("Electric Motor", "Assembler", ("Electromagnetic Control Rod", "Rotor"))),
            "Modular Frame": (
                Recipe("Modular Frame", "Assembler", ("Reinforced Iron Plate", "Iron Rod"), handcraftable=True),
                Recipe("Bolted Frame", "Assembler", ("Reinforced Iron Plate", "Screw"), minimal_belt_speed=3),
                Recipe("Steeled Frame", "Assembler", ("Reinforced Iron Plate", "Steel Pipe"))),
            "Heavy Modular Frame": (
                Recipe("Heavy Modular Frame", "Manufacturer", ("Modular Frame", "Steel Pipe", "Encased Industrial Beam", "Screw"), minimal_belt_speed=3, handcraftable=True),
                Recipe("Heavy Flexible Frame", "Manufacturer", ("Modular Frame", "Encased Industrial Beam", "Rubber", "Screw"), minimal_belt_speed=4),
                Recipe("Heavy Encased Frame", "Manufacturer", ("Modular Frame", "Encased Industrial Beam", "Steel Pipe", "Concrete"))),
            "Encased Industrial Beam": (
                Recipe("Encased Industrial Beam", "Assembler", ("Steel Beam", "Concrete"), handcraftable=True),
                Recipe("Encased Industrial Pipe", "Assembler", ("Steel Pipe", "Concrete"))),
            "Computer": (
                Recipe("Computer", "Manufacturer", ("Circuit Board", "Cable", "Plastic", "Screw"), minimal_belt_speed=3, handcraftable= True),
                Recipe("Crystal Computer", "Assembler", ("Circuit Board", "Crystal Oscillator")),
                Recipe("Caterium Computer", "Manufacturer", ("Circuit Board", "Quickwire", "Rubber"), minimal_belt_speed=2)),
            "Circuit Board": (
                Recipe("Circuit Board", "Assembler", ("Copper Sheet", "Plastic"), handcraftable=True),
                Recipe("Electrode Circuit Board", "Assembler", ("Rubber", "Petroleum Coke")),
                Recipe("Silicon Circuit Board", "Assembler", ("Copper Sheet", "Silica")),
                Recipe("Caterium Circuit Board", "Assembler", ("Plastic", "Quickwire"))),
            "Crystal Oscillator": (
                Recipe("Crystal Oscillator", "Manufacturer", ("Quartz Crystal", "Cable", "Reinforced Iron Plate"), handcraftable=True),
                Recipe("Insulated Crystal Oscillator", "Manufacturer", ("Quartz Crystal", "Rubber", "AI Limiter"))),
            "AI Limiter": (
                Recipe("AI Limiter", "Assembler", ("Copper Sheet", "Quickwire"), minimal_belt_speed=2, handcraftable=True), ),
            "Electromagnetic Control Rod": (
                Recipe("Electromagnetic Control Rod", "Assembler", ("Stator", "AI Limiter"), handcraftable=True),
                Recipe("Electromagnetic Connection Rod", "Assembler", ("Stator", "High-Speed Connector"))),
            "High-Speed Connector": (
                Recipe("High-Speed Connector", "Manufacturer", ("Quickwire", "Cable", "Circuit Board"), minimal_belt_speed=3, handcraftable=True),
                Recipe("Silicon High-Speed Connector", "Manufacturer", ("Quickwire", "Silica", "Circuit Board"), minimal_belt_speed=2)),
            "Smart Plating": (
                Recipe("Smart Plating", "Assembler", ("Reinforced Iron Plate", "Rotor")), 
                Recipe("Plastic Smart Plating", "Manufacturer", ("Reinforced Iron Plate", "Rotor", "Plastic"))),
            "Versatile Framework": (
                Recipe("Versatile Framework", "Assembler", ("Modular Frame", "Steel Beam")), 
                Recipe("Flexible Framework", "Manufacturer", ("Modular Frame", "Steel Beam", "Rubber"))),
            "Automated Wiring": (
                Recipe("Automated Wiring", "Assembler", ("Stator", "Cable")), 
                Recipe("Automated Speed Wiring", "Manufacturer", ("Stator", "Wire", "High-Speed Connector"), minimal_belt_speed=2)),
            "Modular Engine": (
                Recipe("Modular Engine", "Manufacturer", ("Motor", "Rubber", "Smart Plating")), ), 
            "Adaptive Control Unit": (
                Recipe("Adaptive Control Unit", "Manufacturer", ("Automated Wiring", "Circuit Board", "Heavy Modular Frame", "Computer")), ),
            "Portable Miner": (
                #Recipe("Portable Miner", "", ("Iron Rod", "Iron Plate"), handcraftable= True), #Handcraft only
                Recipe("Automated Miner", "Manufacturer", ("Motor", "Steel Pipe", "Iron Rod", "Iron Plate")), ),
            # turbo fuel
            # alumina
            # super computers

            #packaged fuel
            #Recipe("Diluted Fuel (refinery)", "Refinery", ("Heavy Oil Residue", "Packaged Water")),
        }

        self.handcraftable_recipes = { part: recipe 
            for part, recipes_per_part in self.recipes.items()
            for recipe in recipes_per_part if recipe.handcraftable 
        }

        self.buildings = {
            "Constructor": Building(Recipe("Constructor", None, ("Reinforced Iron Plate", "Cable")), PowerLevel.Simpel),
            "Assembler": Building(Recipe("Assembler", None, ("Reinforced Iron Plate", "Rotor", "Cable")), PowerLevel.Simpel),
            "Manufacturer": Building(Recipe("Manufacturer", None, ("Motor", "Heavy Modular Frame", "Cable", "Plastic")), PowerLevel.Advanced),
            "Packager": Building(Recipe("Packager", None, ("Steel Beam", "Rubber", "Plastic")), PowerLevel.Simpel),
            "Refinery": Building(Recipe("Refinery", None, ("Motor", "Encased Industrial Beam", "Steel Pipe", "Copper Sheet")), PowerLevel.Advanced),
            "Blender": Building(Recipe("Blender", None, ("Motor", "Heavy Modular Frame", "Aluminum Casing", "Radio Control Unit")), PowerLevel.Complex),
            "Particle Accelerator": Building(Recipe("Particle Accelerator", None, ("Radio Control Unit", "Electromagnetic Control Rod", "Supercomputer", "Cooling System", "Fused Modular Frame", "Turbo Motor")), PowerLevel.Complex),
            "Biomass Burner": Building(Recipe("Biomass Burner", None, ("Iron Plate", "Iron Rod", "Wire"))),
            "Coal Generator": Building(Recipe("Coal Generator", None, ("Reinforced Iron Plate", "Rotor", "Cable"))),
            "Fuel Generator": Building(Recipe("Coal Generator", None, ("Computer", "Heavy Modular Frame", "Motor", "Rubber", "Quickwire"))),
            "Geothermal_Generator": Building(Recipe("Geothermal_Generator", None, ("Supercomputer", "Heavy Modular Frame", "High-Speed Connector", "Copper Sheet", "Rubber"))),
            "Nuclear Power Plant": Building(Recipe("Nuclear Power Plant", None, ("Concrete", "Heavy Modular Frame", "Supercomputer", "Cable", "Alclad Aluminum Sheet"))),
            "Miner Mk.1": Building(Recipe("Miner Mk.1", None, ("Iron Plate", "Concrete")), PowerLevel.Simpel),
            "Miner Mk.2": Building(Recipe("Miner Mk.2", None, ("Encased Industrial Beam", "Steel Pipe", "Modular Frame")), PowerLevel.Simpel),
            "Miner Mk.3": Building(Recipe("Miner Mk.3", None, ("Steel Pipe", "Supercomputer", "Fused Modular Frame", "Turbo Motor")), PowerLevel.Advanced),
            "Oil Extractor": Building(Recipe("Oil Extractor", None, ("Motor", "Encased Industrial Beam", "Cable"))),
            "Water Extractor": Building(Recipe("Water Extractor", None, ("Copper Sheet", "Reinforced Iron Plate", "Rotor"))),
            "Smelter": Building(Recipe("Smelter", None, ("Iron Rod", "Wire")), PowerLevel.Simpel),
            "Foundry": Building(Recipe("Foundry", None, ("Modular Frame", "Rotor", "Concrete")), PowerLevel.Simpel)
        }

        self.requirement_per_powerlevel = {
            PowerLevel.Simpel: (
                Recipe("Biomass Power", "Biomass Burner", ("Solid Biomass", )),
                Recipe("Coal Generator Power", "Coal Generator", ("Coal", "Water"))
            ),
            PowerLevel.Advanced: (
                Recipe("Geothermal Generator Power", "Geothermal Generator", None),
                Recipe("Fuel Generator Power (Fuel)","Fuel Generator", ("Fuel", )),
                Recipe("Fuel Generator Power (Turbofuel)","Fuel Generator", ("Turbofuel", )),
                Recipe("Fuel Generator Power (Liquid Biofuel)","Fuel Generator", ("Liquid Biofuel", )),
            ),
            PowerLevel.Complex: (
                Recipe("Nuclear Power Plant Power (Uranium)","Nuclear Power Plant", ("Uranium Fuel Rod", "Water")),
                Recipe("Nuclear Power Plant Power (Plutonium)","Nuclear Power Plant", ("Plutonium Fuel Rod", "Water")),
            )
        }

        self.slots_per_milestone = 8

        self.hub_layout = (
            # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildHubData.CC_BuildHubData'
            ( # Tier 1
                {"Concrete":200, "Iron Plate":100, "Iron Rod":100, }, # Schematic: Base Building (Schematic_1-1_C)
                {"Iron Plate":150, "Iron Rod":150, "Wire":300, }, # Schematic: Logistics (Schematic_1-2_C)
                {"Wire":300, "Screw":300, "Iron Plate":100, }, # Schematic: Field Research (Schematic_1-3_C)
                {"Wire":100, "Screw":200, "Concrete":200, }, # Schematic: Archipelago Additional Tier1 (Schem_ApExtraTier1_C)
            ),
            ( # Tier 2
                {"Cable":200, "Iron Rod":200, "Screw":500, "Iron Plate":300, }, # Schematic: Part Assembly (Schematic_2-1_C)
                {"Screw":500, "Cable":100, "Concrete":100, }, # Schematic: Obstacle Clearing (Schematic_2-2_C)
                {"Rotor":50, "Iron Plate":300, "Cable":150, }, # Schematic: Jump Pads (Schematic_2-3_C)
                {"Concrete":400, "Wire":500, "Iron Rod":200, "Iron Plate":200, }, # Schematic: Resource Sink Bonus Program (Schematic_2-5_C)
                {"Reinforced Iron Plate":50, "Concrete":200, "Iron Rod":300, "Iron Plate":300, }, # Schematic: Logistics Mk.2 (Schematic_3-2_C)
            ),
            ( # Tier 3
                {"Reinforced Iron Plate":150, "Rotor":50, "Cable":300, }, # Schematic: Coal Power (Schematic_3-1_C)
                {"Modular Frame":25, "Rotor":100, "Cable":200, "Iron Rod":400, }, # Schematic: Vehicular Transport (Schematic_3-3_C)
                {"Modular Frame":50, "Rotor":150, "Concrete":300, "Wire":1000, }, # Schematic: Basic Steel Production (Schematic_3-4_C)
                {"Reinforced Iron Plate":100, "Cable":200, "Wire":1500, }, # Schematic: Improved Melee Combat (Schematic_4-2_C)
            ),
            ( # Tier 4
                {"Steel Pipe":200, "Rotor":200, "Wire":1500, "Concrete":300, }, # Schematic: Advanced Steel Production (Schematic_4-1_C)
                {"Modular Frame":100, "Steel Beam":100, "Wire":1000, }, # Schematic: Expanded Power Infrastructure (Schematic_4-3_C)
                {"Copper Sheet":300, "Steel Pipe":300, "Encased Industrial Beam":50, }, # Schematic: Hypertubes (Schematic_4-4_C)
                {"Modular Frame":100, "Steel Beam":200, "Cable":500, "Concrete":1000, }, # Schematic: FICSIT Blueprints (Schematic_4-5_C)
                {"Steel Beam":200, "Steel Pipe":100, "Concrete":500, }, # Schematic: Logistics Mk.3 (Schematic_5-3_C)
            ),
            ( # Tier 5
                {"Motor":50, "Encased Industrial Beam":100, "Steel Pipe":500, "Copper Sheet":500, }, # Schematic: Oil Processing (Schematic_5-1_C)
                {"Motor":100, "Plastic":200, "Rubber":200, "Cable":1000, }, # Schematic: Industrial Manufacturing (Schematic_5-2_C)
                {"Heavy Modular Frame":25, "Motor":100, "Plastic":200, "Wire":3000, }, # Schematic: Alternative Fluid Transport (Schematic_5-4_C)
                {"Rubber":200, "Plastic":100, "Fabric":50, }, # Schematic: Gas Mask (Schematic_6-4_C)
            ),
            ( # Tier 6
                {"Heavy Modular Frame":50, "Computer":100, "Encased Industrial Beam":200, "Rubber":400, }, # Schematic: Logistics Mk.4 (Schematic_6-1_C)
                # "Packaged Fuel":50, removed as packaging is not yet in logic
                {"Motor":50, "Plastic":100, "Rubber":100, }, # Schematic: Jetpack (Schematic_6-2_C)
                {"Computer":50, "Heavy Modular Frame":100, "Steel Beam":500, "Steel Pipe":600, }, # Schematic: Monorail Train Technology (Schematic_6-3_C)
                {"Copper Sheet":1000, "Plastic":400, "Rubber":400, "Heavy Modular Frame":50, }, # Schematic: Pipeline Engineering Mk.2 (Schematic_6-5_C)
            ),
            ( # Tier 7
                {"Computer":50, "Heavy Modular Frame":100, "Motor":200, "Rubber":500, }, # Schematic: Bauxite Refinement (Schematic_7-1_C)
                {"Alclad Aluminum Sheet":100, "Encased Industrial Beam":200, "Reinforced Iron Plate":300, }, # Schematic: Logistics Mk.5 (Schematic_7-2_C)
                {"Aluminum Casing":50, "Quickwire":500, "Gas Filter":50, }, # Schematic: Hazmat Suit (Schematic_7-3_C)
                {"Radio Control Unit":50, "Alclad Aluminum Sheet":100, "Aluminum Casing":200, "Motor":300, }, # Schematic: Aeronautical Engineering (Schematic_7-4_C)
                {"Motor":200, "Heavy Modular Frame":100, "Computer":100, "Alclad Aluminum Sheet":200, }, # Schematic: Hover Pack (Schematic_8-3_C)
            ),
            ( # Tier 8
                {"Supercomputer":50, "Heavy Modular Frame":200, "Cable":1000, "Concrete":2000, }, # Schematic: Nuclear Power (Schematic_8-1_C)
                {"Radio Control Unit":50, "Aluminum Casing":100, "Alclad Aluminum Sheet":200, "Wire":3000, }, # Schematic: Advanced Aluminum Production (Schematic_8-2_C)
                {"Fused Modular Frame":50, "Supercomputer":100, "Steel Pipe":1000, }, # Schematic: Leading-edge Production (Schematic_8-4_C)
                {"Electromagnetic Control Rod":400, "Cooling System":400, "Fused Modular Frame":200, "Turbo Motor":100, }, # Schematic: Particle Enrichment (Schematic_8-5_C)
            ),
        )

        self.space_elevator_tiers = (
            { "Smart Plating": 50 },
            { "Smart Plating": 500, "Versatile Framework": 500, "Automated Wiring": 100 },
            { "Versatile Framework": 2500, "Modular Engine": 500, "Adaptive Control Unit": 100 },
            { "Assembly Director System": 4000, "Magnetic Field Generator": 4000, "Nuclear Pasta": 1000, "Thermal Propulsion Rocket": 1000 },
        )

        # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildMamData.CC_BuildMamData'
        self.mam_nodes_layout = {
            # Alien Organisms (BPD_ResearchTree_AlienOrganisms_C)
            "Node: Alien Organisms - Inflated Pocket Dimension": MamNode({"Alien Protein":3,"Cable":1000,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrgans_3_C)
            "Node: Alien Organisms - Hostile Organism Detection": MamNode({"Alien DNA Capsule":10,"Crystal Oscillator":5,"High-Speed Connector":5,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrganisms_2_C)
            "Node: Alien Organisms - Expanded Toolbelt": MamNode({"Alien DNA Capsule":5,"Steel Beam":500,}, depends_on=("Node: Alien Organisms - Inflated Pocket Dimension", )), #(Research_ACarapace_3_C)
            "Node: Alien Organisms - Bio-Organic Properties": MamNode({"Alien Protein":5,}, depends_on=("Node: Alien Organisms - Spitter Research", "Node: Alien Organisms - Hog Research", "Node: Alien Organisms - Hatcher Research", "Node: Alien Organisms - Stinger Research", )), #(Research_AO_DNACapsule_C)
            "Node: Alien Organisms - Stinger Research": MamNode({"Stinger Remains":1,}, depends_on=()), #(Research_AO_Stinger_C)
            "Node: Alien Organisms - Hatcher Research": MamNode({"Hatcher Remains":1,}, depends_on=()), #(Research_AO_Hatcher_C)
            "Node: Alien Organisms - Hog Research": MamNode({"Hog Remains":1,}, depends_on=()), #(Research_ACarapace_0_C)
            "Node: Alien Organisms - Spitter Research": MamNode({"Plasma Spitter Remains":1,}, depends_on=()), #(Research_AOrgans_0_C)
            "Node: Alien Organisms - Structural Analysis": MamNode({"Alien DNA Capsule":5,"Iron Rod":100,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AO_Pre_Rebar_C)
            "Node: Alien Organisms - Protein Inhaler": MamNode({"Alien Protein":2,"Beryl Nut":20,"Rotor":50,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrgans_2_C)
            "Node: Alien Organisms - The Rebar Gun": MamNode({"Rotor":25,"Reinforced Iron Plate":50,"Screw":500,}, depends_on=("Node: Alien Organisms - Structural Analysis", )), #(Research_ACarapace_2_C)
            # Caterium (BPD_ResearchTree_Caterium_C)
            "Node: Caterium - Caterium Electronics": MamNode({"Quickwire":100,}, depends_on=("Node: Caterium - Quickwire", "Node: Caterium - Quickwire", "Node: Caterium - Quickwire", )), #(Research_Caterium_3_C)
            "Node: Caterium - Bullet Guidance System": MamNode({"High-Speed Connector":10,"Rifle Ammo":500,}, depends_on=("Node: Caterium - High-Speed Connector", )), #(Research_Caterium_6_3_C)
            "Node: Caterium - High-Speed Connector": MamNode({"Quickwire":500,"Plastic":50,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_5_C)
            "Node: Caterium - Caterium": MamNode({"Caterium Ore":10,}, depends_on=()), #(Research_Caterium_0_C)
            "Node: Caterium - Caterium Ingots": MamNode({"Caterium Ore":50,}, depends_on=("Node: Caterium - Caterium", )), #(Research_Caterium_1_C)
            "Node: Caterium - Quickwire": MamNode({"Caterium Ingot":50,}, depends_on=("Node: Caterium - Caterium Ingots", )), #(Research_Caterium_2_C)
            "Node: Caterium - Power Switch": MamNode({"Steel Beam":100,"AI Limiter":50,}, depends_on=("Node: Caterium - AI Limiter", )), #(Research_Caterium_4_1_2_C)
            "Node: Caterium - Power Poles Mk.2": MamNode({"Quickwire":300,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_4_2_C)
            "Node: Caterium - AI Limiter": MamNode({"Quickwire":200,"Copper Sheet":50,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_4_1_C)
            "Node: Caterium - Smart Splitter": MamNode({"AI Limiter":10,"Reinforced Iron Plate":50,}, depends_on=("Node: Caterium - AI Limiter", )), #(Research_Caterium_4_1_1_C)
            "Node: Caterium - Programmable Splitter": MamNode({"Supercomputer":50,"Heavy Modular Frame":50,}, depends_on=("Node: Caterium - Supercomputer", )), #(Research_Caterium_7_1_C)
            "Node: Caterium - Supercomputer": MamNode({"AI Limiter":50,"High-Speed Connector":50,"Computer":50,}, depends_on=("Node: Caterium - AI Limiter", "Node: Caterium - High-Speed Connector", "Node: Caterium - High-Speed Connector", )), #(Research_Caterium_6_1_C)
            "Node: Caterium - Zipline": MamNode({"Quickwire":100,"Cable":50,}, depends_on=("Node: Caterium - Quickwire", )), #(Research_Caterium_2_1_C)
            "Node: Caterium - Geothermal Generator": MamNode({"Supercomputer":50,"Heavy Modular Frame":50,"Rubber":300,}, depends_on=("Node: Caterium - Supercomputer", )), #(Research_Caterium_7_2_C)
            "Node: Caterium - Priority Power Switch": MamNode({"High-Speed Connector":25,"Circuit Board":50,}, depends_on=("Node: Caterium - High-Speed Connector", )), #(Research_Caterium_5_1_C)
            "Node: Caterium - Stun Rebar": MamNode({"Quickwire":50,"Iron Rebar":10,}, depends_on=("Node: Caterium - Quickwire", )), #(Research_Caterium_3_2_C)
            "Node: Caterium - Power Poles Mk.3": MamNode({"High-Speed Connector":50,"Steel Pipe":200,}, depends_on=("Node: Caterium - Power Poles Mk.2", )), #(Research_Caterium_6_2_C)
            # Hard Drive (BPD_ResearchTree_HardDrive_C)
            # Mycelia (BPD_ResearchTree_Mycelia_C)
            "Node: Mycelia - Therapeutic Inhaler": MamNode({"Mycelia":15,"Bacon Agaric":1,"Alien Protein":1,}, depends_on=("Node: Mycelia - Medical Properties", )), #(Research_Mycelia_6_C)
            "Node: Mycelia - Expanded Toolbelt": MamNode({"Fabric":50,"Rotor":100,}, depends_on=("Node: Mycelia - Fabric", )), #(Research_Mycelia_7_C)
            "Node: Mycelia - Mycelia": MamNode({"Mycelia":5,}, depends_on=()), #(Research_Mycelia_1_C)
            "Node: Mycelia - Fabric": MamNode({"Mycelia":25,"Biomass":100,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_2_C)
            "Node: Mycelia - Medical Properties": MamNode({"Mycelia":25,"Stator":10,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_4_C)
            "Node: Mycelia - Toxic Cellular Modification": MamNode({"Nobelisk":10,"Mycelia":100,"Biomass":200,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_8_C)
            "Node: Mycelia - Vitamin Inhaler": MamNode({"Mycelia":10,"Paleberry":5,}, depends_on=("Node: Mycelia - Medical Properties", )), #(Research_Mycelia_5_C)
            "Node: Mycelia - Parachute": MamNode({"Fabric":10,"Cable":50,}, depends_on=("Node: Mycelia - Fabric", )), #(Research_Mycelia_3_C)
            "Node: Mycelia - Synthethic Polyester Fabric": MamNode({"Fabric":25,"Polymer Resin":100,}, depends_on=("Node: Mycelia - Fabric", "Node: Mycelia - Fabric", )), #(Research_Mycelia_2_1_C)
            # Nutrients (BPD_ResearchTree_Nutrients_C)
            "Node: Nutrients - Bacon Agaric": MamNode({"Bacon Agaric":1,}, depends_on=()), #(Research_Nutrients_2_C)
            "Node: Nutrients - Beryl Nut": MamNode({"Beryl Nut":5,}, depends_on=()), #(Research_Nutrients_1_C)
            "Node: Nutrients - Paleberry": MamNode({"Paleberry":2,}, depends_on=()), #(Research_Nutrients_0_C)
            "Node: Nutrients - Nutritional Processor": MamNode({"Modular Frame":25,"Steel Pipe":50,"Wire":500,}, depends_on=("Node: Nutrients - Beryl Nut", "Node: Nutrients - Bacon Agaric", "Node: Nutrients - Paleberry", )), #(Research_Nutrients_3_C)
            "Node: Nutrients - Nutritional Inhaler": MamNode({"Bacon Agaric":2,"Paleberry":4,"Beryl Nut":10,}, depends_on=("Node: Nutrients - Nutritional Processor", )), #(Research_Nutrients_4_C)
            # Power Slugs (BPD_ResearchTree_PowerSlugs_C)
            "Node: Power Slugs - Slug Scanning": MamNode({"Iron Rod":50,"Wire":100,"Screw":200,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_3_C)
            "Node: Power Slugs - Blue Power Slugs": MamNode({"Blue Power Slug":1,}, depends_on=()), #(Research_PowerSlugs_1_C)
            "Node: Power Slugs - Yellow Power Shards": MamNode({"Yellow Power Slug":1,"Rotor":25,"Cable":100,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_4_C)
            "Node: Power Slugs - Purple Power Shards": MamNode({"Purple Power Slug":1,"Modular Frame":25,"Copper Sheet":100,}, depends_on=("Node: Power Slugs - Yellow Power Shards", )), #(Research_PowerSlugs_5_C)
            "Node: Power Slugs - Overclock Production": MamNode({"Power Shard":1,"Iron Plate":50,"Wire":50,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_2_C)
            # Quartz (BPD_ResearchTree_Quartz_C)
            "Node: Quartz - Crystal Oscillator": MamNode({"Quartz Crystal":100,"Reinforced Iron Plate":50,}, depends_on=("Node: Quartz - Quartz Crystals", "Node: Quartz - Quartz Crystals", )), #(Research_Quartz_2_C)
            "Node: Quartz - Quartz Crystals": MamNode({"Raw Quartz":20,}, depends_on=("Node: Quartz - Quartz", )), #(Research_Quartz_1_1_C)
            "Node: Quartz - Quartz": MamNode({"Raw Quartz":10,}, depends_on=()), #(Research_Quartz_0_C)
            "Node: Quartz - Shatter Rebar": MamNode({"Quartz Crystal":30,"Iron Rebar":150,}, depends_on=("Node: Quartz - Quartz Crystals", )), #(Research_Quartz_2_1_C)
            "Node: Quartz - Silica": MamNode({"Raw Quartz":20,}, depends_on=("Node: Quartz - Quartz", )), #(Research_Quartz_1_2_C)
            "Node: Quartz - Explosive Resonance Application": MamNode({"Crystal Oscillator":5,"Nobelisk":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_3_4_C)
            "Node: Quartz - Blade Runners": MamNode({"Silica":50,"Modular Frame":10,}, depends_on=("Node: Quartz - Silica", )), #(Research_Caterium_4_3_C)
            "Node: Quartz - The Explorer": MamNode({"Crystal Oscillator":10,"Modular Frame":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_3_1_C)
            "Node: Quartz - Radio Signal Scanning": MamNode({"Crystal Oscillator":100,"Motor":100,"Object Scanner":1,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_4_1_C)
            "Node: Quartz - Inflated Pocket Dimension": MamNode({"Silica":200,}, depends_on=("Node: Quartz - Silica", )), #(Research_Caterium_3_1_C)
            "Node: Quartz - Radar Technology": MamNode({"Crystal Oscillator":50,"Heavy Modular Frame":50,"Circuit Board":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_4_C)
            # Sulfur (BPD_ResearchTree_Sulfur_C)
            "Node: Sulfur - The Nobelisk Detonator": MamNode({"Black Powder":50,"Steel Pipe":100,"Cable":200,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_3_1_C)
            "Node: Sulfur - Smokeless Powder": MamNode({"Black Powder":100,"Plastic":50,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_3_C)
            "Node: Sulfur - Sulfur": MamNode({"Sulfur":10,}, depends_on=()), #(Research_Sulfur_0_C)
            "Node: Sulfur - Inflated Pocket Dimension": MamNode({"Smokeless Powder":50,"Circuit Board":50,}, depends_on=("Node: Sulfur - Nuclear Deterrent Development", "Node: Sulfur - Turbo Rifle Ammo", "Node: Sulfur - Cluster Nobelisk", "Node: Sulfur - The Rifle", )), #(Research_Sulfur_6_C)
            "Node: Sulfur - The Rifle": MamNode({"Smokeless Powder":50,"Motor":100,"Rubber":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_1_C)
            "Node: Sulfur - Compacted Coal": MamNode({"Hard Drive":1,"Sulfur":25,"Coal":25,}, depends_on=("Node: Sulfur - Experimental Power Generation", )), #(Research_Sulfur_CompactedCoal_C)
            "Node: Sulfur - Black Powder": MamNode({"Sulfur":50,"Coal":25,}, depends_on=("Node: Sulfur - Sulfur", )), #(Research_Sulfur_1_C)
            "Node: Sulfur - Explosive Rebar": MamNode({"Smokeless Powder":200,"Iron Rebar":200,"Steel Beam":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_2_C)
            "Node: Sulfur - Cluster Nobelisk": MamNode({"Smokeless Powder":100,"Nobelisk":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_C)
            "Node: Sulfur - Experimental Power Generation": MamNode({"Sulfur":25,"Modular Frame":50,"Rotor":100,}, depends_on=("Node: Sulfur - Sulfur", )), #(Research_Sulfur_ExperimentalPower_C)
            "Node: Sulfur - Turbo Rifle Ammo": MamNode({"Rifle Ammo":1000,"Packaged Turbofuel":50,"Aluminum Casing":100,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_5_2_C)
            "Node: Sulfur - Turbo Fuel": MamNode({"Hard Drive":1,"Compacted Coal":15,"Packaged Fuel":50,}, depends_on=("Node: Sulfur - Experimental Power Generation", )), #(Research_Sulfur_TurboFuel_C)
            "Node: Sulfur - Expanded Toolbelt": MamNode({"Black Powder":100,"Encased Industrial Beam":50,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_5_C)
            "Node: Sulfur - Nuclear Deterrent Development": MamNode({"Nobelisk":500,"Encased Uranium Cell":10,"AI Limiter":100,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_5_1_C)
        }

        # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildMamData.CC_BuildMamData'
        self.mam_trees_layout = {
                "Tree: Alien Organisms":
                MamTree(access_items=("Hog Remains", "Plasma Spitter Remains", ),
                    nodes=("Node: Alien Organisms - Inflated Pocket Dimension",
                        "Node: Alien Organisms - Hostile Organism Detection",
                        "Node: Alien Organisms - Expanded Toolbelt",
                        "Node: Alien Organisms - Bio-Organic Properties",
                        "Node: Alien Organisms - Stinger Research",
                        "Node: Alien Organisms - Hatcher Research",
                        "Node: Alien Organisms - Hog Research",
                        "Node: Alien Organisms - Spitter Research",
                        "Node: Alien Organisms - Structural Analysis",
                        "Node: Alien Organisms - Protein Inhaler",
                        "Node: Alien Organisms - The Rebar Gun",)
                    ),
            "Tree: Caterium":
                MamTree(access_items=("Caterium Ore", ),
                    nodes=("Node: Caterium - Caterium Electronics",
                        "Node: Caterium - Bullet Guidance System",
                        "Node: Caterium - High-Speed Connector",
                        "Node: Caterium - Caterium",
                        "Node: Caterium - Caterium Ingots",
                        "Node: Caterium - Quickwire",
                        "Node: Caterium - Power Switch",
                        "Node: Caterium - Power Poles Mk.2",
                        "Node: Caterium - AI Limiter",
                        "Node: Caterium - Smart Splitter",
                        "Node: Caterium - Programmable Splitter",
                        "Node: Caterium - Supercomputer",
                        "Node: Caterium - Zipline",
                        "Node: Caterium - Geothermal Generator",
                        "Node: Caterium - Priority Power Switch",
                        "Node: Caterium - Stun Rebar",
                        "Node: Caterium - Power Poles Mk.3",)
                    ),
            "Tree: Hard Drive":
                MamTree(access_items=("Hard Drive", ),
                    nodes=()
                    ),
            "Tree: Mycelia":
                MamTree(access_items=("Mycelia", ),
                    nodes=("Node: Mycelia - Therapeutic Inhaler",
                        "Node: Mycelia - Expanded Toolbelt",
                        "Node: Mycelia - Mycelia",
                        "Node: Mycelia - Fabric",
                        "Node: Mycelia - Medical Properties",
                        "Node: Mycelia - Toxic Cellular Modification",
                        "Node: Mycelia - Vitamin Inhaler",
                        "Node: Mycelia - Parachute",
                        "Node: Mycelia - Synthethic Polyester Fabric",)
                    ),
            "Tree: Nutrients":
                MamTree(access_items=("Paleberry", "Beryl Nut", "Bacon Agaric", ),
                    nodes=("Node: Nutrients - Bacon Agaric",
                        "Node: Nutrients - Beryl Nut",
                        "Node: Nutrients - Paleberry",
                        "Node: Nutrients - Nutritional Processor",
                        "Node: Nutrients - Nutritional Inhaler",)
                    ),
            "Tree: Power Slugs":
                MamTree(access_items=("Blue Power Slug", ),
                    nodes=("Node: Power Slugs - Slug Scanning",
                        "Node: Power Slugs - Blue Power Slugs",
                        "Node: Power Slugs - Yellow Power Shards",
                        "Node: Power Slugs - Purple Power Shards",
                        "Node: Power Slugs - Overclock Production",)
                    ),
            "Tree: Quartz":
                MamTree(access_items=("Raw Quartz", ),
                    nodes=("Node: Quartz - Crystal Oscillator",
                        "Node: Quartz - Quartz Crystals",
                        "Node: Quartz - Quartz",
                        "Node: Quartz - Shatter Rebar",
                        "Node: Quartz - Silica",
                        "Node: Quartz - Explosive Resonance Application",
                        "Node: Quartz - Blade Runners",
                        "Node: Quartz - The Explorer",
                        "Node: Quartz - Radio Signal Scanning",
                        "Node: Quartz - Inflated Pocket Dimension",
                        "Node: Quartz - Radar Technology",)
                    ),
            "Tree: Sulfur":
                MamTree(access_items=("Sulfur", ),
                    nodes=("Node: Sulfur - The Nobelisk Detonator",
                        "Node: Sulfur - Smokeless Powder",
                        "Node: Sulfur - Sulfur",
                        "Node: Sulfur - Inflated Pocket Dimension",
                        "Node: Sulfur - The Rifle",
                        "Node: Sulfur - Compacted Coal",
                        "Node: Sulfur - Black Powder",
                        "Node: Sulfur - Explosive Rebar",
                        "Node: Sulfur - Cluster Nobelisk",
                        "Node: Sulfur - Experimental Power Generation",
                        "Node: Sulfur - Turbo Rifle Ammo",
                        "Node: Sulfur - Turbo Fuel",
                        "Node: Sulfur - Expanded Toolbelt",
                        "Node: Sulfur - Nuclear Deterrent Development",)
                    ),
        }
