# REQUIREMENTS VENV

TODO METTRE ÇA DANS README 

Nous avons utilisé python3.11
 ?? # TODO

### 

    brew install python@3.11

# TODO LINUX

## vérifier bien installé :
python3.11 --version



### Créer un environnement virtuel
- Vérifier si le module `venv` est disponible

    ```
    python3.11 -m venv --help
    ```

    - Si cette commande retourne une aide ou ne génère aucune erreur, `venv` est déjà installé.

    - Sinon : 

        - Sur Linux (Ubuntu):

            ```
            sudo apt update
            sudo apt install python3-venv
            ```

        - Sur Mac : Si Python a été installé via Homebrew, le module `venv`est généralement inclus. Sinon mettre à jour Python : 

            ```
            brew install python
            ```

- À la racine du projet, créer un environnement virtuel avec venv 

    ```
    python3.11 -m venv ludo_venv
    ```

- Activer l'environnement virtuel 
(sur Linux/Mac)

    ```
    source ludo_venv/bin/activate
    ```

<!-- sur windows : ludo_venv\Scripts\activate -->

- Pour éviter tout problème, mettre à jour `pip` dnas l'environnement virtuel 

    ```
    pip install --upgrade pip
    ```

### Installer les dépendances actuelles 

    ```
    pip install -r requirements_venv.txt
    ```

### Pour quitter / désactive l'environnement virtuel

    ```
    deactivate
    ```

Fichier pour vérifier que toutes les foncitonnalités ont été testées (tous les requirements venv approprié).
Ce que j'ai testé : 

- lancer les tests pytest :

    ```
    pytest game/tests_pytest/
    ```

TODO : expliquer comment faire pour mettre le venv sur les notebooks


### Lancer un notebook

Lorsque vous essayer de lancer un notebook 

sur vscode : 
- "Run All"
- "Select Another Kernel..."
- "Python Environments..."
- Sélectionner "ludo_venv"
- (ipykernel)
