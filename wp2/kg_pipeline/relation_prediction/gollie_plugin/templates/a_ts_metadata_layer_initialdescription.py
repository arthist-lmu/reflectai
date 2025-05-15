from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  
"""


@dataclass
class ArtGenre(Template):
    """
    Form of art in terms of a medium, format, or theme
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    art_genre: str  # Art Genres such as Pre-Impressionism, 19th-century style, Romanticism, Symbolism, Futurism


def art_genre_relation_to_triplet(package: ArtGenre):
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
                "label": package.art_genre,
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
    movement: str  # Art movements such as Impressionism, Dadaism, Constructivism, Rococo, Suprematism



def art_movement_relation_to_triplet(package: ArtMovement):
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
    material: str  # Art materials such as Tempera on wood, ink on rice paper, watercolor on parchment, mixed media, acrylic on linen



def art_material_relation_to_triplet(package: ArtMaterial):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "made from material", 
                "wikidata_id": "wdt:P186"
            },
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
    fabricated: str  # Artistic technique such as Sfumato, drypoint engraving, mosaic inlay, glazing, fresco


def artistic_technique_relation_to_triplet(package: ArtisticTechnique):
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
    instance: str  # Types of work of art such as fresco, print, installation, performance art, tapestry


def type_of_work_of_art_relation_to_triplet(package: TypeOfWorkOfArt):
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
    time: str  # Points in time such as 1300s, 1874, the High Renaissance, 1920s (Bauhaus period), Medieval period


def point_in_time_relation_to_triplet(package: PointInTime):
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
    time: str  # Start time such as 1420, 1860, 1919 (Bauhaus founded), 1947 (Abstract Expressionism emerges), 1780


def start_time_relation_to_triplet(package: StartTime):
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
    time: str  # End times such as 1527 (High Renaissance wanes), 1918 (end of Art Nouveau), 1970s, 1945, 1804


def end_time_relation_to_triplet(package: EndTime):
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
class PersonCreated(Template):
    """
    being that has certain capacities or attributes constituting personhood
    ### hier muss klargestellt werden, dass nur dann Entitäte extrahiert werden sollen, wenn es sich um den Künstler selber handelt. 
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    creator: str  # Persons such as Rembrandt van Rijn, Claude Monet, Kazimir Malevich, Cindy Sherman, Caravaggio


def person_created_relation_to_triplet(package: PersonCreated):
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
                "label": package.creator,
            },
        },
        {
            "subject": {
                "label": package.creator,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person",  # or human
                "wikidata_id": "wd:Q5",  # instead of "wd:Q215627", since that is what wikidata says
            },
        }
    ]

    return triplets



@dataclass
class PersonInfluenced(Template):
    """
    being that has certain capacities or attributes constituting personhood
    ### hier muss klargestellt werden, dass nur dann Entitäte extrahiert werden sollen, wenn es sich um die Person handelt, die den Künstler beeinflusst hat. 
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    influenced: str  # Persons like Rembrandt van Rijn, Claude Monet, Kazimir Malevich, Cindy Sherman, Caravaggio



def person_influenced_relation_to_triplet(package: PersonInfluenced):
    triplets = [
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
    PersonCreated,
    PersonInfluenced
]

ENTITY_PARSER = {
    "ArtGenre": art_genre_relation_to_triplet,
    "ArtMovement": art_movement_relation_to_triplet,
    "ArtMaterial": art_material_relation_to_triplet,
    "ArtisticTechnique": artistic_technique_relation_to_triplet,
    "TypeOfWorkOfArt": type_of_work_of_art_relation_to_triplet,
    "PointInTime": point_in_time_relation_to_triplet,
    "StartTime": start_time_relation_to_triplet,
    "EndTime": end_time_relation_to_triplet,
    "PersonCreated": person_created_relation_to_triplet,
    "PersonInfluenced": person_influenced_relation_to_triplet
}
