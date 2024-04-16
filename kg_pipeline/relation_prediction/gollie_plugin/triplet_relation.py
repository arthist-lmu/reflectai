from typing import List

from .utils_typing import Relation, dataclass
from .utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class InceptionRelation(Template):
    """Year when an painting was painted or created. The creation date of a painting refers to the specific year or range of years 
    during which the artwork was produced. This date can sometimes be precisely known or estimated based on historical records, 
    stylistic analysis, or the artist's own documentation."""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    date: int # The year in which the picture was painted or created


@dataclass
class CreatorRelation(Template):
    """The name or pseudonym of the painter that created the painting. The creator is involved in the conception and creation of artwork 
    through various techniques and mediums including oil, acrylic, watercolor, frescoes, and more. 
    Their work is not limited to just creating paintings; many painters also delve into the realms of 
    drawing, sculpting, and other forms of visual art expressions. 
    """

    painting: str  # The name of the painting, Such as Mona Lisa, Starry Night, Guernica, The Scream
    creator: str  # The name of the painter, i.e. Leonardo da Vinci, Vincent van Gogh, Pablo Picasso, Edvard Munch


@dataclass
class PaintingDepictsRelation(Template):
    """The object the painting depicts. The subject matter of a painting refers to the main object, scene, or theme that is depicted in the artwork. 
    This can include people, landscapes, still lifes, abstract forms, and more. The subject matter is a critical element of art that helps convey 
    the painter's message, emotions, and intent."""

    painting: str  # The name of the painting, Such as Mona Lisa, Starry Night, Guernica, The Scream
    depicts: str  # The name of an object shown in the painting, Such as Portrait, Landscape, abstract forms, emotions, historical scences, saints, biblical episodes 


@dataclass
class LocationCreationRelation(Template):
    """Name of the location the painting was created. The location of creation refers to the specific place or setting where an artwork, 
    particularly a painting, was physically created by the artist. This could be an artist's studio, a plein air (outdoor) site, a particular 
    city or country, or any space that has influenced the work's execution."""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    creator: str  # The name of the location, i.e. Florence, Provence, Paris, Oslo


@dataclass
class MovementRelation(Template):
    """The movement with which the painting is associated. An artistic movement is a style or tendency in art with a specific common philosophy or 
    goal, followed by a group of artists during a restricted period of time. Artistic movements are usually characterized by a distinctive style 
    or technique that emerges as a reaction to preceding art forms, social conditions, or artistic philosophies.

"""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    movement: str  # The name of the movement, i.e. Renaissance, Impressionism, Kubism, Expressionism


ENTITY_DEFINITIONS: List[Template] = [
    InceptionRelation,
    CreatorRelation,
    PaintingDepictsRelation,
    LocationCreationRelation,
    MovementRelation,
]
