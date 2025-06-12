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
                "s_class": "WorkOfArt",
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
                "s_class": "Color",
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
        return triplets

    triplets.append(
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
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
                "s_class": "PhysicalObject",
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
                "s_class": "WorkOfArt",
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
                "s_class": "Season",
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
    Identify a **job, profession, or social role**.
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
        return triplets

    triplets.append(
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
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
                "s_class": "Occupation",
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

    body_as_whole: Optional[str] = (
        None  # Body as a whole such as human body, torso, nude figure
    )
    head: Optional[str] = (
        None  # Parts of the head such as face, eye, ear, nose, mouth, hair
    )
    limb: Optional[str] = None  # Limbs such as arm, hand, finger, leg, foot, toe
    internal_organ: Optional[str] = (
        None  # Internal Organs such as heart, brain, lung, liver, ribcage (as a skeletal part)
    )
    other_part: Optional[str] = (
        None  # For anatomical parts not covered by specific categories (e.g., bone, skeleton, skin)
    )


def anatomical_structure_relation_to_triplet(
    package: AnatomicalStructure,
) -> List[dict]:
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
        return triplets

    triplets.append(
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
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
                "s_class": "AnatomicalStructure",
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


@dataclass
class Person(Template):
    """
    Identify a **human figure** or **person**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    historical_figure: Optional[str] = (
        None  # Historical figures Napoleon, Julius Caesar, Marie Antoinette, Queen Elizabeth I, Leonardo da Vinci
    )
    mythological_figure: Optional[str] = (
        None  # Mythological figures such as Venus, Zeus, Hercules, Medusa, Cupid, Leda
    )
    religious_figure: Optional[str] = (
        None  # Religious figures such as Jesus Christ, Virgin Mary, Saint Peter, Buddha, Prophet Muhammad
    )
    other_person_type: Optional[str] = (
        None  # For specific types not covered by the above (e.g., unknown person, self-portrait, group)
    )

    # These fields are for descriptive purposes only and WILL NOT be extracted into Wikidata triplets.
    gender: Optional[str] = None  # Examples: man, woman, child, boy, girl
    age_group: Optional[str] = (
        None  # Examples: infant, toddler, child, adolescent, adult, elderly person
    )


def person_relation_to_triplet(package: Person) -> List[dict]:
    triplets = []

    person_label: Optional[str] = None
    if package.historical_figure is not None:
        person_label = package.historical_figure
    elif package.mythological_figure is not None:
        person_label = package.mythological_figure
    elif package.religious_figure is not None:
        person_label = package.religious_figure
    elif package.other_person_type is not None:
        person_label = package.other_person_type

    if person_label is None:
        return triplets

    triplets.append(
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": person_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": person_label,
                "s_class": "Person",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "human",
                "wikidata_id": "wd:Q5",
            },
        }
    )
    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    Color,
    PhysicalObject,
    Season,
    Occupation,
    AnatomicalStructure,
    Person,
]

ENTITY_PARSER = {
    "Color": color_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
    "Season": season_relation_to_triplet,
    "Occupation": occupation_relation_to_triplet,
    "AnatomicalStructure": anatomical_structure_relation_to_triplet,
    "Person": person_relation_to_triplet,
}
