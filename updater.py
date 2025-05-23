import requests
import os
import sys
import shutil
import subprocess

def check_for_updates():
    """
    Checks for updates on GitHub and installs the latest release if available.
    """
    repo_owner = "alext973"
    repo_name = "CSVConverter"
    current_version = "1.0.555"

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release["tag_name"]

        if latest_version != current_version:
            print(f"New version available: {latest_version}. Updating...")
            download_url = latest_release["assets"][0]["browser_download_url"]
            exe_dir = os.getcwd()
            exe_path_new = os.path.join(exe_dir, "main_new.exe")

            # Download the new main.exe as main_new.exe
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(exe_path_new, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            print("Update downloaded. Starting updater...")
            # Start the updater script and exit
            updater_script = os.path.join(exe_dir, "run_updater.bat")
            subprocess.Popen([updater_script], shell=True)
            sys.exit(0)
        else:
            print("You are using the latest version.")

    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
    except KeyError:
        print("Unexpected response structure from GitHub API.")
    except Exception as e:
        print(f"An error occurred: {e}")