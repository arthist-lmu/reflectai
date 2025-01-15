from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class ArtGenre(Template):
    """
    form of art in terms of a medium, format, or theme
    """

    genre: str  # Genre like pre-impressionistic or 19th-century style


@dataclass
class ArtMaterial(Template):
    """
    substance, raw ingredient, or tool that is utilized by an artist to create a work of art
    """

    material: str  # Material such as Oil on Canvas, Drawing, Photography, Woodcut


@dataclass
class ArtMovement(Template):
    """
    tendency or style in art with a specific common philosophy or goal, possibly associated with a specific historical period
    """

    movement: str  # Movement like Cubism, Renaissance, Baroque or Historicism


@dataclass
class ArtisticTechnique(Template):
    """
    method by which art is produced
    """

    technique: str  # Technique like etching, impasto,wet paint


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
    ArtGenre,
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


def ArtGenre_relation_to_triplet(package: ArtGenre):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has genre",
                "wikidata_id": "wdt:Q1792379",
            },
            "object": {
                "label": package.ArtGenre,
            },
        }
    ]

    return triplets


def ArtMaterial_relation_to_triplet(package: ArtMaterial):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "material",
                "wikidata_id": "wdt:Q15303351",
            },
            "object": {
                "label": package.ArtMaterial,
            },
        }
    ]

    return triplets


def ArtMovement_relation_to_triplet(package: ArtMovement):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "art movement",
                "wikidata_id": "wdt:Q968159",
            },
            "object": {
                "label": package.ArtMovement,
            },
        }
    ]

    return triplets


def ArtisticTechnique_relation_to_triplet(package: ArtisticTechnique):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "art movement",
                "wikidata_id": "wdt:Q11177771",
            },
            "object": {
                "label": package.ArtisticTechnique,
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
    ArtGenre.__name__: ArtGenre_relation_to_triplet,
    ArtMaterial.__name__: ArtMaterial_relation_to_triplet,
    ArtMovement.__name__: ArtMovement_relation_to_triplet,
    ArtisticTechnique.__name__: ArtisticTechnique_relation_to_triplet,
    TypeOfWork.__name__: TypeOfWork_relation_to_triplet,
    WorkOfArt.__name__: WorkOfArt_relation_to_triplet,
    PointInTime.__name__: PointInTime_relation_to_triplet,
    StartTime.__name__: StartTime_relation_to_triplet,
    EndTime.__name__: EndTime_relation_to_triplet,
    Person.__name__: Person_relation_to_triplet,
}
