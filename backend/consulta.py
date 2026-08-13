from estados import CONSULTAS
from utils import limpar_cnpj


def buscar_inscricao_estadual(cnpj, uf="CE"):
    uf = uf.strip().upper()
    consulta = CONSULTAS.get(uf)
    if not consulta:
        return {"erro": f"UF não suportada: {uf}"}
    return consulta(limpar_cnpj(cnpj))
