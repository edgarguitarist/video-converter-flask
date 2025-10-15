#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guía de soluciones para problemas de Whisper
"""

import os
import subprocess

def check_running_processes():
    """Verifica procesos Python que puedan estar colgados"""
    try:
        # En Windows
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and 'python.exe' in result.stdout:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            python_procs = []
            for line in lines:
                if 'python.exe' in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        pid = parts[1].strip('"')
                        python_procs.append(pid)
            
            if python_procs:
                print(f"🔍 Encontrados {len(python_procs)} procesos Python:")
                for pid in python_procs:
                    print(f"   PID: {pid}")
                
                print("\n💡 Para terminar procesos colgados:")
                print("   taskkill /F /PID <numero_pid>")
                print("   O usar: taskkill /F /IM python.exe")
            else:
                print("✅ No hay procesos Python ejecutándose")
        
    except Exception as e:
        print(f"⚠️  No se pudo verificar procesos: {e}")

def cleanup_suggestions():
    """Muestra sugerencias para limpiar"""
    print("🧹 SUGERENCIAS DE LIMPIEZA")
    print("=" * 30)
    
    print("📂 Buscar archivos temporales:")
    print("   Dir /s *temp*.mp3")
    print("   Dir /s *temp*.wav")
    print("   Get-ChildItem -Recurse -Include '*temp*' | Remove-Item")
    
    print("\n🔄 Terminar procesos Python:")
    print("   taskkill /F /IM python.exe")
    
    print("\n🧠 Liberar memoria:")
    print("   - Cerrar navegadores con muchas pestañas")
    print("   - Cerrar programas no esenciales")
    print("   - Reiniciar si es necesario")

def whisper_troubleshooting():
    """Guía de resolución de problemas"""
    print("\n🚨 RESOLUCIÓN DE PROBLEMAS DE WHISPER")
    print("=" * 45)
    
    print("❌ PROBLEMA: Transcripción se cuelga/toma mucho tiempo")
    print("✅ SOLUCIONES:")
    print("   1. Usar modelo más pequeño:")
    print("      python app.py --srt video.mp4 --model tiny")
    print("   2. Verificar tamaño del archivo:")
    print("      - <100MB: modelo base/small")
    print("      - >100MB: modelo tiny")
    print("   3. Verificar duración:")
    print("      - <30 min: cualquier modelo")
    print("      - >30 min: modelo tiny/base")
    
    print("\n❌ PROBLEMA: Error de memoria")
    print("✅ SOLUCIONES:")
    print("   1. Cerrar otros programas")
    print("   2. Usar modelo tiny")
    print("   3. Dividir video en partes")
    
    print("\n❌ PROBLEMA: Proceso colgado")
    print("✅ SOLUCIONES:")
    print("   1. Ctrl+C para cancelar")
    print("   2. taskkill /F /IM python.exe")
    print("   3. Usar el nuevo sistema de timeout")

def main():
    print("🛠️  DIAGNÓSTICO Y SOLUCIONES PARA WHISPER")
    print("=" * 50)
    
    # Verificar procesos
    check_running_processes()
    
    # Sugerencias de limpieza
    cleanup_suggestions()
    
    # Guía de resolución
    whisper_troubleshooting()
    
    print("\n🎯 MEJORAS IMPLEMENTADAS:")
    print("   ✅ Sistema de progreso con tiempo transcurrido")
    print("   ✅ Timeout automático (evita cuelgues indefinidos)")
    print("   ✅ Información detallada del archivo")
    print("   ✅ Configuración optimizada para velocidad")
    print("   ✅ Detección automática de hardware (CPU/GPU)")
    print("   ✅ Warnings de archivos grandes")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("   1. Terminar procesos colgados si los hay")
    print("   2. Probar con archivo pequeño primero")
    print("   3. Usar modelo 'tiny' para pruebas")
    print("   4. El nuevo código ya tiene timeouts!")

if __name__ == "__main__":
    main()