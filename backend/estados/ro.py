import re

from selectolax.parser import HTMLParser

from cliente import nova_sessao
from .parser_util import nao_encontrado

URL = "https://portalcontribuinte.sefin.ro.gov.br/Publico/parametropublica.jsp"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        pagina = session.get(URL, timeout=20)
        parser = HTMLParser(pagina.text)
        dados = {
            campo.attributes.get("name"): campo.attributes.get("value", "")
            for campo in parser.css("input")
            if campo.attributes.get("name")
        }
        dados["cnpj"] = cnpj
        resposta = session.post(URL, data=dados, timeout=20)
        parser = HTMLParser(resposta.text)
        texto = parser.body.text(strip=True) if parser.body else resposta.text

        if nao_encontrado(texto):
            return {"erro": "Contribuinte não encontrado"}

        match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
