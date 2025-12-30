# Hear Yourself 🎙

A free, low-latency audio monitor for macOS. Hear your microphone through your speakers/headphones in real-time.

**[Download for macOS →](https://github.com/gabrycina/hear-yourself/releases/latest)**

![Screenshot](screenshot.png)

## Features

- **Low latency** - As low as ~1.3ms delay
- **Menu bar app** - Lives quietly in your menu bar
- **Live device switching** - Change input/output without restart
- **Free & open source** - No ads, no subscriptions

## Why?

The popular tool [LineIn](https://rogueamoeba.com/legacy/) was discontinued in 2017 and doesn't work on modern macOS. Paid alternatives cost $50-120. We made a free one.

## Use Cases

- Test your microphone setup
- Monitor yourself while recording podcasts
- Hear yourself while streaming
- Practice singing or speaking
- Reduce audio delay when gaming

## Installation

### Option 1: Download the App (Recommended)
1. Download `HearYourself.app.zip` from [Releases](https://github.com/gabrycina/hear-yourself/releases/latest)
2. Unzip and drag to Applications
3. Double-click to run
4. Look for 🎙 in your menu bar

### Option 2: Run from Source
```bash
git clone https://github.com/gabrycina/hear-yourself.git
cd hear-yourself
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Usage

1. Click the 🎙 icon in your menu bar
2. Select your input device (microphone)
3. Select your output device (speakers/headphones)
4. Click "Start Monitoring"
5. Adjust latency if needed (lower = less delay, but may cause glitches)

## Requirements

- macOS 10.13 or later
- Microphone access permission

## Tech Stack

- Python 3
- [sounddevice](https://python-sounddevice.readthedocs.io/) (PortAudio bindings)
- [rumps](https://github.com/jaredks/rumps) (macOS menu bar framework)

---

Made with ♥ by [Gabrycina](https://github.com/gabrycina) & Claude Opus
