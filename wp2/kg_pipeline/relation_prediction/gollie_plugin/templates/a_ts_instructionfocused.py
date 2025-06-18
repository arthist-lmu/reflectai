from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  # ignoring most if not all the meta data relations
"""


@dataclass
class ArtisticTheme(Template):
    """
    Identify the main **subject, story, or idea**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    theme: str  # Themes such as Adoration, Vanitas, Last Supper, Annunciation, Judgment Day, Triumph of Death


def artistic_theme_relation_to_triplet(package: ArtisticTheme):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.theme,
            },
        },
        {
            "subject": {
                "label": package.theme,
                "s_class": "ArtisticTheme",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "artistic theme",
                "wikidata_id": "wd:Q1406161",
            },
        },
    ]

    return triplets


@dataclass
class Composition(Template):
    """
    Identify the specific **elements, figures, or motifs** present in a visual composition.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    composition_of_artwork: str  # Compositions such as Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes


def composition__relation_to_triplet(package: Composition):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.composition_of_artwork,
            },
        },
        {
            "subject": {
                "label": package.composition_of_artwork,
                "s_class": "Composition",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "compositional technique",
                "wikidata_id": "wd:Q462437",
            },
        },
    ]

    return triplets


@dataclass
class WorkOfArt(Template):
    """
    Identify an **artistic object** (e.g., painting, sculpture, or other artistic production).
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night


def work_of_art_relation_to_triplet(package: WorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "work of art",
                "wikidata_id": "wd:Q838948",
            },
        },
    ]

    return triplets


@dataclass
class Concept(Template):
    """
    Identify **abstract ideas, emotions, or messages**, excluding specific persons.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    concept_of_artwork: (
        str  # Concepts such as Harmony, man, nature, balance, duality, chaos, order
    )


def concept_relation_to_triplet(package: Concept):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.concept_of_artwork,
            },
        },
        {
            "subject": {
                "label": package.concept_of_artwork,
                "s_class": "Concept",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "concept",
                "wikidata_id": "wd:Q151885",
            },
        },
    ]

    return triplets


@dataclass
class RhetoricalDevice(Template):
    """
    Identify **techniques in language or visuals** used to convey a deeper meaning.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    device: str  # Rhetorical Devices such as irony, allegory, sarcasm, metaphor, symbolism, hyperbole


def rhetorical_device_relation_to_triplet(package: RhetoricalDevice):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.device,
            },
        },
        {
            "subject": {
                "label": package.device,
                "s_class": "RhetoricalDevice",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "rhetorical device",
                "wikidata_id": "wd:Q1762471",
            },
        },
    ]

    return triplets


@dataclass
class Emotion(Template):
    """
    Identify the **emotion or mood** conveyed or depicted.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_emotion: str  # Emotions such as Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe


def emotion_relation_to_triplet(package: Emotion):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_emotion,
            },
        },
        {
            "subject": {
                "label": package.type_of_emotion,
                "s_class": "Emotion",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "emotion",
                "wikidata_id": "wd:Q9415",
            },
        },
    ]

    return triplets


@dataclass
class Quality(Template):
    """
    Identify a **characteristic or feature** that defines meaning or value.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_quality: str  # Qualities such as vibrant, delicate, beautiful, impressive, rough, smooth, luminous, dark, ethereal


def quality_relation_to_triplet(package: Quality):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "has characteristic",
                "wikidata_id": "wdt:P1552",
            },
            "object": {
                "label": package.type_of_quality,
            },
        },
        {
            "subject": {
                "label": package.type_of_quality,
                "s_class": "Quality",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "quality",
                "wikidata_id": "wd:Q1207505",  # distinguishing feature rather than Q185957
            },
        },
    ]

    return triplets


@dataclass
class Color(Template):
    """
    Identify **colors** (hues, shades, or tones) depicted as visual characteristics in a work of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_color: str  # Colors such as gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre


def color_relation_to_triplet(package: Color):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_color,
            },
        },
        {
            "subject": {
                "label": package.type_of_color,
                "s_class": "Color",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "color",
                "wikidata_id": "wd:Q1075",
            },
        },
    ]

    return triplets


@dataclass
class PointInTime(Template):
    """
    Identify a **specific moment or historical reference** depicted in a work of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_point_in_time: str  # Point in time such as 12 April 1450, circa 1890, mid-16th century, Renaissance period, 3rd century BCE


def point_in_time_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_point_in_time,
            },
        },
        {
            "subject": {
                "label": package.type_of_point_in_time,
                "s_class": "PointInTime",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "point in time",
                "wikidata_id": "wd:Q186408",
            },
        },
    ]

    return triplets


@dataclass
class Season(Template):
    """
    Identify the **season** (Spring, Summer, Fall, or Winter) described.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_season: str  # Type of seasons such as spring, summer, fall, winter, rainy season, dry season


def season_relation_to_triplet(package: Season):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_season,
            },
        },
        {
            "subject": {
                "label": package.type_of_season,
                "s_class": "Season",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "season",
                "wikidata_id": "wd:Q10688145",
            },
        },
    ]

    return triplets


@dataclass
class Person(Template):
    """
    Identify a **human figure**.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_person: str  # Persons such as Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I


def person_relation_to_triplet(package: Person):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
                "s_class": "WorkOfArt",
            },
            "relation": {
                "label": "depicts",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.type_of_person,
            },
        },
        {
            "subject": {
                "label": package.type_of_person,
                "s_class": "Person",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "human",
                "wikidata_id": "wd:Q5",  # instead of q215627 as it is recommende by wikidata
            },
        },
    ]

    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    ArtisticTheme,
    Composition,
    #CompositionContains,
    #CompositionDepicts,
    WorkOfArt,
    Concept,
    #ConceptSymbolize,
    #ConceptDepicts,
    RhetoricalDevice,
    #RhetoricalDeviceSymbolize,
    #RhetoricalDeviceDepicts,
    Emotion,
    Quality,
    Color,
    PointInTime,
    Season,
    Person,
]

ENTITY_PARSER = {
    "ArtisticTheme": artistic_theme_relation_to_triplet,
    "Composition": composition__relation_to_triplet,
    #"CompositionContains": composition_contains_relation_to_triplet,
    #"CompositionDepicts": composition_depicts_relation_to_triplet,
    "WorkOfArt": work_of_art_relation_to_triplet,
    "Concept": concept_relation_to_triplet,
    #"ConceptSymbolize": concept_symbolize_relation_to_triplet,
    #"ConceptDepicts": concept_depicts_relation_to_triplet,
    "RhetoricalDevice": rhetorical_device_relation_to_triplet,
    #"RhetoricalDeviceSymbolize": rhetorical_device_symbolize_relation_to_triplet,
    #"RhetoricalDeviceDepicts": rhetorical_device_depicts_relation_to_triplet,
    "Emotion": emotion_relation_to_triplet,
    "Quality": quality_relation_to_triplet,
    "Color": color_relation_to_triplet,
    "PointInTime": point_in_time_relation_to_triplet,
    "Season": season_relation_to_triplet,
    "Person": person_relation_to_triplet,
}
