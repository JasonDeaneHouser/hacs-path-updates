"""
Core DataUpdateCoordinator implementation for hoboken_path.

This coordinator manages data fetching from the PATH train API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api import PathApiClientError
from ..const import LOGGER

if TYPE_CHECKING:
    from ..data import PathConfigEntry


class PathDataUpdateCoordinator(DataUpdateCoordinator):
    """
    Coordinator to manage fetching PATH train data.

    This coordinator handles periodic data updates from the PATH API
    and distributes the data to all sensor entities.

    Attributes:
        config_entry: The config entry for this integration instance.
    """

    config_entry: PathConfigEntry

    async def _async_setup(self) -> None:
        """Set up the coordinator."""
        LOGGER.debug("PATH coordinator setup complete for %s", self.config_entry.entry_id)

    async def _async_update_data(self) -> dict[str, Any]:
        """
        Fetch train arrival data from the PATH API.

        Returns:
            Dictionary with station codes as keys and arrival data as values.

        Example:
            {
                "HOB": {
                    "station_code": "HOB",
                    "directions": {
                        "ToNY": [
                            {
                                "target": "33S",
                                "seconds_to_arrival": 120,
                                "arrival_message": "2 min",
                                "line_color": "FF9900",
                                "head_sign": "33rd Street",
                                "last_updated": "2025-12-30T..."
                            }
                        ]
                    }
                }
            }

        Raises:
            UpdateFailed: If data fetching fails.
        """
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except PathApiClientError as exception:
            LOGGER.exception("Error fetching PATH train data")
            raise UpdateFailed(
                translation_domain="hoboken_path",
                translation_key="update_failed",
            ) from exception
