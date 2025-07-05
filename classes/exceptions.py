class MissingEnvironmentVariableException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f'Missing the envvar "{name}"')


class TelegramException(Exception):
    def __init__(self) -> None:
        super().__init__("Telegram exception")

