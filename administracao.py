from dataclasses import dataclass


@dataclass
class Administracao:
    nome: str
    cpf: str
    telefone: str
    login: str
    senha: str
    tipo: str
    ativo: int