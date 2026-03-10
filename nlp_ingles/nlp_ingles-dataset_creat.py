import pandas as pd
import spacy
from spacy.tokens import DocBin
import os
from tqdm import tqdm

ruta_csv_unico = os.path.join('Ingles_dataset', 'dataset_ingles.csv')
carpeta_base = 'nlp_ingles'
carpeta_train = os.path.join(carpeta_base, 'train_corpus')

os.makedirs(carpeta_train, exist_ok=True)

nlp = spacy.blank("en")

def guardar_a_spacy(df_subset, ruta_salida, desc, leave_pbar=True):
    db = DocBin()
    
    for text, label in tqdm(zip(df_subset['text'], df_subset['label']), 
                            total=len(df_subset), desc=desc, leave=leave_pbar):
        doc = nlp.make_doc(str(text))
        if int(label) == 1:
            doc.cats = {"TOXICO": 1.0, "NO_TOXICO": 0.0}
        else:
            doc.cats = {"TOXICO": 0.0, "NO_TOXICO": 1.0}
        db.add(doc)
    
    db.to_disk(ruta_salida)

try:
    df = pd.read_csv(ruta_csv_unico).dropna(subset=['text'])
    
    df_dev = df.iloc[:8000]
    df_train_total = df.iloc[8000:]

    ruta_dev = os.path.join(carpeta_base, "dev_en.spacy")
    guardar_a_spacy(df_dev, ruta_dev, "Guardando dev_en.spacy")
    print(f"--> Guardado: {ruta_dev} ({len(df_dev)} textos)\n")

    tamano_lote = 20000
    rango_lotes = range(0, len(df_train_total), tamano_lote)
    
    for i in tqdm(rango_lotes, desc="Progreso total de lotes"):
        lote = df_train_total.iloc[i : i + tamano_lote]
        num_lote = (i // tamano_lote) + 1
        
        nombre_lote = f"train_part_{num_lote}_en.spacy"
        ruta_lote = os.path.join(carpeta_train, nombre_lote)
        
        guardar_a_spacy(lote, ruta_lote, f"Procesando {nombre_lote}", leave_pbar=False)


except Exception as e:
    print(f"ERROR: {e}")