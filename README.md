# PLATAFORMA WEB PARA EL ANÁLISIS DE AUDIO Y VIDEO EN VIDEOS DE YOUTUBE Y DIAGNÓSTICO CON IA

## Descripción
Esta plataforma permite analizar la calidad de video y audio de transmisiones en **YouTube** mediante su URL. Extrae información técnica del video, incluyendo resolución, bitrate, FPS y características del audio. Además, emplea **inteligencia artificial** para analizar los comentarios y obtener información sobre la percepción de los usuarios.

---

## Características Principales
✅ **Análisis técnico del video**: Resolución, bitrate, FPS, códec, espacio de color, etc.  
✅ **Análisis del audio**: Bitrate, frecuencia de muestreo, códec de audio, canales, etc.  
✅ **Análisis de comentarios con IA**: Procesamiento del sentimiento y detección de tendencias.  
✅ **Modo oscuro**: Interfaz adaptable con cambio dinámico de temas.  
✅ **Interfaz intuitiva**: Diseño moderno con una presentación clara de resultados.  
✅ **Términos y Política de Privacidad**: Página dedicada con información sobre seguridad y uso de APIs.  

---

## 📂 Estructura del Proyecto

TFG-PlataformaAnalisis-CalidadVideoAudio  
- static  
  - css → Estilos y temas de la plataforma  
  - js → Funcionalidad y scripts  
  - images → Iconos y recursos gráficos  
- templates  
  - index.html → Página principal  
  - terms.html → Página de Términos y Condiciones  
- backend  
  - app.py → Servidor Flask para procesar análisis  
- .env → Claves API necesarias  
- requirements.txt → Dependencias del proyecto  
- README.md → Documentación del proyecto  


---

## Tecnologías Utilizadas
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask y FFprobe)  
- **APIs**: YouTube Data API, OpenAI API  

---

## Requisitos Previos
Antes de ejecutar la plataforma, asegúrate de tener:  
- Python 3.8 instalado.  
- Claves API para YouTube Data API y OpenAI en un archivo `.env`.  
- Librerías necesarias instaladas (ver `requirements.txt`).  

---

## Instalación

### 1. Clonar el repositorio 

- git clone https://github.com/jvelles/TFG-PlataformaAnalisis-CalidadVideoyAudio.git
- cd TFG-PlataformaAnalisis-CalidadVideoyAudio

### 2. Instalar dependencias

pip install -r requirements.txt

### 3. Configurar las claves API

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

- YOUTUBE_API_KEY=TU_CLAVE_AQUI
- OPENAI_API_KEY=TU_CLAVE_AQUI

### 4. Ejecutar la aplicación

python app.py

La aplicación estará disponible en http://127.0.0.1:5000/.

## Uso de la Plataforma
1. Introducir la URL de un video de YouTube.
2. Analizar el contenido para obtener estadísticas técnicas.
3. Ver el análisis de los comentarios basado en IA.
4. Alternar entre modo claro y oscuro según preferencia.
5. Consultar los Terminos de Uso y Política de Privacidad

---

## Mejoras Futuras
- Implementación de más plataformas de streaming.
- Soporte para tener acceso todo el mundo vía host.
- Generación de informes descargables en PDF.
- Integración con bases de datos para almacenamiento de resultados.

---

## Licencia
Este proyecto es de código abierto y está disponible bajo la licencia **MIT**.

---

## Contacto
- **Email**: [j.velles.2019@alumnos.urjc.es](mailto:j.velles.2019@alumnos.urjc.es)
- **GitHub Repo**: [TFG-PlataformaAnalisis-CalidadVideoyAudio](https://github.com/jvelles/TFG-PlataformaAnalisis-CalidadVideoyAudio)
