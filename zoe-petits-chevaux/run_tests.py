import os
import subprocess

if __name__ == "__main__":
    # Définit PYTHONPATH à la racine du projet et exécute le test
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    subprocess.run(["python3", "-m", "tests.test_findepartie"], env=env)
