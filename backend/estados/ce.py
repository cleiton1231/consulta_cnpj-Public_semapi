from selectolax.parser import HTMLParser

from cliente import nova_sessao

URL = "https://consultapublica.sefaz.ce.gov.br/sintegra/consultar"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        response = session.get(
            URL,
            params={"tipdocumento": "2", "numcnpjcgf": cnpj},
            timeout=15,
        )
        response.raise_for_status()

        if "Nenhum contribuinte" in response.text:
            return {"erro": "Nenhum contribuinte encontrado para o CNPJ informado"}

        parser = HTMLParser(response.text)
        tabela = parser.css_first("#dadossintegraresp") or parser.css_first("#dadossintegra")
        if not tabela:
            return {"erro": "Tabela de resultados não encontrada (possível bloqueio por CAPTCHA)"}

        linha = tabela.css_first("tbody tr")
        if not linha:
            return {"erro": "Linha de dados não encontrada"}

        colunas = linha.css("td")
        if len(colunas) >= 3:
            return {"inscricao_estadual": colunas[1].text(strip=True)}
        return {"erro": "Colunas de dados não encontradas"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
