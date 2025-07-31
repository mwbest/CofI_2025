# cofi_reduction/__init__.py

from .processor import CofiProcessor
from .widget import CofiReductionWidget
from .rvprocessor import AstroAnalysis
from .log import CofiLogger
from .cofi_stacker import stacker
# from .widget4 import CofiReductionWidget1
# FunctionParameterWidget1 is no longer needed

__all__ = ["CofiProcessor", "CofiReductionWidget", "AstroAnalysis", "CofiLogger","stacker"]
