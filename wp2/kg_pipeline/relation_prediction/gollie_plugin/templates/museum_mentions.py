from typing import List

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
    year: int # The year of the artwork within in the museum

@dataclass
class AuctionHousesMentioned(Template):
    """An auction house that is mentioned in the article
    """

    name: str  # The name of the auctionhouse mentioned
    location: str # The location of the auctionhouse
    year: int # The date of the transaction with the auction house
    


ENTITY_DEFINITIONS: List[Template] = [
    MuseumsMentioned,
    AuctionHousesMentioned,
]


ENTITY_PARSER = {}

def name_mentioned_relation_to_triplet(package: NamesMentioned) -> List:
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