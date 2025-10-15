# 🎵 Ejemplos de Extracción de Audio MP3

Este archivo contiene ejemplos prácticos para usar la nueva funcionalidad de extracción de audio.

## 💻 Línea de Comandos Python

```bash
# Ejemplo básico - misma carpeta
python app.py --mp3 "mi_video.mp4"
# Resultado: mi_video.mp3 (en la misma carpeta)

# Con ruta específica
python app.py --mp3 "presentacion.mov" "C:\Audio\presentacion.mp3"

# Desde cualquier formato
python app.py --mp3 "conferencia.mkv"
python app.py --mp3 "entrevista.avi"
python app.py --mp3 "webinar.webm"
```

## ⚡ PowerShell

```powershell
# Función rápida
cvt-mp3 "video.mp4"

# Con ruta específica
cvt-mp3 "C:\Videos\presentacion.mp4" "C:\Audio\presentacion.mp3"

# Función completa
Convert-Video -MP3 "conferencia.mov"

# Múltiples archivos en batch
Get-ChildItem "*.mp4" | ForEach-Object { cvt-mp3 $_.Name }
```

## 🌐 Interfaz Web

1. Abrir http://localhost:5000
2. Arrastrar video o hacer clic en "Examinar"
3. Seleccionar "MP3 (Audio solamente)" en formato
4. Hacer clic en "Convertir"
5. Descargar el archivo MP3 resultante

## 🤖 Casos de Uso para IA

### Transcripción con Whisper

```python
import whisper

# 1. Extraer audio
# cvt-mp3 "conferencia.mp4"

# 2. Transcribir
model = whisper.load_model("base")
result = model.transcribe("conferencia.mp3")
print(result["text"])
```

### Traducción con OpenAI

```python
import openai

# 1. Transcribir primero (como arriba)
transcription = "Texto transcrito del audio..."

# 2. Traducir
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Traduce el siguiente texto al inglés:"},
        {"role": "user", "content": transcription}
    ]
)
print(response.choices[0].message.content)
```

## 📊 Calidad del Audio

- **Bitrate**: 192 kbps (ideal para transcripción)
- **Sample Rate**: 44.1 kHz (calidad estándar)
- **Formato**: MP3 estéreo
- **Codec**: libmp3lame (alta compatibilidad)

## 🔧 Parámetros ffmpeg Utilizados

```bash
ffmpeg -i input_video.mp4 -vn -c:a libmp3lame -b:a 192k -ar 44100 output.mp3
```

- `-vn`: Deshabilitar video (solo audio)
- `-c:a libmp3lame`: Usar encoder MP3 de alta calidad
- `-b:a 192k`: Bitrate de audio 192 kbps
- `-ar 44100`: Sample rate 44.1 kHz

## 🚀 Flujo de Trabajo Completo

```powershell
# 1. Extraer audio de video
cvt-mp3 "conferencia_espanol.mp4"

# 2. El archivo se genera automáticamente
# → conferencia_espanol.mp3

# 3. Usar con servicios de IA:
# - Whisper para transcripción
# - ChatGPT/Claude para traducción
# - Azure Speech Services
# - Google Speech-to-Text
```

## ⚡ Rendimiento

| Duración Video | Tiempo Extracción | Tamaño MP3 (aprox.) |
| -------------- | ----------------- | ------------------- |
| 5 minutos      | 10-15 segundos    | 7-10 MB             |
| 30 minutos     | 30-45 segundos    | 42-60 MB            |
| 2 horas        | 2-3 minutos       | 168-240 MB          |

## 💡 Tips

1. **Calidad original**: El MP3 mantendrá la calidad del audio original
2. **Múltiples idiomas**: Funciona con cualquier idioma en el video
3. **Formato de entrada**: Acepta cualquier formato de video soportado
4. **Sin GPU**: La extracción de audio no requiere GPU
5. **Rápido**: Mucho más rápido que conversión de video completa

## 🎯 Próximos Pasos

Después de extraer el audio MP3, puedes:

1. **Transcribir** con Whisper, Azure Speech, etc.
2. **Traducir** el texto transcrito con IA
3. **Analizar** el contenido con herramientas de NLP
4. **Crear subtítulos** automáticamente
5. **Generar resúmenes** del contenido de audio
