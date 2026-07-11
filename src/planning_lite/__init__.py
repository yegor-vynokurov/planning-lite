"""Planning Lite distribution CLI."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("planning-lite")
except PackageNotFoundError:
    # Allows importing directly from an unpacked source tree before installation.
    __version__ = "0+unknown"

__all__ = ["__version__"]
