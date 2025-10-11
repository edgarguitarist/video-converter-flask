# 🎬 Conversor de Videos

Aplicación Flask para conversión de videos con soporte de línea de comandos y interfaz web.

## 🚀 Uso Rápido

### **Interfaz Web**

```powershell
.\convert.ps1
# Abre http://localhost:5000 en tu navegador
```

### **Línea de Comandos**

#### Conversiones básicas:

```powershell
# Convertir a MP4 (salida en ./converted/)
.\convert.ps1 --mp4 "video.mov"

# Convertir a WebM con GPU
.\convert.ps1 --webm "video.mp4" --gpu

# Convertir a MKV con ruta específica
.\convert.ps1 --mkv "video.avi" "C:\salida\video.mkv"

# Convertir a AVI
.\convert.ps1 --avi "video.mp4"
```

#### Ver todas las opciones:

```powershell
.\convert.ps1 --help
```

## 📋 Formatos Soportados

| Entrada                                 | Salida              |
| --------------------------------------- | ------------------- |
| MP4, MOV, MKV, AVI, WMV, FLV, WebM, M4V | MP4, WebM, AVI, MKV |

## ⚡ Aceleración GPU

```powershell
# Usar NVENC (requiere GPU NVIDIA compatible)
.\convert.ps1 --mp4 "video.mov" --gpu
```

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
