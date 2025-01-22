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
class WorkofArt(Template):
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
class TypeOfWork(Template):
    """
    type of art work based on shared characteristics, functions, or stylistic features
    """

    type: str  # Type or category like painting, sculpture, oil painting or marble sculpture


@dataclass
class WorkOfArt(Template):
    """
    aesthetic item or artistic creation
    """

    type: str  # Title or names of specific names of artworks like Mona Lisa and Sistine Chapel


@dataclass
class PointInTime(Template):
    """
    position of a particular instant in time
    """

    type: str  # Any specific date, year or period related to a work of art


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
    ArtMaterial,
    ArtMovement,
    ArtisticTechnique,
    TypeOfWork,
    WorkOfArt,
    PointInTime,
    StartTime,
    EndTime,
    Person,
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


def TypeOfWork_relation_to_triplet(package: TypeOfWork):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "art movement",
                "wikidata_id": "wdt:Q116474095",
            },
            "object": {
                "label": package.TypeOfWork,
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
                "label": "art movement",
                "wikidata_id": "wdt:Q838948",
            },
            "object": {
                "label": package.WorkOfArt,
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
                "label": "art movement",
                "wikidata_id": "wdt:Q186408",
            },
            "object": {
                "label": package.PointInTime,
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
    TypeOfWork.__name__: TypeOfWork_relation_to_triplet,
    WorkOfArt.__name__: WorkOfArt_relation_to_triplet,
    PointInTime.__name__: PointInTime_relation_to_triplet,
    StartTime.__name__: StartTime_relation_to_triplet,
    EndTime.__name__: EndTime_relation_to_triplet,
    Person.__name__: Person_relation_to_triplet,
}
