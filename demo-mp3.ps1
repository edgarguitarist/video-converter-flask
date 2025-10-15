#!/usr/bin/env pwsh

# 🎵 Demo de Extracción de Audio MP3
# ================================

Write-Host "🎬 Conversor de Videos - Demo de Extracción de Audio MP3" -ForegroundColor Blue
Write-Host "=========================================================" -ForegroundColor Blue
Write-Host ""

# Verificar si el proyecto está configurado
$ProjectDir = "E:\workspace\video-converter-flask"
$VenvPython = Join-Path $ProjectDir ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "❌ ERROR: Entorno virtual no configurado" -ForegroundColor Red
    Write-Host "💡 Configurar primero:" -ForegroundColor Yellow
    Write-Host "   cd `"$ProjectDir`"" -ForegroundColor Gray
    Write-Host "   python -m venv .venv" -ForegroundColor Gray
    Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
    exit
}

Write-Host "✅ Entorno virtual encontrado" -ForegroundColor Green
Write-Host ""

# Ejemplos de uso
Write-Host "📋 Ejemplos de uso de extracción de audio MP3:" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔧 CLI Python:" -ForegroundColor Cyan
Write-Host "  python app.py --mp3 `"video.mp4`"" -ForegroundColor White
Write-Host "  python app.py --mp3 `"video.mov`" `"audio.mp3`"" -ForegroundColor White
Write-Host ""

Write-Host "⚡ PowerShell (después de cargar converter.ps1):" -ForegroundColor Cyan
Write-Host "  cvt-mp3 `"video.mp4`"" -ForegroundColor White
Write-Host "  Convert-Video -MP3 `"video.avi`" `"audio.mp3`"" -ForegroundColor White
Write-Host ""

Write-Host "🌐 Web:" -ForegroundColor Cyan
Write-Host "  python app.py" -ForegroundColor White
Write-Host "  Luego abrir http://localhost:5000" -ForegroundColor White
Write-Host "  Seleccionar MP3 en el formato de salida" -ForegroundColor White
Write-Host ""

Write-Host "🎯 Características del MP3 generado:" -ForegroundColor Yellow
Write-Host "  • Bitrate: 192 kbps" -ForegroundColor White
Write-Host "  • Sample Rate: 44.1 kHz" -ForegroundColor White
Write-Host "  • Codec: libmp3lame" -ForegroundColor White
Write-Host "  • Ideal para transcripción con IA" -ForegroundColor White
Write-Host ""

Write-Host "🤖 Casos de uso para IA:" -ForegroundColor Yellow
Write-Host "  • Transcripción con Whisper" -ForegroundColor White
Write-Host "  • Traducción automática" -ForegroundColor White
Write-Host "  • Análisis de sentimientos" -ForegroundColor White
Write-Host "  • Generación de subtítulos" -ForegroundColor White
Write-Host "  • Creación de resúmenes" -ForegroundColor White
Write-Host ""

Write-Host "📚 Documentación:" -ForegroundColor Yellow
Write-Host "  • AUDIO-EXTRACTION.md - Guía completa" -ForegroundColor White
Write-Host "  • MP3-EXAMPLES.md - Ejemplos prácticos" -ForegroundColor White
Write-Host "  • README.md - Documentación general" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Para empezar:" -ForegroundColor Green
Write-Host "  1. Tener un video en cualquier formato" -ForegroundColor White
Write-Host "  2. Ejecutar: cvt-mp3 `"mi_video.mp4`"" -ForegroundColor White
Write-Host "  3. Obtener: mi_video.mp3 (listo para IA)" -ForegroundColor White
Write-Host ""

Write-Host "¡Listo para extraer audio y usar con IA! 🎵🤖" -ForegroundColor Green