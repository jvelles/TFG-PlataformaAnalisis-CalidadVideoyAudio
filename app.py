from flask import Flask, request, jsonify, render_template
import subprocess
import os
import json
import requests
import openai
from dotenv import load_dotenv
import yt_dlp as youtube_dl
from bs4 import BeautifulSoup
import re



# Cargar variables de entorno desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, template_folder='templates', static_folder='static')


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

def clean_comment(comment):
    # Eliminar etiquetas HTML con BeautifulSoup
    soup = BeautifulSoup(comment, "html.parser")
    clean_text = soup.get_text()

    # Eliminar marcas de tiempo en formato "5:48" o "05:48"
    clean_text = re.sub(r'\b\d{1,2}:\d{2}\b', '', clean_text)

    # Quitar espacios adicionales
    clean_text = clean_text.strip()
    return clean_text


# Obtener comentarios del video
def get_video_comments(video_id):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?videoId={video_id}&part=snippet&key={YOUTUBE_API_KEY}&maxResults=10"
    response = requests.get(url)
    comments_data = response.json()

    # Procesar cada comentario y limpiar HTML y marcas de tiempo
    cleaned_comments = []
    for item in comments_data.get("items", []):
        raw_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        cleaned_comment = clean_comment(raw_comment)
        cleaned_comments.append({"text": cleaned_comment})

    return cleaned_comments

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
        r'C:\Program Files (x86)\ffmpeg\bin\ffprobe.exe', 
        '-v', 'error',
        '-show_format', '-show_streams',
        '-print_format', 'json',
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def analyze_technical_data(video_streams, audio_streams):
    prompt = f"""
    Proporciona un análisis fluido y continuo de la calidad técnica del siguiente video y audio. No uses listas ni puntos, 
    sino una narrativa coherente que explique las características del video y audio de forma integrada.

    Datos técnicos:
    - Video:
      - Resolución: {video_streams[0].get('width')}x{video_streams[0].get('height')}
      - Bitrate: {video_streams[0].get('bit_rate')}
      - FPS: {video_streams[0].get('avg_frame_rate')}
      - Códec: {video_streams[0].get('codec_name')}
      - Formato de Píxeles: {video_streams[0].get('pix_fmt')}
      - Espacio de Color: {video_streams[0].get('color_space')}
      - Transf. de Color: {video_streams[0].get('color_transfer')}
      - Prim. de Color: {video_streams[0].get('color_primaries')}
    - Audio:
      - Códec: {audio_streams[0].get('codec_name')}
      - Canales: {audio_streams[0].get('channels')}
      - Bitrate: {audio_streams[0].get('bit_rate')}
      - Frecuencia de Muestreo: {audio_streams[0].get('sample_rate')}
      - Formato de Píxeles: {audio_streams[0].get('sample_fmt')}
      - Frame Size: {audio_streams[0].get('frame_size')}

   Por favor, escribe de manera accesible y evita la jerga técnica. Explica cómo estos datos influyen en la calidad del video y 
    el audio en términos comprensibles, y sugiere áreas de mejora si es necesario.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Ajusta la temperatura para hacer que la respuesta sea más variada y fluida
            top_p=0.9
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error en analyze_technical_data: {e}")
        return "Error al analizar los datos técnicos."

def analyze_user_comments(comments):
    prompt = f"""
    Proporciona un resumen fluido y continuo de los siguientes comentarios de usuarios sobre el video. Usa un lenguaje natural y evita 
    cortes en párrafos o puntos separados. Integra las ideas principales de los comentarios y describe las preferencias de los usuarios.

    Comentarios de usuarios:
    {"\\n".join([f'"{comment}"' for comment in comments])}

    El análisis debe ser accesible y directo, usando un estilo narrativo para facilitar la lectura. Explica en general si los comentarios 
    reflejan satisfacción, críticas o sugerencias, y si hay temas o puntos recurrentes. Finaliza con una conclusión breve.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Ajusta la temperatura para hacer que la respuesta sea más variada y fluida
            top_p=0.9
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error en analyze_user_comments: {e}")
        return "Error al analizar los comentarios."


# Ruta de la API para analizar un video
@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.json.get('video_url')
    video_id = video_url.split("v=")[-1]  # Extraer el ID del video de la URL

    # Obtener información del video desde la API de YouTube
    video_info = get_video_info(video_id)

    # Obtener comentarios del video
    comments = get_video_comments(video_id)
    comment_texts = [comment["text"] for comment in comments]  # Lista de solo texto


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


    # Realizar análisis técnico y de comentarios
    technical_analysis = analyze_technical_data(video_streams, audio_streams)
    comments_analysis = analyze_user_comments(comments)

    # Eliminar el video después del análisis
    os.remove(video_path)


    # Devolver la información obtenida y el análisis del video como respuesta JSON
    return jsonify({
        'video_info': video_info,
        'video_streams': video_streams,
        'audio_streams': audio_streams,
        'comments': comment_texts,  
        'technical_analysis': technical_analysis,
        'comments_analysis': comments_analysis
    })

if __name__ == '__main__':
    app.run(debug=True)