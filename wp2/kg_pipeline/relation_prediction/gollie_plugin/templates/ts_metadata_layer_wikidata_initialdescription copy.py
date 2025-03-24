from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

@dataclass
class ArtGenre(Template):
    """
    Art Genre is a form of art defined by its medium, format, or overarching theme.
    """

    genre: str  # Pre-Impressionism, 19th-century style, Romanticism, Symbolism, Futurism


@dataclass
class ArtMaterial(Template):
    """
    Art Material is a substance, ingredient, or tool utilized by an artist to create a work of art.
    """

    material: str  # Oil on canvas, charcoal on paper, bronze sculpture, digital photography, woodcut print


@dataclass
class ArtMovement(Template):
    """
    Art Movement is a tendency or style in art with a shared philosophy, aesthetic principles, or historical period.
    """

    movement: str  # Cubism, Renaissance, Baroque, Historicism, Surrealism


@dataclass
class ArtisticTechnique(Template):
    """
    Artistic Technique is a method or process used to create a work of art.
    """

    technique: str  # Etching, impasto, wet-on-wet painting, chiaroscuro, stippling


@dataclass
class TypeOfWork(Template):
    """
    Type of Work is a category of artwork based on shared characteristics, function, or stylistic features.
    """

    type: str  # Painting, sculpture, oil painting, marble sculpture, lithograph


@dataclass
class WorkOfArt(Template):
    """
    Work of Art is an aesthetic item or artistic creation.
    """

    work: str  # Mona Lisa, The Sistine Chapel Ceiling, The Persistence of Memory, The Birth of Venus


@dataclass
class PointInTime(Template):
    """
    Point in Time is a particular instant in time.
    """

    point: str  # 1495, 20th century, the Baroque period, the Dutch Golden Age


@dataclass
class StartTime(Template):
    """
    Start Time is the beginning of a temporal interval.
    """

    start: str  # 1508, 1917, early Renaissance, 14th century


@dataclass
class EndTime(Template):
    """
    End Time is the end of a temporal interval.
    """

    end: str  # 1512, 1945, late Baroque, 19th century


@dataclass
class Person(Template):
    """
    Person is a human figure.
    """

    person: str  # Michelangelo, Leonardo da Vinci, Frida Kahlo, Artemisia Gentileschi, Vincent van Gogh


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
                "label": package.genre,
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
                "label": package.material,
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
                "label": package.movement,
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
                "label": package.technique,
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
                "label": package.type,
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
                "label": package.work,
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
                "label": package.point,
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
                "label": package.start,
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
                "label": package.end,
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
                "label": package.person,
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
