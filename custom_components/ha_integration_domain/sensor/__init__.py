"""Sensor platform for hoboken_path."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN, PARALLEL_UPDATES as PARALLEL_UPDATES, STATIONS

if TYPE_CHECKING:
    from ..coordinator import PathDataUpdateCoordinator
    from ..data import PathConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PathConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PATH train sensors."""
    coordinator = entry.runtime_data.coordinator

    # Create sensors for each station/destination combination
    entities: list[PathTrainSensor] = []

    # Wait for first data fetch
    if coordinator.data:
        # Collect all unique destinations per station
        station_destinations: dict[str, set[str]] = {}

        for station_code, station_data in coordinator.data.items():
            destinations = set()

            # Collect all unique destinations from all directions
            for trains in station_data.get("directions", {}).values():
                for train in trains:
                    destination = train.get("head_sign")
                    if destination:
                        destinations.add(destination)

            if destinations:
                station_destinations[station_code] = destinations

        # Create one sensor per (station, destination) combination
        for station_code, destinations in station_destinations.items():
            station_name = STATIONS.get(station_code, station_code)

            entities.extend(
                PathTrainSensor(
                    coordinator=coordinator,
                    station_code=station_code,
                    station_name=station_name,
                    destination=destination,
                )
                for destination in sorted(destinations)
            )

    async_add_entities(entities)


class PathTrainSensor(CoordinatorEntity, SensorEntity):
    """Sensor for PATH train arrivals to a specific destination."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = None

    def __init__(
        self,
        coordinator: PathDataUpdateCoordinator,
        station_code: str,
        station_name: str,
        destination: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._station_code = station_code
        self._station_name = station_name
        self._destination = destination

        # Create unique ID using destination
        # Use a safe version of destination for unique_id
        safe_destination = destination.lower().replace(" ", "_").replace("&", "and")
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{station_code}_{safe_destination}"

        # Set entity name - shows destination: "to World Trade Center"
        self._attr_name = f"to {destination}"

        # Set device info - group by station
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{coordinator.config_entry.entry_id}_{station_code}")},
            "name": station_name,
            "manufacturer": "Port Authority of NY & NJ",
            "model": "PATH Station",
        }

    @property
    def native_value(self) -> str | None:
        """Return the next train arrival time for this destination."""
        trains = self._get_trains_to_destination()

        if not trains:
            return "No trains"

        # Return the arrival message of the next train
        return trains[0].get("arrival_message", "Unknown")

    def _get_trains_to_destination(self) -> list[dict[str, Any]]:
        """Get all trains heading to the specific destination."""
        if not self.coordinator.data:
            return []

        station_data = self.coordinator.data.get(self._station_code)
        if not station_data:
            return []

        # Collect all trains going to this destination from all directions
        matching_trains: list[dict[str, Any]] = []

        for trains in station_data.get("directions", {}).values():
            matching_trains.extend(train for train in trains if train.get("head_sign") == self._destination)

        # Sort by arrival time (seconds_to_arrival)
        matching_trains.sort(key=lambda t: t.get("seconds_to_arrival", 999999))

        return matching_trains

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return upcoming trains to this specific destination."""
        trains = self._get_trains_to_destination()

        if not trains:
            return {
                "station": self._station_name,
                "station_code": self._station_code,
                "destination": self._destination,
                "trains": "No trains scheduled",
            }

        # Build attributes showing next trains to this destination
        attributes = {
            "station": self._station_name,
            "station_code": self._station_code,
            "destination": self._destination,
            "train_count": len(trains[:4]),
        }

        # Add each train (up to 4)
        for i, train in enumerate(trains[:4], 1):
            arrival = train.get("arrival_message", "")
            color = train.get("line_color", "FFFFFF")
            minutes = train.get("seconds_to_arrival", 0) // 60

            attributes[f"train_{i}_arrival"] = arrival
            attributes[f"train_{i}_minutes"] = minutes
            attributes[f"train_{i}_color"] = f"#{color}"
            attributes[f"train_{i}_last_updated"] = train.get("last_updated", "")

        # Summary of all trains to this destination
        if len(trains) > 1:
            arrivals_list = [train.get("arrival_message", "") for train in trains[:4]]
            attributes["all_arrivals"] = ", ".join(arrivals_list)

            train_summary = "\n".join([f"{i}. {train.get('arrival_message')}" for i, train in enumerate(trains[:4], 1)])
            attributes["arrival_list"] = train_summary

        return attributes

    @property
    def icon(self) -> str:
        """Return the icon for the sensor."""
        return "mdi:train"
