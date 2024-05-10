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

@dataclass
class ReligiousFigures(Template):
    """Religious Figrues depicted in the painting"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    figure: list  # The figures depicted in the painting, i.e. Jesus, Mary Magdalene, Angel etc.


ENTITY_DEFINITIONS: List[Template] = [
    Attributes,
    ReligiousFigures,
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

def ReligiousFigures_relation_to_triplet(package: Attributes):
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
                "label": package.figure,
            },
        }
    ]

    return triplets

ENTITY_PARSER = {
    Attributes.__name__: Attributes_relation_to_triplet,
    ReligiousFigures.__name__: ReligiousFigures_relation_to_triplet
}
