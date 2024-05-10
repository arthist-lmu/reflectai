from typing import List, Dict

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

@dataclass
class MuseumsMentioned(Template):
    """A museum that is mentioned in the article
    """

    name: str  # The name of the museum mentioned
    location: str # The location of the museum

@dataclass
class AuctionHousesMentioned(Template):
    """An auction house that is mentioned in the article
    """

    name: str  # The name of the auctionhouse mentioned
    location: str # The location of the auctionhouse
    


ENTITY_DEFINITIONS: List[Template] = [
    MuseumsMentioned,
    AuctionHousesMentioned,
]

def name_mentioned_relation_to_triplet(package: MuseumsMentioned) -> List:
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "displayed",
                "wikidata_id": "P276",
            },
            "object": {
                "label": package.museum,
            },
        }
    ]

    return triplets

ENTITY_PARSER: Dict = {
    MuseumsMentioned.__name__: name_mentioned_relation_to_triplet

}