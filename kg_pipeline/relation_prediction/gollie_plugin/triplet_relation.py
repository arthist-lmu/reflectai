from typing import List

from .utils_typing import Relation, dataclass
from .utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class InceptionRelation(Template):
    """Year when an painting was painted or created."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    date: int # The year in which the picture was painted or created


@dataclass
class CreatorRelation(Template):
    """Name of the painter of a painting."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    creator: str  # The name of the painter, i.e. Leonardo da Vinci


@dataclass
class PaintingDepictsRelation(Template):
    """The object the painting depicts."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    depicts: str  # The name of an object shown in the painting


@dataclass
class LocationCreationRelation(Template):
    """Name of the location the painting was created."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    creator: str  # The name of the location, i.e. Florence


@dataclass
class MovementRelation(Template):
    """The movement with which the painting is associated."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    movement: str  # The name of the movement, i.e. Renaissance


ENTITY_DEFINITIONS: List[Template] = [
    InceptionRelation,
    CreatorRelation,
    PaintingDepictsRelation,
    LocationCreationRelation,
    MovementRelation,
]
