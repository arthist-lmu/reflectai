from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

@dataclass
class AliasNames(Template):
    """Alias names for artworks refer to alternative titles or nicknames that a piece of art
    may acquire beyond its official title. These alternative names often arise from the
    public, critics, or the artists themselves and can reflect popular interpretations,
    striking features, or emotional responses elicited by the artwork."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    alias: List[str]  # The alias name of a painting, i.e. La Gioconda

@dataclass
class TitleLanguages(Template):
    """Names of artworks in different languages represent the various translations or
    adaptations of an artwork's title across cultural and linguistic boundaries."""

    painting: str  # The name of the painting, i.e. The Scream
    german_name: str  # The German name of a painting, Der Schrei
    french_name: str  # The French name of a painting, Le Cri
    english_name: str  # The English name of painting, The Scream



ENTITY_DEFINITIONS: List[Template] = [
    AliasNames,
    TitleLanguages,
]

def AliasNames_to_triplet(package: AliasNames):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "alias",
                "wikidata_id": "",
            },
            "object": {
                "label": alias,
            },
        }
        for alias in package.alias
    ]

    return triplets


def TitleLanguages_to_triplet(package: TitleLanguages):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "language",
                "wikidata_id": "",
            },
            "object": {
                "label": package.german_name,
            },
        }
    ]

    return triplets


ENTITY_PARSER = {
    AliasNames.__name__: AliasNames_to_triplet,
    TitleLanguages.__name__: TitleLanguages_to_triplet,
}
