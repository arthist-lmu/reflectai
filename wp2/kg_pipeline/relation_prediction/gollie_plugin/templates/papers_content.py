from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class NamesMentioned(Template):
    """Names of people, researchers, artists, writer, philosophers or other people which are mentioned in the article. They could be quoted or
    cited in order to enrich the text.
    """

    name: str  # The name of the researcher, artist, writer, philosopher who was quoted in the article


@dataclass
class ArtworksMentioned(Template):
    """
    …
    """

    name: str  # The name of the artworks mentioned in the text like



ENTITY_DEFINITIONS: List[Template] = [
    NamesMentioned,
    ArtworksMentioned,
]


ENTITY_PARSER = {}

def name_mentioned_relation_to_triplet(package: NamesMentioned):
    triplets = [
        {
            "subject": {
                "label": package.paper,
            },
            "relation": {
                "label": "cites",
                "wikidata_id": "P2860",
            },
            "object": {
                "label": package.mentioned,
            },
        }
    ]

    return triplets