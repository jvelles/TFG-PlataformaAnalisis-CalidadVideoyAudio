from flask import Flask, request, jsonify, render_template
import subprocess
import os
import json
import requests
import openai
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import io



# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurar la API Key de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ruta para mostrar el index.html
@app.route('/')
def home():
    return render_template('index.html')

# Obtener la clave de la API de YouTube desde las variables de entorno
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Función para obtener datos de la API de YouTube
def get_video_info(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    return response.json()

# Obtener comentarios del video
def get_video_comments(video_id):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?videoId={video_id}&part=snippet&key={YOUTUBE_API_KEY}&maxResults=10"
    response = requests.get(url)
    return response.json()


# Función para descargar el video usando yt-dlp
def download_video(video_url, video_id):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Descargar video y audio en MP4
        'outtmpl': f'{video_id}.mp4',  # Guardar el video como video_id.mp4
        'quiet': True  # No mostrar la salida en la consola
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except Exception as e:
            print(f"Error al descargar el video: {str(e)}")
            return None
    return f'{video_id}.mp4'

# Función para analizar el video usando ffprobe
def analyze_video(video_path):
    command = [
        r'C:\Users\jvell\Desktop\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe', '-v', 'error',
        '-show_format', '-show_streams',
        '-print_format', 'json',
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def analyze_video_with_openai(video_data):
    """
    Genera un análisis detallado del video basado en sus métricas técnicas.
    """
    # Formateamos los datos de entrada para el modelo de OpenAI
    prompt = (
        f"Analiza la calidad de este video en base a las siguientes características técnicas:\n\n"
        f"Códec: {video_data['codec_name']}\n"
        f"Resolución: {video_data['width']}x{video_data['height']}\n"
        f"Bitrate: {video_data['bit_rate']} bps\n"
        f"FPS: {video_data['avg_frame_rate']}\n"
        f"Formato de Píxeles: {video_data.get('pix_fmt', 'No disponible')}\n"
        f"Espacio de Color: {video_data.get('color_space', 'No disponible')}\n"
        f"Transferencia de Color: {video_data.get('color_transfer', 'No disponible')}\n"
        f"Primarios de Color: {video_data.get('color_primaries', 'No disponible')}\n\n"
        f"Da un análisis sobre la calidad de video en base a estas características y sugiere mejoras si es posible."
    )
    
    # Realizamos la petición a OpenAI utilizando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Eres un experto en análisis de calidad de video y audio."},
            {"role": "user", "content": prompt}
        ],
        
        max_tokens=300,
        temperature=0.5
    )
    
    # Extraemos la respuesta generada
    analysis_text = response['choices'][0]['message']['content'].strip()
    return analysis_text


def analyze_comments_with_openai(comments):
    """
    Genera un análisis de los comentarios para identificar el feedback del público.
    """
    # Extrae el texto de los comentarios
    comments_text = "\n".join(
        [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comments['items']]
    )
    
    prompt = (
        f"Analiza el siguiente conjunto de comentarios sobre un video:\n\n"
        f"{comments_text}\n\n"
        f"Proporciona un análisis general del sentimiento del público (positivo, negativo, mixto) y "
        f"destaca las principales críticas o elogios."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Eres un experto en análisis de feedback de usuarios."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5
    )
    
    # Extraemos la respuesta generada
    feedback_analysis = response['choices'][0]['message']['content'].strip()
    return feedback_analysis


# Ruta de la API para analizar un video
@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.json.get('video_url')
    video_id = video_url.split("v=")[-1]  # Extraer el ID del video de la URL

    # Obtener información del video desde la API de YouTube
    video_info = get_video_info(video_id)

    # Obtener comentarios del video
    comments = get_video_comments(video_id)

    # Descargar el video usando yt-dlp
    video_path = download_video(video_url, video_id)
    if not video_path:
        return jsonify({"error": "Error al descargar el video"}), 500

    # Análisis del video utilizando la función analyze_video
    analysis_result = analyze_video(video_path)

    # Separar información de video y audio del análisis
    analysis_json = json.loads(analysis_result)
    video_streams = [stream for stream in analysis_json['streams'] if stream['codec_type'] == 'video']
    audio_streams = [stream for stream in analysis_json['streams'] if stream['codec_type'] == 'audio']

    # Generar análisis técnico y de comentarios usando OpenAI
    technical_analysis = analyze_video_with_openai(video_streams[0])
    feedback_analysis = analyze_comments_with_openai(comments)

    # Devolver la información obtenida y el análisis del video como respuesta JSON
    return jsonify({
        'video_info': video_info,
        'video_streams': video_streams,
        'audio_streams': audio_streams,
        'comments': comments,
        'technical_analysis': technical_analysis,
        'feedback_analysis': feedback_analysis
    })

if __name__ == '__main__':
    app.run(debug=True)
