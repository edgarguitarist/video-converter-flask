# 🤖 Transcripción con IA - Generación de Subtítulos SRT

Esta funcionalidad utiliza **OpenAI Whisper** (IA gratuita local) para transcribir automáticamente el audio de videos y generar archivos de subtítulos SRT con timestamps precisos.

## ✨ Características Principales

- **IA Local**: Usa OpenAI Whisper completamente gratis y sin conexión
- **Timestamps Precisos**: Genera subtítulos con tiempo sincronizado
- **Múltiples Modelos**: Desde rápido (tiny) hasta máxima calidad (large)
- **Formato SRT**: Compatible con todos los reproductores de video
- **Proceso Automático**: Extrae audio MP3 → Transcribe → Genera SRT
- **Multiidioma**: Detecta automáticamente el idioma del audio

## 🚀 Instalación de Dependencias

```bash
# Instalar Whisper y dependencias
pip install openai-whisper torch torchaudio

# O usando el requirements.txt actualizado
pip install -r requirements.txt
```

## 💻 Uso desde Línea de Comandos

### Python CLI

```bash
# Generar subtítulos básico (modelo base)
python app.py --srt "conferencia.mp4"
# Resultado: conferencia.srt

# Con modelo específico
python app.py --srt "video.mov" --model medium
# Resultado: video.srt

# Con ruta de salida específica
python app.py --srt "presentacion.mkv" "C:\subtitulos\presentacion.srt" --model large
```

### PowerShell

```powershell
# Función rápida (modelo base)
cvt-srt "conferencia.mp4"

# Con modelo específico
cvt-srt "video.mp4" -Model medium

# Con ruta de salida
cvt-srt "video.mkv" "C:\subtitulos\video.srt" -Model large

# Función completa
Convert-Video -SRT "video.avi" -Model small
Convert-Video -SRT "video.mp4" "subtitulos.srt" -Model medium
```

## 🤖 Modelos Whisper Disponibles

| Modelo   | Tamaño   | Velocidad  | Precisión | Uso Recomendado          |
| -------- | -------- | ---------- | --------- | ------------------------ |
| `tiny`   | ~39 MB   | Muy rápida | Básica    | Pruebas rápidas          |
| `base`   | ~74 MB   | Rápida     | Buena     | **Recomendado general**  |
| `small`  | ~244 MB  | Media      | Muy buena | Conferencias importantes |
| `medium` | ~769 MB  | Lenta      | Excelente | Contenido profesional    |
| `large`  | ~1550 MB | Muy lenta  | Máxima    | Máxima calidad requerida |

## 📄 Formato SRT Generado

```srt
1
00:00:00,000 --> 00:00:04,500
Bienvenidos a esta conferencia sobre inteligencia artificial.

2
00:00:04,500 --> 00:00:09,200
Hoy vamos a explorar las últimas tendencias en machine learning.

3
00:00:09,200 --> 00:00:13,800
Comenzaremos con una introducción a los modelos de lenguaje.
```

## ⚡ Proceso Automático

El comando `--srt` ejecuta automáticamente estos pasos:

1. **Extracción de Audio**: Convierte el video a MP3 temporal
2. **Carga del Modelo**: Descarga y carga el modelo Whisper especificado
3. **Transcripción**: Procesa el audio con IA para generar texto con timestamps
4. **Generación SRT**: Crea el archivo de subtítulos en formato estándar
5. **Limpieza**: Elimina el archivo MP3 temporal

## 🎯 Casos de Uso Ideales

### 📚 Educativo

- **Conferencias**: Generar subtítulos para accesibilidad
- **Cursos online**: Crear transcripciones automáticas
- **Webinars**: Facilitar búsqueda en contenido

### 💼 Empresarial

- **Reuniones**: Transcribir automáticamente las juntas
- **Presentaciones**: Crear subtítulos para videos corporativos
- **Entrevistas**: Generar transcripciones para análisis

### 🌐 Contenido Web

- **YouTube**: Generar subtítulos automáticamente
- **Redes sociales**: Hacer videos accesibles
- **Podcasts**: Convertir audio a texto para SEO

## 📊 Tiempos de Procesamiento

| Duración Video | Modelo Base | Modelo Medium | Modelo Large |
| -------------- | ----------- | ------------- | ------------ |
| 5 minutos      | 30-45 seg   | 1-2 min       | 3-5 min      |
| 30 minutos     | 3-5 min     | 8-12 min      | 15-25 min    |
| 2 horas        | 15-20 min   | 35-50 min     | 60-90 min    |

_Tiempos aproximados en CPU moderna. GPU puede acelerar significativamente._

## 🔧 Configuración Avanzada

### Selección de Modelo por Idioma

```powershell
# Para inglés: tiny o base suelen ser suficientes
cvt-srt "english_video.mp4" -Model base

# Para español: base o small recomendados
cvt-srt "video_español.mp4" -Model small

# Para idiomas complejos: medium o large
cvt-srt "chinese_video.mp4" -Model large
```

### Optimización de Recursos

```powershell
# Para máquina con poca RAM: usar tiny o base
cvt-srt "video.mp4" -Model tiny

# Para máquina potente: usar medium o large
cvt-srt "video.mp4" -Model large
```

## 🛠️ Solución de Problemas

### Error: "Whisper no está instalado"

```bash
pip install openai-whisper torch torchaudio
```

### Error: "Memoria insuficiente"

```powershell
# Usar modelo más pequeño
cvt-srt "video.mp4" -Model tiny
```

### Calidad de transcripción baja

1. **Usar modelo más grande**: `-Model medium` o `-Model large`
2. **Verificar calidad de audio**: Audio claro mejora resultados
3. **Probar con audio original**: Algunos videos comprimidos pierden calidad

## 🌍 Idiomas Soportados

Whisper detecta automáticamente y soporta:

- **Español** (nativo)
- **Inglés** (excelente)
- **Francés, Alemán, Italiano** (muy bueno)
- **Portugués, Ruso, Japonés** (bueno)
- **Y más de 90 idiomas adicionales**

## 💡 Tips para Mejores Resultados

1. **Audio limpio**: Videos con audio claro dan mejores resultados
2. **Modelo apropiado**: Balance entre velocidad y calidad según necesidad
3. **Verificación manual**: Revisar y corregir transcripciones importantes
4. **Formato original**: Videos sin compresión excesiva funcionan mejor

## 🔄 Flujo de Trabajo Completo

```powershell
# 1. Generar subtítulos
cvt-srt "mi_video.mp4" -Model base

# 2. Revisar archivo generado
# mi_video.srt (se abre con cualquier editor de texto)

# 3. Usar en reproductor de video
# VLC, Windows Media Player, etc. detectan automáticamente el .srt

# 4. Opcional: Editar manualmente para correcciones
# Usar editores como Subtitle Edit, Aegisub, etc.
```

## 📋 Formatos de Video Soportados

La transcripción funciona con todos los formatos de video soportados:

- MP4, MOV, MKV, AVI, WMV, FLV, WebM, M4V

## 🎬 Integración con Editores de Video

Los archivos SRT generados son compatibles con:

- **Adobe Premiere Pro**
- **DaVinci Resolve**
- **Final Cut Pro**
- **OpenShot**
- **Kdenlive**
- Y todos los editores que soporten SRT estándar

¡Ahora puedes generar subtítulos automáticamente con IA completamente gratis! 🤖✨
