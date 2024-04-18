from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Company:
    cnpj: str
    nome_razao: str
    nome_fantasia: str
    cnae: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
