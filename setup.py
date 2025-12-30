"""
Setup script for building Hear Yourself as a standalone macOS app.
"""

from setuptools import setup

APP = ['app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Hear Yourself',
        'CFBundleDisplayName': 'Hear Yourself',
        'CFBundleIdentifier': 'com.gabrycina.hearyourself',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.13',
        'LSUIElement': True,  # Menu bar app, no dock icon
        'NSHighResolutionCapable': True,
        'NSMicrophoneUsageDescription': 'Hear Yourself needs microphone access to pass audio through to your speakers.',
    },
    'packages': ['rumps', 'sounddevice', 'numpy'],
}

setup(
    app=APP,
    name='Hear Yourself',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
