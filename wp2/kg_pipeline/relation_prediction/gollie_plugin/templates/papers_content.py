from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class NamesMentioned(Template):
    """Each distinct person, or set of people, mentioned in a document refers to an entity of type Person. For example, people may be specified by name ("John Smith"), occupation ("the butcher"), family relation ("mum"), pronoun ("they"), etc., or by some combination of these.
    """

    name: str  # The name of the person mentioned in the article

@dataclass
class ArtistsMentioned(Template):
    """Names of other artists that are mentioned in the article. 
    """

    name: str  # The name of the mentioned artists i.e. Leonardo da Vinci, Michelangelo, van Gogh

@dataclass
class MuseumsMentioned(Template):
    """Names of museums that are mentioned in the article. Museums are places and locations that collect artworks.
    """

    name: str  # The name of the museum, i.e. Louvre, Tate Gallery, Smithsonian

@dataclass
class ArtworksMentioned(Template):
    """
    …
    """

    name: str  # The name of the artworks mentioned in the text like



ENTITY_DEFINITIONS: List[Template] = [
    NamesMentioned,
    ArtistsMentioned,
    ArtworksMentioned,
    MuseumsMentioned,
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