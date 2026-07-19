from decouple import RepositoryEnv, Config

from app.models import Constants


def get_message_from_key(key: str):
    """
        this function gets the message string for a key in messages.properties file
        :return: str
    """
    try:
        config_path = Constants.MESSAGE_FILE_PATH
        config = Config(RepositoryEnv(config_path))
        message_string = config.get(key, cast=str)
        return message_string
    except Exception as e:
        print("Error while getting message value ", e)


def get_value_from_key(key: str):
    """
        this function gets the value for a key from 'application.properties' file
        :return: str
    """
    try:
        config_path = Constants.PROPERTIES_FILE_PATH
        config = Config(RepositoryEnv(config_path))
        value = config.get(key, cast=str)
        return value
    except Exception as e:
        print("Error while getting key value", e)
