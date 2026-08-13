from selectolax.parser import HTMLParser

from cliente import nova_sessao

URL = "https://portalapp.sefaz.rr.gov.br/siate/servlet/wp_siate_consultasintegra"


def buscar_inscricao_estadual(cnpj):
    try:
        session = nova_sessao()
        pagina = session.get(URL, timeout=15)
        parser = HTMLParser(pagina.text)
        dados = {
            campo.attributes.get("name"): campo.attributes.get("value", "")
            for campo in parser.css("input")
            if campo.attributes.get("name")
        }
        dados.update(
            {
                "vDMNTIPODOCUMENTOCONTRIBUINTE": "3",
                "vDOCUMENTO": cnpj,
                "BTNCONSULTAR": "Consultar",
            }
        )
        resposta = session.post(URL, data=dados, timeout=15)
        parser = HTMLParser(resposta.text)
        ie = parser.css_first("#span_CTLCONINSEST")
        if ie:
            valor = ie.text(strip=True)
            if valor:
                return {"inscricao_estadual": valor}
        return {"erro": "Contribuinte não encontrado"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
