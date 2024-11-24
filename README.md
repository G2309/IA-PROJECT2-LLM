# IA Project 2: Agente Interactivo con Python y CSV  
**Autor**: Gustavo Adolfo Cruz Bardales  
**Carnet**: 22779  

## Video Demostrativo
[Link](https://youtu.be/tNhKbRxVIBA)

---
Este proyecto implementa un agente interactivo que permite:  
- Ejecutar código Python.  
- Analizar archivos CSV.  
- Responder preguntas personalizadas utilizando un modelo de lenguaje (LLM).  
---
## Estructura del Proyecto  

- **app.py**: Archivo principal de la aplicación.  
- **data.csv**: Archivo CSV de ejemplo para pruebas.  
- **Dockerfile**: Archivo para construir el contenedor Docker del proyecto.  
- **history.txt**: Archivo donde se almacena el historial de interacciones del agente.  
- **requirements.txt**: Archivo que contiene las dependencias de Python necesarias.  
- **.env**: Archivo con las claves API requeridas para la ejecución.  
---
## Variables de Entorno  

El archivo `.env` debe contener las siguientes claves API:  

```dotenv
PINECONE_API_KEY=""        # No requerido para este proyecto.
INDEX_NAME=""              # No requerido para este proyecto.
export OPENAI_API_KEY=""   # Clave API de OpenAI (REQUIRED).
FIRECRAWL_API_KEY=""       # No requerido para este proyecto.
PINECONE_ENVIRONMENT=""    # No requerido para este proyecto.
```
---
## Como Ejecutar el Proyecto
```sh
git clone https://github.com/G2309/IA-PROJECT2-LLM.git
cd IA-PROJECT2-LLM
docker buildx build -t ia-2 .
docker run ia-2:latest
```

Por si deseas acceder al historial, puedes verlo en el navegador al final de la página o puedes ingresar al contenedor y ver el archivo directamente.
Mientras el contenedor está en ejecucion puedes hacer:
```sh
docker ps -a
```
Esto te da el nombre del contenedor más reciente y lo colocas en el siguiente comando:
```sh
docker exec -it {nombre_del_contenedor} sh
cat history.txt
```
