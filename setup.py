from setuptools import setup

APP = ['app.py']
OPTIONS = {
    'iconfile': 'media/ear.jpeg',
    'plist': {
        'CFBundleName': 'SystemTrayApp',
        'CFBundleIdentifier': 'com.example.SystemTrayApp',
        'LSUIElement': 1,
    },
    'packages': ['PyQt6'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
