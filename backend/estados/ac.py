import re

from selectolax.parser import HTMLParser

from cliente import nova_sessao
from .parser_util import nao_encontrado

URL = "http://sefaznet.ac.gov.br/sefaz/servlet/hwsconsultacadastro"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        response = session.get(URL, params={"CNPJ": cnpj}, timeout=20)
        parser = HTMLParser(response.text)
        texto = parser.body.text(strip=True) if parser.body else response.text

        if nao_encontrado(texto):
            return {"erro": "Contribuinte não encontrado"}

        match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        for linha in parser.css("tr"):
            colunas = [c.text(strip=True) for c in linha.css("td, th")]
            for i, coluna in enumerate(colunas):
                if re.search(r"inscri[cç][aã]o\s*estadual", coluna, re.I) and i + 1 < len(colunas):
                    ie = re.sub(r"\D", "", colunas[i + 1])
                    if ie:
                        return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
