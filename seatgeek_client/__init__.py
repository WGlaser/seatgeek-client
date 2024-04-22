# flake8: noqa
from .seatgeek import SeatGeek

from . import _version

__version__ = _version.get_versions(verbose=True)["version"]
