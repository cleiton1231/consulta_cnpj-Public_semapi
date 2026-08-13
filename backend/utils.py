import re

def limpar_cnpj(cnpj):
    return re.sub(r"[.\-\/\s]", "", cnpj)
