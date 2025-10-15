# =============================================================================
# Script de Prueba - Nuevas Rutas de Salida CLI
# =============================================================================

Write-Host "🧪 Probando nuevas rutas de salida CLI vs Web..." -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 COMPORTAMIENTO ACTUAL:" -ForegroundColor Yellow
Write-Host ""

Write-Host "💻 CLI (Línea de Comandos):" -ForegroundColor Green
Write-Host "  Input:  C:\Videos\input.mov" -ForegroundColor Gray
Write-Host "  Output: C:\Videos\input.mp4 (misma carpeta)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Comando: python app.py --mp4 'C:\Videos\input.mov'" -ForegroundColor White
Write-Host "  Resultado: Se crea en la misma carpeta del archivo original" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 Interfaz Web:" -ForegroundColor Green
Write-Host "  Input:  archivo subido vía web" -ForegroundColor Gray
Write-Host "  Output: ./converted/archivo-timestamp.formato" -ForegroundColor Gray
Write-Host ""
Write-Host "  URL: http://localhost:5000" -ForegroundColor White
Write-Host "  Resultado: Se crea en ./converted/ como siempre" -ForegroundColor Green
Write-Host ""

Write-Host "⚡ PowerShell Functions:" -ForegroundColor Green
Write-Host "  Siguen el comportamiento CLI (misma carpeta)" -ForegroundColor Gray
Write-Host ""
Write-Host "  cvt-mp4 'D:\MyVideos\clip.webm'" -ForegroundColor White
Write-Host "  → D:\MyVideos\clip.mp4" -ForegroundColor Green
Write-Host ""

Write-Host "🔍 EJEMPLOS DE USO:" -ForegroundColor Yellow
Write-Host ""

Write-Host "Ejemplo 1 - CLI básico:" -ForegroundColor Cyan
Write-Host "  python app.py --mp4 'D:\Videos\vacation.mov'" -ForegroundColor White
Write-Host "  ✅ Crea: D:\Videos\vacation.mp4" -ForegroundColor Green
Write-Host ""

Write-Host "Ejemplo 2 - CLI con ruta específica:" -ForegroundColor Cyan
Write-Host "  python app.py --webm 'video.mp4' 'C:\Output\converted.webm'" -ForegroundColor White
Write-Host "  ✅ Crea: C:\Output\converted.webm" -ForegroundColor Green
Write-Host ""

Write-Host "Ejemplo 3 - PowerShell function:" -ForegroundColor Cyan
Write-Host "  cvt-mkv 'C:\Temp\input.avi'" -ForegroundColor White
Write-Host "  ✅ Crea: C:\Temp\input.mkv" -ForegroundColor Green
Write-Host ""

Write-Host "Ejemplo 4 - Web (sin cambios):" -ForegroundColor Cyan
Write-Host "  Subir archivo via http://localhost:5000" -ForegroundColor White
Write-Host "  ✅ Crea: ./converted/archivo-20241014-123456.mp4" -ForegroundColor Green
Write-Host ""

Write-Host "💡 VENTAJAS DEL CAMBIO:" -ForegroundColor Yellow
Write-Host "  ✅ Archivos CLI quedan donde el usuario los espera" -ForegroundColor Green
Write-Host "  ✅ No necesita crear carpeta 'converted' para CLI" -ForegroundColor Green
Write-Host "  ✅ Interfaz web mantiene organización en carpeta dedicada" -ForegroundColor Green
Write-Host "  ✅ Comportamiento intuitivo para ambos casos de uso" -ForegroundColor Green