# Extracción de Audio MP3

Esta funcionalidad permite extraer el audio de videos en formato MP3, optimizado para transcripción con IA y traducción.

## 🎵 Características del MP3 Generado

- **Bitrate**: 192 kbps (alta calidad para transcripción)
- **Sample Rate**: 44.1 kHz (estándar de calidad)
- **Codec**: MP3 con libmp3lame
- **Sin video**: Solo se extrae la pista de audio

## 🚀 Uso desde Línea de Comandos

### Python CLI

```bash
# Extraer audio a MP3
python app.py --mp3 "video.mp4"

# Especificar archivo de salida
python app.py --mp3 "conferencia.mov" "audio_conferencia.mp3"

# Extraer desde cualquier formato de video
python app.py --mp3 "presentacion.mkv"
```

### PowerShell

```powershell
# Función rápida
cvt-mp3 "video.mp4"

# Con ruta de salida específica
cvt-mp3 "video.mp4" "C:\audio\mi_audio.mp3"

# Función completa
Convert-Video -MP3 "video.avi"

# Con ruta absoluta
Convert-Video -MP3 "C:\videos\presentacion.mp4" "C:\audio\presentacion.mp3"
```

## 🌐 Uso desde Interfaz Web

1. Selecciona o arrastra tu video
2. En "Formato de salida", elige **MP3 (Audio solamente)**
3. La opción GPU se deshabilitará automáticamente (no necesaria para audio)
4. Haz clic en "Convertir"

## 📁 Ubicación de Archivos

Por defecto, el archivo MP3 se guarda en la misma carpeta que el video original:

```
📂 Mis Videos/
├── conferencia.mp4      (original)
└── conferencia.mp3      (audio extraído)
```

## 🤖 Integración con IA

### Para Transcripción

Este formato MP3 es ideal para servicios como:

- OpenAI Whisper
- Google Speech-to-Text
- Azure Speech Services
- Amazon Transcribe

### Para Traducción

Después de transcribir, puedes usar:

- OpenAI GPT para traducción
- Google Translate API
- DeepL API

## ⚡ Rendimiento

La extracción de audio es muy rápida ya que:

- No requiere recodificación de video
- No usa GPU (innecesaria para audio)
- Proceso directo de extracción de pista de audio

## 📊 Ejemplos de Tiempo

| Duración del Video | Tiempo de Extracción (aprox.) |
| ------------------ | ----------------------------- |
| 5 minutos          | 10-15 segundos                |
| 30 minutos         | 30-45 segundos                |
| 2 horas            | 2-3 minutos                   |

## 🔧 Parámetros Técnicos de ffmpeg

```bash
ffmpeg -i input_video -vn -c:a libmp3lame -b:a 192k -ar 44100 output.mp3
```

- `-vn`: No video (solo audio)
- `-c:a libmp3lame`: Codec MP3 de alta calidad
- `-b:a 192k`: Bitrate de 192 kbps
- `-ar 44100`: Sample rate de 44.1 kHz

## 🎯 Casos de Uso Ideales

- **Conferencias y presentaciones**: Para transcripción y creación de subtítulos
- **Entrevistas**: Para análisis de contenido y transcripción
- **Videos educativos**: Para crear material de audio complementario
- **Contenido multiidioma**: Para traducción automática
- **Análisis de sentimientos**: Procesamiento de audio con IA
- **Podcasts**: Extraer audio de videos de YouTube/Vimeo

## 💡 Consejos

1. **Calidad del audio original**: El MP3 extraído mantendrá la calidad del audio original
2. **Formato de entrada**: Funciona con cualquier formato de video soportado
3. **Tamaño de archivo**: Los archivos MP3 son mucho más pequeños que los videos
4. **Compatibilidad**: MP3 es universalmente compatible con servicios de IA

## 🚀 Flujo de Trabajo Recomendado

1. **Extracción**: `cvt-mp3 "mi_video.mp4"`
2. **Transcripción**: Usar Whisper o similar con el MP3
3. **Traducción**: Procesar el texto transcrito con IA
4. **Resultado**: Texto traducido listo para usar

```powershell
# Ejemplo completo
cvt-mp3 "conferencia_espanol.mp4"
# → Genera: conferencia_espanol.mp3
# → Transcribir con Whisper
# → Traducir con ChatGPT/Claude
```
