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
    
    """



ENTITY_DEFINITIONS: List[Template] = [
    ArtGenre,
    ArtMaterial,
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


ENTITY_PARSER = {
    ArtGenre.__name__: ArtGenre_relation_to_triplet,
    ArtMaterial.__name__: ArtMaterial_relation_to_triplet,
    ArtMovement.__name__: ArtMovement_relation_to_triplet,
}
