from typing import List, Optional  # Import Optional for optional fields
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
    Identify an **item** or **object** in an artwork.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    # The general 'type_of_physical_object' is removed as it's handled by picking one of these.
    clothing: Optional[str] = (
        None  # Examples: robe, cloak, tunic, dress, armor, veil, crown, hat, sash, shoe, dress
    )
    instrument: Optional[str] = (
        None  # Examples: lute, viola da gamba, flute, trumpet, harp, drum, organ, piano
    )
    religious_object: Optional[str] = (
        None  # Examples: crucifix, rosary, chalice, menorah, prayer beads, altar, icon, thurible, ark
    )
    tool: Optional[str] = (
        None  # Examples: hammer, chisel, paintbrush, compass, quill, spindle, plow, loom, telescope, astrolabe
    )
    weapon: Optional[str] = (
        None  # Examples: sword, spear, bow and arrow, shield, dagger, cannon, musket, axe, slingshot
    )
    other_object: Optional[str] = (
        None  # For physical objects not covered by the specific categories (e.g., chair, goblet, mirror, book, crown, candle)
    )


def physical_object_relation_to_triplet(package: PhysicalObject) -> List[dict]:
    triplets = []

    object_label: Optional[str] = None
    if package.clothing is not None:
        object_label = package.clothing
    elif package.instrument is not None:
        object_label = package.instrument
    elif package.religious_object is not None:
        object_label = package.religious_object
    elif package.tool is not None:
        object_label = package.tool
    elif package.weapon is not None:
        object_label = package.weapon
    elif package.other_object is not None:
        object_label = package.other_object

    if object_label is None:
        raise ValueError()

    triplets.append(
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": object_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": object_label,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical object",
                "wikidata_id": "wd:Q223557",
            },
        }
    )

    return triplets


ENTITY_DEFINITIONS: List[Template] = [Color, PhysicalObject]

ENTITY_PARSER = {
    "Color": color_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
}
