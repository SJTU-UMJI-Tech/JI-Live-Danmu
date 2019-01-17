# JI-Live-Danmu-Client

## Usage

```bash
cp <cert_filepath> .
LiteDanmu.py [-h] [-serverurl SERVERURL]
```

## Build

1. Install pyinstaller

   ```bash
   pip install pyinstaller
   ```

2. Build

   ```bash
   pyinstaller .\LiteDanmu.py
   mv dist/LiteDanmu/PyQt5/Qt/plugins/platforms/ dist/LiteDanmu
   ```

3. Run

   ```bash
   dist/LiteDanmu/LiteDanmu.exe [-h] [-serverurl SERVERURL]
   ```
