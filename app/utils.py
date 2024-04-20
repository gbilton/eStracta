import re
from typing import Optional
from pycpfcnpj import cpfcnpj

from app.exceptions import InvalidParameters


def validate_parameters(
    cnpj: Optional[str] = None,
    cnae: Optional[str] = None,
    nome_razao: Optional[str] = None,
    nome_fantasia: Optional[str] = None,
) -> None:

    if cnpj:
        valid_cnpj = validate_cnpj(cnpj=cnpj)
        if not valid_cnpj:
            raise InvalidParameters("Invalid CNPJ")
    if cnae:
        valid_cnae = validate_cnae(cnae=cnae)
        if not valid_cnae:
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


def extract_digits(s: str) -> str:
    return "".join(re.findall(r"\d", s))


def format_cnpj(cnpj: str) -> str:
    digits = extract_digits(cnpj)
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"


def format_cnae(cnae: str) -> str:
    digits = extract_digits(cnae)
    return f"{digits[:4]}-{digits[4]}/{digits[5:]}"
