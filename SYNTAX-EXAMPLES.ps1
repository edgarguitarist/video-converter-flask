# =============================================================================
# Ejemplos de Uso - Conversor de Videos (Nueva Sintaxis)
# =============================================================================

<#
.SYNOPSIS
    Ejemplos de uso con la nueva sintaxis de switches

.DESCRIPTION
    Después de cargar converter.ps1 en tu perfil, puedes usar estas funciones
#>

Write-Host "🎬 Ejemplos de uso del Conversor de Videos" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

Write-Host "📋 NUEVA SINTAXIS - Función principal:" -ForegroundColor Yellow
Write-Host "  Convert-Video -MP4 'video.mov'"
Write-Host "  Convert-Video -WebM 'video.mp4' -GPU"
Write-Host "  Convert-Video -AVI 'video.mkv'"
Write-Host "  Convert-Video -MKV 'video.mp4' 'C:\salida\video.mkv'"
Write-Host "  Convert-Video -Web"
Write-Host "  Convert-Video -Help"
Write-Host ""

Write-Host "📋 Funciones de conveniencia (sin cambios):" -ForegroundColor Yellow
Write-Host "  cvt-mp4 'video.mov'"
Write-Host "  cvt-webm 'video.mp4' -GPU"
Write-Host "  cvt-avi 'video.mkv'"
Write-Host "  cvt-mkv 'video.mp4' 'salida.mkv'"
Write-Host "  cvt-web"
Write-Host "  cvt-help"
Write-Host ""

Write-Host "✅ VENTAJAS de la nueva sintaxis:" -ForegroundColor Green
Write-Host "  - Consistente con el script Python (--mp4, --webm, etc.)"
Write-Host "  - IntelliSense/autocompletado funciona mejor"
Write-Host "  - Previene errores de escritura en formatos"
Write-Host "  - Más claro qué formato se está especificando"
Write-Host ""

Write-Host "❌ SINTAXIS ANTERIOR (ya no funciona):" -ForegroundColor Red
Write-Host "  Convert-Video mp4 'video.mov'  # ❌ Ya no válido"
Write-Host "  Convert-Video 'webm' 'video.mp4'  # ❌ Ya no válido"
Write-Host ""

Write-Host "✅ SINTAXIS ACTUAL (corregida):" -ForegroundColor Green
Write-Host "  Convert-Video -MP4 'video.mov'  # ✅ Correcto"
Write-Host "  Convert-Video -WebM 'video.mp4'  # ✅ Correcto"
Write-Host ""

Write-Host "💡 Tip: Usa 'cvt-help' para ver la ayuda completa" -ForegroundColor Cyan