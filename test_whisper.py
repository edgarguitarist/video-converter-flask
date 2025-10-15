#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar las mejoras de Whisper con progreso y timeouts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import transcribe_with_progress, get_audio_info, WHISPER_AVAILABLE, DEVICE
import whisper

def test_transcription(audio_path):
    """Prueba la transcripción con las nuevas mejoras"""
    
    if not WHISPER_AVAILABLE:
        print("❌ Whisper no disponible")
        return
    
    if not os.path.exists(audio_path):
        print(f"❌ Archivo no encontrado: {audio_path}")
        return
    
    print("🧪 PRUEBA DE TRANSCRIPCIÓN CON MEJORAS")
    print("=" * 50)
    
    # Mostrar información del archivo
    duration = get_audio_info(audio_path)
    
    # Cargar modelo pequeño para prueba
    print(f"\n🤖 Cargando modelo 'tiny' en {DEVICE.upper()}...")
    model = whisper.load_model("tiny", device=DEVICE)
    
    # Configuración optimizada
    transcribe_options = {
        'fp16': (DEVICE == "cuda"),
        'condition_on_previous_text': False,
        'temperature': 0.0,
        'compression_ratio_threshold': 2.4,
        'logprob_threshold': -1.0,
        'no_speech_threshold': 0.6
    }
    
    # Timeout corto para prueba
    timeout_mins = 5
    print(f"⏰ Timeout para prueba: {timeout_mins} minutos")
    
    try:
        print(f"\n🎵 Iniciando transcripción con timeout...")
        result = transcribe_with_progress(
            model, 
            audio_path, 
            timeout_minutes=timeout_mins, 
            **transcribe_options
        )
        
        if result and 'text' in result:
            text_preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            print(f"\n📝 Texto detectado:")
            print(f"   {text_preview}")
            print(f"\n✅ Transcripción exitosa!")
            
            if 'segments' in result:
                print(f"📊 Segmentos detectados: {len(result['segments'])}")
        
    except TimeoutError as e:
        print(f"\n⏰ {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python test_whisper.py <archivo_audio>")
        print("Ejemplo: python test_whisper.py audio.mp3")
        sys.exit(1)
    
    test_transcription(sys.argv[1])