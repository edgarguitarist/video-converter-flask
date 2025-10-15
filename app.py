
import os, re, json, uuid, subprocess, threading, queue, time, argparse, sys
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, send_file, abort, Response, jsonify, url_for
from werkzeug.utils import secure_filename

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
    
    return codec_args, chosen_encoder if use_gpu else None

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
        
        if ret == 0:
            print(f"✓ Conversión completada exitosamente: {output_path}")
            return True
        else:
            print(f"✗ Error en la conversión. ffmpeg terminó con código {ret}")
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

    if target_format not in {'mp4','webm','avi','mkv'}:
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
    parser.add_argument('output', nargs='?', help='Ruta de salida (opcional, usa la misma carpeta del video de entrada por defecto)')
    parser.add_argument('--gpu', action='store_true', help='Usar aceleración GPU (NVENC)')
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
    
    # Modo CLI
    if input_file and target_format:
        # Determinar ruta de salida
        if args.output:
            output_path = args.output
        else:
            # Usar la misma carpeta del archivo de entrada
            input_path_obj = Path(input_file)
            output_filename = f"{input_path_obj.stem}.{target_format}"
            output_path = input_path_obj.parent / output_filename
            output_path = str(output_path)  # Convertir a string para compatibilidad
        
        # Realizar conversión
        success = convert_video_cli(input_file, output_path, target_format, args.gpu)
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
