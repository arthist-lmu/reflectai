from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class Attributes(Template):
    """Objects depicted in the painting"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    objects: list  # The objects depicted in the painting


ENTITY_DEFINITIONS: List[Template] = [
    Attributes,
]


def Attributes_relation_to_triplet(package: Attributes):
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
                "label": package.objects,
            },
        }
    ]

    return triplets

ENTITY_PARSER = {
    Attributes.__name__: Attributes_relation_to_triplet,
}
