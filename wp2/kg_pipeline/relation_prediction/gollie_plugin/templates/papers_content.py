from typing import List

from ..utils_typing import Relation, dataclass
from ..utils_typing import Generic as Template

"""
Relation definitions
"""


@dataclass
class NamesMentioned(Template):
    """Names of people, researchers, artists, writer, philosophers or other people which are mentioned in the article. They could be quoted or
    cited in order to enrich the text.
    """

    text: str  # The name of the given article
    name: str  # The name of the researcher, artist, writer, philosopher who was quoted in the article


@dataclass
class ArtworksMentioned(Template):
    """
    …
    """

    text: str  # The name of the given article
    name: str  # The name of the artworks mentioned in the text like


@dataclass
class InceptionRelation(Template):
    """Year when an painting was painted or created. The creation date of a painting refers to the specific year or range of years
    during which the artwork was produced. This date can sometimes be precisely known or estimated based on historical records,
    stylistic analysis, or the artist's own documentation."""

    painting: str  # The name of the painting, i.e. Mona Lisa, Starry Night, Guernica, The Scream
    date: int  # The year in which the picture was painted or created


@dataclass
class PaintingMaterial(Template):
    """The material of a painting like oil painting on canvas"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    material: str  # The material of a painting, i.e. oil on canvas


@dataclass
class PaintingGenre(Template):
    """The genre of a painting like abstract, portrait, still life or landscape"""

    painting: str  # The name of the painting, i.e. Mona Lisa
    subject: str  # The genre of a painting, i.e. portrait, landscape


@dataclass
class AliasNames(Template):
    """Alias names for artworks refer to alternative titles or nicknames that a piece of art
    may acquire beyond its official title. These alternative names often arise from the
    public, critics, or the artists themselves and can reflect popular interpretations,
    striking features, or emotional responses elicited by the artwork."""

    painting: str  # The name of the painting, i.e. Mona Lisa
    alias: str  # The alias name of a painting, i.e. La Gioconda


@dataclass
class TitleLanguages(Template):
    """Names of artworks in different languages represent the various translations or
    adaptations of an artwork's title across cultural and linguistic boundaries."""

    painting: str  # The name of the painting, i.e. The Scream
    GermanName: str  # The German name of a painting, Der Schrei
    FrenchName: str  # The French name of a painting, Le Cri
    EnglishName: str  # The English name of painting, The Scream


ENTITY_DEFINITIONS: List[Template] = [
    NamesMentioned,
    ArtworksMentioned,
]


ENTITY_PARSER = {}
