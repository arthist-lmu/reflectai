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

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    theme: str  # Adoration, Vanitas, Last Supper, Annunciation, Judgment Day, Triumph of Death


def ArtisticTheme_relation_to_triplet(package: ArtisticTheme):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.theme,
            },
        },
        {
            "subject": {
                "label": package.theme,
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
    Composition is the arrangement of visual elements to create balance, movement, or focus in a work of art.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    CompositionOfArtwork: str  # Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes


def Composition_relation_to_triplet(package: Composition):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.CompositionOfArtwork,
            },
        },
        {
            "subject": {
                "label": package.CompositionOfArtwork,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "compositional technique",
                "wikidata_id": "wdt:Q462437",
            },
        },
    ]

    return triplets


@dataclass
class WorkOfArt(Template):
    """
    Work of Art is an artistic object, such as a painting, sculpture, or other artistic production.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night


def WorkOfArt_relation_to_triplet(package: WorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.work,
            },
        },
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "work of art",
                "wikidata_id": "wdt:Q838948",
            },
        },
    ]

    return triplets


@dataclass
class Concept(Template):
    """
    Concept is an abstract idea, feeling, or message expressed through artistic means.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    ConceptOfArtwork: str  # Harmony, man, nature, balance, duality, chaos, order


def Concept_relation_to_triplet(package: Concept):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.ConceptOfArtwork,
            },
        },
        {
            "subject": {
                "label": package.ConceptOfArtwork,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "concept",
                "wikidata_id": "wdt:Q151885",
            },
        },
    ]

    return triplets


@dataclass
class RhetoricalDevice(Template):
    """
    Rhetorical Device is a technique in language or visuals to convey a deeper meaning.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    device: str  # Irony, allegory, sarcasm, metaphor, symbolism, hyperbole


def RhetoricalDevice_relation_to_triplet(package: RhetoricalDevice):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.device,
            },
        },
        {
            "subject": {
                "label": package.device,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "rhetorical device",
                "wikidata_id": "wdt:Q1762471",
            },
        },
    ]

    return triplets


@dataclass
class Emotion(Template):
    """
    Emotion is a feeling or mood.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfEmotion: (
        str  # Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe
    )


def Emotion_relation_to_triplet(package: Emotion):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfEmotion,
            },
        },
        {
            "subject": {
                "label": package.TypeOfEmotion,
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
    Quality is a characteristic or feature that defines meaning or value.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfQuality: str  # Vibrant, delicate, beautiful, impressive, rough, smooth, luminous, dark, ethereal


def Quality_relation_to_triplet(package: Quality):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfQuality,
            },
        },
        {
            "subject": {
                "label": package.TypeOfQuality,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "quality",
                "wikidata_id": "wd:Q185957",
            },
        },
    ]

    return triplets


@dataclass
class Color(Template):
    """
    Color is a visual characteristic, including different hues, shades, and tones.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfColor: (
        str  # Gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre
    )


def Color_relation_to_triplet(package: Color):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfColor,
            },
        },
        {
            "subject": {
                "label": package.TypeOfColor,
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
    Point in Time is a specific moment or historical reference.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPointInTime: str  # 12 April 1450, circa 1890, mid-16th century, Renaissance period, 3rd century BCE


def PointInTime_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPointInTime,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPointInTime,
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
    Season is a time of year—Spring, Summer, Fall, or Winter—depicted visually.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfSeason: str  # Spring, summer, fall, winter, rainy season, dry season


def Season_relation_to_triplet(package: Season):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfSeason,
            },
        },
        {
            "subject": {
                "label": package.TypeOfSeason,
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
    Person is a human figure.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPerson: (
        str  # Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I
    )


def Person_relation_to_triplet(package: Person):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPerson,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPerson,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person",
                "wikidata_id": "wd:Q215627",
            },
        },
    ]

    return triplets


@dataclass
class MythicalCharacter(Template):
    """
    Mythical Character is a person from myths or legends.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalCharacter: (
        str  # Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor
    )


def MythicalCharacter_relation_to_triplet(package: MythicalCharacter):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfMythicalCharacter,
            },
        },
        {
            "subject": {
                "label": package.TypeOfMythicalCharacter,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical character",
                "wikidata_id": "wd:Q215627",
            },
        },
    ]

    return triplets


@dataclass
class ReligiousCharacter(Template):
    """
    Religious character is a person that alludes to religious and biblical stories.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfReligiousCharacter: (
        str  # Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna
    )


def ReligiousCharacter_relation_to_triplet(package: ReligiousCharacter):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfReligiousCharacter,
            },
        },
        {
            "subject": {
                "label": package.TypeOfReligiousCharacter,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "religious character",
                "wikidata_id": "wd:Q18563354",
            },
        },
    ]

    return triplets


@dataclass
class AnatomicalStructure(Template):
    """
    Anatomical Structure is a body or body part.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnatomicalStructure: (
        str  # Torso, arm, head, hands, legs, feet, ribcage, eye, fingers
    )


def AnatomicalStructure_relation_to_triplet(package: AnatomicalStructure):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfAnatomicalStructure,
            },
        },
        {
            "subject": {
                "label": package.TypeOfAnatomicalStructure,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "anatomical structure",
                "wikidata_id": "wd:Q4936952",
            },
        },
    ]

    return triplets


@dataclass
class Occupation(Template):
    """
    Occupation is a job, profession, or social role linked to a person.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfOccupation: str  # Blacksmith, priest, mourning woman, soldier, merchant, noblewoman, peasant, scholar


def Occupation_relation_to_triplet(package: Occupation):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfOccupation,
            },
        },
        {
            "subject": {
                "label": package.TypeOfOccupation,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "occupation",
                "wikidata_id": "wd:Q12737077",
            },
        },
    ]

    return triplets


@dataclass
class Posture(Template):
    """
    Posture is the pose or stance of a figure.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPosture: str  # Reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


def Posture_relation_to_triplet(package: Posture):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPosture,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPosture,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "posture",
                "wikidata_id": "wd:Q8514257",
            },
        },
    ]

    return triplets


@dataclass
class ArchitecturalStructure(Template):
    """
    Architectural Structure is a building or constructed form.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfArchitecturalStructure: str  # Palace, bridge, water garden, castle, cathedral, temple, tower, amphitheater


def ArchitecturalStructure_relation_to_triplet(package: ArchitecturalStructure):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfArchitecturalStructure,
            },
        },
        {
            "subject": {
                "label": package.TypeOfArchitecturalStructure,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "architectural structure",
                "wikidata_id": "wd:Q811979",
            },
        },
    ]

    return triplets


@dataclass
class GeographicalFeature(Template):
    """
    Geographical Feature is a naturally occurring landform.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfGeographicalFeature: (
        str  # Forest, fields, pathways, mountains, river, desert, coastline, cliffs
    )


def GeographicalFeature_relation_to_triplet(package: GeographicalFeature):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfGeographicalFeature,
            },
        },
        {
            "subject": {
                "label": package.TypeOfGeographicalFeature,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "geographical feature",
                "wikidata_id": "wd:Q618123",
            },
        },
    ]

    return triplets


@dataclass
class MythicalLocation(Template):
    """
    Mythical Location is a place from myths, legends, or folklore.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalLocation: (
        str  # Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis
    )


def MythicalLocation_relation_to_triplet(package: MythicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfMythicalLocation,
            },
        },
        {
            "subject": {
                "label": package.TypeOfMythicalLocation,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical location",
                "wikidata_id": "wd:Q3238337",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalLocation(Template):
    """
    Physical Location is a specific, real-world place.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalLocation: str  # Camposanto, Paris, Mount Fuji, Eiffel Tower, Grand Canyon, Rome, Taj Mahal


def PhysicalLocation_relation_to_triplet(package: PhysicalLocation):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPhysicalLocation,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPhysicalLocation,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical location",
                "wikidata_id": "wd:Q17334923",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalSurface(Template):
    """
    Physical surface is a defined material area which has certain qualities.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalSurface: str  # Brick wall, marble floor, wood wall, rough stone, polished metal, woven fabric


def PhysicalSurface_relation_to_triplet(package: PhysicalSurface):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPhysicalSurface,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPhysicalSurface,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical surface",
                "wikidata_id": "wd:Q3783831",
            },
        },
    ]

    return triplets


@dataclass
class Animal(Template):
    """
    Animal is a living creature.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnimal: str  # Dog, giraffe, cat, horse, fish, elephant, lion, eagle


def Animal_relation_to_triplet(package: Animal):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfAnimal,
            },
        },
        {
            "subject": {
                "label": package.TypeOfAnimal,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "animal",
                "wikidata_id": "wd:Q729",
            },
        },
    ]

    return triplets


@dataclass
class MythicalAnimal(Template):
    """
    Mythical Animal is a legendary or folkloric living creature.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalAnimal: (
        str  # Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera
    )


def MythicalAnimal_relation_to_triplet(package: MythicalAnimal):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfMythicalAnimal,
            },
        },
        {
            "subject": {
                "label": package.TypeOfMythicalAnimal,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "mythical animal",
                "wikidata_id": "wd:Q24334299",
            },
        },
    ]

    return triplets


@dataclass
class Food(Template):
    """
    Food is an edible or drinkable item.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfFood: str  # Bread, peach, plums, brioche, wine, grapes, pomegranate, figs


def Food_relation_to_triplet(package: Food):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfFood,
            },
        },
        {
            "subject": {
                "label": package.TypeOfFood,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "food",
                "wikidata_id": "wd:Q2095",
            },
        },
    ]

    return triplets


@dataclass
class PhysicalObject(Template):
    """
    Physical object is a tangible item contributing to composition, narrative, or symbolism.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalObject: (
        str  # Viola da gamba, sword, chair, goblet, mirror, book, crown, candle
    )


def PhysicalObject_relation_to_triplet(package: PhysicalObject):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPhysicalObject,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPhysicalObject,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical object",
                "wikidata_id": "wd:Q223557",
            },
        },
    ]

    return triplets


@dataclass
class Plant(Template):
    """
    Plant is a botanical element.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPlant: str  # Iris, tree, cactus, acanthus, laurel, olive branch, lotus, vine


def Plant_relation_to_triplet(package: Plant):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "depict",
                "wikidata_id": "wdt:P180",
            },
            "object": {
                "label": package.TypeOfPlant,
            },
        },
        {
            "subject": {
                "label": package.TypeOfPlant,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "plant",
                "wikidata_id": "wd:Q756",
            },
        },
    ]

    return triplets


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
