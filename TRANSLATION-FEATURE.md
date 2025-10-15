# 🌍 Traducción Automática de Subtítulos

Esta funcionalidad extiende la transcripción con IA para generar automáticamente subtítulos en múltiples idiomas usando Google Translate gratuito.

## ✨ Características Principales

- **Transcripción + Traducción**: Genera SRT original y traducido automáticamente
- **Google Translate**: Servicio gratuito y confiable para traducción
- **Múltiples Idiomas**: Más de 100 idiomas soportados
- **Proceso Automático**: Video → MP3 → Transcripción → Traducción → 2 archivos SRT
- **Calidad Preservada**: Mantiene timestamps precisos en ambos archivos

## 🚀 Instalación de Dependencias

```bash
# Instalar dependencias de traducción
pip install deep-translator

# O usando el requirements.txt actualizado
pip install -r requirements.txt
```

## 💻 Uso desde Línea de Comandos

### Python CLI

```bash
# Generar SRT original + traducido a inglés
python app.py --srt "video_espanol.mp4" --translate english

# Con modelo específico para mejor calidad
python app.py --srt "conferencia.mov" --translate french --model medium

# Con ruta de salida específica
python app.py --srt "video.mkv" "subtitulos.srt" --translate german --model large
```

### PowerShell

```powershell
# Función rápida con traducción
cvt-srt "video_espanol.mp4" -Translate english

# Con modelo específico
cvt-srt "conferencia.mp4" -Model medium -Translate french

# Función completa
Convert-Video -SRT "video.avi" -Translate italian -Model large
```

## 📄 Archivos Generados

Cuando usas traducción, se generan **2 archivos SRT**:

### Ejemplo: `video_espanol.mp4`

```
📁 Carpeta/
├── video_espanol.mp4 (original)
├── video_espanol.srt (transcripción original en español)
└── video_espanol_english.srt (traducción a inglés)
```

### Contenido de los Archivos

**video_espanol.srt** (original):

```srt
1
00:00:00,000 --> 00:00:04,500
Bienvenidos a esta conferencia sobre inteligencia artificial.

2
00:00:04,500 --> 00:00:09,200
Hoy vamos a explorar las últimas tendencias en machine learning.
```

**video_espanol_english.srt** (traducido):

```srt
1
00:00:00,000 --> 00:00:04,500
Welcome to this conference on artificial intelligence.

2
00:00:04,500 --> 00:00:09,200
Today we are going to explore the latest trends in machine learning.
```

## 🌍 Idiomas Soportados

### Códigos de Idioma Principales

| Idioma        | Código              | Ejemplo de Uso           |
| ------------- | ------------------- | ------------------------ |
| **Inglés**    | `english` / `en`    | `--translate english`    |
| **Español**   | `spanish` / `es`    | `--translate spanish`    |
| **Francés**   | `french` / `fr`     | `--translate french`     |
| **Alemán**    | `german` / `de`     | `--translate german`     |
| **Italiano**  | `italian` / `it`    | `--translate italian`    |
| **Portugués** | `portuguese` / `pt` | `--translate portuguese` |
| **Ruso**      | `russian` / `ru`    | `--translate russian`    |
| **Japonés**   | `japanese` / `ja`   | `--translate japanese`   |
| **Coreano**   | `korean` / `ko`     | `--translate korean`     |
| **Chino**     | `chinese` / `zh`    | `--translate chinese`    |
| **Holandés**  | `dutch` / `nl`      | `--translate dutch`      |
| **Árabe**     | `arabic` / `ar`     | `--translate arabic`     |

### Puedes usar nombres en español o códigos ISO

```powershell
# Todas estas opciones son equivalentes:
cvt-srt "video.mp4" -Translate english
cvt-srt "video.mp4" -Translate inglés
cvt-srt "video.mp4" -Translate en
```

## ⚡ Proceso Completo (3 Pasos)

### Paso 1: Extracción de Audio

```
🎬 video.mp4 → 🎵 audio_temp.mp3
```

### Paso 2: Transcripción con IA

```
🎵 audio_temp.mp3 → 🤖 Whisper → 📄 video.srt (original)
```

### Paso 3: Traducción Automática

```
📄 video.srt → 🌍 Google Translate → 📄 video_english.srt (traducido)
```

## 🎯 Casos de Uso Reales

### 📚 **Contenido Educativo Multiidioma**

```powershell
# Conferencia en español → subtítulos en inglés
cvt-srt "conferencia_universidad.mp4" -Translate english -Model medium

# Resultado:
# conferencia_universidad.srt (español original)
# conferencia_universidad_english.srt (traducción inglés)
```

### 💼 **Reuniones Internacionales**

```powershell
# Reunión en inglés → subtítulos en español
cvt-srt "meeting_quarterly.mp4" -Translate spanish -Model base

# Resultado:
# meeting_quarterly.srt (inglés original)
# meeting_quarterly_spanish.srt (traducción español)
```

### 🌐 **Contenido para Redes Sociales**

```powershell
# Video en español → múltiples idiomas
cvt-srt "tutorial_programacion.mp4" -Translate english
cvt-srt "tutorial_programacion.mp4" -Translate french
cvt-srt "tutorial_programacion.mp4" -Translate german

# Resultado:
# tutorial_programacion.srt (español)
# tutorial_programacion_english.srt (inglés)
# tutorial_programacion_french.srt (francés)
# tutorial_programacion_german.srt (alemán)
```

## 📊 Calidad de Traducción por Idioma

### Excelente Calidad

- **Inglés ↔ Español** (muy preciso)
- **Inglés ↔ Francés** (muy preciso)
- **Inglés ↔ Alemán** (muy preciso)
- **Español ↔ Portugués** (muy preciso)

### Muy Buena Calidad

- **Inglés ↔ Italiano**
- **Inglés ↔ Ruso**
- **Español ↔ Francés**
- **Cualquier idioma ↔ Inglés** (inglés como puente)

### Buena Calidad

- **Idiomas asiáticos** (Japonés, Coreano, Chino)
- **Árabe ↔ Idiomas latinos**
- **Idiomas menos comunes**

## ⏱️ Tiempos de Procesamiento

| Duración Video | Transcripción | Traducción | Total   |
| -------------- | ------------- | ---------- | ------- |
| 5 minutos      | 30-45 seg     | 10-15 seg  | ~1 min  |
| 30 minutos     | 3-5 min       | 30-45 seg  | ~6 min  |
| 2 horas        | 15-20 min     | 2-3 min    | ~23 min |

_La traducción es muy rápida comparada con la transcripción_

## 🔧 Configuración Avanzada

### Optimización por Tipo de Contenido

```powershell
# Conferencias técnicas (usar modelo grande para precisión)
cvt-srt "conferencia_tecnica.mp4" -Model large -Translate english

# Conversaciones casuales (modelo base es suficiente)
cvt-srt "chat_informal.mp4" -Model base -Translate french

# Presentaciones corporativas (modelo medium balanceado)
cvt-srt "presentacion_empresa.mp4" -Model medium -Translate german
```

### Múltiples Traducciones del Mismo Video

```powershell
# Generar original + inglés
cvt-srt "video.mp4" -Translate english

# Generar solo francés (usa el SRT original ya creado)
cvt-srt "video.mp4" -Translate french

# Resultado final:
# video.srt (original)
# video_english.srt
# video_french.srt
```

## 🛠️ Solución de Problemas

### Error: "deep-translator no está instalado"

```bash
pip install deep-translator
```

### Error: "Límite de traducción excedido"

- **Causa**: Subtítulos muy largos
- **Solución**: La herramienta divide automáticamente en chunks más pequeños

### Traducción de baja calidad

1. **Verificar idioma original**: Asegúrate que Whisper detecte correctamente el idioma
2. **Usar modelo más grande**: `-Model medium` o `-Model large` mejora la transcripción original
3. **Revisar manualmente**: Corregir errores en el SRT original mejora la traducción

## 💡 Tips para Mejores Resultados

1. **Audio claro = mejor traducción**: La calidad de audio afecta la transcripción inicial
2. **Modelo apropiado**: Más calidad en transcripción = mejor traducción
3. **Revisar contexto**: Términos técnicos pueden necesitar revisión manual
4. **Usar inglés como puente**: Para idiomas raros, traducir a inglés primero

## 🔄 Flujo de Trabajo Completo

### Para Contenido Educativo

```powershell
# 1. Generar español → inglés
cvt-srt "curso_matematicas.mp4" -Translate english -Model medium

# 2. Revisar y corregir manualmente si es necesario
# Editar curso_matematicas.srt y curso_matematicas_english.srt

# 3. Usar en plataforma educativa con subtítulos multiidioma
```

### Para YouTube/Redes Sociales

```powershell
# 1. Generar subtítulos en idioma principal + inglés
cvt-srt "tutorial_cocina.mp4" -Translate english

# 2. Subir video con ambos archivos SRT
# YouTube detecta automáticamente los subtítulos
```

## 🎉 Resultado Final

Con esta funcionalidad puedes:

✅ **Transcribir** cualquier video automáticamente  
✅ **Traducir** a más de 100 idiomas  
✅ **Generar** 2 archivos SRT simultáneamente  
✅ **Crear** contenido accesible multiidioma  
✅ **Acelerar** localización de videos  
✅ **Automatizar** subtítulos para redes sociales

**¡Perfecto para hacer tu contenido accesible globalmente! 🌍✨**

---

## 🚀 Comando de Prueba Rápida

```powershell
# Para probar inmediatamente:
cvt-srt "tu_video.mp4" -Translate english

# Resultado:
# tu_video.srt (idioma original)
# tu_video_english.srt (traducción)
```

**¡Ahora puedes crear subtítulos multiidioma automáticamente! 🤖🌍**
