import re

URL = "https://sat.sef.sc.gov.br/tax.NET/Sat.Cadastro.Web/ComprovanteIE/Consulta.aspx"


def buscar_inscricao_estadual(cnpj):
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, timeout=30000)
            page.locator("a.select2-choice").click()
            page.locator(".select2-results li").filter(has_text="CNPJ").click()
            page.locator("#Body_Main_Main_sepBusca_idnContribuinte_MaskedField").fill(cnpj)
            page.locator("#Body_Main_Main_sepBusca_btnBuscar").click()
            page.wait_for_timeout(6000)
            texto = page.inner_text("body")
            browser.close()

        if any(x in texto.lower() for x in ("não encontr", "nao encontr", "não localiz", "nao localiz")):
            return {"erro": "Contribuinte não encontrado"}

        match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except ModuleNotFoundError:
        return {"erro": "Playwright não instalado (necessário para consultar SC)"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
