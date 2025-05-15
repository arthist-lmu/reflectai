from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

@dataclass
class PaintingDepictedConcept(Template):
    """A depicted concept in a painting. This includes all objects, scenes, items of clothing and people."""

    painting: str  # The name of the painting, i.e. Last Supper
    depict: str  # The depicted concepts
    """
    A list of mentioned attributes of the mentioned depicted conceptes
    """
    attributes: List[str]


@dataclass
class PaintingDepicts(Template):
    """A list of concepts that have been depicted in a painting."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    depicts: List[str]  # The name of the object shown in the painting


ENTITY_DEFINITIONS: List[Template] = [
    PaintingDepictedConcept,
    PaintingDepicts,
]