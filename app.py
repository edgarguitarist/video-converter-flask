
import os, re, json, uuid, subprocess, threading, queue, time, argparse, sys
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, request, send_file, abort, Response, jsonify, url_for
from werkzeug.utils import secure_filename

# Importación condicional de Whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

# Importación condicional de deep-translator
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    GoogleTranslator = None

ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.avi', '.wmv', '.flv', '.webm', '.m4v'}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2GB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['CONVERTED_FOLDER'] = os.path.join(os.getcwd(), 'converted')
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'change-me'

jobs = {}  # job_id -> dict


def list_ffmpeg_encoders() -> str:
    try:
        out = subprocess.check_output(['ffmpeg','-hide_banner','-encoders'], stderr=subprocess.STDOUT, text=True)
        return out
    except Exception:
        return ""

def has_encoder(name: str) -> bool:
    encs = list_ffmpeg_encoders()
    return (name in encs) if encs else False

def seconds_to_srt_time(seconds: float) -> str:
    """
    Convierte segundos a formato de tiempo SRT (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def transcribe_audio_to_srt(audio_path: str, output_srt_path: str, model_size: str = "base") -> bool:
    """
    Transcribe audio usando Whisper y genera archivo SRT con timestamps
    """
    if not WHISPER_AVAILABLE:
        print("❌ ERROR: Whisper no está instalado. Instala con: pip install openai-whisper")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ ERROR: Archivo de audio no encontrado: {audio_path}")
        return False
    
    try:
        print(f"🤖 Cargando modelo Whisper ({model_size})...")
        model = whisper.load_model(model_size)
        
        print(f"🎵 Transcribiendo audio: {audio_path}")
        result = model.transcribe(audio_path, word_timestamps=True)
        
        print(f"📄 Generando archivo SRT: {output_srt_path}")
        
        # Crear directorio de salida si no existe
        os.makedirs(os.path.dirname(output_srt_path), exist_ok=True)
        
        with open(output_srt_path, 'w', encoding='utf-8') as f:
            subtitle_index = 1
            
            for segment in result['segments']:
                start_time = seconds_to_srt_time(segment['start'])
                end_time = seconds_to_srt_time(segment['end'])
                text = segment['text'].strip()
                
                f.write(f"{subtitle_index}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
                
                subtitle_index += 1
        
        print(f"✅ Subtítulos generados exitosamente: {output_srt_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR durante la transcripción: {e}")
        return False

def translate_text(text: str, target_language: str, source_language: str = 'auto') -> str:
    """
    Traduce texto usando Google Translator
    """
    if not TRANSLATOR_AVAILABLE:
        print("❌ ERROR: deep-translator no está instalado. Instala con: pip install deep-translator")
        return text
    
    try:
        # Mapeo de códigos de idioma comunes
        language_map = {
            'spanish': 'es', 'español': 'es', 'es': 'es',
            'english': 'en', 'inglés': 'en', 'ingles': 'en', 'en': 'en',
            'french': 'fr', 'francés': 'fr', 'frances': 'fr', 'fr': 'fr',
            'german': 'de', 'alemán': 'de', 'aleman': 'de', 'de': 'de',
            'italian': 'it', 'italiano': 'it', 'it': 'it',
            'portuguese': 'pt', 'portugués': 'pt', 'portugues': 'pt', 'pt': 'pt',
            'russian': 'ru', 'ruso': 'ru', 'ru': 'ru',
            'japanese': 'ja', 'japonés': 'ja', 'japones': 'ja', 'ja': 'ja',
            'korean': 'ko', 'coreano': 'ko', 'ko': 'ko',
            'chinese': 'zh', 'chino': 'zh', 'zh': 'zh',
            'dutch': 'nl', 'holandés': 'nl', 'holandes': 'nl', 'nl': 'nl',
            'arabic': 'ar', 'árabe': 'ar', 'arabe': 'ar', 'ar': 'ar'
        }
        
        # Convertir idioma objetivo a código
        target_lang_code = language_map.get(target_language.lower(), target_language.lower())
        source_lang_code = language_map.get(source_language.lower(), source_language.lower()) if source_language != 'auto' else 'auto'
        
        # Crear traductor
        translator = GoogleTranslator(source=source_lang_code, target=target_lang_code)
        
        # Traducir texto en chunks para evitar límites
        max_length = 4000  # Límite conservador
        if len(text) <= max_length:
            return translator.translate(text)
        else:
            # Dividir texto en chunks más pequeños
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            translated_chunks = []
            for chunk in chunks:
                translated_chunks.append(translator.translate(chunk))
            return ' '.join(translated_chunks)
            
    except Exception as e:
        print(f"⚠️  Error al traducir: {e}")
        return text  # Retornar texto original si hay error

def transcribe_and_translate_to_srt(audio_path: str, output_srt_path: str, target_language: str, model_size: str = "base") -> bool:
    """
    Transcribe audio usando Whisper y genera dos archivos SRT: original y traducido
    """
    if not WHISPER_AVAILABLE:
        print("❌ ERROR: Whisper no está instalado. Instala con: pip install openai-whisper")
        return False
    
    if not TRANSLATOR_AVAILABLE:
        print("❌ ERROR: deep-translator no está instalado. Instala con: pip install deep-translator")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ ERROR: Archivo de audio no encontrado: {audio_path}")
        return False
    
    try:
        print(f"🤖 Cargando modelo Whisper ({model_size})...")
        model = whisper.load_model(model_size)
        
        print(f"🎵 Transcribiendo audio: {audio_path}")
        result = model.transcribe(audio_path, word_timestamps=True)
        
        # Crear rutas para ambos archivos SRT
        original_srt_path = output_srt_path
        translated_srt_path = output_srt_path.replace('.srt', f'_{target_language}.srt')
        
        print(f"📄 Generando archivo SRT original: {original_srt_path}")
        print(f"🌍 Generando archivo SRT traducido: {translated_srt_path}")
        
        # Crear directorio de salida si no existe
        os.makedirs(os.path.dirname(output_srt_path), exist_ok=True)
        
        # Generar archivo SRT original
        with open(original_srt_path, 'w', encoding='utf-8') as f_orig:
            subtitle_index = 1
            
            for segment in result['segments']:
                start_time = seconds_to_srt_time(segment['start'])
                end_time = seconds_to_srt_time(segment['end'])
                text = segment['text'].strip()
                
                f_orig.write(f"{subtitle_index}\n")
                f_orig.write(f"{start_time} --> {end_time}\n")
                f_orig.write(f"{text}\n\n")
                
                subtitle_index += 1
        
        print(f"✅ Archivo SRT original generado: {original_srt_path}")
        
        # Generar archivo SRT traducido
        print(f"🌍 Traduciendo subtítulos a {target_language}...")
        with open(translated_srt_path, 'w', encoding='utf-8') as f_trans:
            subtitle_index = 1
            
            for segment in result['segments']:
                start_time = seconds_to_srt_time(segment['start'])
                end_time = seconds_to_srt_time(segment['end'])
                original_text = segment['text'].strip()
                
                # Traducir el texto
                translated_text = translate_text(original_text, target_language)
                
                f_trans.write(f"{subtitle_index}\n")
                f_trans.write(f"{start_time} --> {end_time}\n")
                f_trans.write(f"{translated_text}\n\n")
                
                subtitle_index += 1
                
                # Mostrar progreso cada 10 subtítulos
                if subtitle_index % 10 == 0:
                    print(f"🔄 Traduciendo... {subtitle_index} subtítulos procesados")
        
        print(f"✅ Archivo SRT traducido generado: {translated_srt_path}")
        print(f"🎉 Proceso completado: 2 archivos SRT creados")
        return True
        
    except Exception as e:
        print(f"❌ ERROR durante la transcripción y traducción: {e}")
        return False

def get_codec_args(target_format: str, use_gpu: bool = False) -> tuple:
    """
    Retorna (codec_args, chosen_encoder) para el formato y configuración dados
    """
    chosen_encoder = None
    
    if target_format == 'mp4':
        if use_gpu:
            chosen_encoder = 'h264_nvenc'
            if has_encoder('h264_nvenc'):
                codec_args = ['-c:v','h264_nvenc','-preset','p5','-cq','23','-c:a','aac','-b:a','128k']
            else:
                use_gpu = False
                codec_args = ['-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','128k']
        else:
            codec_args = ['-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','128k']
    elif target_format == 'webm':
        if use_gpu:
            chosen_encoder = 'av1_nvenc'
            if has_encoder('av1_nvenc'):
                codec_args = ['-c:v','av1_nvenc','-cq','28','-c:a','libopus','-b:a','96k']
            else:
                use_gpu = False
                codec_args = ['-c:v','libvpx-vp9','-b:v','0','-crf','33','-c:a','libopus','-b:a','96k']
        else:
            codec_args = ['-c:v','libvpx-vp9','-b:v','0','-crf','33','-c:a','libopus','-b:a','96k']
    elif target_format == 'avi':
        # AVI no suele beneficiarse del pipeline NVENC moderno; mantenemos SW
        codec_args = ['-c:v','mpeg4','-qscale:v','5','-c:a','libmp3lame','-q:a','4']
    elif target_format == 'mp3':
        # Extracción de audio en MP3 - sin video
        codec_args = ['-vn', '-c:a', 'libmp3lame', '-b:a', '192k', '-ar', '44100']
        chosen_encoder = 'Audio only'
    else:  # mkv
        if use_gpu:
            chosen_encoder = 'hevc_nvenc'
            if has_encoder('hevc_nvenc'):
                codec_args = ['-c:v','hevc_nvenc','-preset','p5','-cq','24','-c:a','aac','-b:a','128k']
            else:
                use_gpu = False
                codec_args = ['-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','128k']
        else:
            codec_args = ['-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','128k']
    
    return codec_args, chosen_encoder if use_gpu or target_format == 'mp3' else None

def convert_video_cli(input_path: str, output_path: str, target_format: str, use_gpu: bool = False) -> bool:
    """
    Convierte un video usando ffmpeg en modo CLI
    Retorna True si la conversión fue exitosa, False en caso contrario
    """
    if not os.path.exists(input_path):
        print(f"Error: El archivo de entrada '{input_path}' no existe.")
        return False
    
    if not allowed_file(input_path):
        print(f"Error: Formato de archivo no soportado. Formatos permitidos: {', '.join(ALLOWED_EXTENSIONS)}")
        return False
    
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Obtener argumentos de codec
    codec_args, chosen_encoder = get_codec_args(target_format, use_gpu)
    
    # Obtener duración para mostrar progreso
    duration = ffprobe_duration(input_path)
    
    print(f"Convirtiendo: {input_path}")
    print(f"Destino: {output_path}")
    print(f"Formato: .{target_format}")
    print(f"GPU: {'Sí' if use_gpu else 'No'}")
    if chosen_encoder:
        print(f"Encoder: {chosen_encoder}")
    print("-" * 50)
    
    # Ejecutar ffmpeg
    cmd = ['ffmpeg', '-hide_banner', '-y', '-i', input_path, *codec_args, output_path]
    
    # Medir tiempo de ejecución
    start_time = time.time()
    
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        time_re = re.compile(r'time=(\d+):(\d+):(\d+(\.\d+)?)')
        
        for line in proc.stderr:
            print(line.rstrip())
            # Mostrar progreso si tenemos duración
            if duration > 0:
                m = time_re.search(line)
                if m:
                    hh, mm, ss = int(m.group(1)), int(m.group(2)), float(m.group(3))
                    cur = hh*3600 + mm*60 + ss
                    pct = max(0.0, min(100.0, (cur/duration)*100.0))
                    print(f"\rProgreso: {pct:.1f}%", end="", flush=True)
        
        ret = proc.wait()
        print()  # Nueva línea después del progreso
        
        # Calcular tiempo transcurrido
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Formatear tiempo en formato legible
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        time_str = f"{minutes:02d}:{seconds:05.2f}" if minutes > 0 else f"{seconds:.2f}s"
        
        if ret == 0:
            print(f"✓ Conversión completada exitosamente: {output_path}")
            print(f"⏱️  Tiempo transcurrido: {time_str}")
            return True
        else:
            print(f"✗ Error en la conversión. ffmpeg terminó con código {ret}")
            print(f"⏱️  Tiempo transcurrido: {time_str}")
            return False
            
    except Exception as e:
        print(f"✗ Error durante la conversión: {e}")
        return False


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def ffprobe_duration(path: str) -> float:
    # Return duration in seconds (float) using ffprobe, or 0 if unknown.
    try:
        cmd = ['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1', path]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
        return float(out) if out else 0.0
    except Exception:
        return 0.0

def sse_format(event: str = None, data: str = "") -> str:
    chunks = []
    if event:
        chunks.append(f"event: {event}")
    # split multi-line data
    for line in data.splitlines() or [""]:
        chunks.append(f"data: {line}")
    return "\n".join(chunks) + "\n\n"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    if 'file' not in request.files:
        abort(400, "No se envió archivo.")
    f = request.files['file']
    target_format = request.form.get('format', '').lower().strip()
    use_gpu = request.form.get('gpu', 'off') == 'on'

    if target_format not in {'mp4','webm','avi','mkv','mp3'}:
        abort(400, "Formato objetivo inválido.")
    if f.filename == '':
        abort(400, "Nombre de archivo vacío.")
    if not allowed_file(f.filename):
        abort(400, "Tipo de archivo no permitido.")

    orig_name = secure_filename(f.filename)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{ts}-{orig_name}")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)
    f.save(input_path)

    base_name = Path(orig_name).stem
    out_name = f"{base_name}-{ts}.{target_format}"
    output_path = os.path.join(app.config['CONVERTED_FOLDER'], out_name)

    # Obtener argumentos de codec
    codec_args, chosen_encoder = get_codec_args(target_format, use_gpu)

    # Precalcular duración para porcentaje
    duration = ffprobe_duration(input_path)

    job_id = uuid.uuid4().hex
    jobs[job_id] = {
        'status': 'running',
        'duration': duration,
        'progress': 0.0,
        'log': queue.Queue(),
        'output_path': output_path,
        'download_name': out_name,
        'error': None
    }

    # Ejecutar ffmpeg en hilo aparte y enviar logs a la cola
    def run_ffmpeg():
        # Log inicial
        try:
            jobs[job_id]['log'].put_nowait(f"Destino: .{target_format}  | GPU: {'Sí' if use_gpu else 'No'}  | Encoder: {chosen_encoder or 'CPU'}")
        except Exception:
            pass
        cmd = ['ffmpeg','-hide_banner','-y','-i', input_path, *codec_args, output_path]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        time_re = re.compile(r'time=(\d+):(\d+):(\d+(\.\d+)?)')
        try:
            for line in proc.stderr:
                # Encolar línea
                try: jobs[job_id]['log'].put_nowait(line.rstrip())
                except queue.Full: pass
                # Extraer tiempo
                m = time_re.search(line)
                if m and duration > 0:
                    hh, mm, ss = int(m.group(1)), int(m.group(2)), float(m.group(3))
                    cur = hh*3600 + mm*60 + ss
                    pct = max(0.0, min(100.0, (cur/duration)*100.0))
                    jobs[job_id]['progress'] = pct
            ret = proc.wait()
            # limpieza del archivo subido
            try: os.remove(input_path)
            except Exception: pass
            if ret == 0:
                jobs[job_id]['progress'] = 100.0
                jobs[job_id]['status'] = 'done'
            else:
                jobs[job_id]['status'] = 'error'
                jobs[job_id]['error'] = f"ffmpeg salió con código {ret}"
        except Exception as e:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = str(e)

    threading.Thread(target=run_ffmpeg, daemon=True).start()

    return jsonify({'job_id': job_id, 'download_url': url_for('download', job_id=job_id, _external=False)})

@app.route('/progress/<job_id>')
def progress(job_id):
    if job_id not in jobs:
        return abort(404, 'Job no encontrado')

    def stream():
        # Primer ping de estado
        yield sse_format(event="status", data=json.dumps({
            'status': jobs[job_id]['status'],
            'progress': jobs[job_id]['progress']
        }))
        # Emitir logs a medida que llegan
        while True:
            if jobs[job_id]['status'] in ('done','error'):
                # drenar pendientes
                while not jobs[job_id]['log'].empty():
                    yield sse_format(event="log", data=jobs[job_id]['log'].get())
                yield sse_format(event="status", data=json.dumps({
                    'status': jobs[job_id]['status'],
                    'progress': jobs[job_id]['progress'],
                    'error': jobs[job_id]['error']
                }))
                break
            try:
                line = jobs[job_id]['log'].get(timeout=0.5)
                yield sse_format(event="log", data=line)
                yield sse_format(event="progress", data=str(jobs[job_id]['progress']))
            except queue.Empty:
                # heartbeat
                yield sse_format(event="progress", data=str(jobs[job_id]['progress']))
                continue

    return Response(stream(), mimetype='text/event-stream')

@app.route('/download/<job_id>')
def download(job_id):
    job = jobs.get(job_id)
    if not job or job['status'] != 'done':
        return abort(404, 'No disponible aún')
    return send_file(job['output_path'], as_attachment=True, download_name=job['download_name'])

def main():
    parser = argparse.ArgumentParser(description='Conversor de videos - Modo web o línea de comandos')
    
    # Argumentos para modo CLI
    parser.add_argument('--mp4', metavar='INPUT', help='Convertir a MP4. Especifica la ruta del video de entrada.')
    parser.add_argument('--webm', metavar='INPUT', help='Convertir a WebM. Especifica la ruta del video de entrada.')
    parser.add_argument('--avi', metavar='INPUT', help='Convertir a AVI. Especifica la ruta del video de entrada.')
    parser.add_argument('--mkv', metavar='INPUT', help='Convertir a MKV. Especifica la ruta del video de entrada.')
    parser.add_argument('--mp3', metavar='INPUT', help='Extraer audio a MP3. Especifica la ruta del video de entrada.')
    parser.add_argument('--srt', metavar='INPUT', help='Extraer audio a MP3 y generar subtítulos SRT con IA. Especifica la ruta del video de entrada.')
    parser.add_argument('output', nargs='?', help='Ruta de salida (opcional, usa la misma carpeta del video de entrada por defecto)')
    parser.add_argument('--gpu', action='store_true', help='Usar aceleración GPU (NVENC) - no aplica para MP3/SRT')
    parser.add_argument('--model', default='base', choices=['tiny', 'base', 'small', 'medium', 'large'], 
                        help='Modelo Whisper para transcripción (tiny/base/small/medium/large). Default: base')
    parser.add_argument('--translate', metavar='LANGUAGE', 
                        help='Idioma para traducir subtítulos (ej: english, spanish, french, german, etc.). Genera SRT original + traducido')
    parser.add_argument('--web', action='store_true', help='Iniciar servidor web (modo por defecto)')
    
    args = parser.parse_args()
    
    # Determinar formato y archivo de entrada
    input_file = None
    target_format = None
    
    if args.mp4:
        input_file = args.mp4
        target_format = 'mp4'
    elif args.webm:
        input_file = args.webm
        target_format = 'webm'
    elif args.avi:
        input_file = args.avi
        target_format = 'avi'
    elif args.mkv:
        input_file = args.mkv
        target_format = 'mkv'
    elif args.mp3:
        input_file = args.mp3
        target_format = 'mp3'
    elif args.srt:
        input_file = args.srt
        target_format = 'srt'
    
    # Modo CLI
    if input_file and target_format:
        # Determinar ruta de salida
        if args.output:
            output_path = args.output
        else:
            # Usar la misma carpeta del archivo de entrada
            input_path_obj = Path(input_file)
            if target_format == 'srt':
                output_filename = f"{input_path_obj.stem}.srt"
            else:
                output_filename = f"{input_path_obj.stem}.{target_format}"
            output_path = input_path_obj.parent / output_filename
            output_path = str(output_path)  # Convertir a string para compatibilidad
        
        # Modo especial para SRT (extrae MP3 primero y luego transcribe)
        if target_format == 'srt':
            # Generar ruta temporal para MP3
            input_path_obj = Path(input_file)
            temp_mp3_path = input_path_obj.parent / f"{input_path_obj.stem}_temp.mp3"
            temp_mp3_path = str(temp_mp3_path)
            
            print(f"🎬 Procesando video para subtítulos: {input_file}")
            print(f"📄 Archivo SRT de salida: {output_path}")
            print(f"🤖 Modelo Whisper: {args.model}")
            if args.translate:
                print(f"🌍 Idioma de traducción: {args.translate}")
                print(f"📋 Se generarán 2 archivos: original + traducido")
            print("-" * 60)
            
            # Paso 1: Extraer audio a MP3
            print("📤 Paso 1/3: Extrayendo audio..." if args.translate else "📤 Paso 1/2: Extrayendo audio...")
            use_gpu = args.gpu and False  # GPU no aplica para audio
            success = convert_video_cli(input_file, temp_mp3_path, 'mp3', use_gpu)
            
            if not success:
                print("❌ Error extrayendo audio")
                sys.exit(1)
            
            # Paso 2: Transcribir con Whisper (y traducir si se especifica)
            start_time = time.time()
            
            if args.translate:
                print(f"\n🤖 Paso 2/3: Transcribiendo con IA...")
                print(f"🌍 Paso 3/3: Traduciendo a {args.translate}...")
                success = transcribe_and_translate_to_srt(temp_mp3_path, output_path, args.translate, args.model)
            else:
                print("\n🤖 Paso 2/2: Transcribiendo con IA...")
                success = transcribe_audio_to_srt(temp_mp3_path, output_path, args.model)
                
            end_time = time.time()
            
            # Limpiar archivo temporal MP3
            try:
                os.remove(temp_mp3_path)
                print(f"🗑️  Archivo temporal MP3 eliminado")
            except Exception:
                pass
            
            # Mostrar tiempo total
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60
            time_str = f"{minutes:02d}:{seconds:05.2f}" if minutes > 0 else f"{seconds:.2f}s"
            
            if success:
                if args.translate:
                    original_srt = output_path
                    translated_srt = output_path.replace('.srt', f'_{args.translate}.srt')
                    print(f"✅ Transcripción completada: {original_srt}")
                    print(f"✅ Traducción completada: {translated_srt}")
                    print(f"🎉 2 archivos SRT generados exitosamente")
                else:
                    print(f"✅ Subtítulos completados: {output_path}")
                print(f"⏱️  Tiempo de procesamiento: {time_str}")
            else:
                print(f"❌ Error en la transcripción")
                print(f"⏱️  Tiempo transcurrido: {time_str}")
            
            sys.exit(0 if success else 1)
        
        # Realizar conversión normal (no SRT)
        else:
            # Para MP3, desactivar GPU ya que es solo audio
            use_gpu = args.gpu and target_format != 'mp3'
            success = convert_video_cli(input_file, output_path, target_format, use_gpu)
            sys.exit(0 if success else 1)
    
    # Modo web (por defecto)
    else:
        print("Iniciando servidor web en http://localhost:5000")
        print("Usa --help para ver opciones de línea de comandos")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)
        app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()
