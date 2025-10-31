import argparse
import uvicorn
import os

def main():
    parser = argparse.ArgumentParser(description="Lancement du serveur Ollama LLM.")
    parser.add_argument("--model", type=str, default="mistral", help="Nom du modèle LLM Ollama à utiliser (ex: llama3, mistral).")
    parser.add_argument("--port", type=int, default=8000, help="Port d'écoute du serveur.")
    args = parser.parse_args()

    host = "127.0.0.1"
    port = args.port
    model_name = args.model

    # On utilise une variable d'environnement pour passer le nom du modèle au serveur
    os.environ["LLM_MODEL_NAME"] = str(model_name)

    print(f"🚀 [SERVER] START {host}:{port}")
    print(f"[SERVER] Modèle Ollama utilisé : {model_name}")
    
    # Lance l'application définie dans server.py
    uvicorn.run("serveur:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()