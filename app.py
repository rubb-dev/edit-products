import requests
import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_PASSWORD
}

collection_id = os.getenv("COLLECTION_ID")
url_collection = f"https://{SHOPIFY_STORE}.myshopify.com/admin/collects.json?collection_id={collection_id}&limit=250"

def obtener_productos_coleccion(url):
    productos = []
    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            datos = response.json().get('collects', [])
            for dato in datos:
                if dato['product_id'] not in productos:
                    productos.append(dato['product_id'])
                else:
                    return productos
            

            link_header = response.headers.get('Link')

            if link_header:

                links = link_header.split(',')
                
                for link in links:

                    if 'rel="next"' in link:
                        
                        next_url = link[link.find("<")+1 : link.find(">")]
                        url = next_url
                        break  
            else:
                url = None   
           
        else:
            print(f"Error al recuperar productos: {response.status_code}")
            print(f"Detalles: {response.text}")
            url = None
def editar_producto(content):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Actua como experto en copywriting, neuroventas y SEO para optimizar el contenido de los productos de nuestro e-commerce [Vetonek.com]. A partir de la información proporcionada por el usuario analiza las palabras clave que más nos puede interesar posicionar y estudia como se posicionan las principales webs para estas palabras clave. Genera contenido que pueda resultar interesante para el lector y donde la descripción responda todas las posibles preguntas que puedan tener los consumidores sobre el rpodcuto e incluya todos los datos del producto proporcionados por la información. Debes generar un título para el producto, la descripción del producto, un metatítulo (60 carácteres aproximadamente, si es necesario para llegar a la longitud puedes añadir ' - Vetonek.com') y una metadescripción (entre 120 y 160 carácteres). Procura evitar el exceso de mayusculas unicamente utilizalas para la primera letra despues de punto y para nombres propios y utiliza html en la descripción para optimizar al máximo el SEO de nuesta página de producto."
                    }
                ]
            },
            {
                "role": "user",
                "content": content
            }    
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "product_info",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                    "title": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "meta_title": {
                        "type": "string"
                    },
                    "meta_description": {
                        "type": "string"
                    }
                    },
                    "additionalProperties": False,
                    "required": [
                    "title",
                    "description",
                    "meta_title",
                    "meta_description"
                    ]
                }
            }
        }     
    )
    return response.choices[0].message.content
def obtener_metafields_producto(product_id):
    url_product_meta = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/2023-10/products/{product_id}/metafields.json"
    
    response = requests.get(url_product_meta, headers=headers)

    if response.status_code == 200:
        metafields = response.json()['metafields']
        meta_title_id = None
        meta_description_id = None

        
        for metafield in metafields:
            if metafield['key'] == 'title_tag':
                meta_title_id = metafield['id']
            elif metafield['key'] == 'description_tag':
                meta_description_id = metafield['id']
        print(meta_description_id, meta_title_id)
        return meta_title_id, meta_description_id
    else:
        print(f"Error al obtener los Metafields del producto {product_id}: {response.status_code}")
        print(f"Detalles: {response.text}")
        return None, None
def actualizar_contenido_producto(product_id, content):
    url_actualizar_producto = f"https://{SHOPIFY_STORE}.myshopify.com/admin/products/{product_id}.json"
    data = {
        "product": {
            "id": product_id,
            "title": content['title'],
            "body_html": content['description']
        }
    }
    response = requests.put(url_actualizar_producto, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Título y descripción actualizado correctamente.")
    else:
        print(f"Error al actualizar título y descripción: {response.status_code}")

    url_meta = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/2023-10/metafields.json"
    
    data_meta_title = {
            "metafield": {
                "namespace": "global",
                "key": "title_tag",
                "value": content['meta_title'],
                "type": "string",
                "description": "Title of the product for search engines",
                "owner_id": product_id,
                "owner_resource": "product"
            }
        }
    response_meta_title = requests.post(url_meta, headers=headers, json=data_meta_title)

    if response_meta_title.status_code == 201:
        print(f"Metatítulo actualizado correctamente.")
    else:
        print(f"Error al actualizar el Metatítulo: {response_meta_title.status_code}, {response_meta_title.text}")

    
    data_meta_description = {
            "metafield": {
                "namespace": "global",
                "key": "description_tag",
                "value": content['meta_description'],
                "type": "string",
                "description": "Description of the product for search engines",
                "owner_id": product_id,
                "owner_resource": "product"
            }
        }
    response_meta_description = requests.post(url_meta, headers=headers, json=data_meta_description)

    if response_meta_description.status_code == 201:
        print(f"Metadescripción actualizada correctamente.")
    else:
        print(f"Error al actualizar la Metadescripción: {response_meta_description.status_code}, {response_meta_description.text}")


products = obtener_productos_coleccion(url_collection)

i=1
for product_id in products:
    url_product = f"https://{SHOPIFY_STORE}.myshopify.com/admin/products/{product_id}.json"
    product = requests.get(url_product, headers = headers)
    
    if product.status_code == 200:
        print(f"Producto: [ {i} / {len(products)} ] - {product_id}")
        #Obtenemos la información del producto
        product = product.json()
        title = product['product']['title']
        description = product['product']['body_html']
        inf_product = f"Esta es la informacióm proporcionada por el proveedor. Título [{title}], Descripción [{description}]"

        #Le pasamos la informacion a ChatGPT y devuelve el contenido
        inf_generada = json.loads(editar_producto(inf_product))

        #Le pasamos el producto y la información que tiene que ponerle
        actualizar_contenido_producto(product_id, inf_generada)

    else:
        print("Producto no encontrado")
    
    print("-"*50)
    i += 1