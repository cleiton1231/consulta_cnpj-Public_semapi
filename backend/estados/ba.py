import re

from selectolax.parser import HTMLParser

from cliente import nova_sessao


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        session.get(
            "https://portal.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp",
            timeout=15,
        )
        response = session.post(
            "https://portal.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/result.asp",
            data={"sefp": "1", "estado": "BA", "CGC": cnpj, "B1": "CNPJ  ->"},
            timeout=15,
        )
        parser = HTMLParser(response.text)
        texto = parser.body.text(strip=True) if parser.body else response.text

        if "nenhum registro encontrado" in texto.lower():
            return {"erro": "Contribuinte não encontrado"}

        for linha in parser.css("tr"):
            colunas = [c.text(strip=True) for c in linha.css("td")]
            if len(colunas) >= 2 and "inscri" in colunas[0].lower():
                ie = re.sub(r"\D", "", colunas[1])
                if ie:
                    return {"inscricao_estadual": ie}

        match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
