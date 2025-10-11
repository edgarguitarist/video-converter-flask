# Conversor de Video (Flask + ffmpeg)

Pequeña app web para convertir videos arrastrando y soltando.

## Requisitos
- Python 3.12+
- ffmpeg instalado y en el PATH del sistema.

### Instalar ffmpeg
**Windows (recomendado con scoop):**
```powershell
scoop install ffmpeg
```
Con Chocolatey:
```powershell
choco install ffmpeg
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

## Instalación y ejecución
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python app.py
```

Abre http://localhost:5000 en tu navegador.