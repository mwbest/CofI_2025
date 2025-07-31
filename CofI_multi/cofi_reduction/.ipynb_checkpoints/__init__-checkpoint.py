# cofi_reduction/__init__.py

from .processor4 import CofiProcessor1
from .widget4 import CofiReductionWidget1
from .rvprocessor import AstroAnalysis
from .log import CofiLogger
from .cofi_stacker import stacker
# from .widget4 import CofiReductionWidget1
# FunctionParameterWidget1 is no longer needed

__all__ = ["CofiProcessor1", "CofiReductionWidget1", "AstroAnalysis", "CofiLogger","stacker"]