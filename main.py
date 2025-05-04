from app import start_app
from updater import check_for_updates

if __name__ == "__main__":
    check_for_updates()  # Check for updates when the program starts
    start_app()