import re

from selectolax.parser import HTMLParser

from cliente import nova_sessao
from .parser_util import nao_encontrado

URL = "https://ww1.receita.fazenda.df.gov.br/aplicacoes/Cadastro/consultaContribuinte.aspx"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        pagina = session.get(URL, timeout=20)
        parser = HTMLParser(pagina.text)
        dados = {}
        for campo in parser.css("input"):
            nome = campo.attributes.get("name")
            if nome:
                dados[nome] = campo.attributes.get("value", "")

        campo_cnpj = None
        for campo in parser.css("input"):
            nome = (campo.attributes.get("name") or "")
            ident = (campo.attributes.get("id") or "")
            if "cnpj" in nome.lower() or "cnpj" in ident.lower():
                campo_cnpj = campo
                break

        if campo_cnpj and campo_cnpj.attributes.get("name"):
            dados[campo_cnpj.attributes["name"]] = cnpj
        else:
            dados["txtCNPJ"] = cnpj

        botao = parser.css_first("input[type=submit], input[type=button]")
        if botao and botao.attributes.get("name"):
            dados[botao.attributes["name"]] = botao.attributes.get("value", "Consultar")

        resposta = session.post(URL, data=dados, timeout=20)
        if resposta.status_code >= 400:
            return {"erro": f"Portal retornou HTTP {resposta.status_code}"}

        parser = HTMLParser(resposta.text)
        texto = parser.body.text(strip=True) if parser.body else resposta.text

        if nao_encontrado(texto):
            return {"erro": "Contribuinte não encontrado"}

        match = re.search(
            r"(?:Inscri[cç][aã]o\s*Estadual|CF/DF)\s*:?\s*(\d[\d./-]*)",
            texto,
            re.I,
        )
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
