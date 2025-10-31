from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import os
import time
from datetime import datetime
import ollama

app = FastAPI()

LLM_MODEL = os.getenv("LLM_MODEL_NAME", "mistral")
LOG_DIR = os.getenv("LOG_DIR", os.path.join("LOGS", "SERVER_OLLAMA"))
os.makedirs(LOG_DIR, exist_ok=True)

class Query(BaseModel):
    prompt: str

print(f"[SERV-OLLAMA] Modèle chargé: {LLM_MODEL}")

def log_request_txt(prompt: str, answer: str, exec_time: float, mode: str):
    """Log la requête dans un fichier texte."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(LOG_DIR, f"log_{timestamp}_{mode}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Mode : {mode}\n")
        f.write(f"Time : {timestamp}\n")
        f.write(f"Durée de la requete : {exec_time:.2f} sec\n")
        f.write(f"LLM Model : {LLM_MODEL}\n")
        f.write("\nPrompt :\n")
        f.write(prompt.strip() + "\n\n")
        f.write("Réponse :\n")
        f.write(answer.strip() + "\n")

def stream_ollama_response(prompt: str, model: str):
    """
    Fonction générateur qui appelle Ollama en mode stream et renvoie chaque fragment.
    Enregistre la réponse complète et le temps d'exécution à la fin.
    """
    t0 = time.time()
    full_response = ""
    
    try:
        stream = ollama.generate(
            model=model,
            prompt=prompt,
            stream=True
        )
        
        for chunk in stream:
            content = chunk.get('response', '')
            full_response += content
            yield content

    except ollama.RequestError as e:
        yield f"\n[Erreur Ollama]: {e}\n"
        full_response += f"\n[Erreur Ollama]: {e}\n"
    except Exception as e:
        yield f"\n[Erreur inattendue]: {e}\n"
        full_response += f"\n[Erreur inattendue]: {e}\n"
        
    exec_time = time.time() - t0
    print(f"[TIME-STREAM] Requête traitée en {exec_time:.2f} sec (Stream mode)")
    log_request_txt(prompt, full_response, exec_time, "STREAM")


@app.post("/stream_query")
def ask_stream(query: Query):
    """Génère une réponse en streaming (caractère par caractère)."""
    
    return StreamingResponse(
        stream_ollama_response(query.prompt, LLM_MODEL), 
        media_type="text/plain" 
    )


@app.post("/query")
def ask_blocking(query: Query):
    """Génère une réponse bloquante (réponse complète d'un coup)."""
    t0 = time.time()
    user_prompt = query.prompt

    try:
        response = ollama.generate(
            model=LLM_MODEL,
            prompt=user_prompt,
            stream=False 
        )
        
        answer = response.get('response', 'Erreur : Aucune réponse du modèle.')

    except ollama.RequestError as e:
        answer = f"Erreur de l'API Ollama: {e}"
        return JSONResponse(status_code=503, content={"answer": answer, "execution_time_sec": 0.0})
    except Exception as e:
        answer = f"Erreur inattendue: {e}"
        return JSONResponse(status_code=500, content={"answer": answer, "execution_time_sec": 0.0})

    exec_time = time.time() - t0
    print(f"[TIME-BLOCK] Requête traitée en {exec_time:.2f} sec (Blocking mode)")

    log_request_txt(user_prompt, answer, exec_time, "BLOCK")
    
    return {"answer": answer, "execution_time_sec": round(exec_time, 2)}