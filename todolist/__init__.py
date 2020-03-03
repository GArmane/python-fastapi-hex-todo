from todolist.interfaces.fastapi import app as web_app


if __name__ == "__main__":
    print(f"Todolist available interfaces: {[web_app.title]}")
