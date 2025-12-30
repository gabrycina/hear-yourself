#!/usr/bin/env python3
"""
Audio Monitor - Menu Bar App
Hear your microphone through your speakers with minimal latency.

Made with love by Gabrycina & Claude Opus
"""

import rumps
import sounddevice as sd
import numpy as np
import os
import sys
import fcntl

# Single instance lock file
LOCK_FILE = os.path.expanduser("~/.audiomonitor.lock")


def ensure_single_instance():
    """Ensure only one instance of the app is running."""
    global lock_file_handle
    lock_file_handle = open(LOCK_FILE, 'w')
    try:
        fcntl.flock(lock_file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Write PID to lock file
        lock_file_handle.write(str(os.getpid()))
        lock_file_handle.flush()
        return True
    except IOError:
        # Another instance is running
        return False


class AudioMonitorApp(rumps.App):
    def __init__(self):
        super().__init__("Audio Monitor", icon=None, quit_button=None)

        self.stream = None
        self.is_running = False
        self.input_device = None
        self.output_device = None
        self.blocksize = 64
        self.samplerate = 48000

        # Get default devices
        self.input_device = sd.default.device[0]
        self.output_device = sd.default.device[1]

        # Build menu
        self.build_menu()

        # Update icon
        self.update_title()

        # Show welcome notification after a brief delay
        rumps.Timer(self.show_welcome, 1).start()

    def build_menu(self):
        """Build the menu with current devices."""
        self.menu.clear()

        # Status / Toggle
        if self.is_running:
            self.menu.add(rumps.MenuItem("● Monitoring Active", callback=None))
            self.menu.add(rumps.MenuItem("Stop Monitoring", callback=self.toggle_monitoring))
        else:
            self.menu.add(rumps.MenuItem("○ Monitoring Stopped", callback=None))
            self.menu.add(rumps.MenuItem("Start Monitoring", callback=self.toggle_monitoring))

        self.menu.add(rumps.separator)

        # Input devices submenu
        input_menu = rumps.MenuItem("Input Device")
        input_devices = self.get_input_devices()
        for idx, name in input_devices:
            item = rumps.MenuItem(
                f"{'✓ ' if idx == self.input_device else '   '}{name}",
                callback=lambda sender, i=idx: self.set_input_device(i)
            )
            input_menu.add(item)
        self.menu.add(input_menu)

        # Output devices submenu
        output_menu = rumps.MenuItem("Output Device")
        output_devices = self.get_output_devices()
        for idx, name in output_devices:
            item = rumps.MenuItem(
                f"{'✓ ' if idx == self.output_device else '   '}{name}",
                callback=lambda sender, i=idx: self.set_output_device(i)
            )
            output_menu.add(item)
        self.menu.add(output_menu)

        self.menu.add(rumps.separator)

        # Latency settings
        latency_menu = rumps.MenuItem("Latency")
        latencies = [
            (32, "Ultra Low (~1.3ms)"),
            (64, "Low (~2.7ms)"),
            (128, "Normal (~5.3ms)"),
            (256, "High (~10.7ms)"),
        ]
        for blocksize, label in latencies:
            item = rumps.MenuItem(
                f"{'✓ ' if blocksize == self.blocksize else '   '}{label}",
                callback=lambda sender, b=blocksize: self.set_latency(b)
            )
            latency_menu.add(item)
        self.menu.add(latency_menu)

        self.menu.add(rumps.separator)

        # About
        self.menu.add(rumps.MenuItem("About", callback=self.show_about))
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))

    def get_input_devices(self):
        """Get list of input devices."""
        devices = []
        for i, dev in enumerate(sd.query_devices()):
            if dev['max_input_channels'] > 0:
                devices.append((i, dev['name']))
        return devices

    def get_output_devices(self):
        """Get list of output devices."""
        devices = []
        for i, dev in enumerate(sd.query_devices()):
            if dev['max_output_channels'] > 0:
                devices.append((i, dev['name']))
        return devices

    def update_title(self):
        """Update menu bar title/icon."""
        if self.is_running:
            self.title = "🎙"
        else:
            self.title = "🎙️"  # Slightly different to show state (or use 🔇)

    def audio_callback(self, indata, outdata, frames, time, status):
        """Direct passthrough callback."""
        if status:
            print(status)
        outdata[:] = indata

    def start_stream(self):
        """Start the audio stream."""
        try:
            self.stream = sd.Stream(
                device=(self.input_device, self.output_device),
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                dtype=np.float32,
                latency='low',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_running = True
            self.update_title()
            self.build_menu()
        except Exception as e:
            rumps.alert("Error", f"Could not start audio stream:\n{e}")

    def stop_stream(self):
        """Stop the audio stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_running = False
        self.update_title()
        self.build_menu()

    def toggle_monitoring(self, _):
        """Toggle monitoring on/off."""
        if self.is_running:
            self.stop_stream()
        else:
            self.start_stream()

    def set_input_device(self, device_idx):
        """Set input device."""
        was_running = self.is_running
        if was_running:
            self.stop_stream()
        self.input_device = device_idx
        self.build_menu()
        if was_running:
            self.start_stream()

    def set_output_device(self, device_idx):
        """Set output device."""
        was_running = self.is_running
        if was_running:
            self.stop_stream()
        self.output_device = device_idx
        self.build_menu()
        if was_running:
            self.start_stream()

    def set_latency(self, blocksize):
        """Set latency (blocksize)."""
        was_running = self.is_running
        if was_running:
            self.stop_stream()
        self.blocksize = blocksize
        self.build_menu()
        if was_running:
            self.start_stream()

    def show_welcome(self, _=None):
        """Show welcome notification pointing to menu bar."""
        try:
            rumps.notification(
                title="Audio Monitor is running!",
                subtitle="Look for 🎙 in your menu bar",
                message="Click the microphone icon to start monitoring and change settings.",
                sound=False
            )
        except Exception:
            pass  # Notification may fail in some environments, that's ok

    def show_about(self, _):
        """Show about dialog."""
        rumps.alert(
            title="Hear Yourself",
            message="Hear your microphone through your speakers\nwith minimal latency.\n\n"
                    "Made with ♥ by Gabrycina & Claude Opus\n\n"
                    "github.com/gabrycina/hear-yourself",
            ok="Nice!"
        )

    def quit_app(self, _):
        """Quit the application."""
        self.stop_stream()
        # Release lock file
        try:
            fcntl.flock(lock_file_handle, fcntl.LOCK_UN)
            lock_file_handle.close()
            os.remove(LOCK_FILE)
        except:
            pass
        rumps.quit_application()


if __name__ == "__main__":
    if not ensure_single_instance():
        # Already running - show alert and exit
        rumps.alert(
            title="Audio Monitor Already Running",
            message="Look for 🎙 in your menu bar!\n\nThe app is already running. Click the microphone icon to access settings.",
            ok="Got it!"
        )
        sys.exit(0)

    app = AudioMonitorApp()
    app.run()
