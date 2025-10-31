# LLM_serveur

## Serveur LLM Ollama avec FastAPI

Ce projet implémente un serveur Python avec FastAPI permettant d'intéragir avec un LLM exécuté localement via Ollama.

## Prérequis

- Ollama
- Un modèle de langage téléchargé via Ollama (ex: ollama pull llama3.1:8b).
- Python 3.8+

## Installation et Démarrage
### 1. Dépendances

Installez toutes les librairies Python requises :
```console
pip install -r requirements.txt
```

### 2. Démarrage du Serveur

Pour lancer le serveur, tapez la commande suivante : 
```console
python run.py --model llama3.1:8b --port 8000
```
Vous pouvez remplacer le nom du modèle par celui que vous utilisez.

Une fois démarré, le serveur sera accessible à l'adresse par défaut : http://127.0.0.1:8000.

## Types de réponse
### 1. Mode Bloquant (Réponse Complète)

Cet endpoint attend que la réponse complète du LLM soit générée avant d'envoyer la réponse JSON au client.

- URL: POST http://127.0.0.1:8000/query
- Utilisation avec curl (Linux/MAC) :
```console
curl -X POST http://127.0.0.1:8000/query \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Qu'est-ce que l'IA ?"}'
```

- Utilisation avec curl (CMD/PowerShell) :
```console
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d "{\"prompt\": \"Qu'est-ce que l'IA ?\"}"
```

La réponse sera renvoyée sous un format JSON.


### 2. Mode Streaming (Caractère par Caractère)

Cet endpoint renvoie la réponse immédiatement, caractère par caractère.

- URL: POST http://127.0.0.1:8000/stream_query
- Utilisation avec curl (Linux/MAC) :
```console
curl -X POST http://127.0.0.1:8000/stream_query \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Qu'est-ce que l'IA ?"}'
```

- Utilisation avec curl (CMD/PowerShell) :
```console
curl -X POST http://127.0.0.1:8000/stream_query -H "Content-Type: application/json" -d "{\"prompt\": \"Qu'est-ce que l'IA ?\"}"
```

La rpeonse sera affichée progressivement dans le terminal.

## Fichiers de Log

Le serveur enregistre chaque requête dans le répertoire LOGS/SERVER_OLLAMA/.

Chaque fichier de log contient le prompt, la réponse complète du LLM, le modèle utilisé, la durée d'exécution et le mode d'appel (BLOCK ou STREAM).

## Paramètres de Lancement

Vous pouvez configurer le serveur en utilisant les arguments du script run_ollama.py :

|   Argument   |   Description |   Valeur par Défaut |
|---    |:-:    |:-:    |
|   ```--model```   |   Nom du modèle LLM à utiliser par Ollama.   |   ```llama3.1:8b``` |
|   ```--port```   |   Le port sur lequel le serveur FastAPI doit écouter.   |   ```8000``` |
