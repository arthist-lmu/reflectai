from typing import List, Dict

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
    A long describtion of the depicted scene, i.e. The painting shows a smiling woman with a 
    green landscape in the background.
    """
    description: str


@dataclass
class PaintingDepictsPerson(Template):
    """A person mentioned in the painting, if no name is mentioned then the general terms like woman, man,
    person or child etc. are sufficient. If other attributes are mentioned that are associated with a person,
    such as clothing, posture or visual characteristics, these should also be extracted.
    """

    painting: str  # The name of the painting, i.e. Mona Lisa
    name: str  # The name of the person shown in the painting, i.e. Lisa del Giocondo
    clothing: List[str]  # List of mentioned clothes or outfits worn by this person
    posture: str  # A posture of the person when mentioned, such as sitting, lying or standing


@dataclass
class PaintingDepictsBuilding(Template):
    """A building mentioned in the painting, if no name is mentioned then the general terms like well, bridge,
    tower, house, castle etc. is sufficient.
    """

    painting: str  # The name of the painting, i.e. Mona Lisa
    building: str  # The name of the mentioned building in the painting


@dataclass
class PaintingDepictsAnimal(Template):
    """A animal mentioned in the painting, if no name is mentioned then the general terms like dog, cat, horse etc. is sufficient."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    animal: str  # The name of the mentioned animal in the painting


@dataclass
class PaintingDepictsLandmark(Template):
    """A landmark mentioned in the painting, if no name is mentioned then the general terms like mountain, river, forest, tree etc. is sufficient."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    landmark: (
        str  # The name of the mentioned landmark in the painting, i.e. mountain, river
    )


@dataclass
class PaintingDepictsItem(Template):
    """A generice item mentioned that should be part of the painting, like chair, flower, bread, table, flower and so on."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    item: str  # The name of the mentioned item in the painting, i.e. bread


ENTITY_DEFINITIONS: List[Template] = [
    PaintingMaterial,
    PaintingSubject,
    PaintingSceneDescription,
    PaintingDepictsPerson,
    PaintingDepictsBuilding,
    PaintingDepictsAnimal,
    PaintingDepictsLandmark,
    PaintingDepictsItem,
]


def painting_subject_to_triplet(package: PaintingSubject):
    triplets = []

    if package.subject is not None and len(package.subject) > 1:
        triplets.append(
            {
                "subject": {
                    "label": package.painting,
                },
                "relation": {
                    "label": "main subject",
                    "wikidata_id": "wdt:P921",
                },
                "object": {
                    "label": package.subject,
                },
            }
        )

    return triplets


def painting_scene_description_to_triplet(package: PaintingSceneDescription):
    triplets = []

    if package.description is not None and len(package.description) > 1:
        triplets.append(
            {
                "subject": {
                    "label": package.painting,
                },
                "relation": {
                    "label": "description",
                    "wikidata_id": "schema:description",
                },
                "object": {
                    "label": package.description,
                },
            }
        )

    return triplets


def painting_material_to_triplet(package: PaintingMaterial):
    triplets = []

    if package.material is not None and len(package.material) > 1:
        triplets.append(
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
        )

    return triplets


def painting_depicts_person_to_triplet(package: PaintingDepictsPerson):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.name,
            },
        },
        {
            "subject": {
                "label": package.name,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "human",
                "wikidata_id": "wd:Q5",
            },
        },
    ]

    # clothing
    if package.clothing and isinstance(package.clothing, (list, set)):
        triplets.extend(
            [
                {
                    "subject": {
                        "label": package.name,
                    },
                    "relation": {
                        "label": "wears",
                        "wikidata_id": "wdt:P3828",
                    },
                    "object": {
                        "label": c,
                    },
                }
                for c in package.clothing
            ]
        )

    if package.posture:
        triplets.append(
            {
                "subject": {
                    "label": package.name,
                },
                "relation": {
                    "label": "expression, gesture or body pose",
                    "wikidata_id": "wdt:P6022",
                },
                "object": {
                    "label": package.posture,
                },
            },
        )
    return triplets


def painting_depicts_landmark_to_triplet(package: PaintingDepictsLandmark):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.landmark,
            },
        },
        {
            "subject": {
                "label": package.landmark,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "landmark",
                "wikidata_id": "wd:Q4895393",
            },
        },
    ]

    return triplets


def painting_depicts_item_to_triplet(package: PaintingDepictsItem):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.item,
            },
        },
        {
            "subject": {
                "label": package.item,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "landmark",
                "wikidata_id": "wd:Q4895393",
            },
        },
    ]

    return triplets


ENTITY_PARSER: Dict = {
    PaintingSubject.__name__: painting_subject_to_triplet,
    PaintingSceneDescription.__name__: painting_scene_description_to_triplet,
    PaintingDepictsPerson.__name__: painting_depicts_person_to_triplet,
    PaintingMaterial.__name__: painting_material_to_triplet,
    PaintingDepictsLandmark.__name__: painting_depicts_landmark_to_triplet,
    PaintingDepictsItem.__name__: painting_depicts_item_to_triplet,
}
