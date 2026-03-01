# components/__init__.py — Reusable video segment components for TheBoringAI
#
# Usage in any scene:
#   from components import Opening, Closing, PauseAndPonder, ChapterCard, Bumper
#   from components import OctopusCreature, OctopusAnimations, OctopusTeaches

from components.opening import *
from components.closing import *
from components.pause_ponder import *
from components.chapter_card import *
from components.bumper import *
from components.watermark import *
from components.subscribe_cta import *
from components.lower_thirds import *
from components.octopus import (
    OctopusCreature,
    ProfessorOctopus,
    BabyOctopus,
    NeuralOctopus,
    DataOctopus,
    OctopusAnimations,
    OctopusTeaches,
)
