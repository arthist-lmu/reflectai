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

    clothing: Optional[str] = (
        None  # Clothing such as robe, cloak, tunic, dress, armor, veil, crown, hat, sash, shoe, dress
    )
    instrument: Optional[str] = (
        None  # Instruments such as lute, viola da gamba, flute, trumpet, harp, drum, organ, piano
    )
    religious_object: Optional[str] = (
        None  # Religious objects such as crucifix, rosary, chalice, menorah, prayer beads, altar, icon, thurible, ark
    )
    tool: Optional[str] = (
        None  # Tools such as hammer, chisel, paintbrush, compass, quill, spindle, plow, loom, telescope, astrolabe
    )
    weapon: Optional[str] = (
        None  # Weapons such as sword, spear, bow and arrow, shield, dagger, cannon, musket, axe, slingshot
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


@dataclass
class Season(Template):
    """
    Identify the **season** (Spring, Summer, Fall, or Winter) described.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_season: str  # Type of seasons such as spring, summer, fall, winter, rainy season, dry season


def season_relation_to_triplet(package: Season):
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
                "label": package.type_of_season,
            },
        },
        {
            "subject": {
                "label": package.type_of_season,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "season",
                "wikidata_id": "wd:Q10688145",
            },
        },
    ]

    return triplets


@dataclass
class Occupation(Template):
    """
    Identify a **job, profession, or social role** depicted in a work of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    job: Optional[str] = (
        None  # Jobs such as blacksmith, baker, carpenter, weaver, scribe, fisherman, farmer
    )
    profession: Optional[str] = (
        None  # Professions such as doctor, lawyer, priest, nun, scholar, architect, artist, musician
    )
    social_role: Optional[str] = (
        None  # Social Roles like noblewoman, peasant, king, queen, soldier, merchant, guardian
    )
    other_occupation: Optional[str] = (
        None  # For occupations not covered by the specific categories (e.g., warrior, pilgrim)
    )


def occupation_relation_to_triplet(package: Occupation) -> List[dict]:
    triplets = []

    occupation_label: Optional[str] = None
    if package.job is not None:
        occupation_label = package.job
    elif package.profession is not None:
        occupation_label = package.profession
    elif package.social_role is not None:
        occupation_label = package.social_role
    elif package.other_occupation is not None:
        occupation_label = package.other_occupation

    if occupation_label is None:
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
                "label": occupation_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": occupation_label,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "occupation",
                "wikidata_id": "wd:Q12737077",
            },
        }
    )

    return triplets


@dataclass
class AnatomicalStructure(Template): 
    """
    Identify a **body or body part** depicted as a visual characteristic in a work of art.
    """
    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    body_as_whole: Optional[str] = None  # Examples: human body, torso, nude figure
    head: Optional[str] = None           # Examples: head, face, eye, ear, nose, mouth, hair
    limb: Optional[str] = None           # Examples: arm, hand, finger, leg, foot, toe
    internal_organ: Optional[str] = None # Examples: heart, brain, lung, liver, ribcage (as a skeletal part)
    other_part: Optional[str] = None     # For anatomical parts not covered by specific categories (e.g., bone, skeleton, skin)


def anatomical_structure_relation_to_triplet(package: AnatomicalStructure) -> List[dict]: 
    triplets = []

    # Find the specific anatomical part mentioned in the package
    anatomical_label: Optional[str] = None
    if package.body_as_whole is not None:
        anatomical_label = package.body_as_whole
    elif package.head is not None:
        anatomical_label = package.head
    elif package.limb is not None:
        anatomical_label = package.limb
    elif package.internal_organ is not None:
        anatomical_label = package.internal_organ
    elif package.other_part is not None:
        anatomical_label = package.other_part

    if anatomical_label is None:
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
                "label": anatomical_label,  
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": anatomical_label,  
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "anatomical structure", 
                "wikidata_id": "wd:Q4936952",    
            },
        }
    )

    return triplets


ENTITY_DEFINITIONS: List[Template] = [Color, PhysicalObject, Occupation, AnatomicalStructure] 

ENTITY_PARSER = {
    "Color": color_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
    "Occupation": occupation_relation_to_triplet,
    "AnatomicalStructure": anatomical_structure_relation_to_triplet,
}