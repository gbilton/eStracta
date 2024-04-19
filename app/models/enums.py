from enum import Enum


class SortOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class CompanySortField(Enum):
    ID = "id"
    CNPJ = "cnpj"
    NOME_RAZAO = "nome_razao"
    NOME_FANTASIA = "nome_fantasia"
    CNAE = "cnae"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
