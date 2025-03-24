from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class ArtisticTheme(Template):
    """
    Artistic Theme is a subject, story, or idea in a work of art.
    """

    theme: str  # Adoration, Vanitas, Last Supper, Annunciation, Judgment Day, Triumph of Death


@dataclass
class Composition(Template):
    """
    Composition is the arrangement of visual elements to create balance, movement, or focus in a work of art.
    """

    CompositionOfArtwork: str  # Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes


@dataclass
class WorkOfArt(Template):
    """
    Work of Art is an artistic object, such as a painting, sculpture, or other artistic production.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night


@dataclass
class Concept(Template):
    """
    Concept is an abstract idea, feeling, or message expressed through artistic means.
    """

    ConceptOfArtwork: str  # Harmony, man, nature, balance, duality, chaos, order


@dataclass
class RhetoricalDevice(Template):
    """
    Rhetorical Device is a technique in language or visuals to convey a deeper meaning.
    """

    device: str  # Irony, allegory, sarcasm, metaphor, symbolism, hyperbole


@dataclass
class Emotion(Template):
    """
    Emotion is a feeling or mood.
    """

    TypeOfEmotion: (
        str  # Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe
    )


@dataclass
class Quality(Template):
    """
    Quality is a characteristic or feature that defines meaning or value.
    """

    TypeOfQuality: str  # Vibrant, delicate, beautiful, impressive, rough, smooth, luminous, dark, ethereal


@dataclass
class Color(Template):
    """
    Color is a visual characteristic, including different hues, shades, and tones.
    """

    TypeOfColor: (
        str  # Gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre
    )


@dataclass
class PointInTime(Template):
    """
    Point in Time is a specific moment or historical reference.
    """

    TypeOfPointInTime: str  # 12 April 1450, circa 1890, mid-16th century, Renaissance period, 3rd century BCE


@dataclass
class Season(Template):
    """
    Season is a time of year—Spring, Summer, Fall, or Winter—depicted visually.
    """

    TypeOfSeason: str  # Spring, summer, fall, winter, rainy season, dry season


@dataclass
class Person(Template):
    """
    Person is a human figure.
    """

    TypeOfPerson: (
        str  # Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I
    )


@dataclass
class MythicalCharacter(Template):
    """
    Mythical Character is a person from myths or legends.
    """

    TypeOfMythicalCharacter: (
        str  # Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor
    )


@dataclass
class ReligiousCharacter(Template):
    """
    Religious character is a person that alludes to religious and biblical stories.
    """

    TypeOfReligiousCharacter: (
        str  # Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna
    )


@dataclass
class AnatomicalStructure(Template):
    """
    Anatomical Structure is a body or body part.
    """

    TypeOfAnatomicalStructure: (
        str  # Torso, arm, head, hands, legs, feet, ribcage, eye, fingers
    )


@dataclass
class Occupation(Template):
    """
    Occupation is a job, profession, or social role linked to a person.
    """

    TypeOfOccupation: str  # Blacksmith, priest, mourning woman, soldier, merchant, noblewoman, peasant, scholar


@dataclass
class Posture(Template):
    """
    Posture is the pose or stance of a figure.
    """

    TypeOfPosture: str  # Reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


@dataclass
class ArchitecturalStructure(Template):
    """
    Architectural Structure is a building or constructed form.
    """

    TypeOfArchitecturalStructure: str  # Palace, bridge, water garden, castle, cathedral, temple, tower, amphitheater


@dataclass
class GeographicalFeature(Template):
    """
    Geographical Feature is a naturally occurring landform.
    """

    TypeOfGeographicalFeature: (
        str  # Forest, fields, pathways, mountains, river, desert, coastline, cliffs
    )


@dataclass
class MythicalLocation(Template):
    """
    Mythical Location is a place from myths, legends, or folklore.
    """

    TypeOfMythicalLocation: (
        str  # Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis
    )


@dataclass
class PhysicalLocation(Template):
    """
    Physical Location is a specific, real-world place.
    """

    TypeOfPhysicalLocation: str  # Camposanto, Paris, Mount Fuji, Eiffel Tower, Grand Canyon, Rome, Taj Mahal


@dataclass
class PhysicalSurface(Template):
    """
    Physical surface is a defined material area which has certain qualities.
    """

    TypeOfPhysicalSurface: str  # Brick wall, marble floor, wood wall, rough stone, polished metal, woven fabric


@dataclass
class Animal(Template):
    """
    Animal is a living creature.
    """

    TypeOfAnimal: str  # Dog, giraffe, cat, horse, fish, elephant, lion, eagle


@dataclass
class MythicalAnimal(Template):
    """
    Mythical Animal is a legendary or folkloric living creature.
    """

    TypeOfMythicalAnimal: (
        str  # Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera
    )


@dataclass
class Food(Template):
    """
    Food is an edible or drinkable item.
    """

    TypeOfFood: str  # Bread, peach, plums, brioche, wine, grapes, pomegranate, figs


@dataclass
class PhysicalObject(Template):
    """
    Physical object is a tangible item contributing to composition, narrative, or symbolism.
    """

    TypeOfPhysicalObject: (
        str  # Viola da gamba, sword, chair, goblet, mirror, book, crown, candle
    )


@dataclass
class Plant(Template):
    """
    Plant is a botanical element.
    """

    TypeOfPlant: str  # Iris, tree, cactus, acanthus, laurel, olive branch, lotus, vine


ENTITY_DEFINITIONS: List[Template] = [
    ArtisticTheme,
    Composition,
    WorkOfArt,
    Concept,
    RhetoricalDevice,
    Emotion,
    Quality,
    Color,
    PointInTime,
    Season,
    Person,
    MythicalCharacter,
    MythicalCharacter,
    ReligiousCharacter,
    AnatomicalStructure,
    Occupation,
    Posture,
    ArchitecturalStructure,
    GeographicalFeature,
    MythicalLocation,
    PhysicalLocation,
    PhysicalSurface,
    Animal,
    MythicalAnimal,
    Food,
    PhysicalObject,
    Plant,
]


def ArtisticTheme_relation_to_triplet(package: ArtisticTheme):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has artistic theme",
                "wikidata_id": "wdt:Q1406161",
            },
            "object": {
                "label": package.theme,
            },
        }
    ]

    return triplets


def Composition_relation_to_triplet(package: Composition):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has composition",
                "wikidata_id": "wdt:Q462437",
            },
            "object": {
                "label": package.CompositionOfArtwork,
            },
        }
    ]

    return triplets


def WorkOfArt_relation_to_triplet(package: WorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is work of art",
                "wikidata_id": "wdt:Q838948",
            },
            "object": {
                "label": package.work,
            },
        }
    ]

    return triplets


def Concept_relation_to_triplet(package: Concept):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has concept",
                "wikidata_id": "wdt:Q151885",
            },
            "object": {
                "label": package.ConceptOfArtwork,
            },
        }
    ]

    return triplets


def RhetoricalDevice_relation_to_triplet(package: RhetoricalDevice):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has rhetorical device",
                "wikidata_id": "wdt:Q1762471",
            },
            "object": {
                "label": package.device,
            },
        }
    ]

    return triplets


def Emotion_relation_to_triplet(package: Emotion):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "includes emotion",
                "wikidata_id": "wdt:Q9415",
            },
            "object": {
                "label": package.TypeOfEmotion,
            },
        }
    ]

    return triplets


def Quality_relation_to_triplet(package: Quality):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has quality",
                "wikidata_id": "wdt:Q185957",
            },
            "object": {
                "label": package.TypeOfQuality,
            },
        }
    ]

    return triplets


def Color_relation_to_triplet(package: Color):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has color",
                "wikidata_id": "wdt:Q1075",
            },
            "object": {
                "label": package.TypeOfColor,
            },
        }
    ]

    return triplets


def PointInTime_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has point in time",
                "wikidata_id": "wdt:Q186408",
            },
            "object": {
                "label": package.TypeOfPointInTime,
            },
        }
    ]

    return triplets


def Season_relation_to_triplet(package: Season):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has season",
                "wikidata_id": "wdt:Q10688145",
            },
            "object": {
                "label": package.TypeOfSeason,
            },
        }
    ]

    return triplets


def Person_relation_to_triplet(package: Person):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has person",
                "wikidata_id": "wdt:Q215627",
            },
            "object": {
                "label": package.TypeOfPerson,
            },
        }
    ]

    return triplets


def MythicalCharakter_relation_to_triplet(package: MythicalCharacter):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has mythical character",
                "wikidata_id": "wdt:Q215627",
            },
            "object": {
                "label": package.TypeOfMythicalCharacter,
            },
        }
    ]

    return triplets


def ReligiousCharacter_relation_to_triplet(package: ReligiousCharacter):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has religious character",
                "wikidata_id": "wdt:Q18563354",
            },
            "object": {
                "label": package.TypeOfReligiousCharacter,
            },
        }
    ]

    return triplets


def AnatomicalStructure_relation_to_triplet(package: AnatomicalStructure):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has anatomical structure",
                "wikidata_id": "wdt:Q4936952",
            },
            "object": {
                "label": package.TypeOfAnatomicalStructure,
            },
        }
    ]

    return triplets


def Occupation_relation_to_triplet(package: Occupation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has occupation",
                "wikidata_id": "wdt:Q12737077",
            },
            "object": {
                "label": package.TypeOfOccupation,
            },
        }
    ]

    return triplets


def Posture_relation_to_triplet(package: Posture):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has posture",
                "wikidata_id": "wdt:Q8514257",
            },
            "object": {
                "label": package.TypeOfPosture,
            },
        }
    ]

    return triplets


def ArchitecturalStructure_relation_to_triplet(package: ArchitecturalStructure):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has architecture",
                "wikidata_id": "wdt:Q811979",
            },
            "object": {
                "label": package.TypeOfArchitecturalStructure,
            },
        }
    ]

    return triplets


def GeographicalFeature_relation_to_triplet(package: GeographicalFeature):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has geographical feature",
                "wikidata_id": "wdt:Q618123",
            },
            "object": {
                "label": package.TypeOfGeographicalFeature,
            },
        }
    ]

    return triplets


def MythicalLocation_relation_to_triplet(package: MythicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has mythical location",
                "wikidata_id": "wdt:Q3238337",
            },
            "object": {
                "label": package.TypeOfMythicalLocation,
            },
        }
    ]

    return triplets


def PhysicalLocation_relation_to_triplet(package: PhysicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has physical location",
                "wikidata_id": "wdt:Q17334923",
            },
            "object": {
                "label": package.TypeOfPhysicalLocation,
            },
        }
    ]

    return triplets


def PhysicalSurface_relation_to_triplet(package: PhysicalSurface):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "has physical surface",
                "wikidata_id": "wdt:Q3783831",
            },
            "object": {
                "label": package.TypeOfPhysicalSurface,
            },
        }
    ]

    return triplets


def Animal_relation_to_triplet(package: Animal):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is animal",
                "wikidata_id": "wdt:Q729",
            },
            "object": {
                "label": package.TypeOfAnimal,
            },
        }
    ]

    return triplets


def MythicalAnimal_relation_to_triplet(package: MythicalAnimal):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is mythical animal",
                "wikidata_id": "wdt:Q24334299",
            },
            "object": {
                "label": package.TypeOfMythicalAnimal,
            },
        }
    ]

    return triplets


def Food_relation_to_triplet(package: Food):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is food",
                "wikidata_id": "wdt:Q2095",
            },
            "object": {
                "label": package.TypeOfFood,
            },
        }
    ]

    return triplets


def PhysicalObject_relation_to_triplet(package: PhysicalObject):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is physical object",
                "wikidata_id": "wdt:Q223557",
            },
            "object": {
                "label": package.TypeOfPhysicalObject,
            },
        }
    ]

    return triplets


def Plant_relation_to_triplet(package: Plant):
    triplets = [
        {
            "subject": {
                "label": package.painting,
            },
            "relation": {
                "label": "is plant",
                "wikidata_id": "wdt:Q756",
            },
            "object": {
                "label": package.TypeOfPlant,
            },
        }
    ]

    return triplets


ENTITY_PARSER = {
    ArtisticTheme.__name__: ArtisticTheme_relation_to_triplet,
    Composition.__name__: Composition_relation_to_triplet,
    WorkOfArt.__name__: WorkOfArt_relation_to_triplet,
    Concept.__name__: Concept_relation_to_triplet,
    RhetoricalDevice.__name__: RhetoricalDevice_relation_to_triplet,
    Emotion.__name__: Emotion_relation_to_triplet,
    Quality.__name__: Quality_relation_to_triplet,
    Color.__name__: Color_relation_to_triplet,
    PointInTime.__name__: PointInTime_relation_to_triplet,
    Season.__name__: Season_relation_to_triplet,
    Person.__name__: Person_relation_to_triplet,
    MythicalCharacter.__name__: MythicalCharakter_relation_to_triplet,
    ReligiousCharacter.__name__: ReligiousCharacter_relation_to_triplet,
    AnatomicalStructure.__name__: AnatomicalStructure_relation_to_triplet,
    Occupation.__name__: Occupation_relation_to_triplet,
    Posture.__name__: Posture_relation_to_triplet,
    ArchitecturalStructure.__name__: ArchitecturalStructure_relation_to_triplet,
    MythicalLocation.__name__: MythicalCharakter_relation_to_triplet,
    PhysicalLocation.__name__: PhysicalLocation_relation_to_triplet,
    PhysicalSurface.__name__: PhysicalLocation_relation_to_triplet,
    Animal.__name__: Animal_relation_to_triplet,
    MythicalAnimal.__name__: MythicalAnimal_relation_to_triplet,
    Food.__name__: Food_relation_to_triplet,
    PhysicalObject.__name__: PhysicalObject_relation_to_triplet,
    Plant.__name__: Plant_relation_to_triplet,
}
