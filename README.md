# DonLimpio

## Descripción

**DonLimpio** es un proyecto de procesamiento de lenguaje natural (NLP) diseñado para detectar toxicidad en textos multilingües (Español, Inglés y Chino). 

El núcleo del proyecto es una API construida con **FastAPI** que integra y compara múltiples modelos de clasificación simultáneamente: 

* Soluciones de **Hugging Face** (Transformers). 
* Librerías especializadas (Detoxify, Pysentimiento). 
* **Modelos personalizados entrenados con spaCy**.

El proyecto ofrece una arquitectura modular que permite **entrenar, validar y desplegar modelos de NLP específicos para cada idioma**, integradas en pipelines de spaCy.

## Estructura

### Descargas Previas

Debido a que los datasets y los nlps ocupan mucho no estan subidos directamente al repositorio de github, para descargarlos hay que acceder a los siguientes links:

`Chino_dataset:`https://workdrive.zohopublic.eu/external/57e5b9a5ce0aa975a4df9b29976d13cc52932e4c77c00498cff527edc8d961f5/download

`Español_dataset:`https://workdrive.zohopublic.eu/external/0b384eb9b3f73337b46129b95cb283a9b2f36ccebe77e7ee9db3e1ccc0d80ecf/download

`Ingles_dataset:`https://workdrive.zohopublic.eu/external/a0d2694b87328eec5b73ac86d8e01875896c6525b09888afc907dbe6fa6104a8/download

`output_zh:`https://workdrive.zohopublic.eu/external/3fbac00029d6924f29f671898ca56e39701ad71dfa7c9d2cb584da008a97c55d/download

`output_es:`https://workdrive.zohopublic.eu/external/a29ce9875de3408d83e58c538a5f559bc109c419795dd6e0289d0d271d18879e/download

`Test_dataset:`https://workdrive.zohopublic.eu/external/b87b050ba4a0732d2eeae87635b6eea4aef0ff8b77cc59488d4303003220eb16/download

### Estructura final

DONLIMPIO/
├── Chino_dataset/          # Datasets para el modelo nlp en Chino
├── Español_dataset/        # Datasets para el modelo nlp en Español
├── Ingles_dataset/         # Datasets para el modelo nlp en Ingles
├── nlp_chino/              # Entorno de entrenamiento para el nlp Chino 
│   ├── output_zh/          # Modelos resultantes
│   ├── config.cfg          # Configuración del pipeline
│ 	├── nlp_chino_dataset_creat.py # Script de conversión CSV -> .spacy
├── nlp_español/            # Entorno de entrenamiento para el nlp Español 
│   ├── output_es/          # Modelos resultantes para iteraciones impares
│   ├── output_es_resume/   # Modelos resultantes para iteraciones pares
│   ├── config_impares.cfg  # Configuración del pipeline para iteraciones impares
│   ├── config_pares.cfg    # Configuración del pipeline para iteraciones pares
│   ├── config.cfg          # Configuración del pipeline base
│   └── nlp_español_dataset_creat.py # Script de conversión CSV -> .spacy
├── nlp_ingles/             # Entorno de entrenamiento para el nlp Ingles
│   ├── config.cfg          # Configuración del pipeline
│   └── nlp_ingles_dataset_creat.py # Script de conversión CSV -> .spacy
├── Test_dataset/           # Datos reservados para validación final
├──	.gitignore              # Configuracion commits github 
├── manage.py               # API principal
├──	README.md               # Documentación
├── requirements_api.txt    # Dependencias para la API
├── requirements_notebook.txt # Dependencias para el notebook
├── requirements_train.txt  # Dependencias para el entrenamiento
└── spacy_results.ipynb     # Notebook de análisis de resultados
```

## Instalación

### 1. Clonar repositorio

Primero clona el repositorio en tu maquina local usando Git.

```bash
git clone https://github.com/ValentinoWZ/DonLimpio.git

cd DonLimpio
```

### 2. Configurar los entornos virtuales para Python

Este proyecto utiliza entornos virtuales separados para Windows y Linux. Ademas es necesario el uso de python en la versión **3.11.x** o superior. Sigue las instrucciones para cada sistema operativo.

#### 2.1. Instalar pyenv

##### macOS:

```bash
brew install pyenv
```
##### Windows:
```PowerShell

invoke-webrequest -useb https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1 | iex
```
##### Linux:
```bash
curl https://pyenv.run | bash
```

#### 2.2. Instalar versión especifica de python

```bash
pyenv install 3.11.14

pyenv rehash
```

#### 2.3. Crear el entorno virtual
```bash
pyenv local 3.11.14

python -m venv donLimpio
```

#### 2.4. Activar y verificar
##### Windows
```PowerShell
.\donLimpio\Scripts\activate 
python --version 
# Salida esperada: Python 3.11.14
```
##### macOS/Linux
```bash
source donLimpio/bin/activate 
python --version 
# Salida esperada: Python 3.11.14
```

## Modelos y Entrenamiento

El proyecto permite entrenar modelos propios para Español, Inglés y Chino. La configuración actual utiliza **Transformers** previamente entrenados para cada idioma específico.

### Arquitectura

Cada uno de los nlps utiliza un `config.cfg` diferente, optimizado exclusivamente para el mismo, algunos de los rasgos mas diferentes en cada uno son:

| **Idioma**  | **Modelo Base (Hugging Face)**          | **Tokenizador** |
| ----------- | --------------------------------------- | --------------- |
| **Español** | `dccuchile/bert-base-spanish-wwm-cased` | spaCy Default   |
| **Inglés**  | `roberta-base`                          | spaCy Default   |
| **Chino**   | `bert-base-chinese`                     | pkuseg/jieba    |

### Dataset

Para el entrenamiento de cada uno de los modelos se han combinado diferentes datasets públicos en internet. En este apartado dejare un registro de donde se obtuvo cada uno de los datasets. Todos ellos se descargaron en la versión disponible a día 12 de febrero de 2026.

#### Chino

`dataset_chino:`Este dataset es la combinación de varios datasets chinos adaptados al formato necesario para el entrenamiento.

Los datasets originales usados son:
*  https://github.com/thu-coai/COLDataset/blob/main/COLDataset/dev.csv 
* https://github.com/DUT-lujunyu/ToxiCN
* https://github.com/thu-coai/COLDataset/blob/main/COLDataset/train.csv 

#### Español

`dataset_español:`Este dataset es la combinación de varios datasets españoles adaptados al formato necesario para el entrenamiento.

Los datasets originales usados son:
*  https://huggingface.co/datasets/Paul/hatecheck-spanish 
* https://www.kaggle.com/datasets/lanreaves/toxic-comment-espaniol?select=final_dataset_great.csv 

#### Ingles

`dataset_ingles:`Este dataset es la combinación de varios datasets ingleses adaptados al formato necesario para el entrenamiento.

Los datasets originales usados son:
*  https://www.kaggle.com/datasets/devkhant24/toxic-comment?select=jigsaw-unintended-bias-train.csv 
*  https://huggingface.co/datasets/SetFit/toxic_conversations_50k 

#### Test_dataset

Todos los datasets para hacer pruebas se sacaron de https://huggingface.co/datasets/textdetox/multilingual_toxicity_dataset, eligiendo el idioma respectivo, a día 12 de febrero de 2026.

### Requisitos del sistema

Para el entrenamiento se requiere de librerías específicas de Deep Learning y es muy recomendable usar GPU, ya que el entrenamiento con CPU puede ser extremadamente lento.

```bash

# 1. Instalar spaCy con soporte para CUDA 12, Transformers y Jieba (para chino)
 pip install -U spacy[cuda12x] spacy-transformers jieba 
 
# 2. Instalar PyTorch 
pip install torch 

# 3. Descargar modelos base de spaCy (necesarios para los pipelines) 
python -m spacy download es_dep_news_trf 
# python -m spacy download en_core_web_trf <-- Descomentar para Inglés 
# python -m spacy download zh_core_web_trf <-- Descomentar para Chino
```

### Tratado de datos

Para el entrenamiento de los modelos es necesario pasar los datos a un formato binario (.spacy), ya que los modelos leen solo este formato.

Antes de todo descarga las dependencias necesarias.

```bash
pip install -r requirements_train.txt
```

Ahora es necesario ejecutar el script de creación del dataset en el idioma elegido. Es importante saber que el programa ya divide el datasat en entrenamiento y validación.

```bash

python nlp_español/nlp_español_dataset_creat.py
# python nlp_ingles/nlp_ingles_dataset_creat.py <-- Descomenta para Inglés
# python nlp_chino/nlp_chino_dataset_creat.py <-- Descomenta para Chino

```

**Importante:** En el caso de querer usar otro dataset se debe hacer las modificaciones pertinentes en el fichero del respectivo idioma.

### Iniciar Entrenamiento

Para iniciar el entrenamiento, una vez ya se tiene configurado todos los apartados anteriores.

```bash

# Entrenamiento español
python -m spacy train "nlp_español/config.cfg" \
--output "nlp_español/output_es" \
--paths.train "nlp_español/train_corpus" \
--paths.dev "nlp_español/dev_es.spacy" \
--gpu-id 0

# Entrenamineto ingles
python -m spacy train "nlp_ingles/config.cfg" \
--output "nlp_ingles/output_en" \
--paths.train "nlp_ingles/train_corpus" \
--paths.dev "nlp_ingles/dev_en.spacy" \
--gpu-id 0

# Entrenamineto chino
python -m spacy train "nlp_chino/config.cfg" \
--output "nlp_chino/output_zh" \
--paths.train "nlp_chino/train_zh.spacy" \
--paths.dev "nlp_chino/dev_zh.spacy" \
--gpu-id 0
```

### Evaluación

Una vez finalizado el entrenamiento, el mejor modelo se guardara en `output_X/model-best`. Y el ultimo entrenamiento en `output_X/model-last`
Para usar cualquiera de los dos en tu código, lo unico que necesitas es importarlo.

```python
import spacy

nlp = spacy.load("nlp_español/output_es/model-best")
```

### Errores y modificaciones

Durante el desarrollo y entrenamiento de estos modelos con arquitecturas pesadas y grandes volúmenes de datos, se han implementado las siguientes modificaciones y soluciones:

#### CUDA Out of Memory

Al entrenar Transformers (especialmente con lotes grandes), la memoria de la GPU (VRAM) tiende a fragmentarse y provocar errores de "Out of Memory", incluso si hay memoria total disponible.

Una forma de suavizar este problema, pero **no** de resolver el problema es forzando a PyTorch a gestionar los segmentos de memoria de forma expandible.

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

#### Entrenamiento en iteraciones

La estructura base del proyecto funciona perfectamente para datasets moderados. Sin embargo, el tamaño de la base de datos de la carpeta `Español_dataset` es demasiado grande para ser procesado y cargado en memoria en una sola ejecución sin colapsar el sistema.

Para lograr que el modelo de español se entrene con toda la base de datos, se ha modificado la carpeta `nlp_español`:

- **División del Dataset:** La configuración de entrenamiento se ha dividido en tres archivos (`config.cfg`, `config_pares.cfg` y `config_impares.cfg`). Esto permite entrenar el modelo sobre trozos optimós de la base de datos.

- **Resume Training (Reentrenamiento):** El flujo consiste en entrenar primero con la configuración base de spacy (`config.cfg`) guardando el modelo en `output_es`. Posteriormente, se utiliza la técnica de _resume training_ en spaCy para continuar entrenando ese mismo modelo alternando entre las otras dos configuraciones (`config_pares.cfg` y `config_impares.cfg`) guardando en `output_es_resume`y `output_es` respectivamente consiguiendo así que el modelo"vea" toda la base de datos sin desbordar la memoria. 

Para entrenar de forma secuencial evitando que la basura acumulada en la VRAM colapse el sistema entre una parte y otra, se utiliza un script en Python que fuerza la limpieza de la memoria caché de la GPU (`torch.cuda.empty_cache()`) y el recolector de basura (`gc.collect()`).

```python
# Ejemplo de resume training 
import torch
import gc

print("Iteracion 1: \n\n")

!python -m spacy train "/content/drive/MyDrive/NLPS/nlp_español/config.cfg" \
--output "/content/drive/MyDrive/NLPS/nlp_español/output_es" \
--paths.train "/content/drive/MyDrive/NLPS/nlp_español/train_corpus/train_part_1_es.spacy" \
--paths.dev "/content/drive/MyDrive/NLPS/nlp_español/dev_es.spacy" \
--gpu-id 0

for i in range(7,10,1):

	print(f"Iteracion {i}: \n\n")
	
	torch.cuda.empty_cache()
	gc.collect()
	
	text = f"/content/drive/MyDrive/NLPS/nlp_español/train_corpus/train_part_{i}_es.spacy"
  
	if i % 2 == 0 :
	
		!python -m spacy train "/content/drive/MyDrive/NLPS/nlp_español/config_pares.cfg" \
		--output "/content/drive/MyDrive/NLPS/nlp_español/output_es_resume" \
		--paths.train {text} \
		--paths.dev "/content/drive/MyDrive/NLPS/nlp_español/dev_es.spacy" \
		--gpu-id 0

else :
	
	!python -m spacy train "/content/drive/MyDrive/NLPS/nlp_español/config_impares.cfg" \
	--output "/content/drive/MyDrive/NLPS/nlp_español/output_es" \
	--paths.train {text} \
	--paths.dev "/content/drive/MyDrive/NLPS/nlp_español/dev_es.spacy" \
	--gpu-id 0
```

## API

### Ejecución

Primero de todo hay que descargar las dependencias necesarias para este apartado.

```bash
pip install -r requirements_api.txt
```

El archivo `manage.py` es el que se ocupa de activar el servidor que recibe una frase y devuelve el análisis de cuatro modelos distintos, junto con los tiempos de carga de cada uno de ellos.

```bash
# Ejecutar el servidor (desde la raíz del proyecto)
uvicorn manage:app --reload
```

### Endpoint

**POST** `/filtro`

Recibe un texto y devuelve el score de toxicidad para 4 modelos y sus tiempos de latencia.

* **Request:**

```JSON
// Ejemplo de request
{ "texto": "Este es un ejemplo de frase a analizar" }
```

* **Response:**

Se divide en dos partes, **"tiempos de carga"** (latencia de cada modelo) y **"resultados"** (clasificación del texto para cada modelo).

```JSON
// Ejemplo de response
{
    "tiempos_carga": {
        "pysentimiento": "0.9890 segundos",
        "detoxify": "1.6024 segundos",
        "textdetox": "0.5297 segundos",
        "nlp_español": "3.3762 segundos"
    },
    "resultados": {
        "pysentimiento": {
            "label": "NEU",
            "scores": {
                "NEG": 0.21683944761753082,
                "NEU": 0.5764897465705872,
                "POS": 0.2066708505153656
            }
        },
        "detoxify": {
            "toxicity_score": {
                "toxicity": 0.007352654822170734,
                "severe_toxicity": 0.00010957282211165875,
                "obscene": 0.0006209902348928154,
                "identity_attack": 0.00023749189858790487,
                "insult": 0.0008034785860218108,
                "threat": 0.003978687338531017,
                "sexual_explicit": 0.0002261556073790416
            }
        },
        "textdetox": {
            "label": "MU BUENO MU BUENO",
            "score": 0.9988157749176025
        },
        "nlp_español": {
            "toxico": 0.14786845445632935,
            "no_toxico": 0.8521315455436707
        }
    }
}
```

## Notebook

Primero de todo hay que descargar las dependencias necesarias para este apartado.

```bash
pip install -r requirements_notebook.txt
```

Una vez tienes entrenado al mejor modelo puedes usar el notebook `spacy_results.ipynb`para generar gráficas y matrices de resultados, con el fin de observar la precisión y robustez de cada modelo. 
Al abrir el notebook se puede observar como esta divido en tres secciones, una para cada nlp, ejecuta la sección pertinente al modelo que tengas entrenado.