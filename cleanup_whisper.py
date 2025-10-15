#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar archivos temporales y procesos colgados de Whisper
"""

import os
import psutil
import subprocess

def cleanup_temp_files():
    """Limpia archivos temporales"""
    print("🧹 LIMPIEZA DE ARCHIVOS TEMPORALES")
    print("=" * 40)
    
    temp_dirs = [
        os.getcwd(),  # Directorio actual
        "uploads",
        "converted",
        os.environ.get('TEMP', ''),
        os.environ.get('TMP', ''),
        "D:\\STORE SSD"  # Tu directorio específico
    ]
    
    temp_patterns = ['*temp*.mp3', '*temp*.wav', '*temp*.m4a']
    
    for temp_dir in temp_dirs:
        if not temp_dir or not os.path.exists(temp_dir):
            continue
            
        print(f"\n📂 Buscando en: {temp_dir}")
        
        try:
            for pattern in temp_patterns:
                files = list(pathlib.Path(temp_dir).glob(pattern))
                for file_path in files:
                    try:
                        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                        print(f"   🗑️  Eliminando: {file_path.name} ({file_size:.1f} MB)")
                        file_path.unlink()
                    except Exception as e:
                        print(f"   ❌ No se pudo eliminar {file_path.name}: {e}")
        except Exception as e:
            print(f"   ⚠️  Error accediendo a {temp_dir}: {e}")

def kill_hung_processes():
    """Termina procesos Python que puedan estar colgados"""
    print("\n🔄 VERIFICANDO PROCESOS COLGADOS")
    print("=" * 40)
    
    python_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent']):
        try:
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'whisper' in cmdline.lower() or 'transcribe' in cmdline.lower():
                    python_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if python_processes:
        print(f"📋 Encontrados {len(python_processes)} procesos relacionados con Whisper:")
        for proc in python_processes:
            try:
                cmdline = ' '.join(proc.info['cmdline'][:3]) + "..." if len(proc.info['cmdline']) > 3 else ' '.join(proc.info['cmdline'])
                print(f"   PID {proc.info['pid']}: {cmdline}")
                
                # Preguntar si terminar el proceso
                response = input(f"   ¿Terminar proceso {proc.info['pid']}? (s/N): ").lower()
                if response == 's':
                    proc.terminate()
                    print(f"   ✅ Proceso {proc.info['pid']} terminado")
            except Exception as e:
                print(f"   ❌ Error con proceso {proc.info['pid']}: {e}")
    else:
        print("✅ No se encontraron procesos Whisper colgados")

def check_system_resources():
    """Verifica recursos del sistema"""
    print("\n💻 RECURSOS DEL SISTEMA")
    print("=" * 30)
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"🖥️  CPU: {cpu_percent}%")
    
    # Memoria
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024**3)
    memory_used_gb = memory.used / (1024**3)
    memory_percent = memory.percent
    print(f"🧠 RAM: {memory_used_gb:.1f}/{memory_gb:.1f} GB ({memory_percent}%)")
    
    # Disco
    disk = psutil.disk_usage('.')
    disk_gb = disk.total / (1024**3)
    disk_used_gb = disk.used / (1024**3)
    disk_percent = (disk.used / disk.total) * 100
    print(f"💾 Disco: {disk_used_gb:.1f}/{disk_gb:.1f} GB ({disk_percent:.1f}%)")
    
    # Recomendaciones
    if memory_percent > 80:
        print("⚠️  Memoria alta - puede causar lentitud en Whisper")
    if cpu_percent > 90:
        print("⚠️  CPU alta - otros procesos pueden estar interfiriendo")
    if disk_percent > 90:
        print("⚠️  Disco lleno - puede causar errores de escritura")

def main():
    import pathlib
    
    print("🛠️  HERRAMIENTA DE DIAGNÓSTICO Y LIMPIEZA")
    print("=" * 50)
    
    # Limpiar archivos temporales
    cleanup_temp_files()
    
    # Verificar procesos colgados
    kill_hung_processes()
    
    # Verificar recursos del sistema
    check_system_resources()
    
    print("\n💡 RECOMENDACIONES PARA EVITAR PROBLEMAS:")
    print("   ✅ Usa modelo 'tiny' para archivos grandes (>100MB)")
    print("   ✅ Divide videos largos (>1 hora) en partes más pequeñas")
    print("   ✅ Cierra otros programas pesados mientras usas Whisper")
    print("   ✅ Verifica que el archivo de audio no esté corrupto")
    print("   ✅ Usa el nuevo sistema de timeout implementado")
    
    print("\n🎉 ¡Limpieza completada!")

if __name__ == "__main__":
    main()