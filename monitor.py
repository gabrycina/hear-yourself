#!/usr/bin/env python3
"""
Low-latency audio monitor - hear your microphone through your speakers/headphones.
Press Ctrl+C to stop.
"""

import sounddevice as sd
import numpy as np
import argparse
import sys


def list_devices():
    """List all available audio devices."""
    print(sd.query_devices())


def audio_callback(indata, outdata, frames, time, status):
    """Direct passthrough callback - copies input to output."""
    if status:
        print(status, file=sys.stderr)
    outdata[:] = indata


def main():
    parser = argparse.ArgumentParser(description='Low-latency microphone monitor')
    parser.add_argument('-l', '--list', action='store_true', help='List audio devices')
    parser.add_argument('-i', '--input', type=int, default=None, help='Input device index')
    parser.add_argument('-o', '--output', type=int, default=None, help='Output device index')
    parser.add_argument('-b', '--blocksize', type=int, default=64,
                        help='Block size in frames (lower = less latency, default: 64)')
    parser.add_argument('-r', '--samplerate', type=int, default=48000,
                        help='Sample rate (default: 48000)')
    parser.add_argument('-c', '--channels', type=int, default=1,
                        help='Number of channels (default: 1)')
    args = parser.parse_args()

    if args.list:
        list_devices()
        return

    # Configure for low latency
    latency = 'low'

    print(f"Audio Monitor - Microphone Passthrough")
    print(f"=======================================")
    print(f"Sample rate: {args.samplerate} Hz")
    print(f"Block size: {args.blocksize} frames")
    print(f"Channels: {args.channels}")
    print(f"Estimated latency: ~{(args.blocksize / args.samplerate) * 1000 * 2:.1f} ms")
    print()

    if args.input is not None:
        print(f"Input device: {sd.query_devices(args.input)['name']}")
    else:
        print(f"Input device: {sd.query_devices(kind='input')['name']} (default)")

    if args.output is not None:
        print(f"Output device: {sd.query_devices(args.output)['name']}")
    else:
        print(f"Output device: {sd.query_devices(kind='output')['name']} (default)")

    print()
    print("Press Ctrl+C to stop...")
    print()

    try:
        with sd.Stream(
            device=(args.input, args.output),
            samplerate=args.samplerate,
            blocksize=args.blocksize,
            dtype=np.float32,
            latency=latency,
            channels=args.channels,
            callback=audio_callback
        ):
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
