#!/usr/bin/env pwsh

# 🤖 Demo de Transcripción con IA - Generación de Subtítulos SRT
# ============================================================

Write-Host "🤖 Conversor de Videos - Demo de Transcripción con IA" -ForegroundColor Blue
Write-Host "====================================================" -ForegroundColor Blue
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

# Verificar si Whisper está instalado
Write-Host "🔍 Verificando instalación de Whisper..." -ForegroundColor Cyan
$WhisperCheck = & $VenvPython -c "try: import whisper; print('OK')" 2>$null
if ($WhisperCheck -eq "OK") {
    Write-Host "✅ OpenAI Whisper instalado correctamente" -ForegroundColor Green
}
else {
    Write-Host "❌ OpenAI Whisper no está instalado" -ForegroundColor Red
    Write-Host "💡 Instalar con:" -ForegroundColor Yellow
    Write-Host "   pip install openai-whisper torch torchaudio" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🔄 ¿Quieres instalarlo ahora? (S/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    if ($response -eq "S" -or $response -eq "s") {
        Write-Host "📦 Instalando Whisper y dependencias..." -ForegroundColor Cyan
        & $VenvPython -m pip install openai-whisper torch torchaudio
        Write-Host "✅ Instalación completada" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Funcionalidad de transcripción no disponible sin Whisper" -ForegroundColor Yellow
        exit
    }
}

Write-Host ""

# Ejemplos de uso
Write-Host "📋 Ejemplos de uso de transcripción con IA:" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔧 CLI Python:" -ForegroundColor Cyan
Write-Host "  python app.py --srt `"video.mp4`"" -ForegroundColor White
Write-Host "  python app.py --srt `"video.mov`" --model medium" -ForegroundColor White
Write-Host "  python app.py --srt `"video.mkv`" `"subtitulos.srt`" --model large" -ForegroundColor White
Write-Host ""

Write-Host "⚡ PowerShell (después de cargar converter.ps1):" -ForegroundColor Cyan
Write-Host "  cvt-srt `"video.mp4`"" -ForegroundColor White
Write-Host "  cvt-srt `"video.mp4`" -Model medium" -ForegroundColor White
Write-Host "  Convert-Video -SRT `"video.avi`" `"subtitulos.srt`" -Model large" -ForegroundColor White
Write-Host ""

Write-Host "🤖 Modelos Whisper disponibles:" -ForegroundColor Yellow
Write-Host "  🏃‍♀️ tiny   (~39 MB)  - Muy rápido, calidad básica" -ForegroundColor White
Write-Host "  ⚡ base   (~74 MB)  - Equilibrado, RECOMENDADO" -ForegroundColor Green
Write-Host "  📈 small  (~244 MB) - Mejor calidad, más lento" -ForegroundColor White
Write-Host "  🎯 medium (~769 MB) - Alta calidad profesional" -ForegroundColor White
Write-Host "  🏆 large  (~1550 MB)- Máxima calidad, muy lento" -ForegroundColor White
Write-Host ""

Write-Host "📄 Proceso automático:" -ForegroundColor Yellow
Write-Host "  1. 📤 Extrae audio del video (MP3 temporal)" -ForegroundColor White
Write-Host "  2. 🤖 Carga modelo Whisper especificado" -ForegroundColor White
Write-Host "  3. 🎵 Transcribe audio con IA" -ForegroundColor White
Write-Host "  4. ⏱️  Genera timestamps precisos" -ForegroundColor White
Write-Host "  5. 📄 Crea archivo SRT estándar" -ForegroundColor White
Write-Host "  6. 🗑️  Limpia archivos temporales" -ForegroundColor White
Write-Host ""

Write-Host "🎯 Casos de uso ideales:" -ForegroundColor Yellow
Write-Host "  📚 Conferencias y cursos educativos" -ForegroundColor White
Write-Host "  💼 Reuniones y presentaciones empresariales" -ForegroundColor White
Write-Host "  🌐 Videos de YouTube y redes sociales" -ForegroundColor White
Write-Host "  🎙️  Podcasts y entrevistas" -ForegroundColor White
Write-Host "  🎬 Contenido multimedia accesible" -ForegroundColor White
Write-Host ""

Write-Host "⏱️  Tiempos aproximados (modelo base):" -ForegroundColor Yellow
Write-Host "  📹 5 minutos  → 30-45 segundos de transcripción" -ForegroundColor White
Write-Host "  📹 30 minutos → 3-5 minutos de transcripción" -ForegroundColor White
Write-Host "  📹 2 horas    → 15-20 minutos de transcripción" -ForegroundColor White
Write-Host ""

Write-Host "🌍 Idiomas soportados:" -ForegroundColor Yellow
Write-Host "  ✅ Español (excelente)" -ForegroundColor White
Write-Host "  ✅ Inglés (excelente)" -ForegroundColor White
Write-Host "  ✅ Francés, Alemán, Italiano (muy bueno)" -ForegroundColor White
Write-Host "  ✅ Y más de 90 idiomas adicionales" -ForegroundColor White
Write-Host ""

Write-Host "📚 Documentación:" -ForegroundColor Yellow
Write-Host "  • TRANSCRIPTION-AI.md - Guía completa de transcripción" -ForegroundColor White
Write-Host "  • AUDIO-EXTRACTION.md - Extracción de audio MP3" -ForegroundColor White
Write-Host "  • README.md - Documentación general" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Para empezar:" -ForegroundColor Green
Write-Host "  1. Tener un video en cualquier formato" -ForegroundColor White
Write-Host "  2. Ejecutar: cvt-srt `"mi_video.mp4`"" -ForegroundColor White
Write-Host "  3. Obtener: mi_video.srt (subtítulos listos)" -ForegroundColor White
Write-Host "  4. Usar en cualquier reproductor de video" -ForegroundColor White
Write-Host ""

Write-Host "💡 Tip: Comienza con modelo 'base' para balance óptimo" -ForegroundColor Cyan
Write-Host "¡Listo para generar subtítulos automáticamente con IA! 🤖📄✨" -ForegroundColor Green