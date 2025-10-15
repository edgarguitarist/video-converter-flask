# 🌐 Guía de Subtítulos en la Versión Web

## ✨ Nueva Funcionalidad Agregada

La versión web ahora incluye **generación automática de subtítulos con IA** y **traducción automática**.

### 🎯 **Características**

#### **📝 Transcripción con IA**

- **Motor**: OpenAI Whisper (IA local gratuita)
- **Modelos disponibles**: Tiny → Large (velocidad vs precisión)
- **Formato**: Archivos SRT con timestamps precisos

#### **🌍 Traducción Automática**

- **Motor**: Google Translate
- **12+ idiomas** soportados
- **Salida dual**: SRT original + SRT traducido en ZIP

---

## 📋 **Cómo Usar**

### 1. **Acceder a la Funcionalidad**

```
http://localhost:5000
```

### 2. **Pasos en la Interfaz**

1. **Cargar video**: Arrastra o selecciona tu archivo de video
2. **Seleccionar formato**: Elige "SRT (Subtítulos con IA)"
3. **Configurar opciones**:
   - **Modelo Whisper**: Balance entre velocidad y precisión
   - **Idioma de traducción**: Opcional, para obtener subtítulos traducidos

### 3. **Opciones de Modelo Whisper**

| Modelo     | Velocidad | Precisión  | Recomendado para                |
| ---------- | --------- | ---------- | ------------------------------- |
| **Tiny**   | ⚡⚡⚡    | ⭐⭐       | Videos cortos, pruebas rápidas  |
| **Base**   | ⚡⚡      | ⭐⭐⭐     | **Uso general** (balance ideal) |
| **Small**  | ⚡        | ⭐⭐⭐⭐   | Mayor precisión                 |
| **Medium** | 🐌        | ⭐⭐⭐⭐⭐ | Contenido profesional           |
| **Large**  | 🐌🐌      | ⭐⭐⭐⭐⭐ | Máxima calidad                  |

---

## 🌍 **Idiomas de Traducción**

### **Idiomas Disponibles**

- 🇺🇸 **English** (Inglés)
- 🇪🇸 **Spanish** (Español)
- 🇫🇷 **French** (Francés)
- 🇩🇪 **German** (Alemán)
- 🇵🇹 **Portuguese** (Portugués)
- 🇮🇹 **Italian** (Italiano)
- 🇨🇳 **Chinese** (Chino)
- 🇯🇵 **Japanese** (Japonés)
- 🇰🇷 **Korean** (Coreano)
- 🇷🇺 **Russian** (Ruso)
- 🇸🇦 **Arabic** (Árabe)
- 🇮🇳 **Hindi** (Hindi)

---

## 📂 **Resultados**

### **Sin traducción**

```
mi_video.srt (idioma original detectado automáticamente)
```

### **Con traducción**

```
mi_video.zip
├── mi_video_original.srt
└── mi_video_english.srt
```

---

## 🔧 **Configuración Técnica**

### **Dependencias Requeridas**

```bash
pip install openai-whisper
pip install deep-translator
```

### **Hardware Recomendado**

- **RAM**: 4GB+ disponibles
- **CPU**: Procesador moderno (para modelos pequeños)
- **GPU**: NVIDIA (opcional, acelera Whisper)

---

## 💡 **Consejos de Uso**

### **Para Mejor Precisión**

1. **Audio claro**: Videos con buena calidad de audio
2. **Modelo adecuado**: Medium/Large para contenido importante
3. **Idioma principal**: Whisper funciona mejor con inglés/español

### **Para Mejor Velocidad**

1. **Modelo Tiny/Base**: Para pruebas rápidas
2. **Videos cortos**: Procesar en segmentos si es muy largo
3. **CPU potente**: O usar GPU si está disponible

### **Para Traducción**

1. **Texto claro**: La traducción depende de la transcripción original
2. **Contexto**: Frases completas se traducen mejor que palabras sueltas
3. **Revisión**: Siempre revisar traducciones automáticas

---

## 🚀 **Proceso Completo**

```
1. 📤 Subir video
2. ⚙️ Configurar opciones
3. 🎧 Extraer audio (automático)
4. 🤖 Transcribir con IA
5. 🌍 Traducir (si se seleccionó)
6. 📝 Generar SRT(s)
7. 📦 Descargar resultado
```

---

## ❗ **Limitaciones**

- **Tamaño máximo**: 2GB por archivo
- **Idiomas**: Whisper funciona mejor con idiomas populares
- **Calidad de audio**: Afecta directamente la precisión
- **Internet**: Necesario para traducciones (Google Translate)

---

## 🛠️ **Troubleshooting**

### **Error: "Whisper no disponible"**

```bash
pip install openai-whisper torch torchaudio
```

### **Error: "Traductor no disponible"**

```bash
pip install deep-translator
```

### **Transcripción imprecisa**

- Usar modelo más grande (Medium/Large)
- Verificar calidad del audio original
- Probar con videos más cortos

### **Traducción incorrecta**

- Verificar transcripción original primero
- Algunos idiomas se traducen mejor que otros
- Considerar revisión manual

---

¡**La funcionalidad está lista para usar!** 🎉
