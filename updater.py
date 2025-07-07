# Created by: Riccardo Fiocco
# Date: 07/07/2025 (dd/mm/yyyy)
# Description: This script checks for changes in a local repository (cloned using git) and commits them on github.

# -- Imports

import subprocess
import sys
import os

# -- Constants

REPO_DIR = "."             # -- Folder where the git repository is located
BRANCH = "main"            # -- Change to your branch name if needed
COMMIT_MESSAGE = "Backup automatico aggiornamenti" # -- Commit message for the backup

def run_git_command(command, cwd=REPO_DIR): # -- Function to run git commands

    result = subprocess.run(

        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True

    )

    return result.stdout.strip(), result.stderr.strip()

def check_changes(): # -- Function to check if there are any changes in the repository

    stdout, _ = run_git_command(["git", "status", "--porcelain"])
    return bool(stdout)

def commit_and_push(): # -- Function to commit and push changes to the repository

    print("[INFO] Aggiungo tutte le modifiche...")
    run_git_command(["git", "add", "."])

    print("[INFO] Creo commit...")
    stdout, stderr = run_git_command(["git", "commit", "-m", COMMIT_MESSAGE])

    if "nothing to commit" in stdout.lower():

        print("[INFO] Nessuna modifica da committare.")
        return

    print("[INFO] Eseguo push...")
    stdout, stderr = run_git_command(["git", "push", "origin", BRANCH])

    if stderr:

        print("[ERRORE PUSH]", stderr)

    else:

        print("[SUCCESSO PUSH]", stdout)

def main(): # -- Main function to execute the script
     
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):

        print("[ERRORE] La cartella non è una repository git.")
        sys.exit(1)

    if check_changes():

        print("[INFO] Sono state rilevate modifiche.")
        commit_and_push()

    else:

        print("[INFO] Nessuna modifica da sincronizzare.")

# -- Entry point of the script

if __name__ == "__main__":
    main()

# -- End of the script