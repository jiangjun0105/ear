# Ear: A Speech Recognition Desktop App using OpenAI Whisper API

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


# Install


# Develop

To setup develop environment (you need `brew` and `conda`):
```bash
# Create virtual environment
conda create -n ear
conda activate ear
```

Install ffmpeg (see more [here](https://qiita.com/ko-izumi/items/449aa2f00ae5bd127672) if the following command doesn't work for you)
```bash
brew postinstall libtasn1
brew install ffmpeg
```

Install all python requirements:
```
pip install -r requirements.txt
```

To encapsulate the app:
```bash
pyinstaller ./ear.spec
```
