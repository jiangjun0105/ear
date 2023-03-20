from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'media/ear.icns',
    'plist': {
        'CFBundleName': 'SystemTrayApp',
        'CFBundleIdentifier': 'com.example.SystemTrayApp',
        'LSUIElement': 1,
        'NSStatusItemVisible': True,
    },
    'packages': ['PyQt6'],
}

setup(
    app=APP,
    name="Ear",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
