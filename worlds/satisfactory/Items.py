from random import Random
from typing import ClassVar, Dict, Literal, Set, NamedTuple, List, TextIO, Tuple, Optional
from BaseClasses import Item, ItemClassification, MultiWorld
from .GameLogic import GameLogic, Recipe
from .Options import get_option_value

class ItemData(NamedTuple):
    category: Literal["Parts", "Equipment", "Ammo", "Recipe", "Building", "Trap"]
    code: int
    type: ItemClassification = ItemClassification.filler

class Items:
    item_data: ClassVar[Dict[str, ItemData]] = {
        # Parts
        "Adaptive Control Unit": ItemData("Parts", 1338000),
        "AI Limiter": ItemData("Parts", 1338001),
        "Alclad Aluminum Sheet": ItemData("Parts", 1338002),
        "Blue Power Slug": ItemData("Parts", 1338003),
        "Yellow Power Slug": ItemData("Parts", 1338004),
        "Alien Protein": ItemData("Parts", 1338005),
        "Purple Power Slug": ItemData("Parts", 1338006),
        "Aluminum Casing": ItemData("Parts", 1338007),
        "Aluminum Ingot": ItemData("Parts", 1338008),
        "Aluminum Scrap": ItemData("Parts", 1338009),
        "Assembly Director System": ItemData("Parts", 1338010),
        "Automated Wiring": ItemData("Parts", 1338011),
        "Battery": ItemData("Parts", 1338012),
        "Bauxite": ItemData("Parts", 1338013),
        "Beacon": ItemData("Parts", 1338014),
        "Biomass": ItemData("Parts", 1338015),
        "Black Powder": ItemData("Parts", 1338016),
        "Cable": ItemData("Parts", 1338017),
        "Caterium Ingot": ItemData("Parts", 1338018),
        "Caterium Ore": ItemData("Parts", 1338019),
        "Circuit Board": ItemData("Parts", 1338020),
        "Coal": ItemData("Parts", 1338021),
        "Color Cartridge": ItemData("Parts", 1338022),
        "Compacted Coal": ItemData("Parts", 1338023),
        "Computer": ItemData("Parts", 1338024),
        "Concrete": ItemData("Parts", 1338025),
        "Cooling System": ItemData("Parts", 1338026),
        "Copper Ingot": ItemData("Parts", 1338027),
        "Copper Ore": ItemData("Parts", 1338028),
        "Copper Powder": ItemData("Parts", 1338029),
        "Copper Sheet": ItemData("Parts", 1338030),
        "Adequate Pioneering Statue": ItemData("Parts", 1338031),
        "Crystal Oscillator": ItemData("Parts", 1338032),
        "Electromagnetic Control Rod": ItemData("Parts", 1338033),
        "Empty Canister": ItemData("Parts", 1338034),
        "Empty Fluid Tank": ItemData("Parts", 1338035),
        "Encased Industrial Beam": ItemData("Parts", 1338036),
        "Encased Plutonium Cell": ItemData("Parts", 1338037, ItemClassification.trap),
        "Encased Uranium Cell": ItemData("Parts", 1338038, ItemClassification.trap),
        "Fabric": ItemData("Parts", 1338039),
        "FICSIT Coupon": ItemData("Parts", 1338040),
        "Flower Petals": ItemData("Parts", 1338041),
        "Fused Modular Frame": ItemData("Parts", 1338042),
        "Hard Drive": ItemData("Parts", 1338043),
        "Heat Sink": ItemData("Parts", 1338044),
        "Heavy Modular Frame": ItemData("Parts", 1338045),
        "High-Speed Connector": ItemData("Parts", 1338046),
        "Satisfactory Pioneering Statue": ItemData("Parts", 1338047), 
        "Pretty Good Pioneering Statue": ItemData("Parts", 1338048),
        "Iron Ingot": ItemData("Parts", 1338049),
        "Iron Ore": ItemData("Parts", 1338050),
        "Iron Plate": ItemData("Parts", 1338051),
        "Iron Rod": ItemData("Parts", 1338052),
        "Golden Nut Statue": ItemData("Parts", 1338053),
        "Leaves": ItemData("Parts", 1338054),
        "Limestone": ItemData("Parts", 1338055),
        "Magnetic Field Generator": ItemData("Parts", 1338056),
        "Mercer Sphere": ItemData("Parts", 1338057),
        "Modular Engine": ItemData("Parts", 1338058),
        "Modular Frame": ItemData("Parts", 1338059),
        "Motor": ItemData("Parts", 1338060),
        "Mycelia": ItemData("Parts", 1338061),
        "Non-fissile Uranium": ItemData("Trap", 1338062, ItemClassification.trap),
        "Nuclear Pasta": ItemData("Parts", 1338063),
        "Lizard Doggo Statue": ItemData("Parts", 1338064),
        "Organic Data Capsule": ItemData("Parts", 1338065),
        "Packaged Alumina Solution": ItemData("Parts", 1338066),
        "Packaged Fuel": ItemData("Parts", 1338067),
        "Packaged Heavy Oil Residue": ItemData("Parts", 1338068),
        "Packaged Liquid Biofuel": ItemData("Parts", 1338069),
        "Packaged Nitric Acid": ItemData("Parts", 1338070),
        "Packaged Nitrogen Gas": ItemData("Parts", 1338071),
        "Packaged Oil": ItemData("Parts", 1338072),
        "Packaged Sulfuric Acid": ItemData("Parts", 1338073),
        "Packaged Turbofuel": ItemData("Parts", 1338074),
        "Packaged Water": ItemData("Parts", 1338075),
        "Petroleum Coke": ItemData("Parts", 1338076),
        "Plastic": ItemData("Parts", 1338077),
        "Plutonium Fuel Rod": ItemData("Trap", 1338078, ItemClassification.trap),
        "Plutonium Pellet": ItemData("Trap", 1338079, ItemClassification.trap),
        "Plutonium Waste (item)": ItemData("Trap", 1338080, ItemClassification.trap),
        "Polymer Resin": ItemData("Parts", 1338081),
        "Power Shard": ItemData("Parts", 1338082),
        "Confusing Creature Statue": ItemData("Parts", 1338083),
        "Pressure Conversion Cube": ItemData("Parts", 1338084),
        "Quantum Computer": ItemData("Parts", 1338085),
        "Quartz Crystal": ItemData("Parts", 1338086),
        "Quickwire": ItemData("Parts", 1338087),
        "Radio Control Unit": ItemData("Parts", 1338088),
        "Raw Quartz": ItemData("Parts", 1338089),
        "Reinforced Iron Plate": ItemData("Parts", 1338090),
        "Rotor": ItemData("Parts", 1338091),
        "Rubber": ItemData("Parts", 1338092),
        "SAM Ore": ItemData("Parts", 1338093),
        "Screw": ItemData("Parts", 1338094),
        "Silica": ItemData("Parts", 1338095),
        "Smart Plating": ItemData("Parts", 1338096),
        "Smokeless Powder": ItemData("Parts", 1338097),
        "Solid Biofuel": ItemData("Parts", 1338098),
        "Somersloop": ItemData("Parts", 1338099),
        "Stator": ItemData("Parts", 1338100),
        "Silver Hog Statue": ItemData("Parts", 1338101),
        "Steel Beam": ItemData("Parts", 1338102),
        "Steel Ingot": ItemData("Parts", 1338103),
        "Steel Pipe": ItemData("Parts", 1338104),
        "Sulfur": ItemData("Parts", 1338105),
        "Supercomputer": ItemData("Parts", 1338106),
        "Superposition Oscillator": ItemData("Parts", 1338107),
        "Thermal Propulsion Rocket": ItemData("Parts", 1338108),
        "Turbo Motor": ItemData("Parts", 1338109),
        "Hog Remains": ItemData("Parts", 1338110),
        "Uranium": ItemData("Trap", 1338111, ItemClassification.trap),
        "Uranium Fuel Rod": ItemData("Trap", 1338112, ItemClassification.trap),
        "Uranium Waste (item)": ItemData("Trap", 1338113, ItemClassification.trap),
        "Versatile Framework": ItemData("Parts", 1338114),
        "Wire": ItemData("Parts", 1338115),
        "Wood": ItemData("Parts", 1338116),
        "Plasma Spitter Remains": ItemData("Parts", 1338117),
        "Stinger Remains": ItemData("Parts", 1338118),
        "Hatcher Remains": ItemData("Parts", 1338119),
        "Alien DNA Capsule": ItemData("Parts", 1338120),
        #1338121 - 1338149 Reserved for future parts

        # Equipment / Ammo
        "Bacon Agaric": ItemData("Equipment", 1338150),
        "Beryl Nut": ItemData("Equipment", 1338151),
        "Blade Runners": ItemData("Equipment", 1338152),
        "Boom Box": ItemData("Equipment", 1338153),
        "Chainsaw": ItemData("Equipment", 1338154),
        "Cluster Nobelisk": ItemData("Ammo", 1338155),
        #"Color Gun": ItemData("Equipment", 1338156), Removed in U8
        "Cup": ItemData("Equipment", 1338157),
        "Cup (gold)": ItemData("Equipment", 1338158),
        "Explosive Rebar": ItemData("Ammo", 1338159),
        "Factory Cart": ItemData("Equipment", 1338160),
        "Factory Cart (gold)": ItemData("Equipment", 1338161),
        "Gas Mask": ItemData("Equipment", 1338162, type=ItemClassification.progression),
        "Gas Nobelisk": ItemData("Ammo", 1338163),
        "Hazmat Suit": ItemData("Equipment", 1338164, type=ItemClassification.progression),
        "Homing Rifle Ammo": ItemData("Ammo", 1338165),
        "Hover Pack": ItemData("Equipment", 1338166, type=ItemClassification.progression),
        "Iron Rebar": ItemData("Ammo", 1338167),
        "Jetpack": ItemData("Equipment", 1338168, type=ItemClassification.progression),
        "Medicinal Inhaler": ItemData("Equipment", 1338169),
        "Nobelisk": ItemData("Ammo", 1338170),
        "Nobelisk Detonator": ItemData("Equipment", 1338171, type=ItemClassification.progression),
        "Nuke Nobelisk": ItemData("Ammo", 1338172),
        "Object Scanner": ItemData("Equipment", 1338173),
        "Paleberry": ItemData("Equipment", 1338174),
        "Parachute": ItemData("Equipment", 1338175),
        "Pulse Nobelisk": ItemData("Ammo", 1338176),
        "Rebar Gun": ItemData("Equipment", 1338177),
        "Rifle": ItemData("Equipment", 1338178),
        "Rifle Ammo": ItemData("Ammo", 1338179),
        "Shatter Rebar": ItemData("Ammo", 1338180),
        "Stun Rebar": ItemData("Ammo", 1338181),
        "Turbo Rifle Ammo": ItemData("Ammo", 1338182),
        "Xeno-Basher": ItemData("Equipment", 1338183),
        "Xeno-Zapper": ItemData("Equipment", 1338184),
        "Zipline": ItemData("Equipment", 1338185),
        "Portable Miner": ItemData("Equipment", 1338186),

        #1338186 - 1338199 Reserved for future equipment/ammo

        #1338200+ Recipes / buildings / schematics / others
        "Recipe: Reinforced Iron Plate": ItemData("Recipe", 1338200, type=ItemClassification.useful),
        "Recipe: Adhered Iron Plate": ItemData("Recipe", 1338201, type=ItemClassification.useful),
        "Recipe: Bolted Iron Plate": ItemData("Recipe", 1338202, type=ItemClassification.useful),
        "Recipe: Stitched Iron Plate": ItemData("Recipe", 1338203, type=ItemClassification.useful),
        "Recipe: Rotor": ItemData("Recipe", 1338204, type=ItemClassification.useful),
        "Recipe: Copper Rotor": ItemData("Recipe", 1338205, type=ItemClassification.useful),
        "Recipe: Steel Rotor": ItemData("Recipe", 1338206, type=ItemClassification.useful),
        "Recipe: Stator": ItemData("Recipe", 1338207, type=ItemClassification.useful),
        "Recipe: Quickwire Stator": ItemData("Recipe", 1338208, type=ItemClassification.useful),
        "Recipe: Plastic": ItemData("Recipe", 1338209, type=ItemClassification.useful),
        "Recipe: Residual Plastic": ItemData("Recipe", 1338210, type=ItemClassification.useful),
        "Recipe: Recycled Plastic": ItemData("Recipe", 1338211, type=ItemClassification.useful),
        "Recipe: Rubber": ItemData("Recipe", 1338212, type=ItemClassification.useful),
        "Recipe: Residual Rubber": ItemData("Recipe", 1338213, type=ItemClassification.useful),
        "Recipe: Recycled Rubber": ItemData("Recipe", 1338214, type=ItemClassification.useful),
        "Recipe: Iron Plate": ItemData("Recipe", 1338215, type=ItemClassification.useful),
        "Recipe: Coated Iron Plate": ItemData("Recipe", 1338216, type=ItemClassification.useful),
        "Recipe: Steel Coated Plate": ItemData("Recipe", 1338217, type=ItemClassification.useful),
        "Recipe: Iron Rod": ItemData("Recipe", 1338218, type=ItemClassification.useful),
        "Recipe: Steel Rod": ItemData("Recipe", 1338219, type=ItemClassification.useful),
        "Recipe: Screw": ItemData("Recipe", 1338220, type=ItemClassification.useful),
        "Recipe: Cast Screw": ItemData("Recipe", 1338221, type=ItemClassification.useful),
        "Recipe: Steel Screw": ItemData("Recipe", 1338222, type=ItemClassification.useful),
        "Recipe: Wire": ItemData("Recipe", 1338223, type=ItemClassification.useful),
        "Recipe: Fused Wire": ItemData("Recipe", 1338224, type=ItemClassification.useful),
        "Recipe: Iron Wire": ItemData("Recipe", 1338225, type=ItemClassification.useful),
        "Recipe: Caterium Wire": ItemData("Recipe", 1338226, type=ItemClassification.useful),
        "Recipe: Cable": ItemData("Recipe", 1338227, type=ItemClassification.useful),
        "Recipe: Coated Cable": ItemData("Recipe", 1338228, type=ItemClassification.useful),
        "Recipe: Insulated Cable": ItemData("Recipe", 1338229, type=ItemClassification.useful),
        "Recipe: Quickwire Cable": ItemData("Recipe", 1338230, type=ItemClassification.useful),
        "Recipe: Quickwire": ItemData("Recipe", 1338231, type=ItemClassification.useful),
        "Recipe: Fused Quickwire": ItemData("Recipe", 1338232, type=ItemClassification.useful),
        "Recipe: Copper Sheet": ItemData("Recipe", 1338233, type=ItemClassification.useful),
        "Recipe: Steamed Copper Sheet": ItemData("Recipe", 1338234, type=ItemClassification.useful),
        "Recipe: Steel Pipe": ItemData("Recipe", 1338235, type=ItemClassification.useful),
        "Recipe: Steel Beam": ItemData("Recipe", 1338236, type=ItemClassification.useful),
        "Recipe: Crude Oil": ItemData("Recipe", 1338237, type=ItemClassification.useful),
        "Recipe: Heavy Oil Residue": ItemData("Recipe", 1338238, type=ItemClassification.useful),
        "Recipe: Polymer Resin": ItemData("Recipe", 1338239, type=ItemClassification.useful),
        "Recipe: Fuel": ItemData("Recipe", 1338240, type=ItemClassification.useful),
        "Recipe: Residual Fuel": ItemData("Recipe", 1338241, type=ItemClassification.useful),
        "Recipe: Diluted Fuel (refinery)": ItemData("Recipe", 1338242, type=ItemClassification.useful),
        "Recipe: Water": ItemData("Recipe", 1338243, type=ItemClassification.useful),
        "Recipe: Concrete": ItemData("Recipe", 1338244, type=ItemClassification.useful),
        "Recipe: Rubber Concrete": ItemData("Recipe", 1338245, type=ItemClassification.useful),
        "Recipe: Wet Concrete": ItemData("Recipe", 1338246, type=ItemClassification.useful),
        "Recipe: Fine Concrete": ItemData("Recipe", 1338247, type=ItemClassification.useful),
        "Recipe: Silica": ItemData("Recipe", 1338248, type=ItemClassification.useful),
        "Recipe: Cheap Silica": ItemData("Recipe", 1338249, type=ItemClassification.useful),
        "Recipe: Quartz Crystal": ItemData("Recipe", 1338250, type=ItemClassification.useful),
        "Recipe: Pure Quartz Crystal": ItemData("Recipe", 1338251, type=ItemClassification.useful),
        "Recipe: Iron Ingot": ItemData("Recipe", 1338252, type=ItemClassification.useful),
        "Recipe: Pure Iron Ingot": ItemData("Recipe", 1338253, type=ItemClassification.useful),
        "Recipe: Iron Alloy Ingot": ItemData("Recipe", 1338254, type=ItemClassification.useful),
        "Recipe: Steel Ingot": ItemData("Recipe", 1338255, type=ItemClassification.useful),
        "Recipe: Coke Steel Ingot": ItemData("Recipe", 1338256, type=ItemClassification.useful),
        "Recipe: Compacted Steel Ingot": ItemData("Recipe", 1338257, type=ItemClassification.useful),
        "Recipe: Solid Steel Ingot": ItemData("Recipe", 1338258, type=ItemClassification.useful),
        "Recipe: Copper Ingot": ItemData("Recipe", 1338259, type=ItemClassification.useful),
        "Recipe: Copper Alloy Ingot": ItemData("Recipe", 1338260, type=ItemClassification.useful),
        "Recipe: Pure Copper Ingot": ItemData("Recipe", 1338261, type=ItemClassification.useful),
        "Recipe: Caterium Ingot": ItemData("Recipe", 1338262, type=ItemClassification.useful),
        "Recipe: Pure Caterium Ingot": ItemData("Recipe", 1338263, type=ItemClassification.useful),
        "Recipe: Limestone": ItemData("Recipe", 1338264, type=ItemClassification.useful),
        "Recipe: Raw Quartz": ItemData("Recipe", 1338265, type=ItemClassification.useful),
        "Recipe: Iron Ore": ItemData("Recipe", 1338266, type=ItemClassification.useful),
        "Recipe: Copper Ore": ItemData("Recipe", 1338267, type=ItemClassification.useful),
        "Recipe: Coal": ItemData("Recipe", 1338268, type=ItemClassification.useful),
        "Recipe: Sulfur": ItemData("Recipe", 1338269, type=ItemClassification.useful),
        "Recipe: Caterium Ore": ItemData("Recipe", 1338270, type=ItemClassification.useful),
        "Recipe: Petroleum Coke": ItemData("Recipe", 1338271, type=ItemClassification.useful),
        "Recipe: Compacted Coal": ItemData("Recipe", 1338272, type=ItemClassification.useful),
        "Recipe: Motor": ItemData("Recipe", 1338273, type=ItemClassification.useful),
        "Recipe: Rigour Motor": ItemData("Recipe", 1338274, type=ItemClassification.useful),
        "Recipe: Electric Motor": ItemData("Recipe", 1338275, type=ItemClassification.useful),
        "Recipe: Modular Frame": ItemData("Recipe", 1338276, type=ItemClassification.useful),
        "Recipe: Bolted Frame": ItemData("Recipe", 1338277, type=ItemClassification.useful),
        "Recipe: Steeled Frame": ItemData("Recipe", 1338278, type=ItemClassification.useful),
        "Recipe: Heavy Modular Frame": ItemData("Recipe", 1338279, type=ItemClassification.useful),
        "Recipe: Heavy Flexible Frame": ItemData("Recipe", 1338280, type=ItemClassification.useful),
        "Recipe: Heavy Encased Frame": ItemData("Recipe", 1338281, type=ItemClassification.useful),
        "Recipe: Encased Industrial Beam": ItemData("Recipe", 1338282, type=ItemClassification.useful),
        "Recipe: Encased Industrial Pipe": ItemData("Recipe", 1338283, type=ItemClassification.useful),
        "Recipe: Computer": ItemData("Recipe", 1338284, type=ItemClassification.useful),
        "Recipe: Crystal Computer": ItemData("Recipe", 1338285, type=ItemClassification.useful),
        "Recipe: Caterium Computer": ItemData("Recipe", 1338286, type=ItemClassification.useful),
        "Recipe: Circuit Board": ItemData("Recipe", 1338287, type=ItemClassification.useful),
        "Recipe: Electrode Circuit Board": ItemData("Recipe", 1338288, type=ItemClassification.useful),
        "Recipe: Silicon Circuit Board": ItemData("Recipe", 1338289, type=ItemClassification.useful),
        "Recipe: Caterium Circuit Board": ItemData("Recipe", 1338290, type=ItemClassification.useful),
        "Recipe: Crystal Oscillator": ItemData("Recipe", 1338291, type=ItemClassification.useful),
        "Recipe: Insulated Crystal Oscillator": ItemData("Recipe", 1338292, type=ItemClassification.useful),
        "Recipe: AI Limiter": ItemData("Recipe", 1338293, type=ItemClassification.useful),
        "Recipe: Electromagnetic Control Rod": ItemData("Recipe", 1338294, type=ItemClassification.useful),
        "Recipe: Electromagnetic Connection Rod": ItemData("Recipe", 1338295, type=ItemClassification.useful),
        "Recipe: High-Speed Connector": ItemData("Recipe", 1338296, type=ItemClassification.useful),
        "Recipe: Silicon High-Speed Connector": ItemData("Recipe", 1338297, type=ItemClassification.useful),
        "Recipe: Smart Plating": ItemData("Recipe", 1338298, type=ItemClassification.useful),
        "Recipe: Plastic Smart Plating": ItemData("Recipe", 1338299, type=ItemClassification.useful),
        "Recipe: Versatile Framework": ItemData("Recipe", 1338300, type=ItemClassification.useful),
        "Recipe: Flexible Framework": ItemData("Recipe", 1338301, type=ItemClassification.useful),
        "Recipe: Automated Wiring": ItemData("Recipe", 1338302, type=ItemClassification.useful),
        "Recipe: Automated Speed Wiring": ItemData("Recipe", 1338303, type=ItemClassification.useful),
        "Recipe: Modular Engine": ItemData("Recipe", 1338304, type=ItemClassification.useful),
        "Recipe: Adaptive Control Unit": ItemData("Recipe", 1338305, type=ItemClassification.useful),
        "Recipe: Diluted Fuel (blender)": ItemData("Recipe", 1338306, type=ItemClassification.useful),
        "Recipe: Alumina Solution": ItemData("Recipe", 1338307, type=ItemClassification.useful),
        "Recipe: Automated Miner": ItemData("Recipe", 1338308, type=ItemClassification.useful),

        #1338312 - 1338399 Reserved for future recipes

        #1338400 - 1338899 buildings / others
        "Building: Constructor": ItemData("Building", 1338400, type=ItemClassification.progression),
        "Building: Assembler": ItemData("Building", 1338401, type=ItemClassification.progression),
        "Building: Manufacturer": ItemData("Building", 1338402, type=ItemClassification.progression),
        "Building: Packager": ItemData("Building", 1338403, type=ItemClassification.progression),
        "Building: Refinery": ItemData("Building", 1338404, type=ItemClassification.progression),
        "Building: Blender": ItemData("Building", 1338405, type=ItemClassification.progression),
        #"Building: Particle Accelerator": ItemData("Building", 1338406, type=ItemClassification.progression),
        "Building: Biomass Burner": ItemData("Building", 1338407, type=ItemClassification.progression),
        "Building: Coal Generator": ItemData("Building", 1338408, type=ItemClassification.progression),
        #"Building: Geothermal_Generator": ItemData("Building", 1338409, type=ItemClassification.progression),
        #"Building: Nuclear Power Plant": ItemData("Building", 1338410, type=ItemClassification.progression),
        "Building: Miner Mk.1": ItemData("Building", 1338411, type=ItemClassification.progression),
        #"Building: Miner Mk.2": ItemData("Building", 1338412, type=ItemClassification.progression),
        #"Building: Miner Mk.3": ItemData("Building", 1338413, type=ItemClassification.progression),
        "Building: Oil Extractor": ItemData("Building", 1338414, type=ItemClassification.progression),
        "Building: Water Extractor": ItemData("Building", 1338415, type=ItemClassification.progression),
        "Building: Smelter": ItemData("Building", 1338416, type=ItemClassification.progression),
        "Building: Foundry": ItemData("Building", 1338417, type=ItemClassification.progression),
        "Building: Space Elevator": ItemData("Building", 1338999, type=ItemClassification.progression),

        #1338900 - 1338998 Handled by trap system
        # Regenerate via /Script/Blutility.EditorUtilityWidgetBlueprint'/Archipelago/Debug/EU_GenerateTrapIds.EU_GenerateTrapIds'
        "Doggo with PowerSlug": ItemData("Parts", 1338909),

        "Hog Basic": ItemData("Trap", 1338900, type=ItemClassification.trap),
        "Hog Alpha": ItemData("Trap", 1338901, type=ItemClassification.trap),
        "Hog Johnny": ItemData("Trap", 1338902, type=ItemClassification.trap),
        "Hog Cliff": ItemData("Trap", 1338903, type=ItemClassification.trap),
        "Hog Cliff Nuclear": ItemData("Trap", 1338904, type=ItemClassification.trap),
        "Not The Bees": ItemData("Trap", 1338905, type=ItemClassification.trap),
        "Hatcher": ItemData("Trap", 1338906, type=ItemClassification.trap),
        "Doggo Pulse Nobelisk": ItemData("Trap", 1338907, type=ItemClassification.trap),
        "Doggo Nuke Nobelisk": ItemData("Trap", 1338908, type=ItemClassification.trap),
        "Doggo Gas Nobelisk": ItemData("Trap", 1338910, type=ItemClassification.trap),
        "Spore Flower": ItemData("Trap", 1338911, type=ItemClassification.trap),
        "Stinger Gas": ItemData("Trap", 1338912, type=ItemClassification.trap),
        "Stinger Elite": ItemData("Trap", 1338913, type=ItemClassification.trap),
        "Stinger Small": ItemData("Trap", 1338914, type=ItemClassification.trap),
        "Spitter Forest": ItemData("Trap", 1338915, type=ItemClassification.trap),
        "Spitter Forest Alpha": ItemData("Trap", 1338916, type=ItemClassification.trap),
        "Nuclear Waste (ground)": ItemData("Trap", 1338917, type=ItemClassification.trap),
        "Plutonium Waste (ground)": ItemData("Trap", 1338918, type=ItemClassification.trap)
    }

    item_names_and_ids: ClassVar[Dict[str, int]] = {name: item_data.code for name, item_data in item_data.items()}

    @classmethod
    def get_item_names_per_category(cls) -> Dict[str, Set[str]]:
        categories: Dict[str, Set[str]] = {}

        for name, data in cls.item_data.items():
            categories.setdefault(data.category, set()).add(name)

        return categories


    player: int
    multiworld: MultiWorld
    logic: GameLogic
    random: Random
    selected_recipes: Optional[Dict[str, Recipe]]
    handcraftable_recipes: Set[str]
    filler_items: Tuple[str]

    def __init__(self, multiworld: Optional[MultiWorld], player: Optional[int], logic: GameLogic, random: Random):
        self.player = player
        self.multiworld = multiworld
        self.logic = logic
        self.random = random

        if multiworld is not None and random is not None and False:
            self.selected_recipes = self.select_progression_recipes() 
        else:
            self.selected_recipes = None

        self.handcraftable_recipes = frozenset(recipe.name 
                                                for recipes_per_part in logic.recipes.values()
                                                for recipe in recipes_per_part 
                                                if recipe.handcraftable)
        
        self.filler_items = tuple(item 
                                  for item, details in self.item_data.items() 
                                  if details.category in {"Parts", "Ammo"})


    def select_recipe_for_part_that_does_not_depend_on_parent_recipes(self,
            part: str, parts_to_avoid: Dict[str, str]) -> Recipe:
        
        recipes: List[Recipe] = list(self.logic.recipes[part])

        while (len(recipes) > 0):
            recipe: Recipe = recipes.pop(self.random.randrange(len(recipes)))

            if recipe.inputs and any(input in parts_to_avoid for input in recipe.inputs):
                continue

            return recipe
        
        raise Exception(f"No recipe available for {part}")


    def build_progression_recipe_tree(self, parts: tuple[str, ...], selected_recipes: Dict[str, str]):
        for part in parts:
            recipe: Recipe = \
                self.select_recipe_for_part_that_does_not_depend_on_parent_recipes(part, selected_recipes)

            selected_recipes[part] = recipe.name

            child_recipes: Dict[str, Recipe] = {}
            if (recipe.inputs):
                for input in recipe.inputs:
                    child_recipes[input] = \
                        self.select_recipe_for_part_that_does_not_depend_on_parent_recipes(input, selected_recipes)
            
            for part, child_recipe in child_recipes.items():
                selected_recipes[part] = child_recipe.name

            for child_recipe in child_recipes.values():
                if child_recipe.inputs:
                    self.build_progression_recipe_tree(child_recipe.inputs, selected_recipes)


    def select_progression_recipes(self) -> Dict[str, str]:
        required_top_level_parts: Tuple[str, ...] = ("Versatile Framework", "Modular Engine", "Adaptive Control Unit")
        selected_recipes: Dict[str, str] = {}

        self.build_progression_recipe_tree(required_top_level_parts, selected_recipes)

        return selected_recipes


    def create_item(self, name: str) -> Item:
        data: ItemData = self.item_data[name]

        if self.selected_recipes and name in self.selected_recipes:
            return Item(name, ItemClassification.progression, data.code, self.player)
        if name in self.handcraftable_recipes:
            return Item(name, ItemClassification.progression, data.code, self.player)
        if not self.selected_recipes and data.category == "Recipe":
            return Item(name, ItemClassification.progression, data.code, self.player)
        else:
            return Item(name, data.type, data.code, self.player)


    def get_filler_item_name(self, random: Random) -> str:
        trap_chance: int = get_option_value(self.multiworld, self.player, "TrapChance")
        enabled_traps: List[str] = get_option_value(self.multiworld, self.player, "Traps")

        if enabled_traps and random.random() < (trap_chance / 100):
            return random.choice(enabled_traps)
        else:
            return random.choice(self.filler_items) 


    def build_item_pool(self, random: Random, excluded_items: Set[str], size: int) -> List[Item]:
        pool: List[Item] = []

        for name, data in self.item_data.items():
            if name not in excluded_items and data.category in { "Recipe", "Building" }:
                item = self.create_item(name)
                pool.append(item)

        # enquipment items that unlock logical progression
        for name in { "Gas Mask", "Hazmat Suit", "Jetpack", "Hover Pack", "Nobelisk Detonator" }:
            item = self.create_item(name)
            pool.append(item)

        for _ in range(size - len(pool)):
            item = self.create_item(self.get_filler_item_name(random))
            pool.append(item)

        return pool


    def write_progression_chain(self, multiworld: MultiWorld, spoiler_handle: TextIO):
        if self.selected_recipes:
            player_name = f'{multiworld.get_player_name(self.player)}: ' if multiworld.players > 1 else ''
            spoiler_handle.write('\n\nSelected Satisfactory Recipes:\n\n')
            spoiler_handle.write('\n'.join(
                f"{player_name}{part} -> {recipe.name}" 
                for part, recipes_per_part in self.logic.recipes.items()
                for recipe in recipes_per_part 
                if recipe.name in self.selected_recipes
            ))
