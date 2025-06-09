# Meshtastic Transmission Simulator

Simulates Meshtastic radio preset transmission speeds by displaying text content in real-time chunks, throttled to match actual LoRa data rates.

## Quick Start

```bash
# Interactive mode
python meshtastic_sim.py

# Quick demo
python meshtastic_sim.py sample

# Test specific file and preset
python meshtastic_sim.py my_file.txt 3
```

## Radio Presets

| # | Preset | Speed | Range | Notes |
|---|--------|-------|-------|-------|
| 1 | Short Turbo | 21.88 kbps | 2-5km | Fastest |
| 2 | Short Fast | 10.94 kbps | 3-8km | Urban |
| 3 | Short Slow | 6.25 kbps | 5-12km | Suburban |
| 4 | Medium Fast | 3.52 kbps | 8-15km | Balanced |
| 5 | Medium Slow | 1.95 kbps | 10-20km | Rural |
| **6** | **Long Fast** | **1.07 kbps** | **15-25km** | **Default** |
| 7 | Long Moderate | 0.34 kbps | 20-35km | Remote |
| 8 | Long Slow | 0.18 kbps | 25-50km+ | Maximum range |

## Example Output

```
======================================================================
  TRANSMISSION ANALYSIS
======================================================================
Preset:     Long Range / Fast (1.07 kbps)
Technical:  SF 11/2048, BW 250kHz, CR 4/5
Content:    1,543 chars (7 packets)
Duration:   2.6 minutes
======================================================================

Starting transmission... (Press Ctrl+C to stop)

[   1/   7] ............... OK
Welcome to the Meshtastic Network!
[   2/   7] ............... OK
This message demonstrates how preset #6 affects delivery time...
```

## Usage

### Interactive Mode
```bash
python meshtastic_sim.py
```
Menu-driven interface with all options.

### Direct Mode
```bash
python meshtastic_sim.py [source] [preset_id]
```

**Sources:**
- `sample` - Built-in demo text
- `file.txt` - Local file path  
- `https://example.com/text.txt` - URL

**Presets:** 1-8 (defaults to 6 - LongFast)

## Features

- **Realistic timing** - Uses actual Meshtastic data rates and 237-byte packets
- **Multiple inputs** - Files, URLs, or sample text
- **Live simulation** - Shows packet-by-packet transmission with delays
- **Analysis** - Pre-transmission estimates and final statistics
- **All presets** - Complete set of Meshtastic radio configurations

## Use Cases

- **Compare presets** for your message types and network conditions
- **Understand trade-offs** between speed, range, and delivery time
- **Plan networks** by testing realistic transmission scenarios
- **Education** - Demonstrate LoRa performance characteristics

## Requirements

- Python 3.7+
- No external dependencies

## Installation

```bash
git clone https://github.com/dillweed/meshtastic-sim.git
cd meshtastic-sim
python meshtastic_sim.py
```

## Technical Notes

- Packet size: 237 bytes (actual Meshtastic payload)
- Data rates: Official Meshtastic specifications
- Timing: Accounts for LoRa spreading factors and coding rates
- Real performance varies by terrain, interference, and network congestion

## License

MIT License