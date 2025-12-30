# Hoboken PATH Trains

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.11%2B-blue.svg)](https://www.home-assistant.io/)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Home Assistant custom integration that provides real-time PATH train arrival information for Hoboken and other PATH stations.

## Features

- 🚂 Real-time train arrival data from Port Authority of NY & NJ
- 📍 Sensors organized by destination station
- ⏱️ Shows next train arrival times with countdown
- 🔄 Updates every 15 seconds
- 🎯 Clean sensor structure: see all trains going to each destination

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository: `https://github.com/JasonDeaneHouser/hacs-path-updates`
5. Category: Integration
6. Click "Add"
7. Search for "Hoboken PATH Trains" in HACS
8. Click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/hoboken_path` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Hoboken PATH Trains**
4. Follow the configuration steps

## Sensor Structure

The integration creates sensors organized by **destination**. Each sensor shows when the next trains are arriving to that specific destination.

### Example Sensors

For each PATH station, you'll get sensors like:
- `sensor.newark_to_world_trade_center` - Next trains to World Trade Center
- `sensor.newark_to_33rd_street` - Next trains to 33rd Street
- `sensor.newark_to_hoboken` - Next trains to Hoboken

### Sensor State

The sensor state shows the **next train's arrival time** (e.g., "2 min", "5 min", "Arriving")

### Sensor Attributes

Each sensor provides detailed information:

- `station` - Current station name (e.g., "Newark")
- `destination` - Where trains are heading (e.g., "World Trade Center")
- `train_count` - Number of upcoming trains (up to 4)
- `train_1_arrival` through `train_4_arrival` - Arrival times for each train
- `train_1_minutes` through `train_4_minutes` - Minutes until arrival
- `train_1_color` through `train_4_color` - LINE color codes
- `all_arrivals` - Comma-separated list of all arrival times
- `arrival_list` - Formatted numbered list of arrivals

## Supported Stations

- Newark (NWK)
- Harrison (HAR)
- Journal Square (JSQ)
- Grove Street (GRV)
- Newport (NEW)
- Exchange Place (EXP)
- World Trade Center (WTC)
- Christopher Street (CHR)
- 9th Street (09S)
- 14th Street (14S)
- 23rd Street (23S)
- 33rd Street (33S)
- Hoboken (HOB)

## API Source

This integration uses the official Port Authority of NY & NJ PATH API:
`https://www.panynj.gov/bin/portauthority/ridepath.json`

No authentication required. Data updates every 15 seconds.

## Support

- Report issues: [GitHub Issues](https://github.com/JasonDeaneHouser/hacs-path-updates/issues)
- Repository: [GitHub](https://github.com/JasonDeaneHouser/hacs-path-updates)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
