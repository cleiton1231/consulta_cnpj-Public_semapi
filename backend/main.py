import sys

from consulta import buscar_inscricao_estadual

def main():
    cnpj = sys.argv[1] if len(sys.argv) > 1 else input("Digite o CNPJ: ")
    uf = sys.argv[2] if len(sys.argv) > 2 else "CE"

    resultado = buscar_inscricao_estadual(cnpj, uf)

    if "erro" in resultado:
        print("Erro:", resultado["erro"])
        return

    print(f"Inscrição Estadual ({uf}):", resultado["inscricao_estadual"])

if __name__ == "__main__":
    main()
