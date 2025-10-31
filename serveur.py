from fastapi import FastAPI
from pydantic import BaseModel
import os
import time
from datetime import datetime
import ollama

app = FastAPI()

# === Récupération du modèle à partir des variables d'environnement ===
LLM_MODEL = os.getenv("LLM_MODEL_NAME", "ollama3.1:8b") # Par défaut si non défini

class Query(BaseModel):
    prompt: str

# === Répertoires de logs (simplifiés) ===
root_log = "LOGS"
dir_log = "SERVER_OLLAMA"
log_dir = os.path.join(root_log, dir_log)
os.makedirs(log_dir, exist_ok=True)

print(f"[SERV-OLLAMA] Modèle chargé: {LLM_MODEL}")

# --- Fonction de logging simplifiée ---
def log_request_txt(prompt: str, answer: str, exec_time: float):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(log_dir, f"log_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Time : {timestamp}\n")
        f.write(f"Durée de la requete : {exec_time:.2f} sec\n")
        f.write(f"LLM Model : {LLM_MODEL}\n")
        f.write("\nPrompt :\n")
        f.write(prompt.strip() + "\n\n")
        f.write("Réponse :\n")
        f.write(answer.strip() + "\n")

# === Endpoint FastAPI (Appel direct à Ollama) ===
@app.post("/query")
def ask(query: Query):
    t0 = time.time()
    
    user_prompt = query.prompt

    try:
        # Appel direct au modèle Ollama pour la génération
        response = ollama.generate(
            model=LLM_MODEL,
            prompt=user_prompt,
            stream=False # Récupère la réponse complète d'un coup
        )
        
        # Le texte généré se trouve dans la clé 'response'
        answer = response.get('response', 'Erreur : Aucune réponse du modèle.')

    except ollama.RequestError as e:
        answer = f"Erreur de l'API Ollama: {e}"
        return {"answer": answer, "execution_time_sec": 0.0}, 503
    except Exception as e:
        answer = f"Erreur inattendue: {e}"
        return {"answer": answer, "execution_time_sec": 0.0}, 500

    exec_time = time.time() - t0
    print(f"[TIME] Requête traitée en {exec_time:.2f} sec")

    # Log sans les chunks RAG
    log_request_txt(user_prompt, answer, exec_time)
    
    return {"answer": answer, "execution_time_sec": round(exec_time, 2)}