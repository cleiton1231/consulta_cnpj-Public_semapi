from selectolax.parser import HTMLParser

from cliente import nova_sessao
from .parser_util import contem, extrair_ie, nao_encontrado, texto_do


def criar_consulta_sintegra(base_url):
    def buscar_inscricao_estadual(cnpj):
        try:
            session = nova_sessao()
            session.get(base_url + "sintegra1.asp", timeout=15)
            response = session.post(
                base_url + "sintegra2.asp",
                data={"CNPJ": cnpj, "TIPDOC": "2"},
                timeout=15,
            )
            parser = HTMLParser(response.text)
            texto = texto_do(parser, response.text)

            if response.status_code == 404 or "not found" in texto.lower():
                return {"erro": "Portal indisponível"}
            if response.status_code == 403 or contem(
                texto, ("indispon", "503", "bloqueado", "acesso negado")
            ):
                return {"erro": "Portal indisponível ou bloqueou a consulta"}
            if nao_encontrado(texto):
                return {"erro": "Contribuinte não encontrado"}

            ie = extrair_ie(parser, response.text)
            if ie:
                return {"inscricao_estadual": ie}
            return {"erro": "Inscrição estadual não encontrada na resposta"}
        except Exception as e:
            return {"erro": f"Erro ao processar: {str(e)}"}

    return buscar_inscricao_estadual
