# 🤖 Curso de Fundamentos de LLM y Agentes

Curso práctico e intensivo sobre los fundamentos del uso de Modelos de Lenguaje de Gran Escala (LLM) y Agentes inteligentes utilizando la API de OpenAI.

## 📋 Descripción

Este repositorio contiene ejemplos prácticos y progresivos que te enseñarán a trabajar con modelos de lenguaje, desde llamadas básicas a la API hasta la implementación de agentes con herramientas personalizadas. El curso está diseñado para desarrolladores que quieren entender y aplicar las capacidades de los LLMs en aplicaciones reales.

## 🎯 ¿Qué Aprenderás?

- ✅ Realizar llamadas a la API de OpenAI de manera directa y mediante librerías
- ✅ Procesar y analizar imágenes con modelos multimodales
- ✅ Integrar búsquedas web en tus consultas
- ✅ Crear y utilizar herramientas personalizadas (function calling)
- ✅ Implementar respuestas en streaming para mejor UX
- ✅ Construir conversaciones con contexto persistente
- ✅ Desarrollar agentes autónomos e inteligentes

## 🚀 Requisitos Previos

- Python 3.8 o superior
- Ambiente virtual con librerías instaladas.
- Una cuenta de OpenAI con créditos disponibles
- API Key de OpenAI

## ⚙️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd agents-course-2025
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar tu API Key**

   Crea una variable de entorno con tu clave de OpenAI:

   ```powershell
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="tu-api-key-aqui"
   
   # Para hacerlo permanente
   [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY','tu-api-key-aqui','User')
   ```

   ```bash
   # Linux/Mac
   export OPENAI_API_KEY="tu-api-key-aqui"
   
   # Para hacerlo permanente, agregar a ~/.bashrc o ~/.zshrc
   echo 'export OPENAI_API_KEY="tu-api-key-aqui"' >> ~/.bashrc
   ```

   > 💡 **Consejo**: Nunca subas tu API key a repositorios públicos. Considera usar archivos `.env` con python-dotenv.

### Módulo 01: Conversaciones

*Próximamente: Gestión de contexto y conversaciones multi-turno*

### Módulo 02: Agentes

*Próximamente: Construcción de agentes autónomos con capacidades avanzadas*

## 💡 Conceptos Clave

- **LLM (Large Language Model)**: Modelos de inteligencia artificial entrenados con grandes volúmenes de texto capaces de generar y comprender lenguaje natural.

- **Prompt**: La instrucción o pregunta que le das al modelo para obtener una respuesta.

- **Streaming**: Técnica para recibir la respuesta del modelo de forma progresiva en lugar de esperar la respuesta completa.

- **Function Calling**: Capacidad del modelo para identificar cuándo debe invocar funciones externas para completar una tarea.

- **Agente**: Sistema autónomo que utiliza un LLM para tomar decisiones y realizar acciones para lograr objetivos específicos.

## 🤝 Contribuciones

Este es un curso educativo. Si encuentras errores o tienes sugerencias de mejora, no dudes en abrir un issue o pull request.
