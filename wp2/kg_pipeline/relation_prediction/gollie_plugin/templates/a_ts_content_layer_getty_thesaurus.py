from typing import List

from ..utils_typing import Relation, dataclass # Assuming Relation might be used by Template or elsewhere
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class ArtisticTheme(Template):
    """
    An underlying intent or meaning in a work of visual or literary art; also a motif, subject, or idea repeated in a number of artistic works.
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
    Structure or arrangement of the internal elements of a work of art, such as a drawing, sculpture, or written or musical work.
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
                "wikidata_id": "wd:Q462437",  
            },
        },
    ]

    return triplets


@dataclass
class WorkOfArt(Template):
    """
    Works of art in any medium, including performance art.
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
                "wikidata_id": "wd:Q838948"
            },
        },
    ]

    return triplets


@dataclass
class Concept(Template):
    """
    None
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
                "wikidata_id": "wd:Q151885"
            },
        },
    ]

    return triplets


@dataclass
class RhetoricalDevice(Template):
    """
    Discipline concerning the principles and rules of composition for persuasive speech, particularly as formulated by ancient critics and interpreted by classical scholars for application to discourse in the vernacular.
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
                "wikidata_id": "wd:Q1762471"
            },
        },
    ]

    return triplets


@dataclass
class Emotion(Template):
    """
    Refers to a complex phenomena and quality of consciousness, featuring the synthesis or combination of subjective experiences and perceptions, expressive physiological and psychological behaviors, and the excitation or stimulation of the nervous system
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfEmotion: str  # Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe 


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
    Use in the context of aesthetic judgment for the concept of inherent merit, worthiness, or excellence in something
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
    Refers to a general perceived attribute of an object or light resulting from the response of vision to the wavelength of reflected or transmitted light. The principal dimensions of color when discussing painting are the variables or attributes of hue, tone, and intensity. When referring to individual chromatic colors and achromatic colors or neutrals, use "colors (hues or tints)."
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfColor: str  # Gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre 


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
    A fundamental dimensional quantity defined by a nonspatial continuum in which events occur in apparently irreversible succession from the past through the present to the future.
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
    The climatic divisions of the year, that are spring, summer, winter, and autumn.
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
    Members of the species Homo sapiens and their close extinct relatives, as distinguished from other animals, spirits, or other entities.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPerson: str  # Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I 


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
    Characters known from legend and stories, whether or not there is a counterpart in recorded history.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalCharacter: str  # Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor


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
                "wikidata_id": "wd:Q4271324",
            },
        },
    ]

    return triplets


@dataclass
class ReligiousCharacter(Template):
    """
    General term for objects comprising or containing the image or represenation of a saint or other holy figure.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfReligiousCharacter: str  # Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna 


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
    General term used to reference various components of a body, usually restricted to the human body. Included may be external parts or internal parts, such as organs.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnatomicalStructure: str  # Torso, arm, head, hands, legs, feet, ribcage, eye, fingers 


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
    Activities, businesses, and professions that people pursue as a livelihood or as their primary endeavor, whether paid or not
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
    The relative disposition and way of arrangement of the various parts of the body of a human, or sometimes of an animal. Includes the position and carriage of the limbs, hands, head, or the body as a whole, often as indicating a particular quality or feeling.
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
    None
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
    Features on earth that comprise physical geography rather than administrative boundaries or manmade built works.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfGeographicalFeature: str  # Forest, fields, pathways, mountains, river, desert, coastline, cliffs


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
    None
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalLocation: str  # Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis


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
    The physical position that is precisely definable in terms of geographic or astronomic measurement, or situation relative to geographic or astronomic features or to elements of the built environment.
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
    Tactile and sometimes visual quality of a surface given to it by the size, shape, arrangement, and proportions of its minute parts, such as granules, particles, threads, or brushstrokes.
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
    Any living organisms, including human beings; may be real or fictional, including mythical or legendary creatures.
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
    Creatures, spirits, or other living entities that are imaginary, fictitious, or belonging to myth or legend
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfMythicalAnimal: str  # Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera (Corrected type hint style)


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
    Any material that can be digested or absorbed by the body of a human or other animal and used as a source of energy or some essential nutrient, to build and replace tissue, or to relieve hunger.
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
    Material things that can be perceived by the senses.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPhysicalObject: str  # Viola da gamba, sword, chair, goblet, mirror, book, crown, candle


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
    Multicellular eukaryotic life forms characterized by photosynthesis, in which chemical energy is produced from water, minerals, and carbon dioxide with the aid of pigments and the radiant energy of the Sun
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