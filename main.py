import subprocess

def start_backend():
    """Démarre le serveur backend Flask."""
    return subprocess.Popen(["python", "backend.py"])

def start_frontend():
    """Démarre le serveur frontend Dash."""
    return subprocess.Popen(["python", "frontend.py"])

if __name__ == "__main__":
    print("Démarrage du backend...")
    backend_process = start_backend()

    print("Démarrage du frontend...")
    frontend_process = start_frontend()

    try:
        print("Les serveurs sont en cours d'exécution. Appuyez sur Ctrl+C pour arrêter.")
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nArrêt des serveurs...")
        backend_process.terminate()
        frontend_process.terminate()