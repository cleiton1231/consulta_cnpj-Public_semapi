from . import ac, am, ba, ce, df, mt, ro, rr, rj, sc
from .sintegra import criar_consulta_sintegra

_SINTEGRA_URLS = {
    "AL": "https://www.sefaz.al.gov.br/sintegra/",
    "AP": "https://sintegra.sefaz.ap.gov.br/sintegra/",
    "ES": "https://sintegr.es.gov.br/sintegra/",
    "MA": "https://sintegra.sefaz.ma.gov.br/sintegra/",
    "MS": "https://www.sefaz.ms.gov.br/sintegra/",
    "PA": "https://www.sefa.pa.gov.br/sintegra/",
    "PB": "https://www.receita.pb.gov.br/sintegra/",
    "PE": "https://servicos.sefaz.pe.gov.br/sintegra/",
    "PI": "https://webas.sefaz.pi.gov.br/sintegra/",
    "RN": "https://uvt.set.rn.gov.br/sintegra/",
    "SE": "https://www.sefaz.se.gov.br/sintegra/",
    "TO": "https://internet.sefaz.to.gov.br/sintegra/",
}

CONSULTAS = {
    **{uf: criar_consulta_sintegra(url) for uf, url in _SINTEGRA_URLS.items()},
    "AC": ac.buscar_inscricao_estadual,
    "AM": am.buscar_inscricao_estadual,
    "BA": ba.buscar_inscricao_estadual,
    "CE": ce.buscar_inscricao_estadual,
    "DF": df.buscar_inscricao_estadual,
    "MT": mt.buscar_inscricao_estadual,
    "RO": ro.buscar_inscricao_estadual,
    "RR": rr.buscar_inscricao_estadual,
    "RJ": rj.buscar_inscricao_estadual,
    "SC": sc.buscar_inscricao_estadual,
}
