import re

from selectolax.parser import HTMLParser

from cliente import nova_sessao
from .parser_util import nao_encontrado

URL = "https://www.sefaz.mt.gov.br/cadastro/emissao/consultaContribuinte/consultaContribuinte.xhtml"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        pagina = session.get(URL, timeout=20)
        if pagina.status_code != 200 or not pagina.text.strip():
            return {"erro": "Portal indisponível"}

        parser = HTMLParser(pagina.text)
        dados = {}
        for campo in parser.css("input"):
            nome = campo.attributes.get("name")
            if nome:
                dados[nome] = campo.attributes.get("value", "")

        for chave in list(dados.keys()):
            if "cnpj" in chave.lower():
                dados[chave] = cnpj
                break
        else:
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
