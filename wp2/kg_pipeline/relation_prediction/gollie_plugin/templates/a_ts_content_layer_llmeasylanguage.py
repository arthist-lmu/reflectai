from typing import List

from ..utils_typing import Relation, dataclass 
from ..utils_typing import Generic as Template

"""
Relation definitions
"""

@dataclass
class ArtisticTheme(Template):
    """
    Artistic Theme is a subject, story, or idea.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    theme: str  # Adoration, Vanitas, Last Supper, Annunciation, Judgment Day, Triumph of Death


def ArtisticTheme_relation_to_triplet(package: ArtisticTheme):
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
    Composition is how things are arranged.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    CompositionOfArtwork: str  # Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes


def Composition_relation_to_triplet(package: Composition):
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
                "wikidata_id": "wd:Q462437"
            },
        },
    ]

    return triplets


@dataclass
class WorkOfArt(Template):
    """
    artwork of Art is something creative like a painting or sculpture.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night


def WorkOfArt_relation_to_triplet(package: WorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "artwork of art",
                "wikidata_id": "wd:Q838948"
            },
        },
    ]

    return triplets


@dataclass
class Concept(Template):
    """
    Concept is an idea, feeling, or message.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    ConceptOfArtwork: str  # Harmony, man, nature, balance, duality, chaos, order


def Concept_relation_to_triplet(package: Concept):
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
                "wikidata_id": "wd:Q151885"
            },
        },
    ]

    return triplets


@dataclass
class RhetoricalDevice(Template):
    """
    Rhetorical Device is a way to add meaning with words or images.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    device: str  # Irony, allegory, sarcasm, metaphor, symbolism, hyperbole


def RhetoricalDevice_relation_to_triplet(package: RhetoricalDevice):
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
                "wikidata_id": "wd:Q1762471"
            },
        },
    ]

    return triplets


@dataclass
class Emotion(Template):
    """
    Emotion is a feeling or mood.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfEmotion: str  # Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe 


def Emotion_relation_to_triplet(package: Emotion):
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
    Quality is a feature or trait.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfQuality: str  # Vibrant, delicate, beautiful, impressive, rough, smooth, luminous, dark, ethereal


def Quality_relation_to_triplet(package: Quality):
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
    Color is a shade or tone.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfColor: str  # Gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre 


def Color_relation_to_triplet(package: Color):
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
    Point in Time is a specific moment.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPointInTime: str  # 12 April 1450, circa 1890, mid-16th century, Renaissance period, 3rd century BCE


def PointInTime_relation_to_triplet(package: PointInTime):
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
    Season is a time of year like Spring or Winter.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfSeason: str  # Spring, summer, fall, winter, rainy season, dry season


def Season_relation_to_triplet(package: Season):
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
    Person is a human.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPerson: str  # Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I 


def Person_relation_to_triplet(package: Person):
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
    Mythical Character is a person from a myth or legend.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalCharacter: str  # Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor 


def MythicalCharacter_relation_to_triplet(package: MythicalCharacter):
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
                "wikidata_id": "wd:Q4271324"
            },
        },
    ]

    return triplets


@dataclass
class ReligiousCharacter(Template):
    """
    Religious Character is a person from a religion.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfReligiousCharacter: str  # Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna 


def ReligiousCharacter_relation_to_triplet(package: ReligiousCharacter):
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
    Anatomical Structure is a body part.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnatomicalStructure: str  # Torso, arm, head, hands, legs, feet, ribcage, eye, fingers 


def AnatomicalStructure_relation_to_triplet(package: AnatomicalStructure):
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
    Occupation is a job.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfOccupation: str  # Blacksmith, priest, mourning woman, soldier, merchant, noblewoman, peasant, scholar


def Occupation_relation_to_triplet(package: Occupation):
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
    Posture is how someone stands or sits.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPosture: str  # Reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


def Posture_relation_to_triplet(package: Posture):
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
    Architectural Structure is a building.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfArchitecturalStructure: str  # Palace, bridge, water garden, castle, cathedral, temple, tower, amphitheater


def ArchitecturalStructure_relation_to_triplet(package: ArchitecturalStructure):
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
    Geographical Feature is a natural place like a mountain.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfGeographicalFeature: str  # Forest, fields, pathways, mountains, river, desert, coastline, cliffs 


def GeographicalFeature_relation_to_triplet(package: GeographicalFeature):
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
    Mythical Location is a place from a myth or legend.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalLocation: str  # Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis


def MythicalLocation_relation_to_triplet(package: MythicalLocation):
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
    Physical Location is a real place.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalLocation: str  # Camposanto, Paris, Mount Fuji, Eiffel Tower, Grand Canyon, Rome, Taj Mahal


def PhysicalLocation_relation_to_triplet(package: PhysicalLocation):
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
    Physical Surface is a material area.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalSurface: str  # Brick wall, marble floor, wood wall, rough stone, polished metal, woven fabric


def PhysicalSurface_relation_to_triplet(package: PhysicalSurface):
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

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnimal: str  # Dog, giraffe, cat, horse, fish, elephant, lion, eagle


def Animal_relation_to_triplet(package: Animal):
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
    Mythical Animal is a creature from a myth or legend.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalAnimal: str  # Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera 


def MythicalAnimal_relation_to_triplet(package: MythicalAnimal):
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
    Food is something to eat or drink.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfFood: str  # Bread, peach, plums, brioche, wine, grapes, pomegranate, figs


def Food_relation_to_triplet(package: Food):
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
    Physical Object is a thing.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalObject: str  # Viola da gamba, sword, chair, goblet, mirror, book, crown, candle 


def PhysicalObject_relation_to_triplet(package: PhysicalObject):
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
    Plant is a type of vegetation.
    """

    artwork: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPlant: str  # Iris, tree, cactus, acanthus, laurel, olive branch, lotus, vine


def Plant_relation_to_triplet(package: Plant):
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
    "ArtisticTheme": ArtisticTheme_relation_to_triplet,
    "Composition": Composition_relation_to_triplet,
    "WorkOfArt": WorkOfArt_relation_to_triplet,
    "Concept": Concept_relation_to_triplet,
    "RhetoricalDevice": RhetoricalDevice_relation_to_triplet,
    "Emotion": Emotion_relation_to_triplet,
    "Quality": Quality_relation_to_triplet,
    "Color": Color_relation_to_triplet,
    "PointInTime": PointInTime_relation_to_triplet,
    "Season": Season_relation_to_triplet,
    "Person": Person_relation_to_triplet,
    "MythicalCharacter": MythicalCharacter_relation_to_triplet,
    "ReligiousCharacter": ReligiousCharacter_relation_to_triplet,
    "AnatomicalStructure": AnatomicalStructure_relation_to_triplet,
    "Occupation": Occupation_relation_to_triplet,
    "Posture": Posture_relation_to_triplet,
    "ArchitecturalStructure": ArchitecturalStructure_relation_to_triplet,
    "GeographicalFeature": GeographicalFeature_relation_to_triplet,
    "MythicalLocation": MythicalLocation_relation_to_triplet,
    "PhysicalLocation": PhysicalLocation_relation_to_triplet,
    "PhysicalSurface": PhysicalSurface_relation_to_triplet,
    "Animal": Animal_relation_to_triplet,
    "MythicalAnimal": MythicalAnimal_relation_to_triplet,
    "Food": Food_relation_to_triplet,
    "PhysicalObject": PhysicalObject_relation_to_triplet,
    "Plant": Plant_relation_to_triplet,
}