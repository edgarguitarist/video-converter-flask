#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para problemas de transcripción con Whisper
"""

import os
import sys
import time
import subprocess
import json

def check_audio_file(audio_path):
    """Verifica información del archivo de audio"""
    if not os.path.exists(audio_path):
        print(f"❌ Archivo no encontrado: {audio_path}")
        return False, 0, 0
    
    # Tamaño del archivo
    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"📁 Tamaño: {size_mb:.1f} MB")
    
    # Información con ffprobe
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        
        # Buscar stream de audio
        audio_stream = None
        for stream in info.get('streams', []):
            if stream.get('codec_type') == 'audio':
                audio_stream = stream
                break
        
        if audio_stream:
            duration = float(info.get('format', {}).get('duration', 0))
            bitrate = int(info.get('format', {}).get('bit_rate', 0))
            sample_rate = int(audio_stream.get('sample_rate', 0))
            channels = int(audio_stream.get('channels', 0))
            codec = audio_stream.get('codec_name', 'unknown')
            
            print(f"📊 Información del audio:")
            print(f"   ⏱️  Duración: {duration:.1f} segundos ({duration/60:.1f} minutos)")
            print(f"   🎛️  Codec: {codec}")
            print(f"   🎛️  Bitrate: {bitrate//1000} kbps")
            print(f"   📻 Sample rate: {sample_rate} Hz")
            print(f"   🔊 Canales: {channels}")
            
            # Predicciones de tiempo
            print(f"\n⏰ Estimaciones de tiempo (CPU):")
            models = ['tiny', 'base', 'small', 'medium', 'large']
            multipliers = [8, 15, 25, 40, 60]  # Multiplicadores aproximados para CPU
            
            for model, mult in zip(models, multipliers):
                est_time = duration * mult / 60
                if est_time < 60:
                    print(f"   {model:6}: {est_time:.1f} minutos")
                else:
                    print(f"   {model:6}: {est_time/60:.1f} horas")
            
            return True, duration, size_mb
        else:
            print("❌ No se encontró stream de audio")
            return False, 0, size_mb
            
    except Exception as e:
        print(f"❌ Error analizando archivo: {e}")
        return False, 0, size_mb

def test_whisper_quick(audio_path, duration):
    """Prueba rápida con Whisper usando solo los primeros 30 segundos"""
    try:
        import whisper
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"\n🧪 Prueba rápida con Whisper en {device.upper()}")
        
        # Cargar modelo tiny para prueba rápida
        print("🤖 Cargando modelo tiny...")
        model = whisper.load_model("tiny", device=device)
        
        # Solo transcribir primeros 30 segundos
        max_duration = min(30, duration)
        print(f"🎵 Transcribiendo primeros {max_duration} segundos...")
        
        start_time = time.time()
        
        # Usar options para limitar duración
        result = model.transcribe(
            audio_path, 
            fp16=(device == "cuda"),
            word_timestamps=False,  # Más rápido sin timestamps de palabras
            condition_on_previous_text=False,  # Más rápido
            language=None,  # Auto-detectar
            task="transcribe"
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Prueba completada en {elapsed:.1f} segundos")
        
        if result and 'text' in result:
            text_preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            print(f"📝 Texto detectado: {text_preview}")
            
            # Calcular tiempo estimado para archivo completo
            if elapsed > 0 and max_duration > 0:
                rate = max_duration / elapsed
                full_time = duration / rate / 60  # en minutos
                print(f"📊 Velocidad: {rate:.1f}x tiempo real")
                print(f"⏰ Tiempo estimado para archivo completo: {full_time:.1f} minutos")
            
            return True
        else:
            print("❌ No se obtuvo texto de la transcripción")
            return False
            
    except ImportError:
        print("❌ Whisper no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python whisper_debug.py <archivo_audio>")
        print("Ejemplo: python whisper_debug.py 'D:\\STORE SSD\\mi video_temp.mp3'")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    print("🔍 DIAGNÓSTICO DE WHISPER")
    print("=" * 50)
    
    # Verificar archivo
    success, duration, size_mb = check_audio_file(audio_path)
    
    if not success:
        sys.exit(1)
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if size_mb > 100:
        print("   ⚠️  Archivo muy grande, usa modelo 'tiny' o 'base'")
    if duration > 3600:  # > 1 hora
        print("   ⚠️  Audio muy largo, considera dividirlo")
    
    print("   ✅ Usa modelo 'tiny' para pruebas rápidas")
    print("   ✅ Usa modelo 'base' para balance velocidad/calidad")
    print("   ✅ Considera usar GPU si está disponible")
    
    # Prueba rápida
    print("\n" + "=" * 50)
    test_whisper_quick(audio_path, duration)

if __name__ == "__main__":
    main()