# 🎬 Conversor de Videos - Guía de Uso Completa

Aplicación Flask para conversión de videos con múltiples interfaces: web, CLI y PowerShell.

## 🚀 Inicio Rápido

### 🌐 **Interfaz Web**

```powershell
# Método 1: Script directo
python app.py

# Método 2: PowerShell (si está configurado)
Convert-Video -Web
# o
cvt-web
```

**URL:** <http://localhost:5000>

**Características:**

- Drag & drop de archivos
- Progreso en tiempo real
- Logs de conversión
- Descarga automática
- Soporte GPU toggle

### 💻 **Línea de Comandos (CLI)**

#### Sintaxis básica:

```powershell
python app.py --<formato> "archivo_entrada" ["archivo_salida"] [--gpu]
```

#### Ejemplos:

```powershell
# Conversión básica (salida en la misma carpeta del archivo de entrada)
python app.py --mp4 "video.mov"           # → video.mp4 (misma carpeta)
python app.py --webm "video.mp4"          # → video.webm (misma carpeta)
python app.py --avi "video.mkv"           # → video.avi (misma carpeta)
python app.py --mkv "video.avi"           # → video.mkv (misma carpeta)

# Con aceleración GPU
python app.py --mp4 "video.mov" --gpu
python app.py --webm "video.mp4" --gpu

# Con ruta de salida específica
python app.py --mkv "input.mp4" "C:\salida\output.mkv"
python app.py --mp4 "video.mov" ".\converted\new-video.mp4"

# Ver ayuda
python app.py --help
```

### ⚡ **PowerShell Integration (Recomendado)**

#### Configuración inicial:

1. **Agregar a tu perfil de PowerShell:**

```powershell
# Abrir perfil para editar
notepad $PROFILE

# Agregar esta línea:
. E:\workspace\video-converter-flask\converter.ps1
```

2. **Recargar perfil:**

```powershell
. $PROFILE
```

#### Uso después de configuración:

```powershell
# Función principal con switches
Convert-Video -MP4 "video.mov"
Convert-Video -WebM "video.mp4" -GPU
Convert-Video -AVI "video.mkv"
Convert-Video -MKV "video.avi" "C:\salida\output.mkv"

# Funciones de conveniencia (más cortas)
cvt-mp4 "video.mov"
cvt-webm "video.mp4" -GPU
cvt-avi "video.mkv"
cvt-mkv "video.avi" "output.mkv"

# Utilidades
cvt-web                    # Iniciar servidor web
cvt-help                   # Ayuda rápida
Convert-Video -Help        # Ayuda completa del script Python
```

## 📋 Formatos y Codecs

### Formatos de Entrada Soportados

**Todos los formatos comunes:**
MP4, MOV, MKV, AVI, WMV, FLV, WebM, M4V

### Formatos de Salida

| Formato  | Video Codec | Audio Codec | GPU Support    | Uso Recomendado        |
| -------- | ----------- | ----------- | -------------- | ---------------------- |
| **MP4**  | H.264       | AAC         | ✅ H.264 NVENC | Máxima compatibilidad  |
| **WebM** | VP9/AV1     | Opus        | ✅ AV1 NVENC\* | Web, streaming         |
| **AVI**  | MPEG-4      | MP3         | ❌ CPU only    | Legacy, compatibilidad |
| **MKV**  | H.264/HEVC  | AAC         | ✅ HEVC NVENC  | Alta calidad, archival |

**\*AV1 NVENC requiere RTX 40 series (Ada Lovelace) o newer**

## ⚡ Aceleración GPU (NVENC)

### Encoders Soportados

| Encoder         | Formatos | Requisitos GPU | Calidad                  |
| --------------- | -------- | -------------- | ------------------------ |
| **H.264 NVENC** | MP4, MKV | GTX 600+       | Excelente compatibilidad |
| **HEVC NVENC**  | MKV      | GTX 10 series+ | Alta eficiencia          |
| **AV1 NVENC**   | WebM     | RTX 40 series+ | Máxima compresión        |

### Fallback Automático

Si el encoder GPU no está disponible:

- ✅ **Detección automática** de capacidades
- ✅ **Fallback a CPU** sin errores
- ✅ **Mensaje informativo** sobre el cambio

### Ejemplos con GPU:

```powershell
# CLI
python app.py --mp4 "video.mov" --gpu
python app.py --webm "video.mp4" --gpu

# PowerShell
Convert-Video -MP4 "video.mov" -GPU
cvt-webm "video.mp4" -GPU
```

## 📁 Gestión de Archivos

### Rutas de Salida

#### Automática (por defecto):

```powershell
# Automática: misma carpeta del archivo de entrada
cvt-mp4 "video.mov"
# Resultado: video.mp4 (en la misma carpeta que video.mov)
```

#### Personalizada:

```powershell
# Especificar ruta completa
cvt-mp4 "video.mov" "C:\Videos\output.mp4"

# Ruta relativa
Convert-Video -MP4 "input.avi" ".\exports\final.mp4"
```

### Limpieza Automática

- ✅ **Archivos temporales** se eliminan automáticamente
- ✅ **Uploads folder** se limpia después de conversión
- ✅ **Solo quedan** los archivos convertidos

## 🔧 Configuraciones Avanzadas

### Calidad de Video

Los presets están optimizados para balance calidad/velocidad:

**CPU (Software):**

- MP4: CRF 23, preset veryfast
- WebM: CRF 33, VP9
- MKV: CRF 23, preset veryfast

**GPU (NVENC):**

- MP4: CQ 23, preset p5
- WebM: CQ 28, AV1
- MKV: CQ 24, preset p5

### Personalización

Para modificar configuraciones, edita la función `get_codec_args()` en `app.py`.

## 🚫 Limitaciones

### Tamaño de Archivos

- **Máximo:** 2GB por archivo
- **Recomendado:** < 1GB para mejor rendimiento

### Formatos No Soportados

**Entrada no válida:**

- Archivos de audio (MP3, WAV, etc.)
- Imágenes (JPG, PNG, etc.)
- Formatos exóticos o corruptos

## 🛠️ Troubleshooting

### Errores Comunes

#### "ffmpeg no encontrado"

```powershell
# Verificar instalación
ffmpeg -version

# Instalar con scoop (recomendado)
scoop install ffmpeg

# O con chocolatey
choco install ffmpeg
```

#### "No se encontró el entorno virtual"

```powershell
# Crear venv
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

#### "Cannot load converter.ps1"

```powershell
# Permitir ejecución de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar carga
. E:\workspace\video-converter-flask\converter.ps1
```

#### GPU no funciona

```powershell
# Verificar drivers NVIDIA actualizados
nvidia-smi

# Verificar encoders disponibles
ffmpeg -encoders | findstr nvenc
```

### Logs y Debug

#### Modo Web

- Los logs aparecen en tiempo real en la interfaz
- Errores se muestran en el área de logs

#### Modo CLI

- Output completo de ffmpeg en terminal
- Progreso en tiempo real con porcentaje
- **Tiempo de conversión** mostrado al finalizar

#### Modo PowerShell

- Información de entrada y salida detallada
- Estado de GPU y encoder utilizado
- **Tiempo transcurrido** al completar operación

## 📊 Rendimiento

### Velocidades Típicas (GPU vs CPU)

**1080p Video (H.264 → H.264):**

- **CPU (Ryzen 7):** ~0.5x velocidad real
- **GPU (RTX 3080):** ~3-5x velocidad real

**4K Video (H.264 → HEVC):**

- **CPU:** ~0.1x velocidad real
- **GPU:** ~1-2x velocidad real

### Recomendaciones

- ✅ **Usa GPU** para archivos grandes (>500MB)
- ✅ **CPU suficiente** para archivos pequeños
- ✅ **WebM/AV1** para máxima compresión
- ✅ **MP4** para máxima compatibilidad

---

**💡 Tip:** Usa `cvt-help` para ver todos los comandos disponibles.

**Encoders GPU soportados:**

- **MP4**: H.264 NVENC
- **WebM**: AV1 NVENC (GPUs Ada/Lovelace)
- **MKV**: HEVC NVENC

## 📁 Rutas de Salida

```powershell
# Automática (./converted/nombre.formato)
.\convert.ps1 --mp4 "video.mov"

# Específica
.\convert.ps1 --mp4 "video.mov" "C:\salida\mi-video.mp4"
```

## 🛠️ Configuración Inicial

1. **Crear entorno virtual:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Instalar ffmpeg:**

   - Descargar desde [ffmpeg.org](https://ffmpeg.org)
   - Agregar al PATH del sistema

3. **Permitir scripts PowerShell:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## 💡 Ejemplos Avanzados

```powershell
# Batch de conversiones
.\convert.ps1 --mp4 "video1.mov"
.\convert.ps1 --mp4 "video2.avi"
.\convert.ps1 --webm "video3.mp4" --gpu

# Uso desde cualquier directorio
E:\workspace\video-converter-flask\convert.ps1 --mp4 "C:\videos\clip.mov"
```

## 🔧 Solución de Problemas

### Error: "No se puede ejecutar scripts"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "ffmpeg no encontrado"

- Instalar ffmpeg y agregarlo al PATH
- O usar ruta completa: `C:\ffmpeg\bin\ffmpeg.exe`

### Error: "No se encontró el entorno virtual"

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
