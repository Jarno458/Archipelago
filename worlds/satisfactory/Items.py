from random import Random
from typing import ClassVar, Dict, Set, List, TextIO, Tuple, Optional
from BaseClasses import Item, ItemClassification as C, MultiWorld
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions
from .ItemData import ItemData, ItemGroups as G

class Items:
    item_data: ClassVar[Dict[str, ItemData]] = {
        # Parts
        "Adaptive Control Unit": ItemData((G.Parts, ), 1338000),
        "AI Limiter": ItemData((G.Parts, ), 1338001),
        "Alclad Aluminum Sheet": ItemData((G.Parts, ), 1338002),
        "Blue Power Slug": ItemData((G.Parts, ), 1338003),
        "Yellow Power Slug": ItemData((G.Parts, ), 1338004),
        "Alien Protein": ItemData((G.Parts, ), 1338005),
        "Purple Power Slug": ItemData((G.Parts, ), 1338006),
        "Aluminum Casing": ItemData((G.Parts, ), 1338007),
        "Aluminum Ingot": ItemData((G.Parts, ), 1338008),
        "Aluminum Scrap": ItemData((G.Parts, ), 1338009),
        "Assembly Director System": ItemData((G.Parts, ), 1338010),
        "Automated Wiring": ItemData((G.Parts, ), 1338011),
        "Battery": ItemData((G.Parts, ), 1338012),
        "Bauxite": ItemData((G.Parts, ), 1338013),
        "Beacon": ItemData((G.Parts, ), 1338014),
        "Biomass": ItemData((G.Parts, ), 1338015),
        "Black Powder": ItemData((G.Parts, ), 1338016),
        "Cable": ItemData((G.Parts, ), 1338017),
        "Caterium Ingot": ItemData((G.Parts, ), 1338018),
        "Caterium Ore": ItemData((G.Parts, ), 1338019),
        "Circuit Board": ItemData((G.Parts, ), 1338020),
        "Coal": ItemData((G.Parts, ), 1338021),
        "Color Cartridge": ItemData((G.Parts, ), 1338022),
        "Compacted Coal": ItemData((G.Parts, ), 1338023),
        "Computer": ItemData((G.Parts, ), 1338024),
        "Concrete": ItemData((G.Parts, ), 1338025),
        "Cooling System": ItemData((G.Parts, ), 1338026),
        "Copper Ingot": ItemData((G.Parts, ), 1338027),
        "Copper Ore": ItemData((G.Parts, ), 1338028),
        "Copper Powder": ItemData((G.Parts, ), 1338029),
        "Copper Sheet": ItemData((G.Parts, ), 1338030),
        "Adequate Pioneering Statue": ItemData((G.Parts, ), 1338031),
        "Crystal Oscillator": ItemData((G.Parts, ), 1338032),
        "Electromagnetic Control Rod": ItemData((G.Parts, ), 1338033),
        "Empty Canister": ItemData((G.Parts, ), 1338034),
        "Empty Fluid Tank": ItemData((G.Parts, ), 1338035),
        "Encased Industrial Beam": ItemData((G.Parts, ), 1338036),
        "Encased Plutonium Cell": ItemData((G.Parts, ), 1338037, C.trap),
        "Encased Uranium Cell": ItemData((G.Parts, ), 1338038, C.trap),
        "Fabric": ItemData((G.Parts, ), 1338039),
        "FICST Coupon": ItemData((G.Parts, ), 1338040),
        "Flower Petals": ItemData((G.Parts, ), 1338041),
        "Fused Modular Frame": ItemData((G.Parts, ), 1338042),
        "Hard Drive": ItemData((G.Parts, ), 1338043),
        "Heat Sink": ItemData((G.Parts, ), 1338044),
        "Heavy Modular Frame": ItemData((G.Parts, ), 1338045),
        "High-Speed Connector": ItemData((G.Parts, ), 1338046),
        "Satisfactory Pioneering Statue": ItemData((G.Parts, ), 1338047), 
        "Pretty Good Pioneering Statue": ItemData((G.Parts, ), 1338048),
        "Iron Ingot": ItemData((G.Parts, ), 1338049),
        "Iron Ore": ItemData((G.Parts, ), 1338050),
        "Iron Plate": ItemData((G.Parts, ), 1338051),
        "Iron Rod": ItemData((G.Parts, ), 1338052),
        "Golden Nut Statue": ItemData((G.Parts, ), 1338053),
        "Leaves": ItemData((G.Parts, ), 1338054),
        "Limestone": ItemData((G.Parts, ), 1338055),
        "Magnetic Field Generator": ItemData((G.Parts, ), 1338056),
        "Mercer Sphere": ItemData((G.Parts, ), 1338057),
        "Modular Engine": ItemData((G.Parts, ), 1338058),
        "Modular Frame": ItemData((G.Parts, ), 1338059),
        "Motor": ItemData((G.Parts, ), 1338060),
        "Mycelia": ItemData((G.Parts, ), 1338061),
        "Non-fissile Uranium": ItemData((G.Trap, ), 1338062, C.trap),
        "Nuclear Pasta": ItemData((G.Parts, ), 1338063),
        "Lizard Doggo Statue": ItemData((G.Parts, ), 1338064),
        "Organic Data Capsule": ItemData((G.Parts, ), 1338065),
        "Packaged Alumina Solution": ItemData((G.Parts, ), 1338066),
        "Packaged Fuel": ItemData((G.Parts, ), 1338067),
        "Packaged Heavy Oil Residue": ItemData((G.Parts, ), 1338068),
        "Packaged Liquid Biofuel": ItemData((G.Parts, ), 1338069),
        "Packaged Nitric Acid": ItemData((G.Parts, ), 1338070),
        "Packaged Nitrogen Gas": ItemData((G.Parts, ), 1338071),
        "Packaged Oil": ItemData((G.Parts, ), 1338072),
        "Packaged Sulfuric Acid": ItemData((G.Parts, ), 1338073),
        "Packaged Turbofuel": ItemData((G.Parts, ), 1338074),
        "Packaged Water": ItemData((G.Parts, ), 1338075),
        "Petroleum Coke": ItemData((G.Parts, ), 1338076),
        "Plastic": ItemData((G.Parts, ), 1338077),
        "Plutonium Fuel Rod": ItemData((G.Trap, ), 1338078, C.trap),
        "Plutonium Pellet": ItemData((G.Trap, ), 1338079, C.trap),
        "Plutonium Waste (item)": ItemData((G.Trap, ), 1338080, C.trap),
        "Polymer Resin": ItemData((G.Parts, ), 1338081),
        "Power Shard": ItemData((G.Parts, ), 1338082),
        "Confusing Creature Statue": ItemData((G.Parts, ), 1338083),
        "Pressure Conversion Cube": ItemData((G.Parts, ), 1338084),
        "Quantum Computer": ItemData((G.Parts, ), 1338085),
        "Quartz Crystal": ItemData((G.Parts, ), 1338086),
        "Quickwire": ItemData((G.Parts, ), 1338087),
        "Radio Control Unit": ItemData((G.Parts, ), 1338088),
        "Raw Quartz": ItemData((G.Parts, ), 1338089),
        "Reinforced Iron Plate": ItemData((G.Parts, ), 1338090),
        "Rotor": ItemData((G.Parts, ), 1338091),
        "Rubber": ItemData((G.Parts, ), 1338092),
        "SAM Ore": ItemData((G.Parts, ), 1338093),
        "Screw": ItemData((G.Parts, ), 1338094),
        "Silica": ItemData((G.Parts, ), 1338095),
        "Smart Plating": ItemData((G.Parts, ), 1338096),
        "Smokeless Powder": ItemData((G.Parts, ), 1338097),
        "Solid Biofuel": ItemData((G.Parts, ), 1338098),
        "Somersloop": ItemData((G.Parts, ), 1338099),
        "Stator": ItemData((G.Parts, ), 1338100),
        "Silver Hog Statue": ItemData((G.Parts, ), 1338101),
        "Steel Beam": ItemData((G.Parts, ), 1338102),
        "Steel Ingot": ItemData((G.Parts, ), 1338103),
        "Steel Pipe": ItemData((G.Parts, ), 1338104),
        "Sulfur": ItemData((G.Parts, ), 1338105),
        "Supercomputer": ItemData((G.Parts, ), 1338106),
        "Superposition Oscillator": ItemData((G.Parts, ), 1338107),
        "Thermal Propulsion Rocket": ItemData((G.Parts, ), 1338108),
        "Turbo Motor": ItemData((G.Parts, ), 1338109),
        "Hog Remains": ItemData((G.Parts, ), 1338110),
        "Uranium": ItemData((G.Trap, ), 1338111, C.trap),
        "Uranium Fuel Rod": ItemData((G.Trap, ), 1338112, C.trap),
        "Uranium Waste (item)": ItemData((G.Trap, ), 1338113, C.trap),
        "Versatile Framework": ItemData((G.Parts, ), 1338114),
        "Wire": ItemData((G.Parts, ), 1338115),
        "Wood": ItemData((G.Parts, ), 1338116),
        "Plasma Spitter Remains": ItemData((G.Parts, ), 1338117),
        "Stinger Remains": ItemData((G.Parts, ), 1338118),
        "Hatcher Remains": ItemData((G.Parts, ), 1338119),
        "Alien DNA Capsule": ItemData((G.Parts, ), 1338120),
        #1338121 - 1338149 Reserved for future parts

        # Equipment / Ammo
        "Bacon Agaric": ItemData((G.Ammo, ), 1338150),
        "Beryl Nut": ItemData((G.Ammo, ), 1338151),
        "Blade Runners": ItemData((G.Equipment, ), 1338152),
        "Boom Box": ItemData((G.Equipment, ), 1338153),
        "Chainsaw": ItemData((G.Equipment, ), 1338154),
        "Cluster Nobelisk": ItemData((G.Ammo, ), 1338155),
        #"Color Gun": ItemData((G.Equipment, ), 1338156), Removed in U8
        "Cup": ItemData((G.Equipment, ), 1338157),
        "Cup (gold)": ItemData((G.Equipment, ), 1338158, count=0),
        "Explosive Rebar": ItemData((G.Ammo, ), 1338159),
        "Factory Cart": ItemData((G.Equipment, ), 1338160),
        "Factory Cart (golden)": ItemData((G.Equipment, ), 1338161, count=0),
        "Gas Mask": ItemData((G.Equipment, ), 1338162, C.progression),
        "Gas Nobelisk": ItemData((G.Ammo, ), 1338163),
        "Hazmat Suit": ItemData((G.Equipment, ), 1338164, C.progression),
        "Homing Rifle Ammo": ItemData((G.Ammo, ), 1338165),
        "Hover Pack": ItemData((G.Equipment, ), 1338166, C.progression),
        "Iron Rebar": ItemData((G.Ammo, ), 1338167),
        "Jetpack": ItemData((G.Equipment, ), 1338168, C.progression),
        "Medicinal Inhaler": ItemData((G.Ammo, ), 1338169),
        "Nobelisk": ItemData((G.Ammo, ), 1338170),
        "Nobelisk Detonator": ItemData((G.Equipment, ), 1338171, C.progression),
        "Nuke Nobelisk": ItemData((G.Ammo, ), 1338172),
        "Object Scanner": ItemData((G.Equipment, ), 1338173),
        "Paleberry": ItemData((G.Ammo, ), 1338174),
        "Parachute": ItemData((G.Equipment, ), 1338175),
        "Pulse Nobelisk": ItemData((G.Ammo, ), 1338176),
        "Rebar Gun": ItemData((G.Equipment, ), 1338177),
        "Rifle": ItemData((G.Equipment, ), 1338178),
        "Rifle Ammo": ItemData((G.Ammo, ), 1338179),
        "Shatter Rebar": ItemData((G.Ammo, ), 1338180),
        "Stun Rebar": ItemData((G.Ammo, ), 1338181),
        "Turbo Rifle Ammo": ItemData((G.Ammo, ), 1338182),
        "Xeno-Basher": ItemData((G.Equipment, ), 1338183),
        "Xeno-Zapper": ItemData((G.Equipment, ), 1338184),
        "Zipline": ItemData((G.Equipment, ), 1338185),
        "Portable Miner": ItemData((G.Equipment, ), 1338186),
        "Gas Filter": ItemData((G.Ammo, ), 1338187, C.progression),
        "Small inflated Pocket Dimension": ItemData((G.Upgrades, ), 1338188, C.useful, 11),
        "Inflated Pocket Dimension": ItemData((G.Upgrades, ), 1338189, C.useful, 5),
        "Expanded Toolbelt": ItemData((G.Upgrades, ), 1338190, C.useful, 5),

        #1338188 - 1338199 Reserved for future equipment/ammo

        #1338200+ Recipes / buildings / schematics / others
        "Recipe: Reinforced Iron Plate": ItemData((G.Recipe, ), 1338200, C.progression),
        "Recipe: Adhered Iron Plate": ItemData((G.Recipe, ), 1338201, C.progression),
        "Recipe: Bolted Iron Plate": ItemData((G.Recipe, ), 1338202, C.progression),
        "Recipe: Stitched Iron Plate": ItemData((G.Recipe, ), 1338203, C.progression),
        "Recipe: Rotor": ItemData((G.Recipe, ), 1338204, C.progression),
        "Recipe: Copper Rotor": ItemData((G.Recipe, ), 1338205, C.progression),
        "Recipe: Steel Rotor": ItemData((G.Recipe, ), 1338206, C.progression),
        "Recipe: Stator": ItemData((G.Recipe, ), 1338207, C.progression),
        "Recipe: Quickwire Stator": ItemData((G.Recipe, ), 1338208, C.progression),
        "Recipe: Plastic": ItemData((G.Recipe, ), 1338209, C.progression),
        "Recipe: Residual Plastic": ItemData((G.Recipe, ), 1338210, C.progression),
        "Recipe: Recycled Plastic": ItemData((G.Recipe, ), 1338211, C.progression),
        "Recipe: Rubber": ItemData((G.Recipe, ), 1338212, C.progression),
        "Recipe: Residual Rubber": ItemData((G.Recipe, ), 1338213, C.progression),
        "Recipe: Recycled Rubber": ItemData((G.Recipe, ), 1338214, C.progression),
        "Recipe: Iron Plate": ItemData((G.Recipe, ), 1338215, C.progression),
        "Recipe: Coated Iron Plate": ItemData((G.Recipe, ), 1338216, C.progression),
        "Recipe: Steel Coated Plate": ItemData((G.Recipe, ), 1338217, C.progression),
        "Recipe: Iron Rod": ItemData((G.Recipe, ), 1338218, C.progression),
        "Recipe: Steel Rod": ItemData((G.Recipe, ), 1338219, C.progression),
        "Recipe: Screw": ItemData((G.Recipe, ), 1338220, C.progression),
        "Recipe: Cast Screw": ItemData((G.Recipe, ), 1338221, C.progression),
        "Recipe: Steel Screw": ItemData((G.Recipe, ), 1338222, C.progression),
        "Recipe: Wire": ItemData((G.Recipe, ), 1338223, C.progression),
        "Recipe: Fused Wire": ItemData((G.Recipe, ), 1338224, C.progression),
        "Recipe: Iron Wire": ItemData((G.Recipe, ), 1338225, C.progression),
        "Recipe: Caterium Wire": ItemData((G.Recipe, ), 1338226, C.progression),
        "Recipe: Cable": ItemData((G.Recipe, ), 1338227, C.progression),
        "Recipe: Coated Cable": ItemData((G.Recipe, ), 1338228, C.progression),
        "Recipe: Insulated Cable": ItemData((G.Recipe, ), 1338229, C.progression),
        "Recipe: Quickwire Cable": ItemData((G.Recipe, ), 1338230, C.progression),
        "Recipe: Quickwire": ItemData((G.Recipe, ), 1338231, C.progression),
        "Recipe: Fused Quickwire": ItemData((G.Recipe, ), 1338232, C.progression),
        "Recipe: Copper Sheet": ItemData((G.Recipe, ), 1338233, C.progression),
        "Recipe: Steamed Copper Sheet": ItemData((G.Recipe, ), 1338234, C.progression),
        "Recipe: Steel Pipe": ItemData((G.Recipe, ), 1338235, C.progression),
        "Recipe: Steel Beam": ItemData((G.Recipe, ), 1338236, C.progression),
        #"Recipe: Crude Oil": ItemData((G.Recipe, ), 1338237),
        "Recipe: Heavy Oil Residue": ItemData((G.Recipe, ), 1338238, C.progression),
        "Recipe: Polymer Resin": ItemData((G.Recipe, ), 1338239, C.progression),
        "Recipe: Fuel": ItemData((G.Recipe, ), 1338240, C.progression),
        "Recipe: Residual Fuel": ItemData((G.Recipe, ), 1338241, C.progression),
        "Recipe: Diluted Fuel (refinery)": ItemData((G.Recipe, ), 1338242, C.progression),
        #"Recipe: Water": ItemData((G.Recipe, ), 1338243),
        "Recipe: Concrete": ItemData((G.Recipe, ), 1338244, C.progression),
        "Recipe: Rubber Concrete": ItemData((G.Recipe, ), 1338245, C.progression),
        "Recipe: Wet Concrete": ItemData((G.Recipe, ), 1338246, C.progression),
        "Recipe: Fine Concrete": ItemData((G.Recipe, ), 1338247, C.progression),
        "Recipe: Silica": ItemData((G.Recipe, ), 1338248, C.progression),
        "Recipe: Cheap Silica": ItemData((G.Recipe, ), 1338249, C.progression),
        "Recipe: Quartz Crystal": ItemData((G.Recipe, ), 1338250, C.progression),
        "Recipe: Pure Quartz Crystal": ItemData((G.Recipe, ), 1338251, C.progression),
        "Recipe: Iron Ingot": ItemData((G.Recipe, ), 1338252, C.progression),
        "Recipe: Pure Iron Ingot": ItemData((G.Recipe, ), 1338253, C.progression),
        "Recipe: Iron Alloy Ingot": ItemData((G.Recipe, ), 1338254, C.progression),
        "Recipe: Steel Ingot": ItemData((G.Recipe, ), 1338255, C.progression),
        "Recipe: Coke Steel Ingot": ItemData((G.Recipe, ), 1338256, C.progression),
        "Recipe: Compacted Steel Ingot": ItemData((G.Recipe, ), 1338257, C.progression),
        "Recipe: Solid Steel Ingot": ItemData((G.Recipe, ), 1338258, C.progression),
        "Recipe: Copper Ingot": ItemData((G.Recipe, ), 1338259, C.progression),
        "Recipe: Copper Alloy Ingot": ItemData((G.Recipe, ), 1338260, C.progression),
        "Recipe: Pure Copper Ingot": ItemData((G.Recipe, ), 1338261, C.progression),
        "Recipe: Caterium Ingot": ItemData((G.Recipe, ), 1338262, C.progression),
        "Recipe: Pure Caterium Ingot": ItemData((G.Recipe, ), 1338263, C.progression),
        #"Recipe: Limestone": ItemData((G.Recipe, ), 1338264),
        #"Recipe: Raw Quartz": ItemData((G.Recipe, ), 1338265),
        #"Recipe: Iron Ore": ItemData((G.Recipe, ), 1338266),
        #"Recipe: Copper Ore": ItemData((G.Recipe, ), 1338267),
        #"Recipe: Coal": ItemData((G.Recipe, ), 1338268),
        #"Recipe: Sulfur": ItemData((G.Recipe, ), 1338269),
        #"Recipe: Caterium Ore": ItemData((G.Recipe, ), 1338270, C.progression),
        "Recipe: Petroleum Coke": ItemData((G.Recipe, ), 1338271, C.progression),
        "Recipe: Compacted Coal": ItemData((G.Recipe, ), 1338272, C.progression),
        "Recipe: Motor": ItemData((G.Recipe, ), 1338273, C.progression),
        "Recipe: Rigour Motor": ItemData((G.Recipe, ), 1338274, C.progression),
        "Recipe: Electric Motor": ItemData((G.Recipe, ), 1338275, C.progression),
        "Recipe: Modular Frame": ItemData((G.Recipe, ), 1338276, C.progression),
        "Recipe: Bolted Frame": ItemData((G.Recipe, ), 1338277, C.progression),
        "Recipe: Steeled Frame": ItemData((G.Recipe, ), 1338278, C.progression),
        "Recipe: Heavy Modular Frame": ItemData((G.Recipe, ), 1338279, C.progression),
        "Recipe: Heavy Flexible Frame": ItemData((G.Recipe, ), 1338280, C.progression),
        "Recipe: Heavy Encased Frame": ItemData((G.Recipe, ), 1338281, C.progression),
        "Recipe: Encased Industrial Beam": ItemData((G.Recipe, ), 1338282, C.progression),
        "Recipe: Encased Industrial Pipe": ItemData((G.Recipe, ), 1338283, C.progression),
        "Recipe: Computer": ItemData((G.Recipe, ), 1338284, C.progression),
        "Recipe: Crystal Computer": ItemData((G.Recipe, ), 1338285, C.progression),
        "Recipe: Caterium Computer": ItemData((G.Recipe, ), 1338286, C.progression),
        "Recipe: Circuit Board": ItemData((G.Recipe, ), 1338287, C.progression),
        "Recipe: Electrode Circuit Board": ItemData((G.Recipe, ), 1338288, C.progression),
        "Recipe: Silicon Circuit Board": ItemData((G.Recipe, ), 1338289, C.progression),
        "Recipe: Caterium Circuit Board": ItemData((G.Recipe, ), 1338290, C.progression),
        "Recipe: Crystal Oscillator": ItemData((G.Recipe, ), 1338291, C.progression),
        "Recipe: Insulated Crystal Oscillator": ItemData((G.Recipe, ), 1338292, C.progression),
        "Recipe: AI Limiter": ItemData((G.Recipe, ), 1338293, C.progression),
        "Recipe: Electromagnetic Control Rod": ItemData((G.Recipe, ), 1338294, C.progression),
        "Recipe: Electromagnetic Connection Rod": ItemData((G.Recipe, ), 1338295, C.progression),
        "Recipe: High-Speed Connector": ItemData((G.Recipe, ), 1338296, C.progression),
        "Recipe: Silicon High-Speed Connector": ItemData((G.Recipe, ), 1338297, C.progression),
        "Recipe: Smart Plating": ItemData((G.Recipe, ), 1338298, C.progression),
        "Recipe: Plastic Smart Plating": ItemData((G.Recipe, ), 1338299, C.progression),
        "Recipe: Versatile Framework": ItemData((G.Recipe, ), 1338300, C.progression),
        "Recipe: Flexible Framework": ItemData((G.Recipe, ), 1338301, C.progression),
        "Recipe: Automated Wiring": ItemData((G.Recipe, ), 1338302, C.progression),
        "Recipe: Automated Speed Wiring": ItemData((G.Recipe, ), 1338303, C.progression),
        "Recipe: Modular Engine": ItemData((G.Recipe, ), 1338304, C.progression),
        "Recipe: Adaptive Control Unit": ItemData((G.Recipe, ), 1338305, C.progression),
        "Recipe: Diluted Fuel": ItemData((G.Recipe, ), 1338306, C.progression),
        "Recipe: Alumina Solution": ItemData((G.Recipe, ), 1338307, C.progression),
        "Recipe: Automated Miner": ItemData((G.Recipe, ), 1338308, C.progression),
        #"Recipe: Bauxite": ItemData((G.Recipe, ), 1338309),
        "Recipe: Aluminum Scrap": ItemData((G.Recipe, ), 1338310, C.progression),
        "Recipe: Electrode - Aluminum Scrap": ItemData((G.Recipe, ), 1338311, C.progression),
        "Recipe: Instant Scrap": ItemData((G.Recipe, ), 1338312, C.progression),
        "Recipe: Aluminum Ingot": ItemData((G.Recipe, ), 1338313, C.progression),
        "Recipe: Pure Aluminum Ingot": ItemData((G.Recipe, ), 1338314, C.progression),
        "Recipe: Alclad Aluminum Sheet": ItemData((G.Recipe, ), 1338315, C.progression),
        "Recipe: Aluminum Casing": ItemData((G.Recipe, ), 1338316, C.progression),
        "Recipe: Alclad Casing": ItemData((G.Recipe, ), 1338317, C.progression),
        "Recipe: Heat Sink": ItemData((G.Recipe, ), 1338318, C.progression),
        "Recipe: Heat Exchanger": ItemData((G.Recipe, ), 1338319, C.progression),
        "Recipe: Nitrogen Gas": ItemData((G.Recipe, ), 1338320, C.progression),
        "Recipe: Nitric Acid": ItemData((G.Recipe, ), 1338321, C.progression),
        "Recipe: Fused Modular Frame": ItemData((G.Recipe, ), 1338322, C.progression),
        "Recipe: Heat-Fused Frame": ItemData((G.Recipe, ), 1338323, C.progression),
        "Recipe: Radio Control Unit": ItemData((G.Recipe, ), 1338324, C.progression),
        "Recipe: Radio Connection Unit": ItemData((G.Recipe, ), 1338325, C.progression),
        "Recipe: Radio Control System": ItemData((G.Recipe, ), 1338326, C.progression),
        "Recipe: Pressure Conversion Cube": ItemData((G.Recipe, ), 1338327, C.progression),
        "Recipe: Cooling System": ItemData((G.Recipe, ), 1338328, C.progression),
        "Recipe: Cooling Device": ItemData((G.Recipe, ), 1338329, C.progression),
        "Recipe: Turbo Motor": ItemData((G.Recipe, ), 1338330, C.progression),
        "Recipe: Turbo Electric Motor": ItemData((G.Recipe, ), 1338331, C.progression),
        "Recipe: Turbo Pressure Motor": ItemData((G.Recipe, ), 1338332, C.progression),
        "Recipe: Battery": ItemData((G.Recipe, ), 1338333, C.progression),
        "Recipe: Classic Battery": ItemData((G.Recipe, ), 1338334, C.progression),
        "Recipe: Supercomputer": ItemData((G.Recipe, ), 1338335, C.progression),
        "Recipe: OC Supercomputer": ItemData((G.Recipe, ), 1338336, C.progression),
        "Recipe: Super-State Computer": ItemData((G.Recipe, ), 1338337, C.progression),
        #"Recipe: Uranium": ItemData((G.Recipe, ), 1338338), 
        "Recipe: Sulfuric Acid": ItemData((G.Recipe, ), 1338339, C.progression),
        #"Recipe: Encased Uranium Cell": duplicated, 
        "Recipe: Encased Uranium Cell": ItemData((G.Recipe, ), 1338341, C.progression),
        "Recipe: Infused Uranium Cell": ItemData((G.Recipe, ), 1338342, C.progression),
        "Recipe: Uranium Fuel Rod": ItemData((G.Recipe, ), 1338343, C.progression),
        "Recipe: Uranium Fuel Unit": ItemData((G.Recipe, ), 1338344, C.progression),
        "Recipe: Beacon": ItemData((G.Recipe, ), 1338345, C.progression),
        "Recipe: Crystal Beacon": ItemData((G.Recipe, ), 1338346, C.progression),
        #"Recipe: Uranium Waste": ItemData((G.Recipe, ), 1338347, C.progression),
        "Recipe: Non-fissile Uranium": ItemData((G.Recipe, ), 1338348, C.progression),
        "Recipe: Fertile Uranium": ItemData((G.Recipe, ), 1338349, C.progression),
        "Recipe: Plutonium Pellet": ItemData((G.Recipe, ), 1338350, C.progression),
        "Recipe: Encased Plutonium Cell": ItemData((G.Recipe, ), 1338351, C.progression),
        "Recipe: Instant Plutonium Cell": ItemData((G.Recipe, ), 1338352, C.progression),
        "Recipe: Plutonium Fuel Rod": ItemData((G.Recipe, ), 1338353, C.progression),
        "Recipe: Plutonium Fuel Unit": ItemData((G.Recipe, ), 1338354, C.progression),
        "Recipe: Gas Filter": ItemData((G.Recipe, ), 1338355, C.progression),
        "Recipe: Iodine Infused Filter": ItemData((G.Recipe, ), 1338356, C.progression),
        "Recipe: Assembly Director System": ItemData((G.Recipe, ), 1338357, C.progression),
        "Recipe: Magnetic Field Generator": ItemData((G.Recipe, ), 1338358, C.progression),
        "Recipe: Copper Powder": ItemData((G.Recipe, ), 1338359, C.progression),
        "Recipe: Nuclear Pasta": ItemData((G.Recipe, ), 1338360, C.progression),
        "Recipe: Thermal Propulsion Rocket": ItemData((G.Recipe, ), 1338361, C.progression),
        #"Recipe: Leaves": ItemData((G.Recipe, ), 1338362), 
        #"Recipe: Wood": ItemData((G.Recipe, ), 1338363), 
        #"Recipe: Hatcher Remains": ItemData((G.Recipe, ), 1338364), 
        #"Recipe: Hog Remains": ItemData((G.Recipe, ), 1338365), 
        #"Recipe: Plasma Spitter Remains": ItemData((G.Recipe", 1338366),
        "Recipe: Pulse Nobelisk":  ItemData((G.Recipe, ), 1338367, C.useful),
        "Recipe: Hatcher Protein": ItemData((G.Recipe, ), 1338368, C.progression),
        "Recipe: Hog Protein": ItemData((G.Recipe, ), 1338369, C.progression),
        "Recipe: Spitter Protein": ItemData((G.Recipe, ), 1338370, C.progression),
        "Recipe: Stinger Protein": ItemData((G.Recipe, ), 1338371, C.progression),
        "Recipe: Biomass (Leaves)": ItemData((G.Recipe, ), 1338372, C.progression),
        "Recipe: Biomass (Wood)": ItemData((G.Recipe, ), 1338373, C.progression),
        "Recipe: Biomass (Mycelia)": ItemData((G.Recipe, ), 1338374, C.progression),
        "Recipe: Biomass (Alien Protein)": ItemData((G.Recipe, ), 1338375, C.progression),
        "Recipe: Turbo Rifle Ammo (Packaged)": ItemData((G.Recipe, ), 1338376),
        "Recipe: Fabric": ItemData((G.Recipe, ), 1338377, C.progression),
        "Recipe: Polyester Fabric": ItemData((G.Recipe, ), 1338378, C.progression),
        "Recipe: Solid Biofuel": ItemData((G.Recipe, ), 1338379, C.progression),
        "Recipe: Liquid Biofuel": ItemData((G.Recipe, ), 1338380, C.progression),
        "Recipe: Empty Canister": ItemData((G.Recipe, ), 1338381, C.progression),
        "Recipe: Coated Iron Canister": ItemData((G.Recipe, ), 1338382, C.progression),
        "Recipe: Steel Canister": ItemData((G.Recipe, ), 1338383, C.progression),
        "Recipe: Empty Fluid Tank": ItemData((G.Recipe, ), 1338384, C.progression),
        "Recipe: Packaged Alumina Solution": ItemData((G.Recipe, ), 1338385, C.progression),
        "Recipe: Packaged Fuel": ItemData((G.Recipe, ), 1338386, C.progression),
        "Recipe: Diluted Packaged Fuel": ItemData((G.Recipe, ), 1338387, C.progression),
        "Recipe: Packaged Heavy Oil Residue": ItemData((G.Recipe, ), 1338388, C.progression),
        "Recipe: Packaged Liquid Biofuel": ItemData((G.Recipe, ), 1338389, C.progression),
        "Recipe: Packaged Nitric Acid": ItemData((G.Recipe, ), 1338390, C.progression),
        "Recipe: Packaged Nitrogen Gas": ItemData((G.Recipe, ), 1338391, C.progression),
        "Recipe: Packaged Oil": ItemData((G.Recipe, ), 1338392, C.progression),
        "Recipe: Packaged Sulfuric Acid": ItemData((G.Recipe, ), 1338393, C.progression),
        "Recipe: Packaged Turbofuel": ItemData((G.Recipe, ), 1338394, C.progression),
        "Recipe: Packaged Water": ItemData((G.Recipe, ), 1338395, C.progression),
        "Recipe: Turbofuel": ItemData((G.Recipe, ), 1338396, C.progression),
        "Recipe: Turbo Heavy Fuel": ItemData((G.Recipe, ), 1338397, C.progression),
        "Recipe: Turbo Blend Fuel": ItemData((G.Recipe, ), 1338398, C.progression),
        "Recipe: Hazmat Suit": ItemData((G.Recipe, ), 1338399, C.progression),
        "Recipe: Gas Mask": ItemData((G.Recipe, ), 1338400, C.progression),
        "Recipe: Black Powder": ItemData((G.Recipe, ), 1338401, C.progression),
        "Recipe: Blade Runners": ItemData((G.Recipe, ), 1338402, C.useful),
        "Recipe: Chainsaw": ItemData((G.Recipe, ), 1338403, C.useful),
        "Recipe: Cluster Nobelisk":  ItemData((G.Recipe, ), 1338404, C.useful),
        "Recipe: Explosive Rebar":  ItemData((G.Recipe, ), 1338405, C.useful),
        "Recipe: Factory Cart": ItemData((G.Recipe, ), 1338406, C.useful),
        "Recipe: Gas Nobelisk":  ItemData((G.Recipe, ), 1338407, C.useful),
        "Recipe: Golden Factory Cart":  ItemData((G.Recipe, ), 1338408, C.useful),
        "Recipe: Homing Rifle Ammo": ItemData((G.Recipe, ), 1338409, C.useful),
        "Recipe: Iron Rebar":  ItemData((G.Recipe, ), 1338410, C.progression),
        "Recipe: Nobelisk":  ItemData((G.Recipe, ), 1338411, C.progression),
        "Recipe: Nuke Nobelisk": ItemData((G.Recipe, ), 1338412, C.useful),
        "Recipe: Nutritional Inhaler":  ItemData((G.Recipe, ), 1338413, C.useful),
        "Recipe: Object Scanner":  ItemData((G.Recipe, ), 1338414, C.progression),
        "Recipe: Parachute":  ItemData((G.Recipe, ), 1338415, C.useful),
        "Recipe: Protein Inhaler": ItemData((G.Recipe, ), 1338416, C.useful),
        "Recipe: Rebar Gun":  ItemData((G.Recipe, ), 1338417, C.useful),
        "Recipe: Rifle": ItemData((G.Recipe, ), 1338418, C.useful),
        "Recipe: Rifle Ammo":  ItemData((G.Recipe, ), 1338419, C.progression),
        "Recipe: Shatter Rebar":  ItemData((G.Recipe, ), 1338420, C.useful),
        "Recipe: Stun Rebar":  ItemData((G.Recipe, ), 1338421, C.useful),
        "Recipe: Therapeutic Inhaler": ItemData((G.Recipe, ), 1338422, C.useful),
        "Recipe: Turbo Rifle Ammo":  ItemData((G.Recipe, ), 1338423, C.useful),
        "Recipe: Vitamin Inhaler":  ItemData((G.Recipe, ), 1338424, C.useful),
        "Recipe: Xeno-Basher": ItemData((G.Recipe, ), 1338425, C.useful),
        "Recipe: Xeno-Zapper":  ItemData((G.Recipe, ), 1338426, C.useful),
        "Recipe: Zipline":  ItemData((G.Recipe, ), 1338427, C.useful),
        "Recipe: Fine Black Powder": ItemData((G.Recipe, ), 1338428, C.progression),
        "Recipe: Smokeless Powder": ItemData((G.Recipe, ), 1338429, C.progression),
        "Recipe: Alien DNA Capsule": ItemData((G.Recipe, ), 1338430, C.progression),
        "Recipe: Power Shard (1)": ItemData((G.Recipe, ), 1338431, C.progression),
        "Recipe: Power Shard (2)": ItemData((G.Recipe, ), 1338432, C.useful),
        "Recipe: Power Shard (5)": ItemData((G.Recipe, ), 1338433, C.useful),

        #1338434 - 1338599 Reserved for future recipes

        #1338400 - 1338899 buildings / others
        "Building: Constructor": ItemData((G.Building, ), 1338600, C.progression),
        "Building: Assembler": ItemData((G.Building, ), 1338601, C.progression),
        "Building: Manufacturer": ItemData((G.Building, ), 1338602, C.progression),
        "Building: Packager": ItemData((G.Building, ), 1338603, C.progression),
        "Building: Refinery": ItemData((G.Building, ), 1338604, C.progression),
        "Building: Blender": ItemData((G.Building, ), 1338605, C.progression),
        "Building: Particle Accelerator": ItemData((G.Building, ), 1338606, C.progression),
        "Building: Biomass Burner": ItemData((G.Building, ), 1338607, C.progression),
        "Building: Coal Generator": ItemData((G.Building, ), 1338608, C.progression),
        "Building: Geothermal Generator": ItemData((G.Building, ), 1338609, C.progression),
        "Building: Nuclear Power Plant": ItemData((G.Building, ), 1338610, C.progression),
        "Building: Miner Mk.1": ItemData((G.Building, ), 1338611, C.progression),
        "Building: Miner Mk.2": ItemData((G.Building, ), 1338612, C.progression),
        "Building: Miner Mk.3": ItemData((G.Building, ), 1338613, C.progression),
        "Building: Oil Extractor": ItemData((G.Building, ), 1338614, C.progression),
        "Building: Water Extractor": ItemData((G.Building, ), 1338615, C.progression),
        "Building: Smelter": ItemData((G.Building, ), 1338616, C.progression),
        "Building: Foundry": ItemData((G.Building, ), 1338617, C.progression),

        ### New
        "Building: Fuel Generator": ItemData((G.Building, ), 1338618, C.progression),
        "Building: Resource Well Pressurizer": ItemData((G.Building, ), 1338619, C.progression),
        "Building: Equipment Workshop": ItemData((G.Building, ), 1338620, C.progression),
        "Building: AWESOME Sink": ItemData((G.Building, ), 1338621, C.progression),
        "Building: AWESOME Shop": ItemData((G.Building, ), 1338622, C.progression),
        "Building: Painted Beams": ItemData((G.Beams, ), 1338623, C.filler),
        "Building: Blueprint Designer": ItemData((G.Building, ), 1338624, C.filler),
        "Building: Fluid Buffer": ItemData((G.Building, ), 1338625, C.filler),
        "Building: Industrial Fluid Buffer": ItemData((G.Building, ), 1338626, C.filler),
        "Building: Jump Pad": ItemData((G.Building, ), 1338627, C.filler),
        "Building: Ladder": ItemData((G.Building, ), 1338628, C.filler),
        "Building: MAM": ItemData((G.Building, ), 1338629, C.progression),
        "Building: Personal Storage Box": ItemData((G.Building, ), 1338630, C.filler),
        "Building: Power Storage": ItemData((G.Building, ), 1338631, C.useful),
        "Building: U-Jelly Landing Pad": ItemData((G.Building, ), 1338632, C.useful),
        "Building: Power Switch": ItemData((G.Building, ), 1338633, C.useful),
        "Building: Priority Power Switch": ItemData((G.Building, ), 1338634, C.useful),
        "Building: Storage Container": ItemData((G.Building, ), 1338635, C.useful),
        "Building: Lookout Tower": ItemData((G.Building, ), 1338636, C.filler),
        #"Building: Power Pole Mk.1": ItemData((G.Building, ), 1338637, C.progression),
        "Building: Power Pole Mk.2": ItemData((G.Building, ), 1338638, C.useful),
        "Building: Power Pole Mk.3": ItemData((G.Building, ), 1338639, C.useful),
        "Building: Industrial Storage Container": ItemData((G.Building, ), 1338640, C.filler),
        "Building: Conveyor Merger": ItemData((G.Building, ), 1338641, C.progression),
        "Building: Conveyor Splitter": ItemData((G.Building, ), 1338642, C.progression),
        "Building: Conveyor Mk.1": ItemData((G.Building, G.ConveyorMk1), 1338643, C.progression),
        "Building: Conveyor Mk.2": ItemData((G.Building, G.ConveyorMk2), 1338644, C.progression),
        "Building: Conveyor Mk.3": ItemData((G.Building, G.ConveyorMk3), 1338645, C.progression),
        "Building: Conveyor Mk.4": ItemData((G.Building, G.ConveyorMk4), 1338646, C.progression),
        "Building: Conveyor Mk.5": ItemData((G.Building, G.ConveyorMk5), 1338647, C.progression),
        "Building: Conveyor Lift Mk.1": ItemData((G.Building, G.ConveyorMk1), 1338648, C.useful),
        "Building: Conveyor Lift Mk.2": ItemData((G.Building, G.ConveyorMk2), 1338649, C.useful),
        "Building: Conveyor Lift Mk.3": ItemData((G.Building, G.ConveyorMk3), 1338650, C.useful),
        "Building: Conveyor Lift Mk.4": ItemData((G.Building, G.ConveyorMk4), 1338651, C.useful),
        "Building: Conveyor Lift Mk.5": ItemData((G.Building, G.ConveyorMk5), 1338652, C.useful),
        "Building: Metal Beams": ItemData((G.Beams, ), 1338653, C.filler, 0),
        "Building: Stackable Conveyor Pole": ItemData((G.Building, G.ConveyorSupports), 1338654, C.useful),
        "Building: Conveyor Wall Mount": ItemData((G.Building, G.ConveyorSupports), 1338655, C.useful, 0),
        "Building: Conveyor Lift Floor Hole": ItemData((G.Building, G.ConveyorSupports), 1338656, C.useful, 0),
        "Building: Conveyor Ceiling Mount": ItemData((G.Building, G.ConveyorSupports), 1338657, C.useful, 0),
        "Building: Pipes Mk.1": ItemData((G.Building, G.PipesMk1), 1338658, C.progression),
        "Building: Pipes Mk.2": ItemData((G.Building, G.PipesMk2), 1338659, C.progression),
        "Building: Pipeline Pump Mk.1": ItemData((G.Building, G.PipesMk1), 1338660, C.progression),
        "Building: Pipeline Pump Mk.2": ItemData((G.Building, G.PipesMk2), 1338661, C.progression),
        "Building: Pipeline Junction Cross": ItemData((G.Building, G.PipesMk1, G.PipesMk2), 1338662, C.progression),
        "Building: Valve": ItemData((G.Building, G.PipesMk1, G.PipesMk2), 1338663, C.useful),
        "Building: Stackable Pipeline Support": ItemData((G.Building, G.PipelineSupports), 1338664, C.useful, 0),
        "Building: Wall Pipeline Support": ItemData((G.Building, G.PipelineSupports), 1338665, C.useful, 0),
        "Building: Pipeline Wall Hole": ItemData((G.Building, G.PipelineSupports), 1338666, C.useful, 0),
        "Building: Pipeline Floor Hole": ItemData((G.Building, G.PipelineSupports), 1338667, C.useful, 0),
        "Building: Lights Control Panel": ItemData((G.Building, G.Lights), 1338668, C.filler, 0),
        "Building: Wall Mounted Flood Light": ItemData((G.Building, G.Lights), 1338669, C.filler, 0),
        "Building: Street Light": ItemData((G.Building, G.Lights), 1338670, C.filler, 0),
        "Building: Flood Light Tower": ItemData((G.Building, G.Lights), 1338671, C.filler, 0),
        "Building: Ceiling Light": ItemData((G.Building, G.Lights), 1338672, C.filler, 0),
        "Building: Power Tower": ItemData((G.Building, ), 1338673, C.useful),
        "Building: Walls Orange": ItemData((G.Building, G.Walls), 1338674, C.useful),
        "Building: Radar Tower": ItemData((G.Building, ), 1338675, C.useful),
        "Building: Smart Splitter": ItemData((G.Building, ), 1338676, C.useful),
        "Building: Programmable Splitter": ItemData((G.Building, ), 1338677, C.useful),
        "Building: Label Sign Bundle": ItemData((G.Building, G.Signs), 1338678, C.filler, 0),
        "Building: Display Sign Bundle": ItemData((G.Building, G.Signs), 1338679, C.filler, 0),
        "Building: Billboard Set": ItemData((G.Building, G.Signs), 1338680, C.filler, 0),
        "Building: Walls Metal": ItemData((G.Building, G.Walls), 1338681, C.filler, 0),
        "Building: Metal Pillar": ItemData((G.Pilars, ), 1338682, C.filler, 0),
        "Building: Concrete Pillar": ItemData((G.Pilars, ), 1338683, C.filler, 0),
        "Building: Frame Pillar": ItemData((G.Pilars, ), 1338684, C.filler, 0),
        "Building: Walls Concrete": ItemData((G.Building, G.Walls), 1338685, C.filler, 0),
        #"Building: Big Metal Pillar": ItemData((G.Pilars, ), 1338686, C.filler, 0),
        #"Building: Big Concrete Pillar": ItemData((G.Pilars, ), 1338687, C.filler, 0),
        #"Building: Big Frame Pillar": ItemData((G.Pilars, ), 1338688, C.filler, 0),
        #"Building: Beam Support": ItemData((G.Beams, ), 1338689, C.filler, 0),
        #"Building: Beam Connector": ItemData((G.Beams, ), 1338690, C.filler, 0),
        #"Building: Beam Connector Double": ItemData((G.Beams, ), 1338691, C.filler, 0),
        "Building: Foundation": ItemData((G.Foundations, ), 1338692, C.filler),
        "Building: Half Foundation": ItemData((G.Foundations, ), 1338693, C.filler, 0),
        "Building: Corner Ramp Pack": ItemData((G.Foundations, ), 1338694, C.filler, 0),
        "Building: Inverted Ramp Pack": ItemData((G.Foundations, ), 1338695, C.filler, 0),
        "Building: Inverted Corner Ramp Pack": ItemData((G.Foundations, ), 1338696, C.filler, 0),
        "Building: Quarter Pipes Pack": ItemData((G.Foundations, ), 1338697, C.filler, 0),
        "Building: Quarter Pipe Extensions Pack": ItemData((G.Foundations, ), 1338698, C.filler, 0),
        "Building: Frame foundation": ItemData((G.Foundations, ), 1338699, C.filler, 0),

        #1338700 - 1338799 Reserved for buildings

        # Large Packages (single item, multiple unlocks)
        # Drones (including Drone)
        "Transport: Drones": ItemData((G.Transport, ), 1338800, C.filler),

        # Trains (including Empty Platform, rails, station, locomotive)
        "Transport: Trains": ItemData((G.Transport, G.Trains), 1338801, C.filler),
        "Transport: Fluid Trains": ItemData((G.Transport, G.Trains), 1338802, C.filler),

        # Tracker / Truck (including truck station)
        "Transport: Tractor": ItemData((G.Transport, G.Trains), 1338803, C.filler),
        "Transport: Truck": ItemData((G.Transport, G.Trains), 1338804, C.filler),
        "Transport: Explorer": ItemData((G.Transport, G.Trains), 1338805, C.filler),
        "Transport: Factory Cart": ItemData((G.Transport, G.Trains), 1338806, C.filler),
        "Transport: Factory Cart (golden)": ItemData((G.Transport, G.Trains), 1338807, C.filler),
        "Transport: Cyber Wagon": ItemData((G.Transport, G.Trains), 1338808, C.filler),

        # Hypertubes (including supports / pipes / entrance / holes)
        "Transport: Hypertube": ItemData((G.Transport, G.HyperTubes), 1338809, C.filler),
        "Transport: Hypertube Floor Hole": ItemData((G.Transport, G.HyperTubes), 1338810, C.filler),
        "Transport: Hypertube Wall Support": ItemData((G.Transport, G.HyperTubes), 1338811, C.filler),
        "Transport: Hypertube Wall Hole": ItemData((G.Transport, G.HyperTubes), 1338812, C.filler),

        #1338900 - 1338998 Handled by trap system
        # Regenerate via /Script/Blutility.EditorUtilityWidgetBlueprint'/Archipelago/Debug/EU_GenerateTrapIds.EU_GenerateTrapIds'
        "Hog Basic": ItemData((G.Trap, ), 1338900, C.trap),
        "Hog Alpha": ItemData((G.Trap, ), 1338901, C.trap),
        "Hog Johnny": ItemData((G.Trap, ), 1338902, C.trap),
        "Hog Cliff": ItemData((G.Trap, ), 1338903, C.trap),
        "Hog Cliff Nuclear": ItemData((G.Trap, ), 1338904, C.trap),
        "Not The Bees": ItemData((G.Trap, ), 1338905, C.trap),
        "Hatcher": ItemData((G.Trap, ), 1338906, C.trap),
        "Doggo Pulse Nobelisk": ItemData((G.Trap, ), 1338907, C.trap),
        "Doggo Nuke Nobelisk": ItemData((G.Trap, ), 1338908, C.trap),
        "Doggo with PowerSlug": ItemData((G.Parts, ), 1338909),
        "Doggo Gas Nobelisk": ItemData((G.Trap, ), 1338910, C.trap),
        "Spore Flower": ItemData((G.Trap, ), 1338911, C.trap),
        "Stinger Gas": ItemData((G.Trap, ), 1338912, C.trap),
        "Stinger Elite": ItemData((G.Trap, ), 1338913, C.trap),
        "Stinger Small": ItemData((G.Trap, ), 1338914, C.trap),
        "Spitter Forest": ItemData((G.Trap, ), 1338915, C.trap),
        "Spitter Forest Alpha": ItemData((G.Trap, ), 1338916, C.trap),
        "Nuclear Waste (ground)": ItemData((G.Trap, ), 1338917, C.trap),
        "Plutonium Waste (ground)": ItemData((G.Trap, ), 1338918, C.trap),

        "Building: Space Elevator": ItemData((G.Building, ), 1338999, C.progression)
    }


    item_names_and_ids: ClassVar[Dict[str, int]] = {name: item_data.code for name, item_data in item_data.items()}
    filler_items: ClassVar[Tuple[str, ...]] = tuple(item for item, details in item_data.items() 
                                                  if any(cat for cat in details.category if cat in {G.Parts, G.Ammo}))


    @classmethod
    def get_item_names_per_category(cls) -> Dict[str, Set[str]]:
        categories: Dict[str, Set[str]] = {}

        for name, data in cls.item_data.items():
            for category in data.category:
                categories.setdefault(category.name, set()).add(name)
                
        return categories


    player: int
    logic: GameLogic
    random: Random
    precalculated_progression_recipes: Optional[Dict[str, Recipe]]


    def __init__(self, player: Optional[int], logic: GameLogic, random: Random):
        self.player = player
        self.logic = logic
        self.random = random

        if False: # major performance boost if we can get it stable
            self.precalculated_progression_recipes = self.select_progression_recipes() 
        else:
            self.precalculated_progression_recipes = None


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

    @classmethod
    def create_item(cls, instance: Optional["Items"], name: str, player: int) -> Item:
        data: ItemData = cls.item_data[name]

        if instance and instance.precalculated_progression_recipes and \
                name not in instance.precalculated_progression_recipes:
            return Item(name, C.useful, data.code, instance.player)

        return Item(name, data.type, data.code, player)


    def get_filler_item_name(self, random: Random, options: SatisfactoryOptions) -> str:
        trap_chance: int = options.trap_chance.value
        enabled_traps: List[str] = options.traps.value

        if enabled_traps and random.random() < (trap_chance / 100):
            return random.choice(enabled_traps)
        else:
            return random.choice(self.filler_items) 


    def build_item_pool(self, random: Random, options: SatisfactoryOptions, excluded_items: Set[str],
                        number_of_locations: int) -> List[Item]:
        
        pool: List[Item] = []

        for name, data in self.item_data.items():
            if name not in excluded_items and data.count > 0 and any(
                    cat for cat in data.category if cat in {G.Recipe, G.Building, G.Equipment, G.Transport, G.Upgrades}):
                for _ in range(data.count):
                    item = self.create_item(self, name, self.player)
                    pool.append(item)

        for _ in range(number_of_locations - len(pool)):
            item = self.create_item(self, self.get_filler_item_name(random, options), self.player)
            pool.append(item)

        return pool


    def write_progression_chain(self, multiworld: MultiWorld, spoiler_handle: TextIO):
        if self.precalculated_progression_recipes:
            player_name = f'{multiworld.get_player_name(self.player)}: ' if multiworld.players > 1 else ''
            spoiler_handle.write('\n\nSelected Satisfactory Recipes:\n\n')
            spoiler_handle.write('\n'.join(
                f"{player_name}{part} -> {recipe.name}" 
                for part, recipes_per_part in self.logic.recipes.items()
                for recipe in recipes_per_part 
                if recipe.name in self.precalculated_progression_recipes
            ))
