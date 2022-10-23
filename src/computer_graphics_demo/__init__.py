"""``computer_graphics_demo/__init__.py``."""

import logging
from typing import Final

logger = logging.getLogger(__name__)

try:
    from get_version import get_version, NoVersionFound

    try:
        __version__ = get_version(__file__)
    except NoVersionFound:
        __version__ = "0.0.0"
except ImportError:
    __version__ = "Please install get_version!"

_binname: Final = "cgdemo"
