import re

_TERMOS_NAO_ENCONTRADO = (
    "nenhum registro",
    "nao cadastr",
    "não cadastr",
    "nao encontr",
    "não encontr",
)


def texto_do(parser, html):
    return parser.body.text(strip=True) if parser.body else html


def contem(texto, termos):
    return any(x in texto.lower() for x in termos)


def nao_encontrado(texto):
    return contem(texto, _TERMOS_NAO_ENCONTRADO)


def ie_regex_match(texto):
    match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
    if match:
        ie = re.sub(r"\D", "", match.group(1))
        return ie or None
    return None


def ie_table_match(parser):
    for linha in parser.css("tr"):
        colunas = [c.text(strip=True) for c in linha.css("td, th")]
        for i, coluna in enumerate(colunas):
            if re.search(r"inscri[cç][aã]o\s*estadual", coluna, re.I) and i + 1 < len(colunas):
                ie = re.sub(r"\D", "", colunas[i + 1])
                if ie:
                    return ie
    return None


def extrair_ie(parser, html):
    texto = texto_do(parser, html)
    return ie_regex_match(texto) or ie_table_match(parser)
