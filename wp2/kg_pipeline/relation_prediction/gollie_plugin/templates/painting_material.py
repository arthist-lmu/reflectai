from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class PaintingMaterial(Template):
    """The material of a painting mentioned in the article like oil painting on canvas"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    material: str  # The material of a painting, i.e. oil on canvas


@dataclass
class PaintingGenre(Template):
    """The genre of a painting like abstract, portrait, still life or landscape"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    genre: str  # The genre of a painting, i.e. portrait, landscape

@dataclass
class Movement(Template):
    """The movement with which the painting is associated. An artistic movement is a style or tendency in art with a specific common philosophy or
    goal, followed by a group of artists during a restricted period of time. Artistic movements are usually characterized by a distinctive style
    or technique that emerges as a reaction to preceding art forms, social conditions, or artistic philosophies.
    """

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    movement: str  # The name of the movement, i.e. Renaissance, Impressionism, Kubism, Expressionism

ENTITY_DEFINITIONS: List[Template] = [
    PaintingMaterial,
    PaintingGenre,
    Movement,
]


def painting_material_relation_to_triplet(package: PaintingMaterial):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "made from material",
                "wikidata_id": "P186",
            },
            "object": {
                "label": package.material,
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

def Movement_to_triplet(package: Movement):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "movement",
                "wikidata_id": "P135",
            },
            "object": {
                "label": package.movement,
            },
        }
    ]

    return triplets



ENTITY_PARSER = {
    PaintingMaterial.__name__: painting_material_relation_to_triplet,
    PaintingGenre.__name__: painting_genre_to_triplet,
    Movement.__name__: Movement_to_triplet,
}
