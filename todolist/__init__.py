from todolist.config.inject import configure_inject
from todolist.interfaces.fastapi import app as web_app

configure_inject()


if __name__ == "__main__":
    print(f"Todolist available interfaces: {[web_app.title]}")
