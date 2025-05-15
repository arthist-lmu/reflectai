from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  # ignoring most if not all the meta data relations
"""


@dataclass
class ArtGenre(Template):
    """
    Form of art in terms of a medium, format, or theme
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    ArtGenre: str  # pre-impressionistic, 19th-century style


def ArtGenre_relation_to_triplet(package: ArtGenre):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "has genre",
                "wikidata_id": "wdt:P921",  # rather than "wdt:P136",
            },
            "object": {
                "label": package.ArtGenre,
            },
        },
        {
            "subject": {
                "label": package.ArtGenre,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art genre",
                "wikidata_id": "wd:Q1792379",
            },
        },
    ]

    return triplets


@dataclass
class ArtMovement(Template):
    """
    tendency or style in art with a specific common philosophy or goal, possibly associated with a specific historical period
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    movement: str  # Cubism


def ArtMovement_relation_to_triplet(package: ArtMovement):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "has movement",
                "wikidata_id": "wdt:P135",  # closest I could find
            },
            "object": {
                "label": package.movement,
            },
        },
        {
            "subject": {
                "label": package.movement,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art movement",
                "wikidata_id": "wd:Q968159",
            },
        },
    ]

    return triplets


@dataclass
class ArtMaterial(Template):
    """
    substance, raw ingredient, or tool that is utilized by an artist to create a artwork of art
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    material: str  # oil on canvas


def ArtMaterial_relation_to_triplet(package: ArtMaterial):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {"label": "made from material", "wikidata_id": "wdt:P186"},
            "object": {
                "label": package.material,
            },
        },
        {
            "subject": {
                "label": package.material,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art material",
                "wikidata_id": "wd:Q15303351",
            },
        },
    ]

    return triplets


@dataclass
class ArtisticTechnique(Template):
    """
    method by which art is produced
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    fabricated: str  # wet paint,


def ArtisticTechnique_relation_to_triplet(package: ArtisticTechnique):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "fabricated by",
                # "wikidata_id": "wdt:P186" has no obvious relation
            },
            "object": {
                "label": package.fabricated,
            },
        },
        {
            "subject": {
                "label": package.fabricated,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art material",
                "wikidata_id": "wd:Q11177771",
            },
        },
    ]

    return triplets


@dataclass
class TypeOfWorkOfArt(Template):
    """
    type of art artwork based on shared characteristics, functions, or stylistic features
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    instance: str  # engraving


def TypeOfWorkOfArt_relation_to_triplet(package: TypeOfWorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "instance of",  ### HERE THIS MIGHT NOT BE THE RELATION THAT WE WANT
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": package.instance,
            },
        },
        {
            "subject": {
                "label": package.instance,
            },
            "relation": {
                "label": "instance of",  ### OR HERE WE NEED TO USE SUBCLASS INSTEAD
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "type of artwork of art",
                "wikidata_id": "wd:Q116474095",
            },
        },
    ]

    return triplets


@dataclass
class PointInTime(Template):
    """
    position of a particular instant in time
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str  # 1502, 1370, 2010, 1875


def PointInTime_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "created in",  ### or inception
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "point in time",
                "wikidata_id": "wd:Q186408",
            },
        },
    ]

    return triplets


@dataclass
class StartTime(Template):
    """
    infimum of a temporal interval
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str  # 1502, 1370, 2010, 1875


def StartTime_relation_to_triplet(package: StartTime):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "created in",  ### or inception
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "start time",
                "wikidata_id": "wd:Q24575110",
            },
        },
    ]

    return triplets


@dataclass
class EndTime(Template):
    """
    time that some temporal entity ceases to exist
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str  # 1502, 1370, 2010, 1875


def EndTime_relation_to_triplet(package: EndTime):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "created in",  ### or inception
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "end time",
                "wikidata_id": "wd:Q24575125",
            },
        },
    ]

    return triplets


@dataclass
class Person(Template):
    """
    being that has certain capacities or attributes constituting personhood
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    person: str  # Massys, sitter, Karl Wittgenstein
    influenced: str  # Massys, sitter, Karl Wittgenstein


def Person_relation_to_triplet(package: Person):
    ### should we rather split those up?
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "created by",
                "wikidata_id": "wdt:P170",
            },
            "object": {
                "label": package.person,
            },
        },
        {
            "subject": {
                "label": package.person,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person",  # or human
                "wikidata_id": "wd:Q5",  # instead of "wd:Q215627", since that is what wikidata says
            },
        },
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "influenced by",
                "wikidata_id": "wdt:P737",
            },
            "object": {
                "label": package.influenced,
            },
        },
        {
            "subject": {
                "label": package.influenced,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person",  # or human
                "wikidata_id": "wd:Q5",  # instead of "wd:Q215627", since that is what wikidata says
            },
        },
    ]

    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    ArtGenre,
    ArtMovement,
    ArtMaterial,
    ArtisticTechnique,
    TypeOfWorkOfArt,
    PointInTime,
    StartTime,
    EndTime,
    Person,
]

ENTITY_PARSER = {
    "ArtGenre": ArtGenre_relation_to_triplet,
    "ArtMovement": ArtMovement_relation_to_triplet,
    "ArtMaterial": ArtMaterial_relation_to_triplet,
    "ArtisticTechnique": ArtisticTechnique_relation_to_triplet,
    "TypeOfWorkOfArt": TypeOfWorkOfArt_relation_to_triplet,
    "PointInTime": PointInTime_relation_to_triplet,
    "StartTime": StartTime_relation_to_triplet,
    "EndTime": EndTime_relation_to_triplet,
    "Person": Person_relation_to_triplet,
}
