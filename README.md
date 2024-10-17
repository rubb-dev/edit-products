# 🛒 Shopify Product Optimization Automation

## Descripción

Esta aplicación automatiza la optimización de productos en tiendas Shopify. Utilizando Python y la API de Shopify, la app extrae información de los productos y envía los datos a la API de ChatGPT, que devuelve títulos, descripciones, meta títulos y meta descripciones optimizados. Luego, actualiza la tienda con los nuevos datos, mejorando el SEO y ahorrando tiempo.

## Características

- **Extracción automática** de productos desde Shopify usando su API.
- **Generación automática de contenido**: títulos, descripciones, meta títulos y meta descripciones optimizados para SEO utilizando ChatGPT.
- **Actualización automática** de la tienda Shopify con los datos optimizados.
- **Ahorro de tiempo** en la gestión de productos, eliminando la necesidad de hacer cambios manuales.
  
## Tecnologías utilizadas

- **Lenguaje:** Python
- **APIs:** 
  - Shopify API para la gestión de productos.
  - ChatGPT API para la generación de contenido.
  
## Requisitos

- Python 3.x
- Una cuenta de Shopify con acceso a la API.
- Claves de API para Shopify y ChatGPT.

## Instalación

1. Clona este repositorio:

   ```
   git clone https://github.com/rubb-dev/edit-products.git
   cd edit-products
2. Instala las dependencias:
   
   ```
   pip install -r requirements.txt
4. Configura las variables de entorno en un archivo ``.env`` con tus claves API:
   
   ```
   SHOPIFY_API_KEY = 'Shopify api key'
   SHOPIFY_PASSWORD = 'Shopify aplication password '
   SHOPIFY_STORE = 'Name of shop'
   OPENAI_API_KEY = 'OpenAi api key'
   COLLECTION_ID = "Collection id in shopify"
6. Ejecuta la aplicación:
   
    ```
   python app.py
## Uso

- La aplicación primero se conecta a tu tienda Shopify utilizando la API y extrae todos los productos disponibles.
- Los datos de cada producto son enviados a la API de ChatGPT para generar títulos y descripciones optimizados.
- Una vez que ChatGPT devuelve los resultados, la app actualiza los productos en tu tienda a través de la API de Shopify.

### Contribución

Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request para mejorar el proyecto.
