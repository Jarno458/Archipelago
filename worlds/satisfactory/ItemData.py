from enum import Enum
from typing import NamedTuple, Tuple
from BaseClasses import ItemClassification

class ItemGroups(Enum, str):
    Parts = 1
    Equipment = 2
    Ammo = 3
    Recipe = 4
    Building = 5
    Trap = 6
    Lights = 7
    Foundations = 8
    Transport = 9
    Trains = 10
    ConveyorMk1 = 11
    ConveyorMk2 = 12
    ConveyorMk3 = 13
    ConveyorMk4 = 14
    ConveyorMk5 = 15
    ConveyorSupports = 16
    PipesMk1 = 17
    PipesMk2 = 18
    PipelineSupports = 19
    HyperTubes = 20
    Signs = 21
    Pilars = 22
    Beams = 23

class ItemData(NamedTuple):
    category: Tuple[ItemGroups, ...]
    code: int
    type: ItemClassification = ItemClassification.filler