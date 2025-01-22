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
class StartTime(Template):
    """
    start of a temporal interval
    """

    type: str  # Date of a Start Time like 1508 or 1512


@dataclass
class EndTime(Template):
    """
    end of a temporal interval
    """

    type: str  # Date of an End Time like 1508 or 1512


@dataclass
class Person(Template):
    """
    being that has certain capacities or attributes constituting personhood
    """

    type: str  # Full names like Michelangelo or Leonardo da Vinci, as well as historical figures mentioned


ENTITY_DEFINITIONS: List[Template] = [
    ArtisticTheme,
    Composition,
    WorkOfArt,
    Concept,
    RhetoricalDevice,
    Emotion,
    Quality,
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


def StartTime_relation_to_triplet(package: StartTime):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "art movement",
                "wikidata_id": "wdt:Q24575110",
            },
            "object": {
                "label": package.StartTime,
            },
        }
    ]

    return triplets


def EndTime_relation_to_triplet(package: EndTime):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "art movement",
                "wikidata_id": "wdt:Q24575125",
            },
            "object": {
                "label": package.EndTime,
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
                "label": "art movement",
                "wikidata_id": "wdt:Q215627",
            },
            "object": {
                "label": package.Person,
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
    StartTime.__name__: StartTime_relation_to_triplet,
    EndTime.__name__: EndTime_relation_to_triplet,
    Person.__name__: Person_relation_to_triplet,
}
