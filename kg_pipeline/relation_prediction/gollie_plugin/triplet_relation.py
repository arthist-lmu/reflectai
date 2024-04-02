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
    """Name of the painter of a painting."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    depicts: str  # The name of an object shown in the painting


ENTITY_DEFINITIONS: List[Template] = [
    InceptionRelation,
    CreatorRelation,
    PaintingDepictsRelation,
]
