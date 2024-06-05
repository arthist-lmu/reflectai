from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

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
    PaintingGenre,
    Movement,
]

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
                "wikidata_id": "wdt:P135",
            },
            "object": {
                "label": package.movement,
            },
        }
    ]

    return triplets



ENTITY_PARSER = {
    PaintingGenre.__name__: painting_genre_to_triplet,
    Movement.__name__: Movement_to_triplet,
}
