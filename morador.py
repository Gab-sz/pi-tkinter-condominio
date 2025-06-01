from dataclasses import dataclass

@dataclass
class Morador:
    nome: str
    telefone: str
    cpf: str
    bloco: str
    apartamento: str
    ativo: int