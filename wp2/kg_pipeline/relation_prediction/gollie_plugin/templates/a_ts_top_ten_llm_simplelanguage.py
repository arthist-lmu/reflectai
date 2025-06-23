from typing import List, Optional  # Import Optional for optional fields
from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions  
"""


@dataclass
class Color(Template):
    """
    Color is a shade or tone.
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
class PhysicalObject(Template):
    """
    Physical Object is a thing.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    clothing: Optional[str] = (
        None  # Clothing such as robe, cloak, tunic, dress, armor, veil, crown, hat, sash, shoe, dress
    )
    instrument: Optional[str] = (
        None  # Instruments such as lute, viola da gamba, flute, trumpet, harp, drum, organ, piano
    )
    religious_object: Optional[str] = (
        None  # Religious objects such as crucifix, rosary, chalice, menorah, prayer beads, altar, icon, thurible, ark
    )
    tool: Optional[str] = (
        None  # Tools such as hammer, chisel, paintbrush, compass, quill, spindle, plow, loom, telescope, astrolabe
    )
    weapon: Optional[str] = (
        None  # Weapons such as sword, spear, bow and arrow, shield, dagger, cannon, musket, axe, slingshot
    )
    other_object: Optional[str] = (
        None  # For physical objects not covered by the specific categories (e.g., chair, goblet, mirror, book, crown, candle)
    )


def physical_object_relation_to_triplet(package: PhysicalObject) -> List[dict]:
    triplets = []

    object_label: Optional[str] = None
    if package.clothing is not None:
        object_label = package.clothing
    elif package.instrument is not None:
        object_label = package.instrument
    elif package.religious_object is not None:
        object_label = package.religious_object
    elif package.tool is not None:
        object_label = package.tool
    elif package.weapon is not None:
        object_label = package.weapon
    elif package.other_object is not None:
        object_label = package.other_object

    if object_label is None:
        return triplets

    triplets.append(
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
                "label": object_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": object_label,
                "s_class": "PhysicalObject",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "physical object",
                "wikidata_id": "wd:Q223557",
            },
        }
    )

    return triplets


@dataclass
class Season(Template):
    """
    Season is a time of year like Spring or Winter.
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
class Occupation(Template):
    """
    Occupation is a job.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    job: Optional[str] = (
        None  # Jobs such as blacksmith, baker, carpenter, weaver, scribe, fisherman, farmer
    )
    profession: Optional[str] = (
        None  # Professions such as doctor, lawyer, priest, nun, scholar, architect, artist, musician
    )
    social_role: Optional[str] = (
        None  # Social Roles like noblewoman, peasant, king, queen, soldier, merchant, guardian
    )
    other_occupation: Optional[str] = (
        None  # For occupations not covered by the specific categories (e.g., warrior, pilgrim)
    )


def occupation_relation_to_triplet(package: Occupation) -> List[dict]:
    triplets = []

    occupation_label: Optional[str] = None
    if package.job is not None:
        occupation_label = package.job
    elif package.profession is not None:
        occupation_label = package.profession
    elif package.social_role is not None:
        occupation_label = package.social_role
    elif package.other_occupation is not None:
        occupation_label = package.other_occupation

    if occupation_label is None:
        return triplets

    triplets.append(
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
                "label": occupation_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": occupation_label,
                "s_class": "Occupation",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "occupation",
                "wikidata_id": "wd:Q12737077",
            },
        }
    )

    return triplets


@dataclass
class AnatomicalStructure(Template):
    """
    Anatomical Structure is a body part.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    body_as_whole: Optional[str] = (
        None  # Body as a whole such as human body, torso, nude figure
    )
    head: Optional[str] = (
        None  # Parts of the head such as face, eye, ear, nose, mouth, hair
    )
    limb: Optional[str] = None  # Limbs such as arm, hand, finger, leg, foot, toe
    internal_organ: Optional[str] = (
        None  # Internal Organs such as heart, brain, lung, liver, ribcage (as a skeletal part)
    )
    other_part: Optional[str] = (
        None  # For anatomical parts not covered by specific categories (e.g., bone, skeleton, skin)
    )


def anatomical_structure_relation_to_triplet(
    package: AnatomicalStructure,
) -> List[dict]:
    triplets = []

    # Find the specific anatomical part mentioned in the package
    anatomical_label: Optional[str] = None
    if package.body_as_whole is not None:
        anatomical_label = package.body_as_whole
    elif package.head is not None:
        anatomical_label = package.head
    elif package.limb is not None:
        anatomical_label = package.limb
    elif package.internal_organ is not None:
        anatomical_label = package.internal_organ
    elif package.other_part is not None:
        anatomical_label = package.other_part

    if anatomical_label is None:
        return triplets

    triplets.append(
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
                "label": anatomical_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": anatomical_label,
                "s_class": "AnatomicalStructure",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "anatomical structure",
                "wikidata_id": "wd:Q4936952",
            },
        }
    )

    return triplets


@dataclass
class Person(Template):
    """
    Person is a human.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    historical_figure: Optional[str] = (
        None  # Historical figures Napoleon, Julius Caesar, Marie Antoinette, Queen Elizabeth I, Leonardo da Vinci
    )
    other_person_type: Optional[str] = (
        None  # For specific types not covered by the above (e.g., unknown person, self-portrait, group)
    )
    gender: Optional[str] = None  # Examples: man, woman, child, boy, girl
    age_group: Optional[str] = (
        None  # Examples: infant, toddler, child, adolescent, adult, elderly person
    )


def person_relation_to_triplet(package: Person) -> List[dict]:
    triplets = []

    person_label: Optional[str] = None
    if package.historical_figure is not None:
        person_label = package.historical_figure
    elif package.gender is not None:
        person_label = package.gender
    elif package.age_group is not None:
        person_label = package.age_group
    elif package.other_person_type is not None:
        person_label = package.other_person_type

    if person_label is None:
        return triplets

    triplets.append(
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
                "label": person_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": person_label,
                "s_class": "Person",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "human",
                "wikidata_id": "wd:Q5",
            },
        }
    )
    return triplets


@dataclass
class Animal(Template):
    """
    Animal is a living creature.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    domestic_animal: Optional[str] = (
        None  # Domestic animals such as dog, cat, horse, cow, sheep, goat, chicken, pig, donkey, goose, duck
    )
    wild_animal: Optional[str] = (
        None  # Wild animals such as lion, tiger, elephant, bear, deer, wolf, fox, boar, leopard, zebra, giraffe
    )
    other_animal: Optional[str] = (
        None  # For animals not covered by the specific categories (e.g., insect, bird, fish, reptile)
    )


def animal_relation_to_triplet(package: Animal) -> List[dict]:
    triplets = []

    animal_label: Optional[str] = None
    if package.domestic_animal is not None:
        animal_label = package.domestic_animal
    elif package.wild_animal is not None:
        animal_label = package.wild_animal
    elif package.other_animal is not None:
        animal_label = package.other_animal

    if animal_label is None:
        return triplets

    triplets.append(
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
                "label": animal_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": animal_label,
                "s_class": "Animal",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "animal",
                "wikidata_id": "wd:Q729",
            },
        }
    )
    return triplets


@dataclass
class Plant(Template):
    """
    Plant is a type of vegetation.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    flower: Optional[str] = (
        None  # Flowers such as rose, lily, sunflower, tulip, daisy, orchid
    )
    tree: Optional[str] = (
        None  # Trees such as oak, willow, pine, cypress, palm, fig tree
    )
    fruit: Optional[str] = (
        None  # Fruits such as apple, grape, orange, lemon, cherry, fig
    )
    vegetable: Optional[str] = (
        None  # Vegetables such as cabbage, carrot, onion, potato, squash, bean
    )
    herb: Optional[str] = (
        None  # Herbs such as rosemary, mint, basil, lavender, parsley, thyme
    )
    aquatic_plant: Optional[str] = (
        None  # Aquatic plants such as water lily, lotus, reeds, seaweed
    )
    mythical_plant: Optional[str] = (
        None  # Mythical plants such as Tree of Life, Golden Bough, Mandrake, Yggdrasil
    )
    other_plant: Optional[str] = (
        None  # For plants not covered by specific categories (e.g., shrub, grass, vine, mushroom (fungus))
    )


def plant_relation_to_triplet(package: Plant) -> List[dict]:
    triplets = []

    plant_label: Optional[str] = None
    if package.flower is not None:
        plant_label = package.flower
    elif package.tree is not None:
        plant_label = package.tree
    elif package.fruit is not None:
        plant_label = package.fruit
    elif package.vegetable is not None:
        plant_label = package.vegetable
    elif package.herb is not None:
        plant_label = package.herb
    elif package.aquatic_plant is not None:
        plant_label = package.aquatic_plant
    elif package.mythical_plant is not None:
        plant_label = package.mythical_plant
    elif package.other_plant is not None:
        plant_label = package.other_plant

    if plant_label is None:
        return triplets

    triplets.append(
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
                "label": plant_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": plant_label,
                "s_class": "Plant",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "plant",
                "wikidata_id": "wd:Q756",
            },
        }
    )
    return triplets


@dataclass
class Emotion(Template):
    """
    Emotion is a feeling or mood.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    joy: Optional[str] = (
        None  # Emotions like joy, happiness, euphoria, delight, amusement
    )
    sadness: Optional[str] = (
        None  # Emotions like sadness, grief, despair, melancholy, sorrow
    )
    anger: Optional[str] = (
        None  # Emotions like anger, rage, fury, irritation, resentment
    )
    fear: Optional[str] = None  # Emotions like fear, terror, anxiety, dread
    surprise: Optional[str] = (
        None  # Emotions like surprise, astonishment, shock, wonder
    )
    disgust: Optional[str] = (
        None  # Emotions like disgust, revulsion, abhorrence, contempt
    )
    love: Optional[str] = (
        None  # Emotions like love, affection, compassion, tenderness, adoration
    )
    calmness: Optional[str] = (
        None  # Emotions like calmness, serenity, tranquility, peace, relaxation
    )
    other_emotion: Optional[str] = (
        None  # For emotions not covered by the specific categories (e.g., confusion, excitement, shame, pride)
    )


def emotion_relation_to_triplet(package: Emotion) -> List[dict]:
    triplets = []

    emotion_label: Optional[str] = None
    if package.joy is not None:
        emotion_label = package.joy
    elif package.sadness is not None:
        emotion_label = package.sadness
    elif package.anger is not None:
        emotion_label = package.anger
    elif package.fear is not None:
        emotion_label = package.fear
    elif package.surprise is not None:
        emotion_label = package.surprise
    elif package.disgust is not None:
        emotion_label = package.disgust
    elif package.love is not None:
        emotion_label = package.love
    elif package.calmness is not None:
        emotion_label = package.calmness
    elif package.other_emotion is not None:
        emotion_label = package.other_emotion

    if emotion_label is None:
        return triplets

    triplets.append(
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
                "label": emotion_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": emotion_label,
                "s_class": "Emotion",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "emotion",
                "wikidata_id": "wd:Q149453",
            },
        }
    )
    return triplets


@dataclass
class GeographicalFeature(Template):
    """
    Geographical Feature is a natural place like a mountain.
    """

    artwork: str  # Artworks such as Mona Lisa, The Sistine Chapel, Guernica, The Birth of Venus, The Night Watch, The Starry Night

    landform: Optional[str] = (
        None  # Landforms such as mountain, hill, valley, plain, desert, island, cave, rock formation
    )
    body_of_water: Optional[str] = (
        None  # Bodies of water such as river, lake, ocean, sea, waterfall, spring, marsh, canal
    )
    climate_feature: Optional[str] = (
        None  # Climate features such as clouds, rain, snow, storm, rainbow, sunlight, moonlight
    )
    natural_phenomenon: Optional[str] = (
        None  # Natural phenomena such as volcano eruption, earthquake, aurora, flood, drought
    )
    other_feature: Optional[str] = (
        None  # For geographical features not covered by specific categories (e.g., forest, field, coast, sky)
    )


def geographical_feature_relation_to_triplet(
    package: GeographicalFeature,
) -> List[dict]:
    triplets = []

    feature_label: Optional[str] = None
    if package.landform is not None:
        feature_label = package.landform
    elif package.body_of_water is not None:
        feature_label = package.body_of_water
    elif package.climate_feature is not None:
        feature_label = package.climate_feature
    elif package.natural_phenomenon is not None:
        feature_label = package.natural_phenomenon
    elif package.other_feature is not None:
        feature_label = package.other_feature

    if feature_label is None:
        return triplets

    triplets.append(
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
                "label": feature_label,
            },
        }
    )

    triplets.append(
        {
            "subject": {
                "label": feature_label,
                "s_class": "GeographicalFeature",
            },
            "relation": {
                "label": "instance of",
                "wikidata_id": "wdt:P31",
            },
            "object": {
                "label": "geographical feature",
                "wikidata_id": "wd:Q271669",
            },
        }
    )
    return triplets


ENTITY_DEFINITIONS: List[Template] = [
    Color,
    PhysicalObject,
    Season,
    Occupation,
    AnatomicalStructure,
    Animal,
    Person,
    Plant,
    Emotion,
    GeographicalFeature,
]

ENTITY_PARSER = {
    "Color": color_relation_to_triplet,
    "PhysicalObject": physical_object_relation_to_triplet,
    "Season": season_relation_to_triplet,
    "Occupation": occupation_relation_to_triplet,
    "AnatomicalStructure": anatomical_structure_relation_to_triplet,
    "Animal": animal_relation_to_triplet,
    "Person": person_relation_to_triplet,
    "Plant": plant_relation_to_triplet,
    "Emotion": emotion_relation_to_triplet,
    "GeographicalFeature": geographical_feature_relation_to_triplet,
}
