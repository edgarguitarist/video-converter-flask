# 🎬 Conversor de Videos (Flask + ffmpeg)

Aplicación web y herramienta de línea de comandos para convertir videos usando ffmpeg con soporte para aceleración GPU.

## ✨ Características

- 🌐 **Interfaz Web**: Drag & drop intuitivo en http://localhost:5000
- 💻 **Línea de Comandos**: Scripts PowerShell para conversión rápida
- ⚡ **Aceleración GPU**: Soporte NVENC para GPUs NVIDIA
- 📊 **Progreso en Tiempo Real**: Barras de progreso y logs detallados
- 🔄 **Múltiples Formatos**: MP4, WebM, AVI, MKV
- 🎯 **Integración PowerShell**: Funciones globales para tu perfil

## 🔧 Requisitos

- **Python 3.12+**
- **ffmpeg** instalado y en el PATH del sistema
- **GPU NVIDIA** (opcional, para aceleración)

### Instalar ffmpeg

**Windows (recomendado con scoop):**

```powershell
scoop install ffmpeg
```

**Con Chocolatey:**

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

## 🚀 Instalación

```powershell
# Clonar o descargar el proyecto
cd video-converter-flask

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# .venv\Scripts\activate.bat   # Windows CMD
# source .venv/bin/activate    # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
```

## 📋 Modos de Uso

### 🌐 **Modo Web (Interfaz Gráfica)**

```powershell
python app.py
# Abre http://localhost:5000 en tu navegador
```

**Características de la interfaz web:**

- Arrastrar y soltar archivos
- Selección de formato de salida
- Opción de aceleración GPU
- Progreso en tiempo real con logs
- Descarga automática del archivo convertido

### 💻 **Modo CLI (Línea de Comandos)**

```powershell
# Sintaxis básica
python app.py --<formato> "archivo_entrada" ["archivo_salida"] [--gpu]

# Ejemplos - salida en la misma carpeta del archivo de entrada
python app.py --mp4 "video.mov"           # → video.mp4 (misma carpeta)
python app.py --webm "video.mp4" --gpu    # → video.webm (misma carpeta)
python app.py --mkv "C:\Videos\video.avi" # → C:\Videos\video.mkv

# Con ruta de salida específica
python app.py --mkv "video.avi" "C:\Output\converted.mkv"
python app.py --help
```

### ⚡ **PowerShell Integration (Recomendado)**

#### Configuración única:

```powershell
# Agregar a tu Microsoft.PowerShell_profile.ps1:
. E:\workspace\video-converter-flask\converter.ps1
```

#### Uso después de la configuración:

```powershell
# Funciones principales
Convert-Video -MP4 "video.mov"
Convert-Video -WebM "video.mp4" -GPU
Convert-Video -MKV "video.avi" "C:\salida\video.mkv"
Convert-Video -Web                    # Inicia servidor web
Convert-Video -Help                   # Ayuda completa

# Funciones de conveniencia
cvt-mp4 "video.mov"
cvt-webm "video.mp4" -GPU
cvt-avi "video.mkv"
cvt-mkv "video.mp4" "salida.mkv"
cvt-web                               # Servidor web
cvt-help                              # Ayuda rápida
```

## 🎯 Formatos Soportados

### Entrada

**Todos los formatos comunes:**

- MP4, MOV, MKV, AVI, WMV, FLV, WebM, M4V

### Salida

| Formato  | Descripción                      | GPU Support    |
| -------- | -------------------------------- | -------------- |
| **MP4**  | H.264/AAC, máxima compatibilidad | ✅ H.264 NVENC |
| **WebM** | VP9/Opus para web                | ✅ AV1 NVENC\* |
| **AVI**  | MPEG-4/MP3, legacy               | ❌ CPU only    |
| **MKV**  | H.264/HEVC/AAC, alta calidad     | ✅ HEVC NVENC  |

_\*AV1 NVENC requiere GPUs Ada Lovelace o newer_

## ⚡ Aceleración GPU

### Encoders NVENC Soportados:

- **H.264 NVENC**: MP4 (todas las GPUs NVIDIA modernas)
- **HEVC NVENC**: MKV (GTX 10 series+)
- **AV1 NVENC**: WebM (RTX 40 series+)

### Fallback Automático

Si el encoder GPU no está disponible, automáticamente usa CPU.

## 📁 Estructura del Proyecto

```
video-converter-flask/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── converter.ps1          # Funciones PowerShell
├── convert-simple.ps1     # Script simple standalone
├── templates/
│   └── index.html        # Interfaz web
├── static/
│   ├── styles.css        # Estilos
│   └── script.js         # JavaScript frontend
├── uploads/              # Archivos temporales
└── converted/            # Archivos de salida (solo web)
```

### Comportamiento de Rutas de Salida

**🌐 Interfaz Web:**

- Archivos temporales en `uploads/`
- Archivos convertidos en `converted/`
- Nombres con timestamp para evitar conflictos

**💻 Línea de Comandos:**

- **Por defecto:** Misma carpeta del archivo de entrada
- **Personalizado:** Ruta especificada por el usuario
- **Ejemplo:** `video.mov` → `video.mp4` (misma carpeta)
  ├── converter.ps1 # Funciones PowerShell
  ├── convert-simple.ps1 # Script simple standalone
  ├── templates/
  │ └── index.html # Interfaz web
  ├── static/
  │ ├── styles.css # Estilos
  │ └── script.js # JavaScript frontend
  ├── uploads/ # Archivos temporales
  └── converted/ # Archivos de salida

````

## 📚 Documentación Adicional

- **[USAGE.md](./USAGE.md)** - Guía detallada de uso
- **[PROFILE-INTEGRATION.md](./PROFILE-INTEGRATION.md)** - Integración con PowerShell
- **[SYNTAX-EXAMPLES.ps1](./SYNTAX-EXAMPLES.ps1)** - Ejemplos de sintaxis

## 🛠️ Desarrollo

### Ejecutar en modo desarrollo:

```powershell
python app.py  # Debug mode habilitado por defecto
````

### Estructura de funciones principales:

- `convert_video_cli()` - Conversión por línea de comandos
- `get_codec_args()` - Configuración de codecs
- `has_encoder()` - Detección de encoders disponibles

## 🔍 Troubleshooting

### Error: "ffmpeg no encontrado"

```powershell
# Verificar instalación
ffmpeg -version

# Si no está instalado, usar scoop:
scoop install ffmpeg
```

### Error: "No se encontró el entorno virtual"

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "No se puede ejecutar scripts"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**⭐ Si te resulta útil, considera darle una estrella al repo!**
