import requests
import os
import sys
import shutil

def check_for_updates():
    """
    Checks for updates on GitHub and installs the latest release if available.
    """
    repo_owner = "alext973"         # Replace with the GitHub username or organization
    repo_name = "CSVConverter"      # Replace with the repository name
    current_version = "1.0.0"       # Replace with the current version of your program

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release["tag_name"]

        if latest_version != current_version:
            print(f"New version available: {latest_version}. Updating...")
            download_url = latest_release["assets"][0]["browser_download_url"]
            exe_path = os.path.join(os.getcwd(), "main.exe")

            # Download the new main.exe
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(exe_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            print("Update installed successfully. Please restart the program.")
            sys.exit(0)
        else:
            print("You are using the latest version.")

    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
    except KeyError:
        print("Unexpected response structure from GitHub API.")
    except Exception as e:
        print(f"An error occurred: {e}")