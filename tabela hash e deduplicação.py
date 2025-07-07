import csv

class Registro:
    """
    Representa um registro genérico lido de um CSV.
    A chave usada para identificar duplicatas será o campo 'chave'.
    """
    def _init_(self, dados: dict, chave: str):
        self.dados = dados
        self.valor_chave = dados[chave]
        self.chave = chave

    def _eq_(self, outro):
        if not isinstance(outro, Registro):
            return False
        return self.valor_chave == outro.valor_chave

    def _hash_(self):
        return hash(self.valor_chave)

    def _str_(self):
        return str(self.dados)


class TabelaHash:
    """
    Classe que implementa uma tabela hash com encadeamento externo.
    """
    def _init_(self, tamanho: int = 100, funcao_hash=None):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]
        self.funcao_hash = funcao_hash if funcao_hash else self.hash_divisao

    def hash_divisao(self, chave: str) -> int:
        """
        Função de hash simples usando divisão.
        (str) -> int
        """
        return sum(ord(c) for c in chave) % self.tamanho

    def inserir(self, registro: Registro):
        """
        Insere o registro na tabela, se ainda não estiver presente.
        (Registro) -> None
        """
        indice = self.funcao_hash(registro.valor_chave)
        balde = self.tabela[indice]

        for item in balde:
            if item == registro:
                return  # já existe, não insere

        balde.append(registro)

    def buscar(self, chave: str) -> Registro:
        """
        Busca um registro pela chave.
        (str) -> Registro ou None
        """
        indice = self.funcao_hash(chave)
        for item in self.tabela[indice]:
            if item.valor_chave == chave:
                return item
        return None

    def remover(self, chave: str):
        """
        Remove um registro pela chave.
        (str) -> bool
        """
        indice = self.funcao_hash(chave)
        balde = self.tabela[indice]
        for i in range(len(balde)):
            if balde[i].valor_chave == chave:
                del balde[i]
                return True
        return False

    def obter_registros(self) -> list:
        """
        Retorna todos os registros armazenados.
        () -> list[Registro]
        """
        resultado = []
        for balde in self.tabela:
            resultado.extend(balde)
        return resultado


def remover_duplicatas_csv(arquivo_csv: str, chave: str, arquivo_saida: str):
    """
    Remove duplicatas do arquivo CSV com base no campo 'chave'.
    (str, str, str) -> None
    """
    tabela = TabelaHash(tamanho=200)

    with open(arquivo_csv, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            registro = Registro(dados=linha, chave=chave)
            tabela.inserir(registro)

    registros_deduplicados = tabela.obter_registros()

    if not registros_deduplicados:
        print("Nenhum dado encontrado.")
        return

    campos = registros_deduplicados[0].dados.keys()
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f_out:
        escritor = csv.DictWriter(f_out, fieldnames=campos)
        escritor.writeheader()
        for reg in registros_deduplicados:
            escritor.writerow(reg.dados)

    print(f"Arquivo '{arquivo_saida}' salvo com {len(registros_deduplicados)} registros únicos.")


# Exemplo de uso:
# Supondo um CSV com cabeçalho: cpf,nome,idade
if _name_ == "_main_":
    remover_duplicatas_csv("entrada.csv", "cpf", "saida_sem_duplicatas.csv")