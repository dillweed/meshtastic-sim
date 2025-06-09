# Meshtastic Transmission Speed Simulator

This Python program simulates the transmission speeds of different Meshtastic radio presets by displaying text file contents in chunks, throttled to match the data rates of various Meshtastic configurations.

## Features

- Simulate message transmission speeds for all Meshtastic radio presets
- Visualize how different presets affect delivery time, speed, and range
- Supports file input, URL input, or built-in sample text
- Interactive and command-line modes

## Usage

### Interactive Mode

```bash
python meshtastic_sim.py
```

Follow the prompts to:
- View radio presets
- Simulate a transmission with a file, URL, or sample text
- See detailed transmission statistics

### Command-Line Mode

```bash
python meshtastic_sim.py [file_or_url] [preset_id]
```

- `file_or_url`: Path to a text file or a URL to fetch text from
- `preset_id`: (Optional) Preset number (1-8). Defaults to 6 (LongFast).

Example:
```bash
python meshtastic_sim.py sample 3
```

## Requirements

- Python 3.7 or higher
- No external dependencies

## License

MIT License. See [LICENSE](LICENSE) for details.
