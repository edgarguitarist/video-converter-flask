#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Conversor de videos - CLI wrapper

.DESCRIPTION
    Script simple para usar el conversor de videos sin activar venv manualmente

.EXAMPLE
    .\convert.ps1 --mp4 "video.mov"
    .\convert.ps1 --webm "video.mp4" --gpu
    .\convert.ps1 --help
#>

param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

# Configuración de rutas
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$AppScript = Join-Path $ProjectDir "app.py"

# Verificaciones básicas
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERROR: No se encontro el entorno virtual."
    Write-Host "Ejecuta: python -m venv .venv && .\.venv\Scripts\Activate.ps1 && pip install -r requirements.txt"
    exit 1
}

if (-not (Test-Path $AppScript)) {
    Write-Host "ERROR: No se encontro app.py"
    exit 1
}

# Cambiar al directorio del proyecto
Set-Location $ProjectDir

# Ejecutar la aplicación
if (-not $Arguments -or $Arguments.Count -eq 0) {
    Write-Host "Iniciando servidor web en http://localhost:5000..."
    & $VenvPython $AppScript
}
else {
    & $VenvPython $AppScript @Arguments
}