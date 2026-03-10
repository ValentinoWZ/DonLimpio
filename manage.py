from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from pydantic import BaseModel
import time

app = FastAPI()
db_usuarios = []

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prueba(BaseModel):
    texto: str

diccionario = {
    "LABEL_0": "MU BUENO MU BUENO",
    "LABEL_1": "MU MALO MU MALO"
}

inicio_py = time.perf_counter()

from pysentimiento import create_analyzer
pysentimiento = create_analyzer(task="sentiment", lang="es")

fin_py = time.perf_counter()


inicio_det = time.perf_counter()

from detoxify import Detoxify
detoxify = Detoxify('multilingual')

fin_det = time.perf_counter()

inicio_nlp = time.perf_counter()

import spacy
nlp = spacy.load("nlp_español/output_es/model-best")

fin_nlp = time.perf_counter()

inicio_text = time.perf_counter()

textdetox= pipeline("text-classification", model="textdetox/xlmr-large-toxicity-classifier-v2")

fin_text = time.perf_counter()


tiempo_total_py = fin_py - inicio_py
tiempo_total_det = fin_det - inicio_det
tiempo_total_nlp = fin_nlp - inicio_nlp
tiempo_total_text = fin_text - inicio_text

@app.post("/filtro")
def filtrado(frase: Prueba):

    result_py = pysentimiento.predict(frase.texto)
    result_det = detoxify.predict(frase.texto)
    result_detox= textdetox(frase.texto)
    result_nlp = nlp(frase.texto)

    scores_py_limpios = {label: float(prob) for label, prob in result_py.probas.items()}
    scores_det_limpios = {k: float(v) for k, v in result_det.items()}

    data_response = {
        "tiempos_carga": {
            "pysentimiento": f"{tiempo_total_py:.4f} segundos",
            "detoxify": f"{tiempo_total_det:.4f} segundos",
            "textdetox": f"{tiempo_total_text:.4f} segundos",
            "nlp_español": f"{tiempo_total_nlp:.4f} segundos"
        },
        "resultados": {
            "pysentimiento": {
                "label": result_py.output,
                "scores": scores_py_limpios
            },
            "detoxify": {
                "toxicity_score": scores_det_limpios
            },
            "textdetox": {
                "label": diccionario[result_detox[0]["label"]],
                "score": result_detox[0]["score"]
            },
            "nlp_español": {
                'toxico': result_nlp.cats['TOXICO'],
                'no_toxico': result_nlp.cats['NO_TOXICO']
            },
        }
    }

    return  data_response