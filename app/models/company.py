from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Company:
    cnpj: str
    nome_razao: str
    nome_fantasia: str
    cnae: str
    id: UUID = field(default_factory=uuid4)
