# Diagnóstico dos portais por UF (2026-08)

Investigação de burla/teste de bibliotecas alternativas sobre os 22 estados.
Testado com `07206816000115` (empresa de CE, então "sem IE" em estados onde ela não tem inscrição é esperado).

## Bibliotecas testadas

| Lib | Resultado |
|-----|-----------|
| `curl_cffi` (chrome/safari/firefox) | Impersonação de TLS — não destrava WAF/Turnstile/JS-challenge |
| `curl_cffi` com `verify=False` | Burlou SSL inválido do PA (mas PA virou SPA+Turnstile) |
| `cloudscraper` | SE voltou a responder 200 (era 415) — mas o portal devolve página de erro SharePoint |
| `tls-client` | API incompatível com a versão instalada no teste |
| `playwright` | Passou desafio Cloudflare do DF (mas DF virou SPA, exige navegação) |

**Conclusão**: nenhuma biblioteca destrava IE em estado que hoje falha. As falhas são de
infraestrutura (DNS morto, SPA+Turnstile, Cloudflare JS-challenge, WAF, erro SharePoint),
não de fingerprint TLS.

## Status por UF

| UF | Endpoint atual | Status | Burla/observação |
|----|----------------|--------|------------------|
| BA | portal.sefaz.ba.gov.br | ✅ OK | retorna IE |
| CE | consultapublica.sefaz.ce.gov.br | ✅ OK | retorna IE |
| AC | sefaznet.ac.gov.br | ✅ responde | só com IE na UF |
| RO | portalcontribuinte.sefin.ro.gov.br | ✅ responde | só com IE na UF |
| RR | portalapp.sefaz.rr.gov.br | ✅ responde | só com IE na UF |
| SC | sat.sef.sc.gov.br | ✅ responde (Playwright) | só com IE na UF |
| AM | online.sefaz.am.gov.br | 🔒 captcha | recaptcha na página |
| RJ | sucief-sincad-web.fazenda.rj.gov.br | 🔒 captcha | iframe de autenticação |
| DF | ww1.receita.fazenda.df.gov.br | 🔒 Cloudflare JS-challenge | virou SPA; Playwright passa o challenge mas exige navegação |
| PA | sefa.pa.gov.br | 🔒 SPA + Turnstile | `.asp` virou shell Angular + Cloudflare Turnstile |
| MS | sefaz.ms.gov.br | 🔒 SPA | antiga 404; consulta virou app JS |
| PE | servicos.sefaz.pe.gov.br | 🔒 WAF 403 | bloqueio por WAF |
| AL | sefaz.al.gov.br/sintegra | ❌ fora do ar | nova URL `sintegra.sefaz.al.gov.br` = 503 |
| AP | sintegra.sefaz.ap.gov.br | ❌ DNS morto | domínio não resolve |
| ES | sintegr.es.gov.br | ❌ DNS morto | domínio não resolve |
| MA | sintegra.sefaz.ma.gov.br | ❌ DNS morto | domínio não resolve |
| TO | internet.sefaz.to.gov.br | ❌ DNS morto | domínio não resolve |
| SE | sefaz.se.gov.br | ❌ SharePoint erro | virou SharePoint com página de erro |
| MT | sefaz.mt.gov.br | ❌ fora do ar | 404; homepage connection reset |
| PB | portal.receita.pb.gov.br | ❌ conexão fechada | reset na conexão |
| RN | uvt.set.rn.gov.br | ❌ timeout | servidor não responde |
| PI | webas.sefaz.pi.gov.br | ❌ 503 | aplicação indisponível (detecção correta) |

## Legenda
- ✅ retorna IE
- ⚠️ responde (retorna IE só se o CNPJ tiver inscrição naquela UF)
- 🔒 bloqueio humano/infraestrutura (captcha, WAF, Turnstile, JS-challenge, SPA) — exige Playwright + resolução de captcha, fora do escopo "sem API"
- ❌ portal morto/fora do ar (DNS, 404, 503, reset, SharePoint erro)
