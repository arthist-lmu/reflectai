from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class PaintingMaterial(Template):
    """The material of a painting like oil painting on canvas"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    material: str  # The material of a painting, i.e. oil on canvas


@dataclass
class PaintingSubject(Template):
    """Main Subject of a painting."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    subject: str  # The main subject of the painting


@dataclass
class PaintingSceneDescription(Template):
    """A long description of the depicted scene in the painting."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    """
    A long describtion of the depicted scene, i.e. The picture shows a smiling woman with a 
    green landscape in the background.
    """
    description: str


@dataclass
class PaintingDepictsPerson(Template):
    """A person mentioned in the picture, if no name is mentioned then the general terms like woman, man,
    person or child etc. are sufficient. If other attributes are mentioned that are associated with a person,
    such as clothing, posture or visual characteristics, these should also be extracted.
    """

    painting: str  # The name of the painting, i.e. Mona Lisa
    name: str  # The name of the person shown in the painting, i.e. Lisa del Giocondo
    clothing: List[str]  # List of mentioned clothes or outfits worn by this person
    posture: str  # A posture of the person when mentioned, such as sitting, lying or standing
    """
    A list of attributes that describe the person, such as hair length, hair color, body proportions
    """
    attributes: List[str]


ENTITY_DEFINITIONS: List[Template] = [
    PaintingMaterial,
    PaintingSubject,
    PaintingDepictsPerson,
]
