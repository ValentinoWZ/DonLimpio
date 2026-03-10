import pandas as pd
import spacy
from spacy.tokens import DocBin
import os
from tqdm import tqdm

ruta_train_csv = os.path.join('Chino_dataset', 'dataset_unificado_chino.csv')
ruta_train_spacy = os.path.join('nlp_chino', 'train_zh.spacy' )

ruta_dev_csv = os.path.join('Dev_dataset', 'chino_dev_procesado.csv')
ruta_dev_spacy = os.path.join('nlp_chino', 'dev_zh.spacy' )

nlp = spacy.blank("zh")

def procesar_csv_a_spacy(ruta_entrada, ruta_salida):
    if not os.path.exists(ruta_entrada):
        print(f"ERROR: No se encontró el archivo: {ruta_entrada}")
        return

    print(f"Leyendo {ruta_entrada}...\n")
    try:
        df = pd.read_csv(ruta_entrada)
        
        df = df.dropna(subset=['text'])
        df['label'] = df['label'].astype(int)
        total_filas = len(df)

        db = DocBin()
        contador = 0
        iterator = tqdm(zip(df['text'], df['label']), total=total_filas, desc="Procesando", unit="docs")
        
        for text, label in iterator:
            text_str = str(text)
            
            doc = nlp.make_doc(text_str)
            
            if label == 1:
                doc.cats = {"TOXICO": 1.0, "NO_TOXICO": 0.0}
            else:
                doc.cats = {"TOXICO": 0.0, "NO_TOXICO": 1.0}
            
            db.add(doc)
            contador += 1
            
        db.to_disk(ruta_salida)
        print(f"\n--> ¡ÉXITO! Guardado {ruta_salida} con {contador} documentos.\n")
        
    except Exception as e:
        print(f"Error procesando el archivo: {e}")

print("--- Generando train_zh.spacy ---")
procesar_csv_a_spacy(ruta_train_csv, ruta_train_spacy)

print("--- Generando dev_zh.spacy ---")
procesar_csv_a_spacy(ruta_dev_csv, ruta_dev_spacy)