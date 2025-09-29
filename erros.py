
class ErroWLAN(Exception):
    def __init__(self, mensage: str = "Erro inesperado interno, verifique o estado do microcontrolador e o firmware"):
        self.erroMensage = mensage

    def pin_error(self) -> bool:
        print(self.erroMensage)
        return False
//>>>>

class ConnectionError(Exception):
    def __init__(self, mensage: str = "senha incorreta") -> None:
        self.erroMensage = mensage

    def password_error(self) -> bool:
        print(self.erroMensage)
        return False


class UnexpectedError(Exception):
    def __init__(self) -> None:
        self.erroMensage = "Erro inesperado"

    def error(self) -> bool:
        print(self.erroMensage)
        return False
