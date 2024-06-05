from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class Attributes(Template):
    """Objects depicted in the painting that have symbolic value like a key or a tool used for certain professions"""

    painting: str  # The name of the painting, i.e. The Last Supper
    objects: List[str]  # The objects depicted in the painting, i.e. key, sword, scale


@dataclass
class ReligiousFigures(Template):
    """Religious Figures depicted in the painting which are part of the content. These religious figures could depict scenes from the Bible or other religious sources."""

    painting: str  # The name of the painting, i.e. The Last Supper
    figure: List[str]  # The figures depicted in the painting, i.e. Jesus, Mary Magdalene, Angel etc.


@dataclass
class MythologicalFigures(Template):
    """Mythological Figures depicted in the painting which are part of the content. These figures could depict scenes from Greek and Roman Mythologies."""

    painting: str  # The name of the painting, i.e. The Last Supper
    figure: List[str]  # The figures depicted in the painting, i.e. Venus, Volcan, Jupyter


@dataclass
class Allegory(Template):
    """An allegory is a visual representation in which a character, place, or event can be interpreted to represent a meaning with moral or political significance"""

    painting: str  # The name of the painting, i.e. The Last Supper
    allegory: str  # The name of the allegory, i.e. Allegory of Fortune, Allegory of Justice, Allegory of Time


ENTITY_DEFINITIONS: List[Template] = [
    Attributes,
    ReligiousFigures,
    MythologicalFigures,
    Allegory,
]


def Attributes_relation_to_triplet(package: Attributes):
    return [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "shown with features",
                "wikidata_id": "P1354",
            },
            "object": {
                "label": object,
            },
        }
        for object in package.objects
    ]



def ReligiousFigures_relation_to_triplet(package: ReligiousFigures):

    triplets = [{
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts person",
                "wikidata_id": "P1354",
            },
            "object": {
                "label": figure,
            },
        }
        for figure in package.figure
    ]

def MythologicalFigures_relation_to_triplet(package: MythologicalFigures):
    return [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts person",
                "wikidata_id": "P1354",
            },
            "object": {
                "label": figure,
            },
        }
        for figure in package.figure
    ]


def Allegory_relation_to_triplet(package: Allegory):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts person",
                "wikidata_id": "P1354",
            },
            "object": {
                "label": x,
            },
        }
        for x in package.allegory
    ]

    return triplets


ENTITY_PARSER = {
    Attributes.__name__: Attributes_relation_to_triplet,
    ReligiousFigures.__name__: ReligiousFigures_relation_to_triplet,
    MythologicalFigures.__name__: MythologicalFigures_relation_to_triplet,
}
