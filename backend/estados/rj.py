import re

URL = "https://sucief-sincad-web.fazenda.rj.gov.br/sincad-web/index.jsf"


def buscar_inscricao_estadual(cnpj):
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, timeout=30000)
            page.wait_for_timeout(2000)

            if page.locator("iframe").count():
                browser.close()
                return {"erro": "Portal exige autenticação ou captcha"}

            campos = page.locator("input[type=text]")
            if campos.count() == 0:
                browser.close()
                return {"erro": "Formulário de consulta não encontrado"}

            for i in range(campos.count()):
                campo = campos.nth(i)
                nome = (campo.get_attribute("name") or "").lower()
                ident = (campo.get_attribute("id") or "").lower()
                if "cnpj" in nome or "cnpj" in ident:
                    campo.fill(cnpj)
                    break
            else:
                campos.first.fill(cnpj)

            botao = page.locator(
                "input[type=submit], button[type=submit], input[value*=Consultar i], button:has-text('Consultar')"
            )
            if botao.count():
                botao.first.click()
                page.wait_for_timeout(5000)

            texto = page.inner_text("body")
            browser.close()

        if "captcha" in texto.lower() or "recaptcha" in texto.lower():
            return {"erro": "Portal exige captcha"}

        if any(x in texto.lower() for x in ("não encontr", "nao encontr", "não localiz", "nao localiz")):
            return {"erro": "Contribuinte não encontrado"}

        match = re.search(r"Inscri[cç][aã]o\s*Estadual\s*:?\s*(\d[\d./-]*)", texto, re.I)
        if match:
            ie = re.sub(r"\D", "", match.group(1))
            if ie:
                return {"inscricao_estadual": ie}

        return {"erro": "Inscrição estadual não encontrada na resposta"}
    except ModuleNotFoundError:
        return {"erro": "Playwright não instalado (necessário para consultar RJ)"}
    except Exception as e:
        return {"erro": f"Erro ao processar: {str(e)}"}
