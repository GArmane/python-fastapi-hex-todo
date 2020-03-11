from todolist.config.environment import get_current_settings
from todolist.interfaces.fastapi.app import init_app


_SETTINGS = get_current_settings()


web_app = init_app(_SETTINGS)
