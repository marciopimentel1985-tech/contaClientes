from datetime import date
from enum import Enum


class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    URGENTE = "Urgente"


class Status(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluída"


class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.projetos = []

    def criar_projeto(self, projeto):
        self.projetos.append(projeto)

    def listar_projetos(self):
        return self.projetos


class Projeto:
    def __init__(self, id, nome, descricao, usuario):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = date.today()
        self.usuario = usuario
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def remover_tarefa(self, tarefa):
        if tarefa in self.tarefas:
            self.tarefas.remove(tarefa)

    def calcular_progresso(self):
        if not self.tarefas:
            return 0

        concluidas = sum(
            1 for tarefa in self.tarefas
            if tarefa.status == Status.CONCLUIDA
        )

        return (concluidas / len(self.tarefas)) * 100


class Tarefa:
    def __init__(
        self,
        id,
        titulo,
        descricao,
        prioridade,
        data_limite,
        projeto
    ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.data_limite = data_limite
        self.status = Status.PENDENTE
        self.projeto = projeto

    def marcar_concluida(self):
        self.status = Status.CONCLUIDA

    def esta_vencida(self):
        return (
            date.today() > self.data_limite
            and self.status != Status.CONCLUIDA
        )


usuarios = []
projetos = []
tarefas = []


def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")

    id_usuario = len(usuarios) + 1
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    usuario = Usuario(id_usuario, nome, email, senha)

    usuarios.append(usuario)

    print("Usuário cadastrado com sucesso!")


def listar_usuarios():
    print("\n=== USUÁRIOS ===")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        print(
            f"ID: {usuario.id} | "
            f"Nome: {usuario.nome} | "
            f"E-mail: {usuario.email}"
        )


def cadastrar_projeto():
    print("\n=== CADASTRO DE PROJETO ===")

    if not usuarios:
        print("Cadastre um usuário primeiro.")
        return

    listar_usuarios()

    id_usuario = int(input("ID do usuário: "))

    usuario = next(
        (u for u in usuarios if u.id == id_usuario),
        None
    )

    if usuario is None:
        print("Usuário não encontrado.")
        return

    id_projeto = len(projetos) + 1
    nome = input("Nome do projeto: ")
    descricao = input("Descrição: ")

    projeto = Projeto(
        id_projeto,
        nome,
        descricao,
        usuario
    )

    projetos.append(projeto)
    usuario.criar_projeto(projeto)

    print("Projeto cadastrado com sucesso!")


def listar_projetos():
    print("\n=== PROJETOS ===")

    if not projetos:
        print("Nenhum projeto cadastrado.")
        return

    for projeto in projetos:
        progresso = projeto.calcular_progresso()

        print(
            f"\nID: {projeto.id}"
            f"\nNome: {projeto.nome}"
            f"\nDescrição: {projeto.descricao}"
            f"\nResponsável: {projeto.usuario.nome}"
            f"\nProgresso: {progresso:.1f}%"
        )


def cadastrar_tarefa():
    print("\n=== CADASTRO DE TAREFA ===")

    if not projetos:
        print("Cadastre um projeto primeiro.")
        return

    listar_projetos()

    id_projeto = int(input("\nID do projeto: "))

    projeto = next(
        (p for p in projetos if p.id == id_projeto),
        None
    )

    if projeto is None:
        print("Projeto não encontrado.")
        return

    id_tarefa = len(tarefas) + 1

    titulo = input("Título: ")
    descricao = input("Descrição: ")

    print("\nPrioridades:")
    print("1 - Baixa")
    print("2 - Média")
    print("3 - Alta")
    print("4 - Urgente")

    opcao = int(input("Escolha: "))

    prioridades = {
        1: Prioridade.BAIXA,
        2: Prioridade.MEDIA,
        3: Prioridade.ALTA,
        4: Prioridade.URGENTE
    }

    prioridade = prioridades.get(opcao)

    if prioridade is None:
        print("Prioridade inválida.")
        return

    data_texto = input("Data limite (AAAA-MM-DD): ")

    try:
        ano, mes, dia = map(int, data_texto.split("-"))
        data_limite = date(ano, mes, dia)
    except ValueError:
        print("Data inválida.")
        return

    tarefa = Tarefa(
        id_tarefa,
        titulo,
        descricao,
        prioridade,
        data_limite,
        projeto
    )

    tarefas.append(tarefa)
    projeto.adicionar_tarefa(tarefa)

    print("Tarefa cadastrada com sucesso!")


def listar_tarefas():
    print("\n=== TAREFAS ===")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for tarefa in tarefas:
        vencida = "SIM" if tarefa.esta_vencida() else "NÃO"

        print(
            f"\nID: {tarefa.id}"
            f"\nTítulo: {tarefa.titulo}"
            f"\nDescrição: {tarefa.descricao}"
            f"\nProjeto: {tarefa.projeto.nome}"
            f"\nPrioridade: {tarefa.prioridade.value}"
            f"\nStatus: {tarefa.status.value}"
            f"\nData limite: {tarefa.data_limite}"
            f"\nVencida: {vencida}"
        )


def concluir_tarefa():
    listar_tarefas()

    if not tarefas:
        return

    id_tarefa = int(input("\nID da tarefa: "))

    tarefa = next(
        (t for t in tarefas if t.id == id_tarefa),
        None
    )

    if tarefa is None:
        print("Tarefa não encontrada.")
        return

    tarefa.marcar_concluida()

    print("Tarefa marcada como concluída!")


def iniciar_tarefa():
    listar_tarefas()

    if not tarefas:
        return

    id_tarefa = int(input("\nID da tarefa: "))

    tarefa = next(
        (t for t in tarefas if t.id == id_tarefa),
        None
    )

    if tarefa is None:
        print("Tarefa não encontrada.")
        return

    tarefa.status = Status.EM_ANDAMENTO

    print("Tarefa marcada como em andamento!")


def relatorio():
    print("\n=== RELATÓRIO DE PRODUTIVIDADE ===")

    total = len(tarefas)

    concluidas = sum(
        1 for tarefa in tarefas
        if tarefa.status == Status.CONCLUIDA
    )

    pendentes = sum(
        1 for tarefa in tarefas
        if tarefa.status == Status.PENDENTE
    )

    andamento = sum(
        1 for tarefa in tarefas
        if tarefa.status == Status.EM_ANDAMENTO
    )

    print(f"Total de tarefas: {total}")
    print(f"Concluídas: {concluidas}")
    print(f"Em andamento: {andamento}")
    print(f"Pendentes: {pendentes}")

    if total > 0:
        percentual = (concluidas / total) * 100
        print(f"Conclusão geral: {percentual:.1f}%")

    print("\n=== TAREFAS POR PRIORIDADE ===")

    for prioridade in Prioridade:
        quantidade = sum(
            1 for tarefa in tarefas
            if tarefa.prioridade == prioridade
        )

        print(f"{prioridade.value}: {quantidade}")


def menu():
    while True:
        print("\n==============================")
        print(" GERENCIADOR DE TAREFAS")
        print("==============================")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Cadastrar projeto")
        print("4 - Listar projetos")
        print("5 - Cadastrar tarefa")
        print("6 - Listar tarefas")
        print("7 - Iniciar tarefa")
        print("8 - Concluir tarefa")
        print("9 - Relatório")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()

        elif opcao == "2":
            listar_usuarios()

        elif opcao == "3":
            cadastrar_projeto()

        elif opcao == "4":
            listar_projetos()

        elif opcao == "5":
            cadastrar_tarefa()

        elif opcao == "6":
            listar_tarefas()

        elif opcao == "7":
            iniciar_tarefa()

        elif opcao == "8":
            concluir_tarefa()

        elif opcao == "9":
            relatorio()

        elif opcao == "0":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()