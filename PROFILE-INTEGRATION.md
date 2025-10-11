# 📋 Integración con PowerShell Profile

Guía completa para integrar las funciones del conversor de videos en tu perfil de PowerShell.

## 🔧 Configuración

### Paso 1: Localizar tu perfil

```powershell
# Ver la ruta de tu perfil
$PROFILE

# Típicamente será algo como:
# C:\Users\TuNombre\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

### Paso 2: Editar el perfil

```powershell
# Abrir perfil para editar (crea el archivo si no existe)
notepad $PROFILE

# O usar tu editor preferido
code $PROFILE
```

### Paso 3: Agregar la integración

Añade esta línea a tu `Microsoft.PowerShell_profile.ps1`:

```powershell
# Scripts del Conversor de Videos
. E:\workspace\video-converter-flask\converter.ps1
```

### Ejemplo de perfil completo:

```powershell

# Scripts Globales
. E:\workspace\edoga-scripts\global.ps1

# Scripts de Git
. E:\workspace\edoga-scripts\git.ps1

# Scripts de Proyectos (Workspace)
. E:\workspace\edoga-scripts\projects.ps1

# Scripts de Test / Desarrollo
. E:\workspace\edoga-scripts\test.ps1

# Scripts del Conversor de Videos
. E:\workspace\video-converter-flask\converter.ps1
```

### Paso 4: Recargar perfil

```powershell
# Opción 1: Recargar perfil actual
. $PROFILE

# Opción 2: Reiniciar PowerShell
```

## 🎯 Funciones Disponibles

### Función Principal

```powershell
Convert-Video [parámetros]
```

**Parámetros:**

- `-MP4` - Convertir a formato MP4
- `-WebM` - Convertir a formato WebM
- `-AVI` - Convertir a formato AVI
- `-MKV` - Convertir a formato MKV
- `-GPU` - Usar aceleración GPU (NVENC)
- `-Web` - Iniciar servidor web
- `-Help` - Mostrar ayuda del script Python

**Posicionales:**

- `InputPath` (posición 0) - Ruta del archivo de entrada
- `OutputPath` (posición 1) - Ruta del archivo de salida (opcional)

### Funciones de Conveniencia

| Función    | Descripción          | Parámetros                        |
| ---------- | -------------------- | --------------------------------- |
| `cvt-mp4`  | Convertir a MP4      | `InputPath`, `OutputPath`, `-GPU` |
| `cvt-webm` | Convertir a WebM     | `InputPath`, `OutputPath`, `-GPU` |
| `cvt-avi`  | Convertir a AVI      | `InputPath`, `OutputPath`         |
| `cvt-mkv`  | Convertir a MKV      | `InputPath`, `OutputPath`, `-GPU` |
| `cvt-web`  | Iniciar servidor web | Ninguno                           |
| `cvt-help` | Mostrar ayuda rápida | Ninguno                           |

### Aliases Globales

| Alias         | Función Destino |
| ------------- | --------------- |
| `convert`     | `Convert-Video` |
| `vid-convert` | `Convert-Video` |

## 💡 Ejemplos de Uso

### Después de la integración, desde cualquier directorio:

```powershell
# Función principal con sintaxis completa
Convert-Video -MP4 "C:\Videos\input.mov"
Convert-Video -WebM ".\video.mp4" -GPU
Convert-Video -MKV "video.avi" "C:\Output\converted.mkv"

# Funciones cortas (más convenientes)
cvt-mp4 "video.mov"
cvt-webm "video.mp4" -GPU
cvt-avi "video.mkv"
cvt-mkv "video.avi" "output.mkv"

# Utilidades
cvt-web                    # Abre http://localhost:5000
cvt-help                   # Ayuda rápida
Convert-Video -Help        # Ayuda completa del Python script

# Usando aliases
convert -MP4 "video.mov"
vid-convert -WebM "video.mp4" -GPU
```

### Trabajando con rutas relativas:

```powershell
# Desde cualquier directorio con videos
cd "D:\MisVideos"
cvt-mp4 ".\clip.webm"                    # Salida: ./converted/clip.mp4
cvt-webm ".\movie.avi" ".\exports\movie.webm"  # Salida personalizada
```

## 🛠️ Troubleshooting

### Error: "Cannot load converter.ps1"

**Causa:** Políticas de ejecución de PowerShell

**Solución:**

```powershell
# Permitir scripts locales
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar política actual
Get-ExecutionPolicy -List
```

### Error: "Convert-Video is not recognized"

**Causa:** Perfil no se cargó correctamente

**Solución:**

```powershell
# Verificar que el archivo existe
Test-Path $PROFILE

# Verificar contenido del perfil
Get-Content $PROFILE

# Recargar manualmente
. $PROFILE

# Probar carga directa
. E:\workspace\video-converter-flask\converter.ps1
```

### Error: "No se encontró el entorno virtual"

**Causa:** El proyecto no está configurado correctamente

**Solución:**

```powershell
# Ir al directorio del proyecto
cd E:\workspace\video-converter-flask

# Crear entorno virtual
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### Funciones no aparecen en autocompletado

**Causa:** PowerShell necesita actualizar caché de comandos

**Solución:**

```powershell
# Forzar actualización de comandos
Import-Module Microsoft.PowerShell.Core -Force

# O reiniciar PowerShell
```

## 🔍 Verificación de Instalación

### Script de prueba:

```powershell
# Verificar que las funciones están cargadas
Get-Command *cvt*

# Debería mostrar:
# cvt-avi, cvt-help, cvt-mkv, cvt-mp4, cvt-web, cvt-webm

# Probar ayuda
cvt-help

# Probar función principal
Convert-Video -Help
```

### Verificar capacidades GPU:

```powershell
# Desde cualquier directorio
Convert-Video -Help | Select-String "nvenc"

# O verificar directamente ffmpeg
ffmpeg -encoders | findstr nvenc
```

## � Rendimiento después de la integración

### Ventajas:

- ✅ **Funciones globales** - Disponibles desde cualquier directorio
- ✅ **Autocompletado** - IntelliSense funciona con parámetros
- ✅ **Rutas relativas** - Se resuelven correctamente
- ✅ **Integración nativa** - Parte del ecosistema PowerShell
- ✅ **Consistency** - Mismo estilo que tus otros scripts

### Comparación de métodos:

```powershell
# Antes: Script standalone
cd E:\workspace\video-converter-flask
.\convert-simple.ps1 --mp4 "C:\Videos\input.mov"

# Después: Función integrada
# Desde cualquier directorio:
cvt-mp4 "C:\Videos\input.mov"
```

## 🔄 Actualización del perfil

Si actualizas el archivo `converter.ps1`, simplemente recarga:

```powershell
# Recargar perfil completo
. $PROFILE

# O solo el script del conversor
. E:\workspace\video-converter-flask\converter.ps1
```

## 🚀 Pro Tips

### Usa tab completion:

```powershell
# Escribe y presiona Tab
cvt-<Tab>           # Cicla entre cvt-mp4, cvt-webm, etc.
Convert-Video -<Tab> # Muestra todos los parámetros disponibles
```

### Combina con otros comandos:

```powershell
# Buscar y convertir videos
Get-ChildItem *.mov | ForEach-Object { cvt-mp4 $_.FullName }

# Batch conversion
@("video1.avi", "video2.mkv") | ForEach-Object { cvt-mp4 $_ }
```

### Crea aliases personalizados:

```powershell
# Agregar a tu perfil para aliases cortos
Set-Alias c2mp4 cvt-mp4
Set-Alias c2webm cvt-webm
```

---

**💡 Una vez configurado, tendrás conversión de videos nativa en PowerShell desde cualquier ubicación!**
