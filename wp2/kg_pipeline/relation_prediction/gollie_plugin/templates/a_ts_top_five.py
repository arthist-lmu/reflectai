from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  
"""


@dataclass
class Color(Template):
    """
    Identify **colors** (hues, shades, or tones) depicted as visual characteristics in a work of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_color: str  # Colors such as gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre


def color_relation_to_triplet(package: Color):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_color,
            },
        },
        {
            "subject": {
                "label": package.type_of_color,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "color",
                "wikidata_id": "wd:Q1075",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalObject(Template):
    """
    Identify an **item** or **object**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    type_of_physical_object: str  # Physical objects such as viola da gamba, sword, chair, goblet, mirror, book, crown, candle
    clothing: (
        str  # Examples: robe, cloak, tunic, dress, armor, veil, crown, hat, sash, shoe
    )
    instrument: (
        str  # Examples: lute, viola da gamba, flute, trumpet, harp, drum, organ, piano
    )
    religious_object: str  # Examples: crucifix, rosary, chalice, menorah, prayer beads, altar, icon, thurible, ark
    tool: str  # Examples: hammer, chisel, paintbrush, compass, quill, spindle, plow, loom, telescope, astrolabe
    weapon: str  # Examples: sword, spear, bow and arrow, shield, dagger, cannon, musket, axe, slingshot


def physical_object_relation_to_triplet(package: PhysicalObject):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_physical_object,
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.clothing,
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.instrument,
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.religious_object,
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.tool,
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.weapon,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_object,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical object",
                "wikidata_id": "wd:Q223557",
            },
        },
    ]

    return triplets


ENTITY_DEFINITIONS: List[Template] = [Color, PhysicalObject]

ENTITY_PARSER = {
    "Color": color_relation_to_triplet,
    "Composition": physical_object_relation_to_triplet,
}
