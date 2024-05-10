from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class CreatorRelation(Template):
    """The name or pseudonym of the painter that created the painting. The creator is involved in the conception and creation of artwork
    through various techniques and mediums including oil, acrylic, watercolor, frescoes, and more.
    Their work is not limited to just creating paintings; many painters also delve into the realms of
    drawing, sculpting, and other forms of visual art expressions.
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

@dataclass
class AliasNames(Template):
    """Alias names for artworks refer to alternative titles or nicknames that a piece of art
    may acquire beyond its official title. These alternative names often arise from the
    public, critics, or the artists themselves and can reflect popular interpretations,
    striking features, or emotional responses elicited by the artwork."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    alias: List[str]  # The alias name of a painting, i.e. La Gioconda


@dataclass
class TitleLanguages(Template):
    """Names of artworks in different languages represent the various translations or
    adaptations of an artwork's title across cultural and linguistic boundaries."""

    painting: str  # The name of the painting, i.e. The Scream
    GermanName: str  # The German name of a painting, Der Schrei
    FrenchName: str  # The French name of a painting, Le Cri
    EnglishName: str  # The English name of painting, The Scream



ENTITY_DEFINITIONS: List[Template] = [
    #CreatorRelation,
    #LocationCreationRelation,
    InceptionRelation,
    PaintingMaterial,
    PaintingGenre,
    #AliasNames,
    #TitleLanguages,
    #MovementRelation,
    LocationDisplayed,
]

'''
def creator_relation_to_triplet(package: CreatorRelation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "creator",
                "wikidata_id": "",
            },
            "object": {
                "label": package.creator,
            },
        }
    ]

    return triplets


def location_creation_relation_to_triplet(package: LocationCreationRelation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "location",
                "wikidata_id": "",
            },
            "object": {
                "label": package.location,
            },
        }
    ]

    return triplets


def inception_relation_to_triplet(package: InceptionRelation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "inception",
                "wikidata_id": "",
            },
            "object": {
                "label": package.year,
            },
        }
    ]

    return triplets


def painting_genre_to_triplet(package: PaintingGenre):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "genre",
                "wikidata_id": "",
            },
            "object": {
                "label": package.genre,
            },
        }
    ]

    return triplets



ENTITY_PARSER = {
    CreatorRelation.__name__: creator_relation_to_triplet,
    LocationCreationRelation.__name__: location_creation_relation_to_triplet,
    InceptionRelation.__name__: inception_relation_to_triplet,
    PaintingGenre.__name__: painting_genre_to_triplet,
}
'''

ENTITY_PARSER = {}

