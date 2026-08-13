# Consulta Inscrição Estadual (scraping puro, sem API)

Consulta a Inscrição Estadual (IE) de um CNPJ diretamente nos portais públicos das SEFAZ, sem depender de API externa.

## Stack otimizada

- **curl_cffi** — impersona o TLS fingerprint do Chrome, burla WAF/Cloudflare que o `requests` comum não passa.
- **selectolax** — parser HTML via seletores CSS, muito mais rápido que BeautifulSoup.
- **playwright** — só para UFs com portal em JS (RJ, SC); import lazy.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py 07206816000115 CE
```

- `CNPJ` obrigatório (com ou sem pontuação)
- `UF` opcional — default `CE`

## Cobertura (22 UFs)

| Grupo | UFs |
|-------|-----|
| Sintegra clássico (factory) | AL, AP, ES, MA, MS, PA, PB, PE, PI, RN, SE, TO |
| HTTP específico | AC, AM, BA, CE, DF, MT, RO, RR |
| Playwright (JS) | RJ, SC |

GO, MG, PR, RS e SP não têm scraper próprio (portais com WAF/captcha obrigatório).

## Estrutura

```
backend/
├── main.py          # entrada (CLI)
├── consulta.py      # orquestra por UF
├── http.py          # sessão curl_cffi (impersonate chrome)
├── utils.py         # limpar_cnpj
└── estados/
    ├── __init__.py  # registry CONSULTAS {UF: função}
    ├── parser_util.py  # helpers de extração (regex + tabela)
    ├── sintegra.py  # factory dos portais Sintegra clássicos
    ├── ac.py, am.py, ba.py, ce.py, df.py, mt.py,
    ├── ro.py, rr.py, rj.py, sc.py
```

## Limitações

- Portais estaduais mudam URL/layout e bloqueiam scraping com frequência — cada UF retorna erro tratado.
- GO, MG, PR, RS e SP exigem captcha/login e ficam fora do escopo de scraping puro.
- RJ/SC exigem `playwright install chromium`.
