from typing import List

from .utils_typing import Relation, dataclass

"""
Relation definitions
"""


@dataclass
class PhysicalRelation(Relation):
    """The Physical Relation captures the physical location relation of entities such as:
    a Person entity located in a Facility, Location or GPE; or two entities that are near,
    but neither entity is a part of the other or located in/at the other."""

    arg1: str
    arg2: str


@dataclass
class PersonalSocialRelation(Relation):
    """The Personal-Social Relation describe the relationship between people. Both arguments must be entities
    of type Person. Please note: The arguments of these Relations are not ordered. The Relations are
    symmetric."""

    arg1: str
    arg2: str


ENTITY_DEFINITIONS: List[Relation] = [
    PhysicalRelation,
    PersonalSocialRelation,
]
