from typing import Tuple, Optional, Dict, Set, List
from enum import IntEnum

class PowerInfrastructureLevel(IntEnum):
    Basic = 1
    Automated = 2
    Advanced = 3
    Complex = 4

liquids: Set[str] = {
    "Water",
    "Liquid Biofuel",
    "Crude Oil",
    "Fuel",
    "Heavy Oil Residue",
    "Turbofuel",
    "Alumina Solution",
    "Sulfuric Acid",
    "Nitrogen Gas",
    "Nitric Acid"
}

radio_actives: Set[str] = {
    "Uranium",
    "Encased Uranium Cell",
    "Uranium Fuel Rod"
    "Uranium Waste",
    "Non-fissile Uranium",
    "Plutonium Pellet",
    "Encased Plutonium Cell",
    "Plutonium Fuel Rod",
    "Plutonium Waste"
}

class Recipe():
    name: str
    building: str
    inputs: Tuple[str, ...]
    minimal_belt_speed: int
    handcraftable: bool
    implicitly_unlocked: bool
    additional_outputs: Tuple[str, ...]

    needs_pipes: bool
    is_radio_active: bool

    def __init__(self, name: str, building: Optional[str] = None, inputs: Optional[Tuple[str, ...]] = None,
            minimal_belt_speed: int = 1, handcraftable: bool = False, implicitly_unlocked: bool = False,
            additional_outputs: Optional[Tuple[str, ...]] = None):
        self.name = "Recipe: " + name
        self.building = building
        self.inputs = inputs
        self.minimal_belt_speed = minimal_belt_speed
        self.handcraftable = handcraftable
        self.implicitly_unlocked = implicitly_unlocked
        self.additional_outputs = additional_outputs

        all_parts: List[str] = [name]
        if inputs:
            all_parts += inputs
        if additional_outputs:
            all_parts += additional_outputs

        self.needs_pipes = not liquids.isdisjoint(all_parts)
        self.is_radio_active = not radio_actives.isdisjoint(all_parts)

class Building(Recipe):
    power_requirement: Optional[PowerInfrastructureLevel]

    def __init__(self, name: str, inputs: Optional[Tuple[str, ...]] = None,
            power_requirement: Optional[PowerInfrastructureLevel] = None):
        super().__init__(name, None, inputs, handcraftable=True)
        self.name = "Building: " + name
        self.power_requirement = power_requirement


class MamNode():
    name: str
    unlock_cost: Dict[str, int]
    depends_on: Tuple[str, ...]

    def __init__(self, name: str, unlock_cost: Dict[str, int], depends_on: Tuple[str, ...]):
        self.name = name
        self.unlock_cost = unlock_cost
        self.depends_on = depends_on


class MamTree():
    access_items: Tuple[str, ...]
    nodes: Tuple[MamNode, ...]

    def __init__(self, access_items: Tuple[str, ...], nodes: Tuple[MamNode, ...]):
        self.access_items = access_items
        self.nodes = nodes


class GameLogic:
    recipes: Dict[str, Tuple[Recipe, ...]] = {
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
            Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue")),
            Recipe("Residual Plastic", "Refinery", ("Polymer Resin", "Water")),
            Recipe("Recycled Plastic", "Refinery", ("Rubber", "Fuel"))),
        "Rubber": (
            Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue")),
            Recipe("Residual Rubber", "Refinery", ("Polymer Resin", "Water")),
            Recipe("Recycled Rubber", "Refinery", ("Plastic", "Fuel"))),
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
            Recipe("Cable", "Constructor", ("Wire", ), handcraftable=True),
            Recipe("Coated Cable", "Refinery", ("Wire", "Heavy Oil Residue"), minimal_belt_speed=2),
            Recipe("Insulated Cable", "Assembler", ("Wire", "Rubber"), minimal_belt_speed=2),
            Recipe("Quickwire Cable", "Assembler", ("Quickwire", "Rubber"))),
        "Quickwire": (
            Recipe("Quickwire", "Constructor", ("Caterium Ingot", ), handcraftable=True),
            Recipe("Fused Quickwire", "Assembler", ("Caterium Ingot", "Copper Ingot"), minimal_belt_speed=2)),
        "Copper Sheet": (
            Recipe("Copper Sheet", "Constructor", ("Copper Ingot", ), handcraftable=True),
            Recipe("Steamed Copper Sheet", "Refinery", ("Copper Ingot", "Water"))),
        "Steel Pipe": (
            Recipe("Steel Pipe", "Constructor", ("Steel Ingot", ), handcraftable=True), ),
        "Steel Beam": (
            Recipe("Steel Beam", "Constructor", ("Steel Ingot", ), handcraftable=True), ),
        "Crude Oil": (
            Recipe("Crude Oil", "Oil Extractor", implicitly_unlocked=True), ),
        "Heavy Oil Residue": (
            Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", )),
            Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Plastic", )),
            Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Rubber", )),
            Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", ), minimal_belt_speed=3)),
        "Polymer Resin": (
            Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", )),
            Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Fuel", )),
            Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", ), minimal_belt_speed=3)),
        "Fuel": (
            Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin")),
            Recipe("Diluted Fuel", "Blender", ("Heavy Oil Residue", "Water")),
            Recipe("Residual Fuel", "Refinery", ("Heavy Oil Residue", ))),
        "Water": (
            Recipe("Water", "Water Extractor", implicitly_unlocked=True), ),
        "Concrete": (
            Recipe("Concrete", "Constructor", ("Limestone", ), handcraftable=True),
            Recipe("Fine Concrete", "Assembler", ("Limestone", "Silica")),
            Recipe("Rubber Concrete", "Assembler", ("Limestone", "Rubber")),
            Recipe("Wet Concrete", "Refinery", ("Limestone", "Water"), minimal_belt_speed=2)),
        "Silica": (
            Recipe("Silica", "Constructor", ("Raw Quartz", ), handcraftable=True),
            Recipe("Alumina Solution", "Refinery", ("Bauxite", "Water"), additional_outputs=("Alumina Solution", ), minimal_belt_speed=2),
            Recipe("Cheap Silica", "Assembler", ("Raw Quartz", "Limestone"))),
        "Quartz Crystal": (
            Recipe("Quartz Crystal", "Constructor", ("Raw Quartz", ), handcraftable=True),
            Recipe("Pure Quartz Crystal", "Refinery", ("Raw Quartz", "Water"), minimal_belt_speed=2)),
        "Iron Ingot": (
            Recipe("Iron Ingot", "Smelter", ("Iron Ore", ), handcraftable=True),
            Recipe("Pure Iron Ingot", "Refinery", ("Iron Ore", "Water"), minimal_belt_speed=2),
            Recipe("Iron Alloy Ingot", "Foundry", ("Iron Ore", "Copper Ore"))),
        "Steel Ingot": (
            Recipe("Steel Ingot", "Foundry", ("Iron Ore", "Coal"), handcraftable=True),
            Recipe("Coke Steel Ingot", "Foundry", ("Iron Ore", "Petroleum Coke"), minimal_belt_speed=2),
            Recipe("Compacted Steel Ingot", "Foundry", ("Iron Ore", "Compacted Coal")),
            Recipe("Solid Steel Ingot", "Foundry", ("Iron Ingot", "Coal"))),
        "Copper Ingot": (
            Recipe("Copper Ingot", "Smelter", ("Copper Ore", ), handcraftable=True),
            Recipe("Copper Alloy Ingot", "Foundry", ("Copper Ore", "Iron Ore"), minimal_belt_speed=2),
            Recipe("Pure Copper Ingot", "Refinery", ("Copper Ore", "Water"))),
        "Caterium Ingot": (
            Recipe("Caterium Ingot", "Smelter", ("Caterium Ore", ), handcraftable=True),
            Recipe("Pure Caterium Ingot", "Refinery", ("Caterium Ore", "Water"))),
        "Limestone": (
            Recipe("Limestone", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Raw Quartz": (
            Recipe("Raw Quartz", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Iron Ore": (
            Recipe("Iron Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Copper Ore": (
            Recipe("Copper Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Coal": (
            Recipe("Coal", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Sulfur": (
            Recipe("Sulfur", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Caterium Ore": (
            Recipe("Caterium Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Petroleum Coke": (
            Recipe("Petroleum Coke", "Refinery", ("Heavy Oil Residue", ), minimal_belt_speed=2), ),
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
            Recipe("Computer", "Manufacturer", ("Circuit Board", "Cable", "Plastic", "Screw"), minimal_belt_speed=3, handcraftable=True),
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
            Recipe("Portable Miner", "Equipment Workshop", ("Iron Rod", "Iron Plate"), handcraftable=True, minimal_belt_speed=0, implicitly_unlocked=True),
            Recipe("Automated Miner", "Manufacturer", ("Motor", "Steel Pipe", "Iron Rod", "Iron Plate")), ),
        "Bauxite": (
            Recipe("Bauxite", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Alumina Solution": (
            Recipe("Alumina Solution", "Refinery", ("Bauxite", "Water"), additional_outputs=("Silica", ), minimal_belt_speed=2), 
            Recipe("Sloppy Alumina", "Refinery", ("Bauxite", "Water"), minimal_belt_speed=3)),
        "Aluminum Scrap": (
            Recipe("Aluminum Scrap", "Refinery", ("Alumina Solution", "Coal"), additional_outputs=("Water", ), minimal_belt_speed=4),
            Recipe("Electrode - Aluminum Scrap", "Refinery", ("Alumina Solution", "Petroleum Coke"), additional_outputs=("Water", ), minimal_belt_speed=4),  
            Recipe("Instant Scrap", "Blender", ("Bauxite", "Coal", "Sulfuric Acid", "Water"), additional_outputs=("Water", ), minimal_belt_speed=3)),
        "Aluminum Ingot": (
            Recipe("Aluminum Ingot", "Foundry", ("Aluminum Scrap", "Silica"), minimal_belt_speed=2, handcraftable=True), 
            Recipe("Pure Aluminum Ingot", "Smelter", ("Aluminum Scrap", ))),
        "Alclad Aluminum Sheet": (
            Recipe("Alclad Aluminum Sheet", "Assembler", ("Aluminum Ingot", "Copper Ingot"), handcraftable=True), ),
        "Aluminum Casing": (
            Recipe("Aluminum Casing", "Constructor", ("Alclad Aluminum Sheet", ), handcraftable=True), 
            Recipe("Alclad Casing", "Assembler", ("Aluminum Ingot", "Copper Ingot"))),
        "Heat Sink": (
            Recipe("Heat Sink", "Assembler", ("Alclad Aluminum Sheet", "Silica"), minimal_belt_speed=2, handcraftable=True), 
            Recipe("Heat Exchanger", "Assembler", ("Aluminum Casing", "Rubber"), minimal_belt_speed=3)),
        "Nitrogen Gas": (
            Recipe("Nitrogen Gas", "Resource Well Pressurizer", implicitly_unlocked=True), ),
        "Nitric Acid": (
            Recipe("Nitric Acid", "Blender", ("Nitrogen Gas", "Water", "Iron Plate")), ),
        "Fused Modular Frame": (
            Recipe("Fused Modular Frame", "Blender", ("Heavy Modular Frame", "Aluminum Casing", "Nitrogen Gas"), minimal_belt_speed=2), 
            Recipe("Heat-Fused Frame", "Blender", ("Heavy Modular Frame", "Aluminum Ingot", "Nitric Acid", "Fuel"), minimal_belt_speed=3)),
        "Radio Control Unit": (
            Recipe("Radio Control Unit", "Manufacturer", ("Aluminum Casing", "Crystal Oscillator", "Computer"), handcraftable=True),
            Recipe("Radio Connection Unit", "Manufacturer", ("Heat Sink", "High-Speed Connector", "Quartz Crystal")),  
            Recipe("Radio Control System", "Manufacturer", ("Crystal Oscillator", "Circuit Board", "Aluminum Casing", "Rubber"), minimal_belt_speed=2)),
        "Pressure Conversion Cube": (
            Recipe("Pressure Conversion Cube", "Assembler", ("Fused Modular Frame", "Radio Control Unit"), handcraftable=True), ),
        "Cooling System": (
            Recipe("Cooling System", "Blender", ("Heat Sink", "Rubber", "Water", "Nitrogen Gas")), 
            Recipe("Cooling Device", "Blender", ("Heat Sink", "Motor", "Nitrogen Gas"))),
        "Turbo Motor": (
            Recipe("Turbo Motor", "Manufacturer", ("Cooling System", "Radio Control Unit", "Motor", "Rubber"), handcraftable=True),
            Recipe("Turbo Electric Motor", "Manufacturer", ("Motor", "Radio Control Unit", "Electromagnetic Control Rod", "Rotor")),
            Recipe("Turbo Pressure Motor", "Manufacturer", ("Motor", "Pressure Conversion Cube", "Packaged Nitrogen Gas", "Stator"))),
        "Battery": (
            Recipe("Battery", "Blender", ("Sulfuric Acid", "Alumina Solution", "Aluminum Casing"), additional_outputs=("Water", )), 
            Recipe("Classic Battery", "Manufacturer", ("Sulfur", "Alclad Aluminum Sheet", "Plastic", "Wire"), minimal_belt_speed=2)),
        "Supercomputer": (
            Recipe("Supercomputer", "Manufacturer", ("Computer", "AI Limiter", "High-Speed Connector", "Plastic"), handcraftable=True),
            Recipe("OC Supercomputer", "Assembler", ("Radio Control Unit", "Cooling System")),
            Recipe("Super-State Computer", "Manufacturer", ("Computer", "Electromagnetic Control Rod", "Battery", "Wire"))),
        "Uranium": (
            Recipe("Uranium", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Sulfuric Acid": (
            Recipe("Sulfuric Acid", "Refinery", ("Sulfur", "Water")), 
            Recipe("Encased Uranium Cell", "Blender", ("Uranium", "Concrete", "Sulfuric Acid"), additional_outputs=("Encased Uranium Cell", ))),
        "Encased Uranium Cell": (
            Recipe("Encased Uranium Cell", "Blender", ("Uranium", "Concrete", "Sulfuric Acid"), additional_outputs=("Sulfuric Acid", )), 
            Recipe("Infused Uranium Cell", "Manufacturer", ("Uranium", "Silica", "Sulfur", "Quickwire"), minimal_belt_speed=2)),
        "Uranium Fuel Rod": (
            Recipe("Uranium Fuel Rod", "Manufacturer", ("Encased Uranium Cell", "Encased Industrial Beam", "Electromagnetic Control Rod")), 
            Recipe("Uranium Fuel Unit", "Manufacturer", ("Encased Uranium Cell", "Electromagnetic Control Rod", "Crystal Oscillator", "Beacon"))),
        "Beacon": (
            Recipe("Beacon", "Equipment Workshop", ("Iron Plate", "Iron Rod", "Wire", "Cable"), handcraftable=True, minimal_belt_speed=0), 
            Recipe("Beacon", "Manufacturer", ("Iron Plate", "Iron Rod", "Wire", "Cable")),
            Recipe("Crystal Beacon", "Manufacturer", ("Steel Beam", "Steel Pipe", "Crystal Oscillator"))),
        "Uranium Waste": (
            Recipe("Uranium Waste", "Nuclear Power Plant", ("Uranium Fuel Rod", "Water"), implicitly_unlocked=True), ),
        "Non-fissile Uranium": (
            Recipe("Non-fissile Uranium", "Blender", ("Uranium Waste", "Silica", "Nitric Acid", "Sulfuric Acid"), additional_outputs=("Water", )), 
            Recipe("Fertile Uranium", "Blender", ("Uranium", "Uranium Waste", "Nitric Acid", "Sulfuric Acid"), additional_outputs=("Water", ), minimal_belt_speed=2)),
        "Plutonium Pellet": (
            Recipe("Plutonium Pellet", "Particle Accelerator", ("Non-fissile Uranium", "Uranium Waste"), minimal_belt_speed=2), ),
        "Encased Plutonium Cell": (
            Recipe("Encased Plutonium Cell", "Assembler", ("Plutonium Pellet", "Concrete")), 
            Recipe("Instant Plutonium Cell", "Particle Accelerator", ("Non-fissile Uranium", "Aluminum Casing"), minimal_belt_speed=2)),
        "Plutonium Fuel Rod": (
            Recipe("Plutonium Fuel Rod", "Manufacturer", ("Encased Plutonium Cell", "Steel Beam", "Electromagnetic Control Rod", "Heat Sink")), 
            Recipe("Plutonium Fuel Unit", "Assembler", ("Encased Plutonium Cell", "Pressure Conversion Cube"))),
        "Gas Filter": (
            Recipe("Gas Filter", "Manufacturer", ("Coal", "Rubber", "Fabric"), handcraftable=True), ),
        "Iodine Infused Filter": (
            Recipe("Iodine Infused Filter", "Manufacturer", ("Gas Filter", "Quickwire", "Aluminum Casing"), handcraftable=True), ),
        "Hazmat Suit": (
            Recipe("Hazmat Suit", "Equipment Workshop", ("Rubber", "Plastic", "Fabric", "Alclad Aluminum Sheet"), handcraftable=True, minimal_belt_speed=0), ),
        "Assembly Director System": (
            Recipe("Assembly Director System", "Assembler", ("Adaptive Control Unit", "Supercomputer")), ),
        "Magnetic Field Generator": (
            Recipe("Magnetic Field Generator", "Manufacturer", ("Versatile Framework", "Electromagnetic Control Rod", "Battery")), ),
        "Copper Powder": (
            Recipe("Copper Powder", "Constructor", ("Copper Ingot", ), handcraftable=True), ),
        "Nuclear Pasta": (
            Recipe("Nuclear Pasta", "Particle Accelerator", ("Copper Powder", "Pressure Conversion Cube")), ),
        "Thermal Propulsion Rocket": (
            Recipe("Thermal Propulsion Rocket", "Manufacturer", ("Modular Engine", "Turbo Motor", "Cooling System", "Fused Modular Frame")), ),
        "Leaves": (
            Recipe("Leaves", handcraftable=True, implicitly_unlocked=True), ),
        "Wood": (
            Recipe("Wood", handcraftable=True, implicitly_unlocked=True), ),
        "Hatcher Remains": (
            Recipe("Hatcher Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Hog Remains": (
            Recipe("Hog Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Plasma Spitter Remains": (
            Recipe("Plasma Spitter Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Stinger Remains": (
            Recipe("Stinger Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Alien Protein": (
            Recipe("Hatcher Protein", "Constructor", ("Hatcher Remains", ), handcraftable=True),
            Recipe("Hog Protein", "Constructor", ("Hog Remains", ), handcraftable=True),
            Recipe("Spitter Protein", "Constructor", ("Plasma Spitter Remains", ), handcraftable=True),
            Recipe("Stinger Protein", "Constructor", ("Stinger Remains", ), handcraftable=True)),
        "Biomass": (
            Recipe("Biomass (Leaves)", "Constructor", ("Leaves", ), minimal_belt_speed=2, handcraftable=True),
            Recipe("Biomass (Wood)", "Constructor", ("Wood", ), minimal_belt_speed=4, handcraftable=True),
            Recipe("Biomass (Mycelia)", "Constructor", ("Mycelia", ), minimal_belt_speed=3, handcraftable=True),
            Recipe("Biomass (Alien Protein)", "Constructor", ("Alien Protein", ), minimal_belt_speed=5, handcraftable=True)),
        "Mycelia": (
            Recipe("Mycelia", handcraftable=True), ),
        "Fabric": (
            Recipe("Fabric", "Assembler", ("Biomass", "Mycelia"), handcraftable=True, minimal_belt_speed=2), 
            Recipe("Polyester Fabric", "Refinery", ("Polymer Resin", "Water"))),
        "Solid Biofuel": (
            Recipe("Solid Biofuel", "Constructor", ("Biomass", ), minimal_belt_speed=2, handcraftable=True), ),
        "Liquid Biofuel": (
            Recipe("Liquid Biofuel", "Refinery", ("Solid Biofuel", "Water"), minimal_belt_speed=2), ),
        "Empty Canister": (
            Recipe("Empty Canister", "Constructor", ("Plastic", ), handcraftable=True),
            Recipe("Coated Iron Canister", "Assembler", ("Iron Plate", "Copper Sheet")),
            Recipe("Steel Canister", "Constructor", ("Steel Ingot", ))),
        "Empty Fluid Tank": (
            Recipe("Empty Fluid Tank", "Constructor", ("Aluminum Ingot", ), handcraftable=True), ),
        "Packaged Alumina Solution": (
            Recipe("Packaged Alumina Solution", "Packager", ("Alumina Solution", "Empty Canister"), minimal_belt_speed=2), ),
        "Packaged Fuel": (
            Recipe("Packaged Fuel", "Packager", ("Fuel", "Empty Canister")),
            Recipe("Diluted Packaged Fuel", "Refinery", ("Heavy Oil Residue", "Packaged Water"))),
        "Packaged Heavy Oil Residue": (
            Recipe("Packaged Heavy Oil Residue", "Packager", ("Heavy Oil Residue", "Empty Canister")), ),
        "Packaged Liquid Biofuel": (
            Recipe("Packaged Liquid Biofuel", "Packager", ("Liquid Biofuel", "Empty Canister")), ),
        "Packaged Nitric Acid": (
            Recipe("Packaged Nitric Acid", "Packager", ("Nitric Acid", "Empty Fluid Tank")), ),
        "Packaged Nitrogen Gas": (
            Recipe("Packaged Nitrogen Gas", "Packager", ("Nitrogen Gas", "Empty Fluid Tank")), ),
        "Packaged Oil": (
            Recipe("Packaged Oil", "Packager", ("Crude Oil", "Empty Fluid Tank")), ),
        "Packaged Sulfuric Acid": (
            Recipe("Packaged Sulfuric Acid", "Packager", ("Sulfuric Acid", "Empty Fluid Tank")), ),
        "Packaged Turbofuel": (
            Recipe("Packaged Turbofuel", "Packager", ("Turbofuel", "Empty Fluid Tank")), ),
        "Packaged Water": (
            Recipe("Packaged Water", "Packager", ("Water", "Empty Fluid Tank")), ),
        "Turbofuel": (
            Recipe("Turbofuel", "Refinery", ("Fuel", "Compacted Coal")),
            Recipe("Turbo Heavy Fuel", "Refinery", ("Heavy Oil Residue", "Compacted Coal")),
            Recipe("Turbo Blend Fuel", "Blender", ("Fuel", "Heavy Oil Residue", "Sulfur", "Petroleum Coke"))),
        "Gas Mask": (
            Recipe("Gas Mask", "Equipment Workshop", ("Rubber", "Plastic", "Fabric"), handcraftable=True, minimal_belt_speed=0), ),
        "Alien DNA Capsule": (
            Recipe("Alien DNA Capsule", "Constructor", ("Alien Protein", ), handcraftable=True), ),
        "Black Powder": (
            Recipe("Black Powder", "Assembler", ("Coal", "Sulfur"), handcraftable=True), 
            Recipe("Fine Black Powder", "Assembler", ("Sulfur", "Compacted Coal"))),
        "Smokeless Powder": (
            Recipe("Smokeless Powder", "Refinery", ("Black Powder", "Heavy Oil Residue"), handcraftable=True), ),
        "Rifle Ammo": (
            Recipe("Rifle Ammo", "Assembler", ("Copper Sheet", "Smokeless Powder"), handcraftable=True, minimal_belt_speed=2), ),
        "Iron Rebar": (
            Recipe("Iron Rebar", "Constructor", ("Iron Rod", ), handcraftable=True), ),
        "Nobelisk": (
            Recipe("Nobelisk", "Assembler", ("Black Powder", "Steel Pipe"), handcraftable=True), ),
        "Beryl Nut": (
            Recipe("Beryl Nut", handcraftable=True, implicitly_unlocked=True), ),
        "Paleberry": (
            Recipe("Paleberry", handcraftable=True, implicitly_unlocked=True), ),
        "Bacon Agaric": (
            Recipe("Bacon Agaric", handcraftable=True, implicitly_unlocked=True), ),
        "Blue Power Slug": (
            Recipe("Blue Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Yellow Power Slug": (
            Recipe("Yellow Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Purple Power Slug": (
            Recipe("Purple Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Power Shard": (
            Recipe("Power Shard (1)", "Constructor", ("Blue Power Slug", ), handcraftable=True),
            Recipe("Power Shard (2)", "Constructor", ("Yellow Power Slug", ), handcraftable=True),
            Recipe("Power Shard (5)", "Constructor", ("Purple Power Slug", ), handcraftable=True)),
        "Hard Drive": (
            Recipe("Hard Drive", handcraftable=True, implicitly_unlocked=True), ),
        "Object Scanner": (
            Recipe("Object Scanner", "Equipment Workshop", ("Reinforced Iron Plate", "Wire", "Screw"), handcraftable=True, minimal_belt_speed=0), ),

        # TODO transport types arent currently in logic
        # TODO fix multiple handcraftable recipes per part
    }

    handcraftable_recipes: Dict[str, Recipe] = { part: recipe 
        for part, recipes_per_part in recipes.items()
        for recipe in recipes_per_part if recipe.handcraftable 
    }

    buildings: Dict[str, Building] = {
        "Constructor": Building("Constructor", ("Reinforced Iron Plate", "Cable"), PowerInfrastructureLevel.Basic),
        "Assembler": Building("Assembler", ("Reinforced Iron Plate", "Rotor", "Cable"), PowerInfrastructureLevel.Basic),
        "Manufacturer": Building("Manufacturer", ("Motor", "Heavy Modular Frame", "Cable", "Plastic"), PowerInfrastructureLevel.Advanced),
        "Packager": Building("Packager", ("Steel Beam", "Rubber", "Plastic"), PowerInfrastructureLevel.Basic),
        "Refinery": Building("Refinery", ("Motor", "Encased Industrial Beam", "Steel Pipe", "Copper Sheet"), PowerInfrastructureLevel.Automated),
        "Blender": Building("Blender", ("Motor", "Heavy Modular Frame", "Aluminum Casing", "Radio Control Unit"), PowerInfrastructureLevel.Complex),
        "Particle Accelerator": Building("Particle Accelerator", ("Radio Control Unit", "Electromagnetic Control Rod", "Supercomputer", "Cooling System", "Fused Modular Frame", "Turbo Motor"), PowerInfrastructureLevel.Complex),
        "Biomass Burner": Building("Biomass Burner", ("Iron Plate", "Iron Rod", "Wire")),
        "Coal Generator": Building("Coal Generator", ("Reinforced Iron Plate", "Rotor", "Cable")),
        "Fuel Generator": Building("Fuel Generator", ("Computer", "Heavy Modular Frame", "Motor", "Rubber", "Quickwire")),
        "Geothermal Generator": Building("Geothermal Generator", ("Supercomputer", "Heavy Modular Frame", "High-Speed Connector", "Copper Sheet", "Rubber")),
        "Nuclear Power Plant": Building("Nuclear Power Plant", ("Concrete", "Heavy Modular Frame", "Supercomputer", "Cable", "Alclad Aluminum Sheet")),
        "Miner Mk.1": Building("Miner Mk.1", ("Iron Plate", "Concrete"), PowerInfrastructureLevel.Basic),
        "Miner Mk.2": Building("Miner Mk.2", ("Encased Industrial Beam", "Steel Pipe", "Modular Frame"), PowerInfrastructureLevel.Automated),
        "Miner Mk.3": Building("Miner Mk.3", ("Steel Pipe", "Supercomputer", "Fused Modular Frame", "Turbo Motor"), PowerInfrastructureLevel.Advanced),
        "Oil Extractor": Building("Oil Extractor", ("Motor", "Encased Industrial Beam", "Cable")),
        "Water Extractor": Building("Water Extractor", ("Copper Sheet", "Reinforced Iron Plate", "Rotor")),
        "Smelter": Building("Smelter", ("Iron Rod", "Wire"), PowerInfrastructureLevel.Basic),
        "Foundry": Building("Foundry", ("Modular Frame", "Rotor", "Concrete"), PowerInfrastructureLevel.Basic),
        "Resource Well Pressurizer": Building("Resource Well Pressurizer", ("Wire", "Rubber", "Encased Industrial Beam", "Motor", "Steel Beam", "Plastic"), PowerInfrastructureLevel.Advanced),
        "Equipment Workshop": Building("Equipment Workshop", ("Iron Plate", "Iron Rod")),
        "AWESOME Sink": Building("AWESOME Sink", ("Reinforced Iron Plate", "Cable", "Concrete")),
        "AWESOME Shop": Building("AWESOME Shop", ("Screw", "Iron Plate", "Cable")),
        "MAM": Building("MAM", ("Reinforced Iron Plate", "Wire", "Cable")),
        "Pipes Mk.1": Building("Pipes Mk.1", ("Copper Sheet", "Iron Plate", "Concrete")),
        "Pipes Mk.2": Building("Pipes Mk.2", ("Copper Sheet", "Plastic", "Iron Plate", "Concrete")),
        "Pipeline Pump Mk.1": Building("Pipeline Pump Mk.1", ("Copper Sheet", "Rotor")),
        "Pipeline Pump Mk.2": Building("Pipeline Pump Mk.2", ("Motor", "Encased Industrial Beam", "Plastic")),
        "Conveyor Merger": Building("Conveyor Merger", ("Iron Plate", "Iron Rod")),
        "Conveyor Splitter": Building("Conveyor Splitter", ("Iron Plate", "Cable")),
        "Conveyor Mk.1": Building("Conveyor Mk.1", ("Iron Plate", "Iron Rod", "Concrete")),
        "Conveyor Mk.2": Building("Conveyor Mk.2", ("Reinforced Iron Plate", "Iron Plate", "Iron Rod", "Concrete")),
        "Conveyor Mk.3": Building("Conveyor Mk.3", ("Steel Beam", "Iron Plate", "Iron Rod", "Concrete")),
        "Conveyor Mk.4": Building("Conveyor Mk.4", ("Encased Industrial Beam", "Iron Plate", "Iron Rod", "Concrete")),
        "Conveyor Mk.5": Building("Conveyor Mk.5", ("Alclad Aluminum Sheet", "Iron Plate", "Iron Rod", "Concrete")),
        "Power Pole Mk.1": Building("Power Pole Mk.1", ("Iron Plate", "Iron Rod", "Concrete")),
        # higher level power poles arent in logic
        #"Power Pole Mk.2": Building("Power Pole Mk.2", ("Quickwire", "Iron Rod", "Concrete")),
        #"Power Pole Mk.3": Building("Power Pole Mk.3", ("High-Speed Connector", "Steel Pipe", "Rubber")),
    }

    requirement_per_powerlevel: Dict[PowerInfrastructureLevel, Tuple[Recipe, ...]] = {
        PowerInfrastructureLevel.Basic: (
            Recipe("Biomass Power", "Biomass Burner", ("Solid Biofuel", ), implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Automated: (
            Recipe("Coal Generator Power", "Coal Generator", ("Coal", "Water"), implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Advanced: (
            Recipe("Geothermal Generator Power", "Geothermal Generator", implicitly_unlocked=True),
            #Recipe("Fuel Generator Power (Liquid Biofuel)","Fuel Generator", ("Liquid Biofuel", ), implicitly_unlocked=True),
            Recipe("Fuel Generator Power (Fuel)","Fuel Generator", ("Fuel", ), implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Complex: (
            Recipe("Fuel Generator Power (Turbofuel)","Fuel Generator", ("Turbofuel", ), implicitly_unlocked=True),
            Recipe("Nuclear Power Plant Power (Uranium)","Nuclear Power Plant", ("Uranium Fuel Rod", "Water"), implicitly_unlocked=True),
            #Recipe("Nuclear Power Plant Power (Plutonium)","Nuclear Power Plant", ("Plutonium Fuel Rod", "Water"), implicitly_unlocked=True),
        )
    }

    slots_per_milestone: int = 8

    hub_layout: Tuple[Tuple[Dict[str, int], ...], ...] = (
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
            {"Motor":50, "Plastic":100, "Rubber":100, "Packaged Fuel":50 }, # Schematic: Jetpack (Schematic_6-2_C)
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

    space_elevator_tiers: Tuple[Dict[str, int], ...] = (
        { "Smart Plating": 50 },
        { "Smart Plating": 500, "Versatile Framework": 500, "Automated Wiring": 100 },
        { "Versatile Framework": 2500, "Modular Engine": 500, "Adaptive Control Unit": 100 },
        { "Assembly Director System": 4000, "Magnetic Field Generator": 4000, "Nuclear Pasta": 1000, "Thermal Propulsion Rocket": 1000 },
    )

    # Turbo Fuel
# Quartz Crystals
# Vitamin Inhaler
# Bacon Agaric

    man_trees: Dict[str, MamTree] = {
        "Alien Organisms": MamTree(("Hog Remains", "Plasma Spitter Remains"), ( # Alien Organisms (BPD_ResearchTree_AlienOrganisms_C)
            MamNode("Inflated Pocket Dimension", {"Alien Protein":3,"Cable":1000,}, depends_on=("Bio-Organic Properties", )), #(Research_AOrgans_3_C)
            MamNode("Hostile Organism Detection", {"Alien DNA Capsule":10,"Crystal Oscillator":5,"High-Speed Connector":5,}, depends_on=("Bio-Organic Properties", )), #(Research_AOrganisms_2_C)
            MamNode("Expanded Toolbelt", {"Alien DNA Capsule":5,"Steel Beam":500,}, depends_on=("Inflated Pocket Dimension", )), #(Research_ACarapace_3_C)
            MamNode("Bio-Organic Properties", {"Alien Protein":5,}, depends_on=("Spitter Research", "Hog Research", "Hatcher Research", "Stinger Research")), #(Research_AO_DNACapsule_C)
            MamNode("Stinger Research", {"Stinger Remains":1,}, depends_on=()), #(Research_AO_Stinger_C)
            MamNode("Hatcher Research", {"Hatcher Remains":1,}, depends_on=()), #(Research_AO_Hatcher_C)
            MamNode("Hog Research", {"Hog Remains":1,}, depends_on=()), #(Research_ACarapace_0_C)
            MamNode("Spitter Research", {"Plasma Spitter Remains":1,}, depends_on=()), #(Research_AOrgans_0_C)
            MamNode("Structural Analysis", {"Alien DNA Capsule":5,"Iron Rod":100,}, depends_on=("Bio-Organic Properties", )), #(Research_AO_Pre_Rebar_C)
            MamNode("Protein Inhaler", {"Alien Protein":2,"Beryl Nut":20,"Rotor":50,}, depends_on=("Bio-Organic Properties", )), #(Research_AOrgans_2_C)
            MamNode("The Rebar Gun", {"Rotor":25,"Reinforced Iron Plate":50,"Screw":500,}, depends_on=("Structural Analysis", )), #(Research_ACarapace_2_C)
        )),
        "Caterium": MamTree(("Caterium Ore", ), ( # Caterium (BPD_ResearchTree_Caterium_C)
            MamNode("Caterium Electronics", {"Quickwire":100,}, depends_on=("Quickwire", )), #(Research_Caterium_3_C)
            MamNode("Bullet Guidance System", {"High-Speed Connector":10,"Rifle Ammo":500,}, depends_on=("High-Speed Connector", )), #(Research_Caterium_6_3_C)
            MamNode("High-Speed Connector", {"Quickwire":500,"Plastic":50,}, depends_on=("Caterium Electronics", )), #(Research_Caterium_5_C)
            MamNode("Caterium", {"Caterium Ore":10,}, depends_on=()), #(Research_Caterium_0_C)
            MamNode("Caterium Ingots", {"Caterium Ore":50,}, depends_on=("Caterium", )), #(Research_Caterium_1_C)
            MamNode("Quickwire", {"Caterium Ingot":50,}, depends_on=("Caterium Ingots", )), #(Research_Caterium_2_C)
            MamNode("Power Switch", {"Steel Beam":100,"AI Limiter":50,}, depends_on=("AI Limiter", )), #(Research_Caterium_4_1_2_C)
            MamNode("Power Poles Mk.2", {"Quickwire":300,}, depends_on=("Caterium Electronics", )), #(Research_Caterium_4_2_C)
            MamNode("AI Limiter", {"Quickwire":200,"Copper Sheet":50,}, depends_on=("Caterium Electronics", )), #(Research_Caterium_4_1_C)
            MamNode("Smart Splitter", {"AI Limiter":10,"Reinforced Iron Plate":50,}, depends_on=("AI Limiter", )), #(Research_Caterium_4_1_1_C)
            MamNode("Programmable Splitter", {"Supercomputer":50,"Heavy Modular Frame":50,}, depends_on=("Supercomputer", )), #(Research_Caterium_7_1_C)
            MamNode("Supercomputer", {"AI Limiter":50,"High-Speed Connector":50,"Computer":50,}, depends_on=("AI Limiter", "High-Speed Connector")), #(Research_Caterium_6_1_C)
            MamNode("Zipline", {"Quickwire":100,"Cable":50,}, depends_on=("Quickwire", )), #(Research_Caterium_2_1_C)
            MamNode("Geothermal Generator", {"Supercomputer":50,"Heavy Modular Frame":50,"Rubber":300,}, depends_on=("Supercomputer", )), #(Research_Caterium_7_2_C)
            MamNode("Priority Power Switch", {"High-Speed Connector":25,"Circuit Board":50,}, depends_on=("High-Speed Connector", )), #(Research_Caterium_5_1_C)
            MamNode("Stun Rebar", {"Quickwire":50,"Iron Rebar":10,}, depends_on=("Quickwire", )), #(Research_Caterium_3_2_C)
            MamNode("Power Poles Mk.3", {"High-Speed Connector":50,"Steel Pipe":200,}, depends_on=("Power Poles Mk.2", )), #(Research_Caterium_6_2_C)
        )),
        "Mycelia": MamTree(("Mycelia", ), ( # Mycelia (BPD_ResearchTree_Mycelia_C)
            MamNode("Therapeutic Inhaler", {"Mycelia":15,"Bacon Agaric":1,"Alien Protein":1,}, depends_on=("Medical Properties", )), #(Research_Mycelia_6_C)
            MamNode("Expanded Toolbelt", {"Fabric":50,"Rotor":100,}, depends_on=("Fabric", )), #(Research_Mycelia_7_C)
            MamNode("Mycelia", {"Mycelia":5,}, depends_on=tuple()), #(Research_Mycelia_1_C)
            MamNode("Fabric", {"Mycelia":25,"Biomass":100,}, depends_on=("Mycelia", )), #(Research_Mycelia_2_C)
            MamNode("Medical Properties", {"Mycelia":25,"Stator":10,}, depends_on=("Mycelia", )), #(Research_Mycelia_4_C)
            MamNode("Toxic Cellular Modification", {"Nobelisk":10,"Mycelia":100,"Biomass":200,}, depends_on=("Mycelia", )), #(Research_Mycelia_8_C)
            MamNode("Vitamin Inhaler", {"Mycelia":10,"Paleberry":5,}, depends_on=("Medical Properties", )), #(Research_Mycelia_5_C)
            MamNode("Parachute", {"Fabric":10,"Cable":50,}, depends_on=("Fabric", )), #(Research_Mycelia_3_C)
            MamNode("Synthethic Polyester Fabric", {"Fabric":25,"Polymer Resin":100,}, depends_on=("Fabric", )), #(Research_Mycelia_2_1_C)
        )),
        "Nutrients": MamTree(("Paleberry", "Beryl Nut", "Bacon Agaric"), ( # Nutrients (BPD_ResearchTree_Nutrients_C)
            MamNode("Bacon Agaric", {"Bacon Agaric":1,}, depends_on=()), #(Research_Nutrients_2_C)
            MamNode("Beryl Nut", {"Beryl Nut":5,}, depends_on=()), #(Research_Nutrients_1_C)
            MamNode("Paleberry", {"Paleberry":2,}, depends_on=()), #(Research_Nutrients_0_C)
            MamNode("Nutritional Processor", {"Modular Frame":25,"Steel Pipe":50,"Wire":500,}, depends_on=("Beryl Nut", "Bacon Agaric", "Paleberry")), #(Research_Nutrients_3_C)
            MamNode("Nutritional Inhaler", {"Bacon Agaric":2,"Paleberry":4,"Beryl Nut":10,}, depends_on=("Nutritional Processor", )), #(Research_Nutrients_4_C)
        )),
        "Power Slugs": MamTree(("Blue Power Slug", ), ( # Power Slugs (BPD_ResearchTree_PowerSlugs_C)
            MamNode("Slug Scanning", {"Iron Rod":50,"Wire":100,"Screw":200,}, depends_on=("Blue Power Slugs", )), #(Research_PowerSlugs_3_C)
            MamNode("Blue Power Slugs", {"Blue Power Slug":1,}, depends_on=()), #(Research_PowerSlugs_1_C)
            MamNode("Yellow Power Shards", {"Yellow Power Slug":1,"Rotor":25,"Cable":100,}, depends_on=("Blue Power Slugs", )), #(Research_PowerSlugs_4_C)
            MamNode("Purple Power Shards", {"Purple Power Slug":1,"Modular Frame":25,"Copper Sheet":100,}, depends_on=("Yellow Power Shards", )), #(Research_PowerSlugs_5_C)
            MamNode("Overclock Production", {"Power Shard":1,"Iron Plate":50,"Wire":50,}, depends_on=("Blue Power Slugs", )), #(Research_PowerSlugs_2_C)
        )),
        "Quartz": MamTree(("Raw Quartz", ), ( # Quartz (BPD_ResearchTree_Quartz_C)
            MamNode("Crystal Oscillator", {"Quartz Crystal":100,"Reinforced Iron Plate":50,}, depends_on=("Quartz Crystals", "Quartz Crystals")), #(Research_Quartz_2_C)
            MamNode("Quartz Crystals", {"Raw Quartz":20,}, depends_on=("Quartz", )), #(Research_Quartz_1_1_C)
            MamNode("Quartz", {"Raw Quartz":10,}, depends_on=()), #(Research_Quartz_0_C)
            MamNode("Shatter Rebar", {"Quartz Crystal":30,"Iron Rebar":150,}, depends_on=("Quartz Crystals", )), #(Research_Quartz_2_1_C)
            MamNode("Silica", {"Raw Quartz":20,}, depends_on=("Quartz", )), #(Research_Quartz_1_2_C)
            MamNode("Explosive Resonance Application", {"Crystal Oscillator":5,"Nobelisk":100,}, depends_on=("Crystal Oscillator", )), #(Research_Quartz_3_4_C)
            MamNode("Blade Runners", {"Silica":50,"Modular Frame":10,}, depends_on=("Silica", )), #(Research_Caterium_4_3_C)
            MamNode("The Explorer", {"Crystal Oscillator":10,"Modular Frame":100,}, depends_on=("Crystal Oscillator", )), #(Research_Quartz_3_1_C)
            MamNode("Radio Signal Scanning", {"Crystal Oscillator":100,"Motor":100,"Object Scanner":1,}, depends_on=("Crystal Oscillator", )), #(Research_Quartz_4_1_C)
            MamNode("Inflated Pocket Dimension", {"Silica":200,}, depends_on=("Silica", )), #(Research_Caterium_3_1_C)
            MamNode("Radar Technology", {"Crystal Oscillator":50,"Heavy Modular Frame":50,"Circuit Board":100,}, depends_on=("Crystal Oscillator", )), #(Research_Quartz_4_C)
        )),
        "Sulfur": MamTree(("Sulfur", ), ( # Sulfur (BPD_ResearchTree_Sulfur_C)
            MamNode("The Nobelisk Detonator", {"Black Powder":50,"Steel Pipe":100,"Cable":200,}, depends_on=("Black Powder", )), #(Research_Sulfur_3_1_C)
            MamNode("Smokeless Powder", {"Black Powder":100,"Plastic":50,}, depends_on=("Black Powder", )), #(Research_Sulfur_3_C)
            MamNode("Sulfur", {"Sulfur":10,}, depends_on=()), #(Research_Sulfur_0_C)
            MamNode("Inflated Pocket Dimension", {"Smokeless Powder":50,"Circuit Board":50,}, depends_on=("Nuclear Deterrent Development", "Turbo Rifle Ammo", "Cluster Nobelisk", "The Rifle")), #(Research_Sulfur_6_C)
            MamNode("The Rifle", {"Smokeless Powder":50,"Motor":100,"Rubber":200,}, depends_on=("Smokeless Powder", )), #(Research_Sulfur_4_1_C)
            MamNode("Compacted Coal", {"Hard Drive":1,"Sulfur":25,"Coal":25,}, depends_on=("Experimental Power Generation", )), #(Research_Sulfur_CompactedCoal_C)
            MamNode("Black Powder", {"Sulfur":50,"Coal":25,}, depends_on=("Sulfur", )), #(Research_Sulfur_1_C)
            MamNode("Explosive Rebar", {"Smokeless Powder":200,"Iron Rebar":200,"Steel Beam":200,}, depends_on=("Smokeless Powder", )), #(Research_Sulfur_4_2_C)
            MamNode("Cluster Nobelisk", {"Smokeless Powder":100,"Nobelisk":200,}, depends_on=("Smokeless Powder", )), #(Research_Sulfur_4_C)
            MamNode("Experimental Power Generation", {"Sulfur":25,"Modular Frame":50,"Rotor":100,}, depends_on=("Sulfur", )), #(Research_Sulfur_ExperimentalPower_C)
            MamNode("Turbo Rifle Ammo", {"Rifle Ammo":1000,"Packaged Turbofuel":50,"Aluminum Casing":100,}, depends_on=("Smokeless Powder", )), #(Research_Sulfur_5_2_C)
            MamNode("Turbo Fuel", {"Hard Drive":1,"Compacted Coal":15,"Packaged Fuel":50,}, depends_on=("Experimental Power Generation", )), #(Research_Sulfur_TurboFuel_C)
            MamNode("Expanded Toolbelt", {"Black Powder":100,"Encased Industrial Beam":50,}, depends_on=("Black Powder", )), #(Research_Sulfur_5_C)
            MamNode("Nuclear Deterrent Development", {"Nobelisk":500,"Encased Uranium Cell":10,"AI Limiter":100,}, depends_on=("Smokeless Powder", )), #(Research_Sulfur_5_1_C)
        ))
    }

    # # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildMamData.CC_BuildMamData'
    # mam_nodes_layout: Dict[str, MamNode] = {
    #     # Alien Organisms (BPD_ResearchTree_AlienOrganisms_C)
    #     "Node: Alien Organisms - Inflated Pocket Dimension": MamNode({"Alien Protein":3,"Cable":1000,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrgans_3_C)
    #     "Node: Alien Organisms - Hostile Organism Detection": MamNode({"Alien DNA Capsule":10,"Crystal Oscillator":5,"High-Speed Connector":5,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrganisms_2_C)
    #     "Node: Alien Organisms - Expanded Toolbelt": MamNode({"Alien DNA Capsule":5,"Steel Beam":500,}, depends_on=("Node: Alien Organisms - Inflated Pocket Dimension", )), #(Research_ACarapace_3_C)
    #     "Node: Alien Organisms - Bio-Organic Properties": MamNode({"Alien Protein":5,}, depends_on=("Node: Alien Organisms - Spitter Research", "Node: Alien Organisms - Hog Research", "Node: Alien Organisms - Hatcher Research", "Node: Alien Organisms - Stinger Research", )), #(Research_AO_DNACapsule_C)
    #     "Node: Alien Organisms - Stinger Research": MamNode({"Stinger Remains":1,}, depends_on=()), #(Research_AO_Stinger_C)
    #     "Node: Alien Organisms - Hatcher Research": MamNode({"Hatcher Remains":1,}, depends_on=()), #(Research_AO_Hatcher_C)
    #     "Node: Alien Organisms - Hog Research": MamNode({"Hog Remains":1,}, depends_on=()), #(Research_ACarapace_0_C)
    #     "Node: Alien Organisms - Spitter Research": MamNode({"Plasma Spitter Remains":1,}, depends_on=()), #(Research_AOrgans_0_C)
    #     "Node: Alien Organisms - Structural Analysis": MamNode({"Alien DNA Capsule":5,"Iron Rod":100,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AO_Pre_Rebar_C)
    #     "Node: Alien Organisms - Protein Inhaler": MamNode({"Alien Protein":2,"Beryl Nut":20,"Rotor":50,}, depends_on=("Node: Alien Organisms - Bio-Organic Properties", )), #(Research_AOrgans_2_C)
    #     "Node: Alien Organisms - The Rebar Gun": MamNode({"Rotor":25,"Reinforced Iron Plate":50,"Screw":500,}, depends_on=("Node: Alien Organisms - Structural Analysis", )), #(Research_ACarapace_2_C)
    #     # Caterium (BPD_ResearchTree_Caterium_C)
    #     "Node: Caterium - Caterium Electronics": MamNode({"Quickwire":100,}, depends_on=("Node: Caterium - Quickwire", "Node: Caterium - Quickwire", "Node: Caterium - Quickwire", )), #(Research_Caterium_3_C)
    #     "Node: Caterium - Bullet Guidance System": MamNode({"High-Speed Connector":10,"Rifle Ammo":500,}, depends_on=("Node: Caterium - High-Speed Connector", )), #(Research_Caterium_6_3_C)
    #     "Node: Caterium - High-Speed Connector": MamNode({"Quickwire":500,"Plastic":50,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_5_C)
    #     "Node: Caterium - Caterium": MamNode({"Caterium Ore":10,}, depends_on=()), #(Research_Caterium_0_C)
    #     "Node: Caterium - Caterium Ingots": MamNode({"Caterium Ore":50,}, depends_on=("Node: Caterium - Caterium", )), #(Research_Caterium_1_C)
    #     "Node: Caterium - Quickwire": MamNode({"Caterium Ingot":50,}, depends_on=("Node: Caterium - Caterium Ingots", )), #(Research_Caterium_2_C)
    #     "Node: Caterium - Power Switch": MamNode({"Steel Beam":100,"AI Limiter":50,}, depends_on=("Node: Caterium - AI Limiter", )), #(Research_Caterium_4_1_2_C)
    #     "Node: Caterium - Power Poles Mk.2": MamNode({"Quickwire":300,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_4_2_C)
    #     "Node: Caterium - AI Limiter": MamNode({"Quickwire":200,"Copper Sheet":50,}, depends_on=("Node: Caterium - Caterium Electronics", )), #(Research_Caterium_4_1_C)
    #     "Node: Caterium - Smart Splitter": MamNode({"AI Limiter":10,"Reinforced Iron Plate":50,}, depends_on=("Node: Caterium - AI Limiter", )), #(Research_Caterium_4_1_1_C)
    #     "Node: Caterium - Programmable Splitter": MamNode({"Supercomputer":50,"Heavy Modular Frame":50,}, depends_on=("Node: Caterium - Supercomputer", )), #(Research_Caterium_7_1_C)
    #     "Node: Caterium - Supercomputer": MamNode({"AI Limiter":50,"High-Speed Connector":50,"Computer":50,}, depends_on=("Node: Caterium - AI Limiter", "Node: Caterium - High-Speed Connector", "Node: Caterium - High-Speed Connector", )), #(Research_Caterium_6_1_C)
    #     "Node: Caterium - Zipline": MamNode({"Quickwire":100,"Cable":50,}, depends_on=("Node: Caterium - Quickwire", )), #(Research_Caterium_2_1_C)
    #     "Node: Caterium - Geothermal Generator": MamNode({"Supercomputer":50,"Heavy Modular Frame":50,"Rubber":300,}, depends_on=("Node: Caterium - Supercomputer", )), #(Research_Caterium_7_2_C)
    #     "Node: Caterium - Priority Power Switch": MamNode({"High-Speed Connector":25,"Circuit Board":50,}, depends_on=("Node: Caterium - High-Speed Connector", )), #(Research_Caterium_5_1_C)
    #     "Node: Caterium - Stun Rebar": MamNode({"Quickwire":50,"Iron Rebar":10,}, depends_on=("Node: Caterium - Quickwire", )), #(Research_Caterium_3_2_C)
    #     "Node: Caterium - Power Poles Mk.3": MamNode({"High-Speed Connector":50,"Steel Pipe":200,}, depends_on=("Node: Caterium - Power Poles Mk.2", )), #(Research_Caterium_6_2_C)
    #     # Hard Drive (BPD_ResearchTree_HardDrive_C)
    #     # Mycelia (BPD_ResearchTree_Mycelia_C)
    #     "Node: Mycelia - Therapeutic Inhaler": MamNode({"Mycelia":15,"Bacon Agaric":1,"Alien Protein":1,}, depends_on=("Node: Mycelia - Medical Properties", )), #(Research_Mycelia_6_C)
    #     "Node: Mycelia - Expanded Toolbelt": MamNode({"Fabric":50,"Rotor":100,}, depends_on=("Node: Mycelia - Fabric", )), #(Research_Mycelia_7_C)
    #     "Node: Mycelia - Mycelia": MamNode({"Mycelia":5,}, depends_on=()), #(Research_Mycelia_1_C)
    #     "Node: Mycelia - Fabric": MamNode({"Mycelia":25,"Biomass":100,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_2_C)
    #     "Node: Mycelia - Medical Properties": MamNode({"Mycelia":25,"Stator":10,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_4_C)
    #     "Node: Mycelia - Toxic Cellular Modification": MamNode({"Nobelisk":10,"Mycelia":100,"Biomass":200,}, depends_on=("Node: Mycelia - Mycelia", )), #(Research_Mycelia_8_C)
    #     "Node: Mycelia - Vitamin Inhaler": MamNode({"Mycelia":10,"Paleberry":5,}, depends_on=("Node: Mycelia - Medical Properties", )), #(Research_Mycelia_5_C)
    #     "Node: Mycelia - Parachute": MamNode({"Fabric":10,"Cable":50,}, depends_on=("Node: Mycelia - Fabric", )), #(Research_Mycelia_3_C)
    #     "Node: Mycelia - Synthethic Polyester Fabric": MamNode({"Fabric":25,"Polymer Resin":100,}, depends_on=("Node: Mycelia - Fabric", "Node: Mycelia - Fabric", )), #(Research_Mycelia_2_1_C)
    #     # Nutrients (BPD_ResearchTree_Nutrients_C)
    #     "Node: Nutrients - Bacon Agaric": MamNode({"Bacon Agaric":1,}, depends_on=()), #(Research_Nutrients_2_C)
    #     "Node: Nutrients - Beryl Nut": MamNode({"Beryl Nut":5,}, depends_on=()), #(Research_Nutrients_1_C)
    #     "Node: Nutrients - Paleberry": MamNode({"Paleberry":2,}, depends_on=()), #(Research_Nutrients_0_C)
    #     "Node: Nutrients - Nutritional Processor": MamNode({"Modular Frame":25,"Steel Pipe":50,"Wire":500,}, depends_on=("Node: Nutrients - Beryl Nut", "Node: Nutrients - Bacon Agaric", "Node: Nutrients - Paleberry", )), #(Research_Nutrients_3_C)
    #     "Node: Nutrients - Nutritional Inhaler": MamNode({"Bacon Agaric":2,"Paleberry":4,"Beryl Nut":10,}, depends_on=("Node: Nutrients - Nutritional Processor", )), #(Research_Nutrients_4_C)
    #     # Power Slugs (BPD_ResearchTree_PowerSlugs_C)
    #     "Node: Power Slugs - Slug Scanning": MamNode({"Iron Rod":50,"Wire":100,"Screw":200,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_3_C)
    #     "Node: Power Slugs - Blue Power Slugs": MamNode({"Blue Power Slug":1,}, depends_on=()), #(Research_PowerSlugs_1_C)
    #     "Node: Power Slugs - Yellow Power Shards": MamNode({"Yellow Power Slug":1,"Rotor":25,"Cable":100,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_4_C)
    #     "Node: Power Slugs - Purple Power Shards": MamNode({"Purple Power Slug":1,"Modular Frame":25,"Copper Sheet":100,}, depends_on=("Node: Power Slugs - Yellow Power Shards", )), #(Research_PowerSlugs_5_C)
    #     "Node: Power Slugs - Overclock Production": MamNode({"Power Shard":1,"Iron Plate":50,"Wire":50,}, depends_on=("Node: Power Slugs - Blue Power Slugs", )), #(Research_PowerSlugs_2_C)
    #     # Quartz (BPD_ResearchTree_Quartz_C)
    #     "Node: Quartz - Crystal Oscillator": MamNode({"Quartz Crystal":100,"Reinforced Iron Plate":50,}, depends_on=("Node: Quartz - Quartz Crystals", "Node: Quartz - Quartz Crystals", )), #(Research_Quartz_2_C)
    #     "Node: Quartz - Quartz Crystals": MamNode({"Raw Quartz":20,}, depends_on=("Node: Quartz - Quartz", )), #(Research_Quartz_1_1_C)
    #     "Node: Quartz - Quartz": MamNode({"Raw Quartz":10,}, depends_on=()), #(Research_Quartz_0_C)
    #     "Node: Quartz - Shatter Rebar": MamNode({"Quartz Crystal":30,"Iron Rebar":150,}, depends_on=("Node: Quartz - Quartz Crystals", )), #(Research_Quartz_2_1_C)
    #     "Node: Quartz - Silica": MamNode({"Raw Quartz":20,}, depends_on=("Node: Quartz - Quartz", )), #(Research_Quartz_1_2_C)
    #     "Node: Quartz - Explosive Resonance Application": MamNode({"Crystal Oscillator":5,"Nobelisk":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_3_4_C)
    #     "Node: Quartz - Blade Runners": MamNode({"Silica":50,"Modular Frame":10,}, depends_on=("Node: Quartz - Silica", )), #(Research_Caterium_4_3_C)
    #     "Node: Quartz - The Explorer": MamNode({"Crystal Oscillator":10,"Modular Frame":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_3_1_C)
    #     "Node: Quartz - Radio Signal Scanning": MamNode({"Crystal Oscillator":100,"Motor":100,"Object Scanner":1,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_4_1_C)
    #     "Node: Quartz - Inflated Pocket Dimension": MamNode({"Silica":200,}, depends_on=("Node: Quartz - Silica", )), #(Research_Caterium_3_1_C)
    #     "Node: Quartz - Radar Technology": MamNode({"Crystal Oscillator":50,"Heavy Modular Frame":50,"Circuit Board":100,}, depends_on=("Node: Quartz - Crystal Oscillator", )), #(Research_Quartz_4_C)
    #     # Sulfur (BPD_ResearchTree_Sulfur_C)
    #     "Node: Sulfur - The Nobelisk Detonator": MamNode({"Black Powder":50,"Steel Pipe":100,"Cable":200,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_3_1_C)
    #     "Node: Sulfur - Smokeless Powder": MamNode({"Black Powder":100,"Plastic":50,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_3_C)
    #     "Node: Sulfur - Sulfur": MamNode({"Sulfur":10,}, depends_on=()), #(Research_Sulfur_0_C)
    #     "Node: Sulfur - Inflated Pocket Dimension": MamNode({"Smokeless Powder":50,"Circuit Board":50,}, depends_on=("Node: Sulfur - Nuclear Deterrent Development", "Node: Sulfur - Turbo Rifle Ammo", "Node: Sulfur - Cluster Nobelisk", "Node: Sulfur - The Rifle", )), #(Research_Sulfur_6_C)
    #     "Node: Sulfur - The Rifle": MamNode({"Smokeless Powder":50,"Motor":100,"Rubber":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_1_C)
    #     "Node: Sulfur - Compacted Coal": MamNode({"Hard Drive":1,"Sulfur":25,"Coal":25,}, depends_on=("Node: Sulfur - Experimental Power Generation", )), #(Research_Sulfur_CompactedCoal_C)
    #     "Node: Sulfur - Black Powder": MamNode({"Sulfur":50,"Coal":25,}, depends_on=("Node: Sulfur - Sulfur", )), #(Research_Sulfur_1_C)
    #     "Node: Sulfur - Explosive Rebar": MamNode({"Smokeless Powder":200,"Iron Rebar":200,"Steel Beam":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_2_C)
    #     "Node: Sulfur - Cluster Nobelisk": MamNode({"Smokeless Powder":100,"Nobelisk":200,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_4_C)
    #     "Node: Sulfur - Experimental Power Generation": MamNode({"Sulfur":25,"Modular Frame":50,"Rotor":100,}, depends_on=("Node: Sulfur - Sulfur", )), #(Research_Sulfur_ExperimentalPower_C)
    #     "Node: Sulfur - Turbo Rifle Ammo": MamNode({"Rifle Ammo":1000,"Packaged Turbofuel":50,"Aluminum Casing":100,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_5_2_C)
    #     "Node: Sulfur - Turbo Fuel": MamNode({"Hard Drive":1,"Compacted Coal":15,"Packaged Fuel":50,}, depends_on=("Node: Sulfur - Experimental Power Generation", )), #(Research_Sulfur_TurboFuel_C)
    #     "Node: Sulfur - Expanded Toolbelt": MamNode({"Black Powder":100,"Encased Industrial Beam":50,}, depends_on=("Node: Sulfur - Black Powder", )), #(Research_Sulfur_5_C)
    #     "Node: Sulfur - Nuclear Deterrent Development": MamNode({"Nobelisk":500,"Encased Uranium Cell":10,"AI Limiter":100,}, depends_on=("Node: Sulfur - Smokeless Powder", )), #(Research_Sulfur_5_1_C)
    # }

    # # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildMamData.CC_BuildMamData'
    # mam_trees_layout: Dict[str, MamTree] = {
    #     "Tree: Alien Organisms":
    #         MamTree(access_items=("Hog Remains", "Plasma Spitter Remains", ),
    #             nodes=("Node: Alien Organisms - Inflated Pocket Dimension",
    #                 "Node: Alien Organisms - Hostile Organism Detection",
    #                 "Node: Alien Organisms - Expanded Toolbelt",
    #                 "Node: Alien Organisms - Bio-Organic Properties",
    #                 "Node: Alien Organisms - Stinger Research",
    #                 "Node: Alien Organisms - Hatcher Research",
    #                 "Node: Alien Organisms - Hog Research",
    #                 "Node: Alien Organisms - Spitter Research",
    #                 "Node: Alien Organisms - Structural Analysis",
    #                 "Node: Alien Organisms - Protein Inhaler",
    #                 "Node: Alien Organisms - The Rebar Gun",)
    #         ),
    #     "Tree: Caterium":
    #         MamTree(access_items=("Caterium Ore", ),
    #             nodes=("Node: Caterium - Caterium Electronics",
    #                 "Node: Caterium - Bullet Guidance System",
    #                 "Node: Caterium - High-Speed Connector",
    #                 "Node: Caterium - Caterium",
    #                 "Node: Caterium - Caterium Ingots",
    #                 "Node: Caterium - Quickwire",
    #                 "Node: Caterium - Power Switch",
    #                 "Node: Caterium - Power Poles Mk.2",
    #                 "Node: Caterium - AI Limiter",
    #                 "Node: Caterium - Smart Splitter",
    #                 "Node: Caterium - Programmable Splitter",
    #                 "Node: Caterium - Supercomputer",
    #                 "Node: Caterium - Zipline",
    #                 "Node: Caterium - Geothermal Generator",
    #                 "Node: Caterium - Priority Power Switch",
    #                 "Node: Caterium - Stun Rebar",
    #                 "Node: Caterium - Power Poles Mk.3",)
    #         ),
    #     "Tree: Hard Drive":
    #         MamTree(access_items=("Hard Drive", ),
    #             nodes=()
    #         ),
    #     "Tree: Mycelia":
    #         MamTree(access_items=("Mycelia", ),
    #             nodes=("Node: Mycelia - Therapeutic Inhaler",
    #                 "Node: Mycelia - Expanded Toolbelt",
    #                 "Node: Mycelia - Mycelia",
    #                 "Node: Mycelia - Fabric",
    #                 "Node: Mycelia - Medical Properties",
    #                 "Node: Mycelia - Toxic Cellular Modification",
    #                 "Node: Mycelia - Vitamin Inhaler",
    #                 "Node: Mycelia - Parachute",
    #                 "Node: Mycelia - Synthethic Polyester Fabric",)
    #         ),
    #     "Tree: Nutrients":
    #         MamTree(access_items=("Paleberry", "Beryl Nut", "Bacon Agaric", ),
    #             nodes=("Node: Nutrients - Bacon Agaric",
    #                 "Node: Nutrients - Beryl Nut",
    #                 "Node: Nutrients - Paleberry",
    #                 "Node: Nutrients - Nutritional Processor",
    #                 "Node: Nutrients - Nutritional Inhaler",)
    #         ),
    #     "Tree: Power Slugs":
    #         MamTree(access_items=("Blue Power Slug", ),
    #             nodes=("Node: Power Slugs - Slug Scanning",
    #                 "Node: Power Slugs - Blue Power Slugs",
    #                 "Node: Power Slugs - Yellow Power Shards",
    #                 "Node: Power Slugs - Purple Power Shards",
    #                 "Node: Power Slugs - Overclock Production",)
    #         ),
    #     "Tree: Quartz":
    #         MamTree(access_items=("Raw Quartz", ),
    #             nodes=("Node: Quartz - Crystal Oscillator",
    #                 "Node: Quartz - Quartz Crystals",
    #                 "Node: Quartz - Quartz",
    #                 "Node: Quartz - Shatter Rebar",
    #                 "Node: Quartz - Silica",
    #                 "Node: Quartz - Explosive Resonance Application",
    #                 "Node: Quartz - Blade Runners",
    #                 "Node: Quartz - The Explorer",
    #                 "Node: Quartz - Radio Signal Scanning",
    #                 "Node: Quartz - Inflated Pocket Dimension",
    #                 "Node: Quartz - Radar Technology",)
    #         ),
    #     "Tree: Sulfur":
    #         MamTree(access_items=("Sulfur", ),
    #             nodes=("Node: Sulfur - The Nobelisk Detonator",
    #                 "Node: Sulfur - Smokeless Powder",
    #                 "Node: Sulfur - Sulfur",
    #                 "Node: Sulfur - Inflated Pocket Dimension",
    #                 "Node: Sulfur - The Rifle",
    #                 "Node: Sulfur - Compacted Coal",
    #                 "Node: Sulfur - Black Powder",
    #                 "Node: Sulfur - Explosive Rebar",
    #                 "Node: Sulfur - Cluster Nobelisk",
    #                 "Node: Sulfur - Experimental Power Generation",
    #                 "Node: Sulfur - Turbo Rifle Ammo",
    #                 "Node: Sulfur - Turbo Fuel",
    #                 "Node: Sulfur - Expanded Toolbelt",
    #                 "Node: Sulfur - Nuclear Deterrent Development",)
    #         ),
    #     }
