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

    artwork: str # The name of the artwork mentioned
    name: str  # The name of the museum mentioned
    location: str # The location of the museum

@dataclass
class AuctionHousesMentioned(Template):
    """An auction house that is mentioned in the article
    """

    artwork: str # The name of the artwork mentioned
    name: str  # The name of the auctionhouse mentioned
    


ENTITY_DEFINITIONS: List[Template] = [
    MuseumsMentioned,
    AuctionHousesMentioned,
]

def museum_mentioned_to_triplet(package: MuseumsMentioned) -> List:
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
                "label": package.name,
            },
        }
    ]

    return triplets

def museum_location_to_triplet(package: MuseumsMentioned) -> List:
    triplets = [
        {
            "subject": {
                "label": package.museum,
            },
            "relation": {
                "label": "displayed",
                "wikidata_id": "P276",
            },
            "object": {
                "label": package.location,
            },
        }
    ]

    return triplets

def auctionhouse_mentioned_to_triplet(package: AuctionHousesMentioned) -> List:
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
                "label": package.name,
            },
        }
    ]

    return triplets

ENTITY_PARSER: Dict = {
    MuseumsMentioned.__name__: museum_mentioned_to_triplet,
    MuseumsMentioned.__name__: museum_location_to_triplet,
    AuctionHousesMentioned.__name__: auctionhouse_mentioned_to_triplet, 
}