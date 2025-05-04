from app import start_app
from updater import check_for_updates

if __name__ == "__main__":
    check_for_updates()
    start_app()