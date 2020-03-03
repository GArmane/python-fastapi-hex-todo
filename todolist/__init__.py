from todolist.interfaces.server.fastapi import app as web_server


if __name__ == "__main__":
    print(f"Todolist available interfaces: {[web_server.title]}")
