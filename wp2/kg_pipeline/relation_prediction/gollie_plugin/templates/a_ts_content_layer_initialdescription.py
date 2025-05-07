from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  # ignoring most if not all the meta data relations
"""


###------ meta classes --------###
@dataclass
class ArtGenre(Template):
    """
    Form of art in terms of a medium, format, or theme
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    ArtGenre: str # pre-impressionistic, 19th-century style


def ArtGenre_relation_to_triplet(package: ArtGenre):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "has genre",
                "wikidata_id": "wdt:P921" # rather than "wdt:P136",
            },
            "object": {
                "label": package.ArtGenre,
            },
        },
        {
            "subject": {
                "label": package.ArtGenre,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art genre",
                "wikidata_id": "wd:Q1792379",
            },
        },
    ]

    return triplets


@dataclass
class ArtMovement(Template):
    """
    tendency or style in art with a specific common philosophy or goal, possibly associated with a specific historical period
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    movement: str # Cubism


def ArtMovement_relation_to_triplet(package: ArtMovement):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "has movement",
                "wikidata_id": "wdt:P135" #closest I could find
            },
            "object": {
                "label": package.movement,
            },
        },
        {
            "subject": {
                "label": package.movement,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art movement",
                "wikidata_id": "wd:Q968159",
            },
        },
    ]

    return triplets

@dataclass
class ArtMaterial(Template):
    """
    substance, raw ingredient, or tool that is utilized by an artist to create a work of art
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    material: str # oil on canvas


def ArtMaterial_relation_to_triplet(package: ArtMaterial):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "made from material",
                "wikidata_id": "wdt:P186"
            },
            "object": {
                "label": package.material,
            },
        },
        {
            "subject": {
                "label": package.material,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art material",
                "wikidata_id": "wd:Q15303351",
            },
        },
    ]

    return triplets


@dataclass
class ArtisticTechnique(Template):
    """
    method by which art is produced
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    fabricated: str # wet paint, 


def ArtisticTechnique_relation_to_triplet(package: ArtisticTechnique):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "fabricated by",
                #"wikidata_id": "wdt:P186" has no obvious relation
            },
            "object": {
                "label": package.fabricated,
            },
        },
        {
            "subject": {
                "label": package.fabricated,
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "art material",
                "wikidata_id": "wd:Q11177771",
            },
        },
    ]

    return triplets


@dataclass
class TypeOfWorkOfArt(Template):
    """
    type of art work based on shared characteristics, functions, or stylistic features
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    instance: str # engraving

def TypeOfWorkOfArt_relation_to_triplet(package: TypeOfWorkOfArt):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "instance of", ### HERE THIS MIGHT NOT BE THE RELATION THAT WE WANT 
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": package.instance,
            },
        },
        {
            "subject": {
                "label": package.instance,
            },
            "relation": {
                "label": "instance of",  ### OR HERE WE NEED TO USE SUBCLASS INSTEAD
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "type of work of art",
                "wikidata_id": "wd:Q116474095",
            },
        },
    ]

    return triplets


@dataclass
class PointInTime(Template):
    """
    position of a particular instant in time
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str # 1502, 1370, 2010, 1875

def PointInTime_relation_to_triplet(package: PointInTime):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "created in",  ### or inception 
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
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
class StartTime(Template):
    """
    infimum of a temporal interval
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str # 1502, 1370, 2010, 1875

def StartTime_relation_to_triplet(package: StartTime):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "created in",  ### or inception 
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
            },
            "relation": {
                "label": "instance of",  
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "start time",
                "wikidata_id": "wd:Q24575110",
            },
        },
    ]

    return triplets


@dataclass
class EndTime(Template):
    """
    time that some temporal entity ceases to exist
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    time: str # 1502, 1370, 2010, 1875

def EndTime_relation_to_triplet(package: EndTime):
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "created in",  ### or inception 
                "wikidata_id": "wdt:P571",
            },
            "object": {
                "label": package.time,
            },
        },
        {
            "subject": {
                "label": package.time,
            },
            "relation": {
                "label": "instance of",  
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "end time",
                "wikidata_id": "wd:Q24575125",
            },
        },
    ]

    return triplets


@dataclass
class Person(Template):
    """
    being that has certain capacities or attributes constituting personhood
    """
    work: str # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    person: str # Massys, sitter, Karl Wittgenstein
    influenced: str # Massys, sitter, Karl Wittgenstein

def Person_relation_to_triplet(package: Person):
    ### should we rather split those up?
    triplets = [
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "created by",  
                "wikidata_id": "wdt:P170",
            },
            "object": {
                "label": package.person,
            },
        },
        {
            "subject": {
                "label": package.person,
            },
            "relation": {
                "label": "instance of",  
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person", # or human
                "wikidata_id": "wd:Q5" # instead of "wd:Q215627", since that is what wikidata says
            },
        },
        {
            "subject": {
                "label": package.work,
            },
            "relation": {
                "label": "influenced by",  
                "wikidata_id": "wdt:P737",
            },
            "object": {
                "label": package.influenced,
            },
        },
          {
            "subject": {
                "label": package.influenced,
            },
            "relation": {
                "label": "instance of",  
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "person", # or human
                "wikidata_id": "wd:Q5" # instead of "wd:Q215627", since that is what wikidata says
            },
        },
    ]

    return triplets

####-------------------------------------------------------------------------###

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
    Composition is the arrangement of visual elements to create balance, movement, or focus in a work of art.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    CompositionOfArtwork: str  # Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes
    contains: str ###---- item or substance loacted within this item but not part of it. e.g. person ----###


def Composition_relation_to_triplet(package: Composition):
    triplets = [
        {
            "subject": {
                "label": package.work,
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
                "wikidata_id": "wd:Q462437",
            },
        },
        # {
        #     "subject": {
        #         "label": package.work,
        #     },
        #     "relation": {
        #         "label": "contains",
        #         "wikidata_id": "wdt:P4330",
        #     },
        #     "object": {
        #         "label": package.contains,
        #     },
        # },
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
    Concept is an abstract idea, feeling, or message expressed through artistic means.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    ConceptOfArtwork: str  # Harmony, man, nature, balance, duality, chaos, order
    symbolize: str ###---- A specific person that is given in the text, but not necessarily in the depicted in the picture ----###

def Concept_relation_to_triplet(package: Concept):
    triplets = [
        {
            "subject": {
                "label": package.work,
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
                "wikidata_id": "wd:Q151885",
            },
        },
        # {
        #     "subject": {
        #         "label": package.work,
        #     },
        #     "relation": {
        #         "label": "symbolizes",
        #         #"wikidata_id": "wdt:P180",
        #     },
        #     "object": {
        #         "label": package.ConceptOfArtwork,
        #     },
        # },
    ]

    return triplets


@dataclass
class RhetoricalDevice(Template):
    """
    Rhetorical Device is a technique in language or visuals to convey a deeper meaning.
    """

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    device: str  # Irony, allegory, sarcasm, metaphor, symbolism, hyperbole
    symbolize: str ###---- A specific concept that is given in the text, but not necessarily in the depicted in the picture ----###


def RhetoricalDevice_relation_to_triplet(package: RhetoricalDevice):
    triplets = [
        {
            "subject": {
                "label": package.work,
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
                "wikidata_id": "wd:Q1762471",
            },
        },
        # {
        #     "subject": {
        #         "label": package.work,
        #     },
        #     "relation": {
        #         "label": "symbolizes",
        #         #"wikidata_id": "wdt:P180",
        #     },
        #     "object": {
        #         "label": package.device,
        #     },
        # },
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
                "label": "has characteristic",
                "wikidata_id": "wdt:P1552",
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
                "wikidata_id": "wd:Q1207505",  # distinguishing feature rather than Q185957
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
    Season is a time of year—Spring, Summer, Fall, or Winter—depictsed visually.
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
                "label": "human",
                "wikidata_id": "wd:Q5", # instead of q215627 as it is recommende by wikidata
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
                "wikidata_id": "wd:Q4271324",
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
    Posture is the pose or stance of a figure.
    """
    person: str # a depicted person ###-------        
    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfPosture: str  # Reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


def Posture_relation_to_triplet(package: Posture):
    triplets = [
        {
            "subject": {
                "label": package.work,
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
        # {
        #     "subject": {
        #         "label": package.person,
        #     },
        #     "relation": {
        #         "label": "has characteristic",
        #         "wikidata_id": "wdt:P1552",
        #     },
        #     "object": {
        #         "label": package.TypeOfQuality,
        #     },
        # },
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

####### THIS IS MISSING THE RELIGIOUS LOCATION!!!########


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

    work: str  # Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    TypeOfAnimal: str  # Dog, giraffe, cat, horse, fish, elephant, lion, eagle


def Animal_relation_to_triplet(package: Animal):
    triplets = [
        {
            "subject": {
                "label": package.work,
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
    #ReligiousLocation,
    PhysicalLocation,
    PhysicalSurface,
    Animal,
    MythicalAnimal,
    Food,
    PhysicalObject,
    Plant,
    # ArtGenre,
    # ArtMovement,
    # ArtMaterial,
    # ArtisticTechnique,
    # TypeOfWorkOfArt,
    # PointInTime,
    # StartTime,
    # EndTime,
    # Person
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
    "MythicalCharacter": MythicalCharacter_relation_to_triplet,  # fixed typo
    "ReligiousCharacter": ReligiousCharacter_relation_to_triplet,
    "AnatomicalStructure": AnatomicalStructure_relation_to_triplet,
    "Occupation": Occupation_relation_to_triplet,
    "Posture": Posture_relation_to_triplet,
    "ArchitecturalStructure": ArchitecturalStructure_relation_to_triplet,
    "GeographicalFeature": GeographicalFeature_relation_to_triplet,
    "MythicalLocation": MythicalLocation_relation_to_triplet,  # wire to the right function
    #"ReligiousLocation": ReligiousLocation_relation_to_triplet,
    "PhysicalLocation": PhysicalLocation_relation_to_triplet,
    "PhysicalSurface": PhysicalSurface_relation_to_triplet,  # now correct
    "Animal": Animal_relation_to_triplet,
    "MythicalAnimal": MythicalAnimal_relation_to_triplet,
    "Food": Food_relation_to_triplet,
    "PhysicalObject": PhysicalObject_relation_to_triplet,
    "Plant": Plant_relation_to_triplet,
    "ArtGenre": ArtGenre_relation_to_triplet,
    "ArtMovement": ArtMovement_relation_to_triplet,
    "ArtMaterial": ArtMaterial_relation_to_triplet,
    "ArtisticTechnique": ArtisticTechnique_relation_to_triplet,
    "TypeOfWorkOfArt": TypeOfWorkOfArt_relation_to_triplet, 
    "PointInTime": PointInTime_relation_to_triplet, 
    "StartTime": StartTime_relation_to_triplet,
    "EndTime": EndTime_relation_to_triplet,
    "Person": Person_relation_to_triplet
}
