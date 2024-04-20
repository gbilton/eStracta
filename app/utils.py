from typing import Optional
from pycpfcnpj import cpfcnpj

from app.exceptions import InvalidParameters


def validate_parameters(
    cnpj: str,
    cnae: str,
    nome_razao: Optional[str],
    nome_fantasia: Optional[str],
) -> None:
    if not validate_cnpj(cnpj=cnpj):
        raise InvalidParameters("Invalid CNPJ")
    if not validate_cnae(cnae=cnae):
        raise InvalidParameters("Invalid CNAE")


def validate_cnpj(cnpj):
    return cpfcnpj.validate(cnpj)


def validate_cnae(cnae):
    if count_digits(input_string=cnae) != 7:
        return False
    return True


def count_digits(input_string):
    count = 0
    for char in input_string:
        if char.isdigit():
            count += 1
    return count
