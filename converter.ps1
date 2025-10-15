# =============================================================================
# Scripts del Conversor de Videos
# =============================================================================

<#
.SYNOPSIS
    Conversor de videos usando ffmpeg con soporte para GPU

.DESCRIPTION
    Funciones para convertir videos desde línea de comandos o iniciar interfaz web

.NOTES
    Requiere: Python, ffmpeg, venv configurado en el proyecto
#>

# Función principal del conversor
function Convert-Video {
    [CmdletBinding()]
    param(
        [Parameter(Position = 0)]
        [string]$InputPath,
        
        [Parameter(Position = 1)]
        [string]$OutputPath,
        
        [switch]$MP4,
        [switch]$WebM,
        [switch]$AVI,
        [switch]$MKV,
        [switch]$MP3,
        [switch]$SRT,
        [switch]$GPU,
        [switch]$Web,
        [switch]$Help,
        
        [ValidateSet('tiny', 'base', 'small', 'medium', 'large')]
        [string]$Model = 'base'
    )
    
    # Configuración de rutas del proyecto
    $ProjectDir = "E:\workspace\video-converter-flask"
    $VenvPython = Join-Path $ProjectDir ".venv\Scripts\python.exe"
    $AppScript = Join-Path $ProjectDir "app.py"
    
    # Verificaciones básicas
    if (-not (Test-Path $VenvPython)) {
        Write-Host "❌ ERROR: No se encontró el entorno virtual en:" -ForegroundColor Red
        Write-Host "   $VenvPython" -ForegroundColor Yellow
        Write-Host "💡 Para configurar:" -ForegroundColor Cyan
        Write-Host "   cd `"$ProjectDir`"" -ForegroundColor Gray
        Write-Host "   python -m venv .venv" -ForegroundColor Gray
        Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
        Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
        return
    }
    
    if (-not (Test-Path $AppScript)) {
        Write-Host "❌ ERROR: No se encontró app.py en $AppScript" -ForegroundColor Red
        return
    }
    
    # Resolver rutas absolutas ANTES de cambiar de directorio
    $OriginalLocation = Get-Location
    
    # Determinar formato basado en switches
    $Format = $null
    $FormatCount = 0
    if ($MP4) { $Format = "mp4"; $FormatCount++ }
    if ($WebM) { $Format = "webm"; $FormatCount++ }
    if ($AVI) { $Format = "avi"; $FormatCount++ }
    if ($MKV) { $Format = "mkv"; $FormatCount++ }
    if ($MP3) { $Format = "mp3"; $FormatCount++ }
    if ($SRT) { $Format = "srt"; $FormatCount++ }
    
    # Validar que solo se especificó un formato
    if ($FormatCount -gt 1) {
        Write-Host "❌ ERROR: Solo puede especificar un formato a la vez" -ForegroundColor Red
        return
    }
    
    if ($InputPath) {
        # Convertir ruta relativa a absoluta desde el directorio actual
        if (-not [System.IO.Path]::IsPathRooted($InputPath)) {
            $InputPath = Join-Path $OriginalLocation $InputPath
        }
        
        # Verificar que el archivo existe
        if (-not (Test-Path $InputPath)) {
            Write-Host "❌ ERROR: El archivo de entrada no existe:" -ForegroundColor Red
            Write-Host "   Ruta: $InputPath" -ForegroundColor Yellow
            Write-Host "   Directorio actual: $OriginalLocation" -ForegroundColor Gray
            return
        }
        
        # Obtener la ruta absoluta completa
        $InputPath = (Get-Item $InputPath).FullName
        Write-Host "📁 Archivo de entrada: $InputPath" -ForegroundColor Gray
    }
    
    if ($OutputPath) {
        # Convertir ruta relativa a absoluta desde el directorio actual
        if (-not [System.IO.Path]::IsPathRooted($OutputPath)) {
            $OutputPath = Join-Path $OriginalLocation $OutputPath
        }
        # Para el archivo de salida, solo necesitamos la ruta absoluta, no verificar que existe
        $OutputPath = [System.IO.Path]::GetFullPath($OutputPath)
        Write-Host "📁 Archivo de salida: $OutputPath" -ForegroundColor Gray
    }
    
    # Cambiar al directorio del proyecto
    Push-Location $ProjectDir
    
    try {
        # Construir argumentos para Python
        $PythonArgs = @()
        
        if ($Help) {
            $PythonArgs += "--help"
        }
        elseif ($Web -or (-not $Format -and -not $InputPath)) {
            # Modo servidor web
            Write-Host "🌐 Iniciando servidor web en http://localhost:5000..." -ForegroundColor Green
            & $VenvPython $AppScript
            return
        }
        else {
            # Modo conversión CLI
            if (-not $Format) {
                Write-Host "❌ ERROR: Debe especificar un formato (-MP4, -WebM, -AVI, -MKV, -MP3, -SRT)" -ForegroundColor Red
                Write-Host "💡 Ejemplo: Convert-Video -MP4 'video.mov'" -ForegroundColor Yellow
                Write-Host "💡 Ejemplo: Convert-Video -MP3 'video.mp4' # Extraer audio" -ForegroundColor Yellow
                Write-Host "💡 Ejemplo: Convert-Video -SRT 'video.mp4' # Generar subtítulos" -ForegroundColor Yellow
                return
            }
            
            if (-not $InputPath) {
                Write-Host "❌ ERROR: Debe especificar la ruta del archivo de entrada" -ForegroundColor Red
                return
            }
            
            # Construir argumentos
            $PythonArgs += "--$Format"
            $PythonArgs += $InputPath
            
            if ($OutputPath) {
                $PythonArgs += $OutputPath
            }
            
            if ($GPU) {
                $PythonArgs += "--gpu"
            }
            
            # Añadir modelo para SRT
            if ($Format -eq "srt") {
                $PythonArgs += "--model"
                $PythonArgs += $Model
            }
            
            Write-Host "🔄 Convirtiendo a $($Format.ToUpper())..." -ForegroundColor Blue
            if ($Format -eq "mp3") {
                Write-Host "🎵 Extrayendo audio..." -ForegroundColor Magenta
            }
            elseif ($Format -eq "srt") {
                Write-Host "🤖 Generando subtítulos con IA (modelo: $Model)..." -ForegroundColor Magenta
            }
            elseif ($GPU) {
                Write-Host "⚡ Usando aceleración GPU" -ForegroundColor Cyan
            }
        }
        
        # Medir tiempo de ejecución
        $StartTime = Get-Date
        
        # Ejecutar conversión
        & $VenvPython $AppScript @PythonArgs
        
        # Calcular tiempo transcurrido
        $EndTime = Get-Date
        $Duration = $EndTime - $StartTime
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Operación completada exitosamente" -ForegroundColor Green
            Write-Host "⏱️  Tiempo transcurrido: $($Duration.ToString('mm\:ss\.ff'))" -ForegroundColor Cyan
        }
        else {
            Write-Host "❌ Error en la operación (código: $LASTEXITCODE)" -ForegroundColor Red
            Write-Host "⏱️  Tiempo transcurrido: $($Duration.ToString('mm\:ss\.ff'))" -ForegroundColor Yellow
        }
    }
    finally {
        # Volver al directorio original
        Pop-Location
    }
}

# Aliases y funciones de conveniencia
function cvt-mp4 {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath,
        [switch]$GPU
    )
    Convert-Video -MP4 -InputPath $InputPath -OutputPath $OutputPath -GPU:$GPU
}

function cvt-webm {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath,
        [switch]$GPU
    )
    Convert-Video -WebM -InputPath $InputPath -OutputPath $OutputPath -GPU:$GPU
}

function cvt-avi {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath
    )
    Convert-Video -AVI -InputPath $InputPath -OutputPath $OutputPath
}

function cvt-mkv {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath,
        [switch]$GPU
    )
    Convert-Video -MKV -InputPath $InputPath -OutputPath $OutputPath -GPU:$GPU
}

function cvt-mp3 {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath
    )
    Convert-Video -MP3 -InputPath $InputPath -OutputPath $OutputPath
}

function cvt-srt {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$InputPath,
        [Parameter(Position = 1)]
        [string]$OutputPath,
        [ValidateSet('tiny', 'base', 'small', 'medium', 'large')]
        [string]$Model = 'base'
    )
    Convert-Video -SRT -InputPath $InputPath -OutputPath $OutputPath -Model $Model
}

function cvt-web {
    Convert-Video -Web
}

function cvt-help {
    Write-Host "🎬 Conversor de Videos - Funciones Disponibles" -ForegroundColor Blue
    Write-Host "=============================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "📋 Función principal:" -ForegroundColor Yellow
    Write-Host "  Convert-Video -MP4 'archivo.mov'           - Convertir a MP4" -ForegroundColor White
    Write-Host "  Convert-Video -WebM 'archivo.mp4' -GPU     - Convertir a WebM con GPU" -ForegroundColor White
    Write-Host "  Convert-Video -AVI 'archivo.mkv'           - Convertir a AVI" -ForegroundColor White
    Write-Host "  Convert-Video -MKV 'archivo.mp4' -GPU      - Convertir a MKV con GPU" -ForegroundColor White
    Write-Host "  Convert-Video -MP3 'archivo.mp4'           - Extraer audio a MP3" -ForegroundColor White
    Write-Host "  Convert-Video -SRT 'archivo.mp4'           - Generar subtítulos con IA" -ForegroundColor White
    Write-Host "  Convert-Video -Web                         - Iniciar servidor web" -ForegroundColor White
    Write-Host "  Convert-Video -Help                        - Mostrar ayuda completa" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Funciones de conveniencia:" -ForegroundColor Yellow
    Write-Host "  cvt-mp4 'video.mov'                        - Convertir a MP4" -ForegroundColor White
    Write-Host "  cvt-webm 'video.mp4' -GPU                  - Convertir a WebM" -ForegroundColor White
    Write-Host "  cvt-avi 'video.mkv'                        - Convertir a AVI" -ForegroundColor White
    Write-Host "  cvt-mkv 'video.avi' 'salida.mkv'           - Convertir a MKV" -ForegroundColor White
    Write-Host "  cvt-mp3 'video.mp4'                        - Extraer audio a MP3" -ForegroundColor White
    Write-Host "  cvt-srt 'video.mp4'                        - Generar subtítulos SRT" -ForegroundColor White
    Write-Host "  cvt-web                                     - Iniciar servidor web" -ForegroundColor White
    Write-Host "  cvt-help                                    - Mostrar esta ayuda" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Ejemplos de uso:" -ForegroundColor Yellow
    Write-Host "  cvt-mp4 'video.mov'" -ForegroundColor Gray
    Write-Host "  cvt-mp3 'conferencia.mp4'" -ForegroundColor Gray
    Write-Host "  cvt-srt 'conferencia.mp4'" -ForegroundColor Gray
    Write-Host "  cvt-srt 'video.mkv' -Model medium" -ForegroundColor Gray
    Write-Host "  Convert-Video -WebM 'video.mp4' -GPU" -ForegroundColor Gray
    Write-Host "  Convert-Video -SRT 'video.avi' 'C:\subtitulos\video.srt' -Model large" -ForegroundColor Gray
    Write-Host "  Convert-Video -Help" -ForegroundColor Gray
    Write-Host "  cvt-web" -ForegroundColor Gray
    Write-Host ""
    Write-Host "⚡ Switches disponibles:" -ForegroundColor Yellow
    Write-Host "  -GPU     : Usar aceleración GPU (NVENC) - no aplica para MP3/SRT" -ForegroundColor White
    Write-Host "  -Model   : Modelo Whisper (tiny/base/small/medium/large) - solo para SRT" -ForegroundColor White
    Write-Host "  -Web     : Iniciar servidor web" -ForegroundColor White
    Write-Host "  -Help    : Mostrar ayuda del script Python" -ForegroundColor White
    Write-Host ""
    Write-Host "🤖 Modelos Whisper disponibles:" -ForegroundColor Yellow
    Write-Host "  tiny     : Más rápido, menos preciso (~39 MB)" -ForegroundColor White
    Write-Host "  base     : Equilibrado, recomendado (~74 MB)" -ForegroundColor White
    Write-Host "  small    : Mejor calidad (~244 MB)" -ForegroundColor White
    Write-Host "  medium   : Alta calidad (~769 MB)" -ForegroundColor White
    Write-Host "  large    : Máxima calidad (~1550 MB)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎵 Extracción de audio:" -ForegroundColor Yellow
    Write-Host "  La extracción a MP3 es ideal para transcripción con IA" -ForegroundColor White
    Write-Host "  Bitrate: 192 kbps, Sample rate: 44.1 kHz" -ForegroundColor White
}

# Alias adicionales
Set-Alias convert Convert-Video
Set-Alias vid-convert Convert-Video