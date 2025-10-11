# =============================================================================
# Script de Prueba para Converter.ps1
# =============================================================================

Write-Host "🧪 Probando funciones del conversor..." -ForegroundColor Cyan

# Cargar las funciones
try {
    . "E:\workspace\video-converter-flask\converter.ps1"
    Write-Host "✅ Funciones cargadas correctamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error cargando funciones: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Funciones disponibles:" -ForegroundColor Yellow
Get-Command -Name "*cvt*" | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "💡 Ejemplo de uso desde cualquier directorio:" -ForegroundColor Yellow
Write-Host "  cvt-mp4 '.\archivo.webm'" -ForegroundColor Gray
Write-Host "  Convert-Video mp4 '.\video.mov' 'C:\salida\video.mp4'" -ForegroundColor Gray

Write-Host ""
Write-Host "🔍 Para probar la resolución de rutas:" -ForegroundColor Yellow
Write-Host "  1. Ve a cualquier directorio que tenga un archivo de video" -ForegroundColor Gray
Write-Host "  2. Ejecuta: cvt-mp4 '.\archivo.ext'" -ForegroundColor Gray
Write-Host "  3. Ahora debería resolverse correctamente la ruta" -ForegroundColor Gray