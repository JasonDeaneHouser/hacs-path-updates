"""
Custom integration for Hoboken PATH Trains with Home Assistant.

This integration provides real-time PATH train arrival information
from the Port Authority of NY & NJ API.

For more details:
https://github.com/JasonDeaneHouser/hacs-path-updates
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import PathApiClient
from .const import DEFAULT_UPDATE_INTERVAL_SECONDS, DOMAIN, LOGGER
from .coordinator import PathDataUpdateCoordinator
from .data import PathData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PathConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Hoboken PATH integration."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PathConfigEntry,
) -> bool:
    """
    Set up PATH trains from a config entry.

    Creates the API client and coordinator for real-time train data.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being set up.

    Returns:
        True if setup was successful.

    """
    # Get optional station filter from config entry
    station_filter = entry.data.get("stations")

    # Initialize API client
    client = PathApiClient(
        session=async_get_clientsession(hass),
        station_filter=station_filter,
    )

    # Initialize data update coordinator
    coordinator = PathDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL_SECONDS),
        always_update=True,
    )

    # Store runtime data
    entry.runtime_data = PathData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # Perform initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PathConfigEntry,
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
