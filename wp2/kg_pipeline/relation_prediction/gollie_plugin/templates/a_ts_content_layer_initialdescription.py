from typing import List
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  # ignoring most if not all the meta data relations
"""


@dataclass
class ArtisticTheme(Template):
    """
    Artistic Theme is a subject, story, or idea in a artwork of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    theme: str  # Themes such as Adoration, Vanitas, Last Supper, Annunciation, Judgment Day, Triumph of Death


def artistic_theme_relation_to_triplet(package: ArtisticTheme):
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
    Composition is the arrangement of visual elements to create balance, movement, or focus in a artwork of art.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    composition_of_artwork: str  # Compositions such as Diagonal lines, symmetry, central figure, perspective grid, foreshortening, overlapping planes
    contains: str  ###---- item or substance loacted within this item but not part of it. e.g. person ----###


def composition_relation_to_triplet(package: Composition):
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
                "label": package.composition_of_artwork,
            },
        },
        {
            "subject": {
                "label": package.composition_of_artwork,
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
        #         "label": package.artwork,
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
    artwork of Art is an artistic object, such as a painting, sculpture, or other artistic production.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night


def work_of_art_relation_to_triplet(package: WorkOfArt):
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    concept_of_artwork: (
        str  # Concepts such as Harmony, man, nature, balance, duality, chaos, order
    )
    symbolize: str  ###---- A specific person that is given in the text, but not necessarily in the depicted in the picture ----###


def concept_relation_to_triplet(package: Concept):
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
                "label": package.concept_of_artwork,
            },
        },
        {
            "subject": {
                "label": package.concept_of_artwork,
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
        #         "label": package.artwork,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    device: str  # Rhetorical Devices such as irony, allegory, sarcasm, metaphor, symbolism, hyperbole
    symbolize: str  ###---- A specific concept that is given in the text, but not necessarily in the depicted in the picture ----###


def rhetorical_device_relation_to_triplet(package: RhetoricalDevice):
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
                "wikidata_id": "wd:Q1762471",
            },
        },
        # {
        #     "subject": {
        #         "label": package.artwork,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_emotion: str  # Emotions such as Sadness, melancholy, joy, despair, serenity, ecstasy, grief, awe


def emotion_relation_to_triplet(package: Emotion):
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
                "label": package.type_of_emotion,
            },
        },
        {
            "subject": {
                "label": package.type_of_emotion,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_quality: str  # Qualities such as vibrant, delicate, beautiful, impressive, rough, smooth, luminous, dark, ethereal


def quality_relation_to_triplet(package: Quality):
    triplets = [
        {
            "subject": {
                "label": package.artwork,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_color: str  # Colors such as gold, emerald green, pastel tones, ultramarine, vermilion, carmine, ochre


def color_relation_to_triplet(package: Color):
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
                "label": package.type_of_color,
            },
        },
        {
            "subject": {
                "label": package.type_of_color,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_point_in_time: str  # Point in time such as 12 April 1450, circa 1890, mid-16th century, Renaissance period, 3rd century BCE


def point_in_time_relation_to_triplet(package: PointInTime):
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
                "label": package.type_of_point_in_time,
            },
        },
        {
            "subject": {
                "label": package.type_of_point_in_time,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_season: str  # Type of seasons such as spring, summer, fall, winter, rainy season, dry season


def season_relation_to_triplet(package: Season):
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
                "label": package.type_of_season,
            },
        },
        {
            "subject": {
                "label": package.type_of_season,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_person: str  # Persons such as Napoleon, Julius Caesar, Marie Antoinette, Cleopatra, Queen Elizabeth I


def person_relation_to_triplet(package: Person):
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
                "label": package.type_of_person,
            },
        },
        {
            "subject": {
                "label": package.type_of_person,
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


@dataclass
class MythicalCharacter(Template):
    """
    Mythical Character is a person from myths or legends.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_character: str  # Mythical characters such as Zeus, Venus, Poseidon, Muses, Medusa, Achilles, Odin, Thor


def mythical_character_relation_to_triplet(package: MythicalCharacter):
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
                "label": package.type_of_mythical_character,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_character,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_religious_character: str  # Religious characters such as Adam, Jesus, Apostles, Mary Magdalene, Saint Francis, Buddha, Krishna


def religious_character_relation_to_triplet(package: ReligiousCharacter):
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
                "label": package.type_of_religious_character,
            },
        },
        {
            "subject": {
                "label": package.type_of_religious_character,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_anatomical_structure: str  # Anatomical structures such as torso, arm, head, hands, legs, feet, ribcage, eye, fingers


def anatomical_structure_relation_to_triplet(package: AnatomicalStructure):
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
                "label": package.type_of_anatomical_structure,
            },
        },
        {
            "subject": {
                "label": package.type_of_anatomical_structure,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_occupation: str  # Occupations such as blacksmith, priest, mourning woman, soldier, merchant, noblewoman, peasant, scholar


def occupation_relation_to_triplet(package: Occupation):
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
                "label": package.type_of_occupation,
            },
        },
        {
            "subject": {
                "label": package.type_of_occupation,
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

    person: str  # a depicted person ###-------
    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_posture: str  # Postures such as reclining, head tilted, moving, sitting, standing, kneeling, running, gesturing


def posture_relation_to_triplet(package: Posture):
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
                "label": package.type_of_posture,
            },
        },
        {
            "subject": {
                "label": package.type_of_posture,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_architectural_structure: str  # Architectural structures such as palace, bridge, water garden, castle, cathedral, temple, tower, amphitheater


def architectural_structure_relation_to_triplet(package: ArchitecturalStructure):
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
                "label": package.type_of_architectural_structure,
            },
        },
        {
            "subject": {
                "label": package.type_of_architectural_structure,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_geographical_feature: str  # FGeographical features such as forest, fields, pathways, mountains, river, desert, coastline, cliffs


def geographical_feature_relation_to_triplet(package: GeographicalFeature):
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
                "label": package.type_of_geographical_feature,
            },
        },
        {
            "subject": {
                "label": package.type_of_geographical_feature,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_location: str  # Mythical locations such as Paradise, Hell, Elysium, Limbo, Avalon, Valhalla, Shangri-La, Atlantis


def mythical_location_relation_to_triplet(package: MythicalLocation):
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
                "label": package.type_of_mythical_location,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_location,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_location: str  # Physical locations such as Camposanto, Paris, Mount Fuji, Eiffel Tower, Grand Canyon, Rome, Taj Mahal


def physical_location_relation_to_triplet(package: PhysicalLocation):
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
                "label": package.type_of_physical_location,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_location,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_surface: str  # Physical surfaces such as brick wall, marble floor, wood wall, rough stone, polished metal, woven fabric


def physical_surface_relation_to_triplet(package: PhysicalSurface):
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
                "label": package.type_of_physical_surface,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_surface,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_animal: (
        str  # Animals such as Dog, giraffe, cat, horse, fish, elephant, lion, eagle
    )


def animal_relation_to_triplet(package: Animal):
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
                "label": package.type_of_animal,
            },
        },
        {
            "subject": {
                "label": package.type_of_animal,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_mythical_animal: str  # Mythical animals such as Pegasus, Sphinx, Centaur, Griffin, Dragon, Phoenix, Chimera


def mythical_animal_relation_to_triplet(package: MythicalAnimal):
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
                "label": package.type_of_mythical_animal,
            },
        },
        {
            "subject": {
                "label": package.type_of_mythical_animal,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_food: str  # Food such as bread, peach, plums, brioche, wine, grapes, pomegranate, figs


def food_relation_to_triplet(package: Food):
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
                "label": package.type_of_food,
            },
        },
        {
            "subject": {
                "label": package.type_of_food,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_physical_object: str  # Physical objects such as viola da gamba, sword, chair, goblet, mirror, book, crown, candle


def physical_object_relation_to_triplet(package: PhysicalObject):
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
                "label": package.type_of_physical_object,
            },
        },
        {
            "subject": {
                "label": package.type_of_physical_object,
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

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night
    type_of_plant: str  # Plants such as Iris, tree, cactus, acanthus, laurel, olive branch, lotus, vine


def plant_relation_to_triplet(package: Plant):
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
                "label": package.type_of_plant,
            },
        },
        {
            "subject": {
                "label": package.type_of_plant,
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
    # ReligiousLocation,
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
    "ArtisticTheme": artistic_theme_relation_to_triplet,
    "Composition": composition_relation_to_triplet,
    "WorkOfArt": work_of_art_relation_to_triplet,
    "Concept": concept_relation_to_triplet,
    "RhetoricalDevice": rhetorical_device_relation_to_triplet,
    "Emotion": emotion_relation_to_triplet,
    "Quality": quality_relation_to_triplet,
    "Color": color_relation_to_triplet,
    "PointInTime": point_in_time_relation_to_triplet,
    "Season": season_relation_to_triplet,
    "Person": person_relation_to_triplet,
    "MythicalCharacter": mythical_character_relation_to_triplet,
    "ReligiousCharacter": religious_character_relation_to_triplet,
    "AnatomicalStructure": anatomical_structure_relation_to_triplet,
    "Occupation": occupation_relation_to_triplet,
    "Posture": posture_relation_to_triplet,
    "ArchitecturalStructure": architectural_structure_relation_to_triplet,
    "GeographicalFeature": geographical_feature_relation_to_triplet,
    "MythicalLocation": mythical_location_relation_to_triplet,
    # "ReligiousLocation": ReligiousLocation_relation_to_triplet,
    "PhysicalLocation": physical_location_relation_to_triplet,
    "PhysicalSurface": physical_surface_relation_to_triplet,
    "Animal": animal_relation_to_triplet,
    "MythicalAnimal": mythical_animal_relation_to_triplet,
    "Food": food_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
    "Plant": plant_relation_to_triplet,
    # "ArtGenre": ArtGenre_relation_to_triplet,
    # "ArtMovement": ArtMovement_relation_to_triplet,
    # "ArtMaterial": ArtMaterial_relation_to_triplet,
    # "ArtisticTechnique": ArtisticTechnique_relation_to_triplet,
    # "TypeOfWorkOfArt": TypeOfWorkOfArt_relation_to_triplet,
    # "PointInTime": PointInTime_relation_to_triplet,
    # "StartTime": StartTime_relation_to_triplet,
    # "EndTime": EndTime_relation_to_triplet,
    # "Person": Person_relation_to_triplet
}
