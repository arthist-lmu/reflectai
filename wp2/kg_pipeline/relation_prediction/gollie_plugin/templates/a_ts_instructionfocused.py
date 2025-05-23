from typing import List, Dict

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class Emotion(Template):
    """
    Identify the **emotion or mood** conveyed or depicted in a work of art.
    """

    artwork: str  # The name of the artwork mentioned (e.g., Mona Lisa, Guernica)
    emotion: str  # The specific emotion (e.g., Sadness, joy, despair, serenity)


def emotion_to_triplet(package: Emotion) -> List[Dict]:
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",  # Wikidata ID for 'depicts'
            },
            "object": {
                "label": package.emotion,
            },
        },
        {
            "subject": {
                "label": package.emotion,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "emotion",
                "wikidata_id": "wd:Q9415",  # Wikidata ID for 'emotion'
            },
        },
    ]
    return triplets


@dataclass
class Color(Template):
    """
    Identify **colors** (hues, shades, or tones) depicted as visual characteristics in a work of art.
    """

    artwork: str  # The name of the artwork mentioned (e.g., The Birth of Venus, The Starry Night)
    color: str  # The specific color (e.g., gold, ultramarine, vermilion, ochre)


def color_to_triplet(package: Color) -> List[Dict]:
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.color,
            },
        },
        {
            "subject": {
                "label": package.color,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "color",
                "wikidata_id": "wd:Q1075",  # Wikidata ID for 'color'
            },
        },
    ]
    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    Emotion,
    Color,
]

ENTITY_PARSER: Dict = {
    Emotion.__name__: emotion_to_triplet,
    Color.__name__: color_to_triplet,
}
