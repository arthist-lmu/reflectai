from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

@dataclass
class ArtisticTheme(Template):
    """
    theme or subject in a work of art
    """

    theme: str  # Artistic theme like Adoration, Vanitas, Last Supper or Annunciation


@dataclass
class Composition(Template):
    """
    placement or arrangement of visual elements in a work of art
    """

    CompositionOfArtwork: str  # Spatial arrangement, placement or arrangement like diagonal lines, symetry or central figure


@dataclass
class WorkOfArt(Template):
    """
    aesthetic item or artistic creation
    """

    work: str  # Titles or names specific of artworks like Mona Lisa, The Sistine Chapel, or Guernica


@dataclass
class Concept(Template):
    """
    semantic unit understood in different ways, e.g., as mental representation, ability, or abstract object
    """

    ConceptOfArtwork: str  # Abstract concept or ideas like harmony, man or nature


@dataclass
class RhetoricalDevice(Template):
    """
    technique or strategy that a person uses with the goal of persuading or to convey deeper meanings
    """

    device: str  # Rhetorical Device like irony, allegory or sarcasm


@dataclass
class Emotion(Template):
    """
    biological states associated with the nervous system
    """

    TypeOfEmotion: str  # Emotions or moods expressed by figures in the work of art like sadness, melancholy or joy


@dataclass
class Quality(Template):
    """
    distinguishing feature
    """

    TypeOfQuality: str  # An artwork can have qualities like vibrant, delicate, beautiful or impressive


@dataclass
class Color(Template):
    """
    characteristic of visual perception
    """

    TypeOfColor: str  # Specific colors like gold, emerald green or pastel tones


@dataclass
class PointInTime(Template):
    """
    position of a particular instant in time
    """

    TypeOfPointInTime: (
        str  # Exact dates like 12. April 1450, circa 1890 or mid-16th century
    )


@dataclass
class Season(Template):
    """
    section of a year
    """

    TypeOfSeason: str  # Mention of seasons like spring, summer, fall and winter


@dataclass
class Person(Template):
    """
    being that has certain capacities or attributes constituting personhood
    """

    TypeOfPerson: (
        str  # Specific persons that are visually represented or symbolically referenced
    )


@dataclass
class MythicalCharacter(Template):
    """
    character from mythology
    """

    TypeOfMythicalCharacter: (
        str  # Characters from mythology like Zeus, Venus, Poseidon or Muses
    )


@dataclass
class ReligiousCharacter(Template):
    """
    character of a religious work, alleged to be historical
    """

    TypeOfReligiousCharacter: (
        str  # Character from religion like Adam, Jesus or Apostles
    )


@dataclass
class AnatomicalStructure(Template):
    """
    entity with a single connected shape
    """

    TypeOfAnatomicalStructure: str  # Anatomical structure like torso, arm, head or arms


@dataclass
class Occupation(Template):
    """
    label applied to a person based on an activity they participate in
    """

    TypeOfOccupation: str  # Blacksmith, Priest, mourning women


@dataclass
class Posture(Template):
    """
    physical configuration that a human can take
    """

    TypeOfPosture: str  # Reclining, head tilted, moving, sitting, standing


@dataclass
class ArchitecturalStructure(Template):
    """
    human-designed and -made structure
    """

    TypeOfArchitecturalStructure: str  # palace, bridge, water garde, castle


@dataclass
class GeographicalFeature(Template):
    """
    components of planets that can be geographically located
    """

    TypeOfGeographicalFeature: str  # forest, fields, pathways, mountains


@dataclass
class MythicalLocation(Template):
    """
    place that only exists in myths, legends, and folklore
    """

    TypeOfMythicalLocation: str  # paradise, hell, elysium, limbo


@dataclass
class PhysicalLocation(Template):
    """
    position of something in space
    """

    TypeOfPhysicalLocation: str  # Camposanto, Paris, Mount Fuji, Eiffel Tower


@dataclass
class PhysicalSurface(Template):
    """
    two-dimensional boundary of three-dimensional object
    """

    TypeOfPhysicalSurface: str  # brick wall, marble floor, wood wall


@dataclass
class PhysicalSurface(Template):
    """
    two-dimensional boundary of three-dimensional object
    """

    TypeOfPhysicalSurface: str  # brick wall, marble floor, wood wall


@dataclass
class Animal(Template):
    """
    kingdom of multicellular eukaryotic organisms
    """

    TypeOfAnimal: str  # dog, giraffe, cat, horse, fish, elephant


@dataclass
class MythicalAnimal(Template):
    """
    creature in mythology and religion
    """

    TypeOfMythicalAnimal: str  # pegasus, sphinx, centaur


@dataclass
class Food(Template):
    """
    any substance consumed to provide nutritional support for the body
    """

    TypeOfMythicalAnimal: str  # bread, peach, plums, brioche


@dataclass
class PhysicalObject(Template):
    """
    singular aggregation of substance(s), with overall properties such as mass, position, or momentum
    """

    TypeOfPhysicalObject: str  # viola da gamba, sword, chair


@dataclass
class Plant(Template):
    """
    living thing in the kingdom of photosynthetic eukaryotes
    """

    TypeOfPlant: str  # Iris, tree, cactus, acanthus


ENTITY_DEFINITIONS: List[Template] = [
    ArtisticTheme,
    Composition,
    WorkOfArt,
    Concept,
    RhetoricalDevice,
    Emotion,
    Quality,
    Color,
    PointInTime,
    Season,
    Person,
    MythicalCharacter,
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


def ArtisticTheme_relation_to_triplet(package: ArtisticTheme):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has artistic theme",
                "wikidata_id": "wdt:Q1406161",
            },
            "object": {
                "label": package.theme,
            },
        }
    ]

    return triplets


def Composition_relation_to_triplet(package: Composition):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has composition",
                "wikidata_id": "wdt:Q462437",
            },
            "object": {
                "label": package.CompositionOfArtwork,
            },
        }
    ]

    return triplets


def WorkOfArt_relation_to_triplet(package: WorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is work of art",
                "wikidata_id": "wdt:Q838948",
            },
            "object": {
                "label": package.work,
            },
        }
    ]

    return triplets


def Concept_relation_to_triplet(package: Concept):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has concept",
                "wikidata_id": "wdt:Q151885",
            },
            "object": {
                "label": package.ConceptOfArtwork,
            },
        }
    ]

    return triplets


def RhetoricalDevice_relation_to_triplet(package: RhetoricalDevice):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has rhetorical device",
                "wikidata_id": "wdt:Q1762471",
            },
            "object": {
                "label": package.device,
            },
        }
    ]

    return triplets


def Emotion_relation_to_triplet(package: Emotion):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "includes emotion",
                "wikidata_id": "wdt:Q9415",
            },
            "object": {
                "label": package.TypeOfEmotion,
            },
        }
    ]

    return triplets


def Quality_relation_to_triplet(package: Quality):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has quality",
                "wikidata_id": "wdt:Q185957",
            },
            "object": {
                "label": package.TypeOfQuality,
            },
        }
    ]

    return triplets


def Color_relation_to_triplet(package: Color):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has color",
                "wikidata_id": "wdt:Q1075",
            },
            "object": {
                "label": package.TypeOfColor,
            },
        }
    ]

    return triplets


def PointInTime_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has point in time",
                "wikidata_id": "wdt:Q186408",
            },
            "object": {
                "label": package.TypeOfPointInTime,
            },
        }
    ]

    return triplets


def Season_relation_to_triplet(package: Season):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has season",
                "wikidata_id": "wdt:Q10688145",
            },
            "object": {
                "label": package.TypeOfSeason,
            },
        }
    ]

    return triplets


def Person_relation_to_triplet(package: Person):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has person",
                "wikidata_id": "wdt:Q215627",
            },
            "object": {
                "label": package.TypeOfPerson,
            },
        }
    ]

    return triplets


def MythicalCharakter_relation_to_triplet(package: MythicalCharacter):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has mythical character",
                "wikidata_id": "wdt:Q215627",
            },
            "object": {
                "label": package.TypeOfMythicalCharacter,
            },
        }
    ]

    return triplets


def ReligiousCharacter_relation_to_triplet(package: ReligiousCharacter):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has religious character",
                "wikidata_id": "wdt:Q18563354",
            },
            "object": {
                "label": package.TypeOfReligiousCharacter,
            },
        }
    ]

    return triplets


def AnatomicalStructure_relation_to_triplet(package: AnatomicalStructure):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has anatomical structure",
                "wikidata_id": "wdt:Q4936952",
            },
            "object": {
                "label": package.TypeOfAnatomicalStructure,
            },
        }
    ]

    return triplets


def Occupation_relation_to_triplet(package: Occupation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has occupation",
                "wikidata_id": "wdt:Q12737077",
            },
            "object": {
                "label": package.TypeOfOccupation,
            },
        }
    ]

    return triplets


def Posture_relation_to_triplet(package: Posture):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has posture",
                "wikidata_id": "wdt:Q8514257",
            },
            "object": {
                "label": package.TypeOfPosture,
            },
        }
    ]

    return triplets


def ArchitecturalStructure_relation_to_triplet(package: ArchitecturalStructure):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has architecture",
                "wikidata_id": "wdt:Q811979",
            },
            "object": {
                "label": package.TypeOfArchitecturalStructure,
            },
        }
    ]

    return triplets


def GeographicalFeature_relation_to_triplet(package: GeographicalFeature):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has geographical feature",
                "wikidata_id": "wdt:Q618123",
            },
            "object": {
                "label": package.TypeOfGeographicalFeature,
            },
        }
    ]

    return triplets


def MythicalLocation_relation_to_triplet(package: MythicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has mythical location",
                "wikidata_id": "wdt:Q3238337",
            },
            "object": {
                "label": package.TypeOfMythicalLocation,
            },
        }
    ]

    return triplets


def PhysicalLocation_relation_to_triplet(package: PhysicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has physical location",
                "wikidata_id": "wdt:Q17334923",
            },
            "object": {
                "label": package.TypeOfPhysicalLocation,
            },
        }
    ]

    return triplets


def PhysicalSurface_relation_to_triplet(package: PhysicalSurface):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has physical surface",
                "wikidata_id": "wdt:Q3783831",
            },
            "object": {
                "label": package.TypeOfPhysicalSurface,
            },
        }
    ]

    return triplets


def Animal_relation_to_triplet(package: Animal):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is animal",
                "wikidata_id": "wdt:Q729",
            },
            "object": {
                "label": package.TypeOfAnimal,
            },
        }
    ]

    return triplets


def MythicalAnimal_relation_to_triplet(package: MythicalAnimal):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is mythical animal",
                "wikidata_id": "wdt:Q24334299",
            },
            "object": {
                "label": package.TypeOfMythicalAnimal,
            },
        }
    ]

    return triplets


def Food_relation_to_triplet(package: Food):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is food",
                "wikidata_id": "wdt:Q2095",
            },
            "object": {
                "label": package.TypeOfFood,
            },
        }
    ]

    return triplets


def PhysicalObject_relation_to_triplet(package: PhysicalObject):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is physical object",
                "wikidata_id": "wdt:Q223557",
            },
            "object": {
                "label": package.TypeOfPhysicalObject,
            },
        }
    ]

    return triplets


def Plant_relation_to_triplet(package: Plant):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is plant",
                "wikidata_id": "wdt:Q756",
            },
            "object": {
                "label": package.TypeOfPlant,
            },
        }
    ]

    return triplets


ENTITY_PARSER = {
    ArtisticTheme.__name__: ArtisticTheme_relation_to_triplet,
    Composition.__name__: Composition_relation_to_triplet,
    WorkOfArt.__name__: WorkOfArt_relation_to_triplet,
    Concept.__name__: Concept_relation_to_triplet,
    RhetoricalDevice.__name__: RhetoricalDevice_relation_to_triplet,
    Emotion.__name__: Emotion_relation_to_triplet,
    Quality.__name__: Quality_relation_to_triplet,
    Color.__name__: Color_relation_to_triplet,
    PointInTime.__name__: PointInTime_relation_to_triplet,
    Season.__name__: Season_relation_to_triplet,
    Person.__name__: Person_relation_to_triplet,
    MythicalCharacter.__name__: MythicalCharakter_relation_to_triplet,
    ReligiousCharacter.__name__: ReligiousCharacter_relation_to_triplet,
    AnatomicalStructure.__name__: AnatomicalStructure_relation_to_triplet,
    Occupation.__name__: Occupation_relation_to_triplet,
    Posture.__name__: Posture_relation_to_triplet,
    ArchitecturalStructure.__name__: ArchitecturalStructure_relation_to_triplet,
    MythicalLocation.__name__: MythicalCharakter_relation_to_triplet,
    PhysicalLocation.__name__: PhysicalLocation_relation_to_triplet,
    PhysicalSurface.__name__: PhysicalLocation_relation_to_triplet,
    Animal.__name__: Animal_relation_to_triplet,
    MythicalAnimal.__name__: MythicalAnimal_relation_to_triplet,
    Food.__name__: Food_relation_to_triplet,
    PhysicalObject.__name__: PhysicalObject_relation_to_triplet,
    Plant.__name__: Plant_relation_to_triplet,
}
