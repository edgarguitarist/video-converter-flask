# 📋 Integración con PowerShell Profile

## 🔧 Configuración

Para agregar las funciones del conversor a tu perfil de PowerShell, añade esta línea a tu `Microsoft.PowerShell_profile.ps1`:

```powershell
# Scripts del Conversor de Videos
. E:\workspace\video-converter-flask\converter.ps1
```

Tu perfil completo quedaría así:

```powershell
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\takuyami.omp.json" | Invoke-Expression

Import-Module -Name Terminal-Icons
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -HistoryNoDuplicates $true
Clear-Host

Add-Type -AssemblyName System.Speech

# Scripts Globales
. E:\workspace\edoga-scripts\global.ps1

# Scripts de Git
. E:\workspace\edoga-scripts\git.ps1

# Scripts de Angular
. E:\workspace\edoga-scripts\angular.ps1

# Scripts de Proyectos (Workspace)
. E:\workspace\edoga-scripts\projects.ps1

# Scripts del Web Scraper
. E:\workspace\web-scraper\scripts.ps1

# Scripts de Test / Desarrollo
. E:\workspace\edoga-scripts\test.ps1

# Scripts de Creación de ZIP del Repo
. E:\workspace\edoga-scripts\repo-zip.ps1

# Scripts del Conversor de Videos
. E:\workspace\video-converter-flask\converter.ps1
```

## 🎯 Funciones Disponibles

### Función Principal

- `Convert-Video` - Función principal con todos los parámetros

### Funciones de Conveniencia

- `cvt-mp4 "video.mov"` - Convertir a MP4
- `cvt-webm "video.mp4" -GPU` - Convertir a WebM con GPU
- `cvt-avi "video.mkv"` - Convertir a AVI
- `cvt-mkv "video.mp4"` - Convertir a MKV
- `cvt-web` - Iniciar servidor web
- `cvt-help` - Mostrar ayuda

### Aliases

- `convert` → `Convert-Video`
- `vid-convert` → `Convert-Video`

## 💡 Ejemplos de Uso

```powershell
# Después de abrir PowerShell, puedes usar directamente:
cvt-mp4 "D:\videos\clip.webm"
cvt-webm "D:\videos\video.mp4" -GPU
Convert-Video -Format mp4 -InputPath "video.mov" -OutputPath "C:\output\video.mp4"
convert -Web  # Iniciar servidor web
cvt-help      # Ver ayuda completa
```

## 🔄 Recargar Perfil

Después de modificar tu perfil, recarga PowerShell o ejecuta:

```powershell
. $PROFILE
```
