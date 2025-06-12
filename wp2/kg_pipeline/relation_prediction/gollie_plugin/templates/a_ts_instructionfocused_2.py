from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  # ignoring most if not all the meta data relations
"""


@dataclass
class MythicalCharacter(Template):
    """
    Identify a **person from myths or legends**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_character: str  # Mythical characters such as Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor


def mythical_character_relation_to_triplet(package: MythicalCharacter):
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
                "label": package.type_of_mythical_character,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_character,
                "s_class": "MythicalCharacter",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical character",
                "wikidata_id": "wd:Q4271324",
            },
        },
    ]

    return triplets


@dataclass
class ReligiousCharacter(Template):
    """
    Identify a **person that alludes to religious and biblical stories**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_religious_character: str  # Religious characters such as Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna


def religious_character_relation_to_triplet(package: ReligiousCharacter):
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
                "label": package.type_of_religious_character,
            },
        },
        {
            "subject": {
                "label": package.type_of_religious_character,
                "s_class": "ReligiousCharacter",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "religious character",
                "wikidata_id": "wd:Q18563354",
            },
        },
    ]

    return triplets


@dataclass
class AnatomicalStructure(Template):
    """
    Identify a **body or body part**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_anatomical_structure: str  # Anatomical structures such as torso, arm, head, hands, legs, feet, ribcage, eye, fingers


def anatomical_structure_relation_to_triplet(package: AnatomicalStructure):
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
                "label": package.type_of_anatomical_structure,
            },
        },
        {
            "subject": {
                "label": package.type_of_anatomical_structure,
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
        },
    ]

    return triplets


@dataclass
class Occupation(Template):
    """
    Identify a **job, profession, or social role**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_occupation: str  # Occupations such as blacksmith, priest, mourning woman, soldier, merchant, noblewoman, peasant, scholar


def occupation_relation_to_triplet(package: Occupation):
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
                "label": package.type_of_occupation,
            },
        },
        {
            "subject": {
                "label": package.type_of_occupation,
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
        },
    ]

    return triplets


@dataclass
class Posture(Template):
    """
    Identify the **pose or stance** of a figure.
    """

    person: str  # A specific person that is given in the text, but not necessarily in the depicted in the picture. for example: Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I
    type_of_posture: str  # Reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


def posture_relation_to_triplet(package: Posture):
    triplets = [
        {
            "subject": {
                "label": package.person,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "has characteristic",
                "wikidata_id": "wdt:P1552",
            },
            "object": {
                "label": package.type_of_posture,
            },
        },
        {
            "subject": {
                "label": package.type_of_posture,
                "s_class": "Posture",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "posture",
                "wikidata_id": "wd:Q8514257",
            },
        },
    ]

    return triplets


@dataclass
class ArchitecturalStructure(Template):
    """
    Identify a **building or constructed form**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_architectural_structure: str  # Architectural structures such as palace, bridge, water garden, castle, cathedral, temple, tower, amphitheater


def architectural_structure_relation_to_triplet(package: ArchitecturalStructure):
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
                "label": package.type_of_architectural_structure,
            },
        },
        {
            "subject": {
                "label": package.type_of_architectural_structure,
                "s_class": "ArchitecturalStructure",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "architectural structure",
                "wikidata_id": "wd:Q811979",
            },
        },
    ]

    return triplets


@dataclass
class GeographicalFeature(Template):
    """
    Identify a **naturally occurring landform**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_geographical_feature: str  # FGeographical features such as forest, fields, pathways, mountains, river, desert, coastline, cliffs


def geographical_feature_relation_to_triplet(package: GeographicalFeature):
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
                "label": package.type_of_geographical_feature,
            },
        },
        {
            "subject": {
                "label": package.type_of_geographical_feature,
                "s_class": "GeographicalFeature",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "geographical feature",
                "wikidata_id": "wd:Q618123",
            },
        },
    ]

    return triplets


@dataclass
class MythicalLocation(Template):
    """
    Identify a **place from myths, legends, or folklore**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_location: str  # Mythical locations such as Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis


def mythical_location_relation_to_triplet(package: MythicalLocation):
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
                "label": package.type_of_mythical_location,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_location,
                "s_class": "MythicalLocation",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical location",
                "wikidata_id": "wd:Q3238337",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalLocation(Template):
    """
    Identify a **specific, real-world place**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_location: str  # Physical locations such as Camposanto, Paris, Mount Fuji, Eiffel Tower, Grand Canyon, Rome, Taj Mahal


def physical_location_relation_to_triplet(package: PhysicalLocation):
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
                "label": package.type_of_physical_location,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_location,
                "s_class": "PhysicalLocation",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical location",
                "wikidata_id": "wd:Q17334923",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalSurface(Template):
    """
    Identify a **defined material area** with specific qualities.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_surface: str  # Physical surfaces such as brick wall, marble floor, wood wall, rough stone, polished metal, woven fabric


def physical_surface_relation_to_triplet(package: PhysicalSurface):
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
                "label": package.type_of_physical_surface,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_surface,
                "s_class": "PhysicalSurface",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical surface",
                "wikidata_id": "wd:Q3783831",
            },
        },
    ]

    return triplets


@dataclass
class Animal(Template):
    """
    Identify an **animal**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_animal: (
        str  # Animals such as Dog, giraffe, cat, horse, fish, elephant, lion, eagle
    )


def animal_relation_to_triplet(package: Animal):
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
                "label": package.type_of_animal,
            },
        },
        {
            "subject": {
                "label": package.type_of_animal,
                "s_class": "Animal",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "animal",
                "wikidata_id": "wd:Q729",
            },
        },
    ]

    return triplets


@dataclass
class MythicalAnimal(Template):
    """
    Identify a **legendary or folkloric creature**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_animal: str  # Mythical animals such as Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera


def mythical_animal_relation_to_triplet(package: MythicalAnimal):
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
                "label": package.type_of_mythical_animal,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_animal,
                "s_class": "MythicalAnimal",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical animal",
                "wikidata_id": "wd:Q24334299",
            },
        },
    ]

    return triplets


@dataclass
class Food(Template):
    """
    Identify an **edible or drinkable item**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_food: str  # Food such as bread, peach, plums, brioche, wine, grapes, pomegranate, figs


def food_relation_to_triplet(package: Food):
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
                "label": package.type_of_food,
            },
        },
        {
            "subject": {
                "label": package.type_of_food,
                "s_class": "Food",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "food",
                "wikidata_id": "wd:Q2095",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalObject(Template):
    """
    Identify an **item** contributing to composition, narrative, or symbolism.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_object: str  # Physical objects such as viola da gamba, sword, chair, goblet, mirror, book, crown, candle


def physical_object_relation_to_triplet(package: PhysicalObject):
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
                "label": package.type_of_physical_object,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_object,
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
        },
    ]

    return triplets


@dataclass
class Plant(Template):
    """
    Identify a **plant**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_plant: str  # Plants such as Iris, tree, cactus, acanthus, laurel, olive branch, lotus, vine


def plant_relation_to_triplet(package: Plant):
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
                "label": package.type_of_plant,
            },
        },
        {
            "subject": {
                "label": package.type_of_plant,
                "s_class": "Plant",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "plant",
                "wikidata_id": "wd:Q756",
            },
        },
    ]

    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    MythicalCharacter,
    ReligiousCharacter,
    AnatomicalStructure,
    Occupation,
    Posture,
    ArchitecturalStructure,
    GeographicalFeature,
    MythicalLocation,
    PhysicalLocation,
    PhysicalSurface,
    Animal,
    MythicalAnimal,
    Food,
    PhysicalObject,
    Plant,
]

ENTITY_PARSER = {
    "MythicalCharacter": mythical_character_relation_to_triplet,
    "ReligiousCharacter": religious_character_relation_to_triplet,
    "AnatomicalStructure": anatomical_structure_relation_to_triplet,
    "Occupation": occupation_relation_to_triplet,
    "Posture": posture_relation_to_triplet,
    "ArchitecturalStructure": architectural_structure_relation_to_triplet,
    "GeographicalFeature": geographical_feature_relation_to_triplet,
    "MythicalLocation": mythical_location_relation_to_triplet,
    "PhysicalLocation": physical_location_relation_to_triplet,
    "PhysicalSurface": physical_surface_relation_to_triplet,
    "Animal": animal_relation_to_triplet,
    "MythicalAnimal": mythical_animal_relation_to_triplet,
    "Food": food_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
    "Plant": plant_relation_to_triplet,
}
