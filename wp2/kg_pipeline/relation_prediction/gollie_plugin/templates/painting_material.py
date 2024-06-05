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


ENTITY_DEFINITIONS: List[Template] = [
    PaintingMaterial,
]


def painting_material_relation_to_triplet(package: PaintingMaterial):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "made from material",
                "wikidata_id": "wdt:P186",
            },
            "object": {
                "label": package.material,
            },
        }
    ]

    return triplets

ENTITY_PARSER = {
    PaintingMaterial.__name__: painting_material_relation_to_triplet,
}
