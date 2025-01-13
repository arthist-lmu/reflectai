from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class CreatorRelation(Template):
    """The name or pseudonym of the painter that created the painting. The creator is involved in 
    the conception and creation of artwork through various techniques and mediums including oil, 
    acrylic, watercolor, frescoes, and more.Their work is not limited to just creating paintings; 
    many painters also delve into the realms of drawing, sculpting, and other forms of visual 
    art expressions.
    """

    painting: str  # The name of the painting, Such as Mona Lisa, Starry Night, Guernica, The Scream
    creator: str  # The name of the painter, i.e. Leonardo da Vinci, Vincent van Gogh, Pablo Picasso, Edvard Munch
    workshop: str  # The name of the workshop

@dataclass
class LocationCreationRelation(Template):
    """The name of the location where the painting was created"""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    location: str  # The name of the location, i.e. Florence, Provence, Paris, Oslo


@dataclass
class InceptionRelation(Template):
    """The Year when an painting was painted or created. The creation date of a painting refers to the specific year or range of years
    during which the artwork was produced."""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    date: int  # The year in which the picture was painted or created


ENTITY_DEFINITIONS: List[Template] = [
    CreatorRelation,
    LocationCreationRelation,
    InceptionRelation,
]

def creator_relation_to_triplet(package: CreatorRelation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "creator",
                "wikidata_id": "wdt:P170",
            },
            "object": {
                "label": package.creator,
            },
        }
    ]

    return triplets


#def location_creation_relation_to_triplet(package: LocationCreationRelation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "location of creation",
                "wikidata_id": "wdt:P1071",
            },
            "object": {
                "label": package.location,
            },
        }
    ]

    return triplets


def inception_relation_to_triplet(package: InceptionRelation):
    date = package.date
    if isinstance(package.date, int):
        date = str(package.date)

    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "inception",
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": date,
            },
        }
    ]

    return triplets


ENTITY_PARSER = {
    CreatorRelation.__name__: creator_relation_to_triplet,
    #LocationCreationRelation.__name__: location_creation_relation_to_triplet,
    InceptionRelation.__name__: inception_relation_to_triplet,
}
