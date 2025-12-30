"""Custom types for hoboken_path."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import PathApiClient
    from .coordinator import PathDataUpdateCoordinator


type PathConfigEntry = ConfigEntry[PathData]


@dataclass
class PathData:
    """Data for hoboken_path."""

    client: PathApiClient
    coordinator: PathDataUpdateCoordinator
    integration: Integration
