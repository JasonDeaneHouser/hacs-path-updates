"""
API Client for hoboken_path.

This module provides the API client for communicating with the PATH train API.
"""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp

from ..const import API_ENDPOINT, API_TIMEOUT


class PathApiClientError(Exception):
    """Base exception to indicate a general API error."""


class PathApiClientCommunicationError(
    PathApiClientError,
):
    """Exception to indicate a communication error with the API."""


class PathApiClient:
    """
    API Client for PATH train data.

    This client fetches real-time train arrival information from the
    Port Authority of NY & NJ PATH API.

    Attributes:
        _session: The aiohttp ClientSession for making requests.
        _station_filter: Optional list of station codes to filter results.

    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        station_filter: list[str] | None = None,
    ) -> None:
        """
        Initialize the API Client.

        Args:
            session: The aiohttp ClientSession to use for requests.
            station_filter: Optional list of station codes to monitor (e.g., ["HOB", "JSQ"]).

        """
        self._session = session
        self._station_filter = station_filter

    async def async_get_data(self) -> dict[str, Any]:
        """
        Get train arrival data from the PATH API.

        Returns:
            A dictionary with station codes as keys and arrival data as values.
            Example structure:
            {
                "HOB": {
                    "station_name": "Hoboken",
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
            PathApiClientCommunicationError: If communication fails.
            PathApiClientError: For other API errors.

        """
        try:
            async with asyncio.timeout(API_TIMEOUT):
                response = await self._session.get(API_ENDPOINT)
                response.raise_for_status()
                data = await response.json()

                # Process the results
                processed_data: dict[str, Any] = {}

                for station_data in data.get("results", []):
                    station_code = station_data.get("consideredStation")

                    # Filter by station if specified
                    if self._station_filter and station_code not in self._station_filter:
                        continue

                    # Process destinations and messages
                    directions: dict[str, list[dict[str, Any]]] = {}
                    for destination in station_data.get("destinations", []):
                        direction_label = destination.get("label")

                        messages = [
                            {
                                "target": msg.get("target"),
                                "seconds_to_arrival": int(msg.get("secondsToArrival", 0)),
                                "arrival_message": msg.get("arrivalTimeMessage"),
                                "line_color": msg.get("lineColor"),
                                "head_sign": msg.get("headSign"),
                                "last_updated": msg.get("lastUpdated"),
                            }
                            for msg in destination.get("messages", [])
                        ]

                        if messages:
                            directions[direction_label] = messages

                    if directions:
                        processed_data[station_code] = {
                            "station_code": station_code,
                            "directions": directions,
                        }

                return processed_data

        except TimeoutError as exception:
            msg = f"Timeout error fetching PATH train data - {exception}"
            raise PathApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching PATH train data - {exception}"
            raise PathApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Unexpected error processing PATH data - {exception}"
            raise PathApiClientError(
                msg,
            ) from exception
