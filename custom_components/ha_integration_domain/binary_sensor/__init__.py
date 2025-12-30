"""Binary sensor platform for hoboken_path."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN, PARALLEL_UPDATES as PARALLEL_UPDATES

if TYPE_CHECKING:
    from ..coordinator import PathDataUpdateCoordinator
    from ..data import PathConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PathConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PATH connectivity sensor."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities([PathConnectivitySensor(coordinator)])


class PathConnectivitySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for PATH API connectivity."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True
    _attr_name = "API Connectivity"

    def __init__(self, coordinator: PathDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_connectivity"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": "PATH Train API",
            "manufacturer": "Port Authority of NY & NJ",
            "model": "PATH Real-time API",
        }

    @property
    def is_on(self) -> bool:
        """Return true if API is connected."""
        return self.coordinator.last_update_success and bool(self.coordinator.data)
