"""Constants for hoboken_path."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# Integration metadata
DOMAIN = "hoboken_path"
ATTRIBUTION = "Data provided by Port Authority of NY & NJ"

# Platform parallel updates - applied to all platforms
PARALLEL_UPDATES = 1

# Default configuration values
DEFAULT_UPDATE_INTERVAL_SECONDS = 15
DEFAULT_ENABLE_DEBUGGING = False

# API Configuration
API_ENDPOINT = "https://www.panynj.gov/bin/portauthority/ridepath.json"
API_TIMEOUT = 10

# Station codes
STATIONS = {
    "NWK": "Newark",
    "HAR": "Harrison",
    "JSQ": "Journal Square",
    "GRV": "Grove Street",
    "NEW": "Newport",
    "EXP": "Exchange Place",
    "WTC": "World Trade Center",
    "CHR": "Christopher Street",
    "09S": "9th Street",
    "14S": "14th Street",
    "23S": "23rd Street",
    "33S": "33rd Street",
    "HOB": "Hoboken",
}
