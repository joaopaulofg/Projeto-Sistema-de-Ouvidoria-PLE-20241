from banco import con
import os

# Cabecalho
def cabecalho(msg):
    print('-'*40)
    print(msg.center(40).upper())
    print('-'*40)
    print()

# Menu Principal
def menuPrincipal():
    print("1 - Listar todas as manifestações\n"
    "2 - Listar manifestações por tipo\n"
    "3 - Inserir manifestação\n"
    "4 - Exibir quantidade de manifestações\n"
    "5 - Pesquisar manifestação por ID\n"
    "6 - Excluir manifestação por ID\n"
    "7 - Sair")

# Leitura de entradas no formato número inteiro.
def lerInteiro(txt):
    while True:
        try:
            entrada = int(input(txt))
        except:
            print("Digite um valor inteiro")
        else:
            break
    return entrada

# Leitura de entradas no formato texto.
def leiaTexto(txt):
    while True:
        try:
            ent = str(input(txt))
        except:
            if ent.isnumeric():
                print("Formato inválido, tente novamente.")
            else:
                break
        return ent

def switch_case(value):
    return {
        '1': 'Elogio',
        '2': 'Reclamação',
        '3': 'Sugestão',
    }.get(value, 'Valor inválido')

# Inserção de manifestações no sistema.
def inserirManifestacao():
    os.system('clear')
    try:
        c = con.cursor()
    except:
        print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
    else:
        try:
            print("-------- INSERÇÃO DE MANIFESTAÇÃO --------")
            while True:
                cpfManifestante = leiaTexto("\nInsira seu CPF: ").strip()
                break

            while True:
                manifestante = leiaTexto("Insira seu nome: ").strip()
                break

            while True:
                print("Qual o tipo da manifestação que você deseja inserir:\n"
                        "\n1 - Elogio\n"
                        "2 - Reclamação\n"
                        "3 - Sugestão\n")
                
                tipo = leiaTexto(">>> Digite uma opcão: ")

                if tipo in ['1', '2', '3']:
                    tipoManifestacao = switch_case(tipo)
                    break
                else:
                    print("Opção inválida. Digite novamente.")

            while True:
                manifestacao = leiaTexto("Insira o seu relato da manifestação: ").strip()
                break

            while True:
                telefone_1 = leiaTexto("Insira seu telefone para contato: ").strip()
                break
        except:
            print("Erro na inserçao de dados da manifestação.")
        else:
            try:
                c = con.cursor()
            except:
                print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
            else:
                try:
                    sql = 'INSERT INTO ouvidoria(cpfManifestante, manifestante, tipoManifestacao, manifestacao, telefone_1) VALUES(?, ?, ?, ?, ?)'
                    c.execute(sql, (cpfManifestante, manifestante, tipoManifestacao, manifestacao, telefone_1))
                    id = c.lastrowid
                except:
                    print("\nErro ao inserir manifestação.")
                else:
                    con.commit()
                    print("\nManifestação cadastrada com sucesso! ID: " + str(id))
                    input("\nPressione qualquer tecla para continuar...")
                    os.system('clear')

# Listagem de manifestações existentes no sistema.
def listarManifestacoes():
    try:
        c = con.cursor()
    except:
        print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
    else:
        sql = 'SELECT * FROM ouvidoria'
        c.execute(sql)
        listaDeManifestacoes = c.fetchall()

        if len(listaDeManifestacoes) == 0:
            print("Nenhuma manifestação cadastrada.")
        else:
            print("--- MANIFESTAÇÕES CADASTRADAS ---")

            for manifestacao in listaDeManifestacoes:
                print("\033[33m\nManifestação - ID #", str(manifestacao[0]).rstrip(), "\033[0m", sep='')
                print("CPF manifestante:", manifestacao[1])
                print("Manifestante:", manifestacao[2])
                print("Tipo da manifestação:", manifestacao[3])
                print("Descrição:", manifestacao[4])

            print("\n-------- FIM DA LISTAGEM --------")
    
    input("\nPressione qualquer tecla para continuar...")
    os.system('clear')

def listarManifestacoesPorTipo():
    try:
        c = con.cursor()
    except:
        print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
    else:
        sql = 'SELECT * FROM ouvidoria'
        c.execute(sql)
        listaDeManifestacoes = c.fetchall()

        if len(listaDeManifestacoes) == 0:
            print("Não há manifestações cadastradas.")
        else:
            while True:
                print("Qual o tipo da manifestação que você deseja inserir:\n"
                            "\n1 - Elogio\n"
                            "2 - Reclamação\n"
                            "3 - Sugestão\n")
                    
                tipo = leiaTexto(">>> Digite uma opcão: ")

                if tipo in ['1', '2', '3']:
                    tipoManifestacao = switch_case(tipo)
                    break
                else:
                    print("Opção inválida. Digite novamente.")

            sql = 'SELECT * FROM ouvidoria WHERE tipoManifestacao = ?'
            c.execute(sql, (tipoManifestacao,))
            listaDeManifestacoes = c.fetchall()

            if len(listaDeManifestacoes) == 0:
                print("Não há manifestações cadastradas com esse tipo.")
            else:
                os.system('clear')
                print("--- MANIFESTAÇÕES DO TIPO " + tipoManifestacao.upper() + " CADASTRADAS ---")
            
                for manifestacao in listaDeManifestacoes:
                    print("\033[33m\nManifestação - ID #", str(manifestacao[0]).rstrip(), "\033[0m", sep='')
                    print("CPF manifestante:", manifestacao[1])
                    print("Manifestante:", manifestacao[2])
                    print("Tipo da manifestação:", manifestacao[3])
                    print("Descrição:", manifestacao[4])
                print("\n---------------- FIM DA LISTAGEM ----------------")

        input("\nPressione qualquer tecla para continuar...")
        os.system('clear')

# Exclusão de manifestações existentes no sistema.
def excluirManifestacao():
    try:
        c = con.cursor()
    except:
        print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
    else:
        print("--- EXCLUSÃO DE MANIFESTAÇÃO ---")
        exclusao = leiaTexto("\nInsira o ID da manifestação que deseja excluir: ")
        sql = 'SELECT * FROM ouvidoria WHERE id = ?'
        c.execute(sql, (exclusao,))
        manifestacao = c.fetchall()

        if manifestacao == []:
                print("\nNão localizamos nenhuma manifestação cadastrada com esse ID.")
                resultado = ""
        else:
            for campo in manifestacao:
                print("\033[33m\nManifestação - ID #", str(campo[0]).rstrip(), "\033[0m", sep='')
                print("Tipo da Manifestação:", campo[1])
                print("Manifestante:", campo[2])
                print("Descrição:", campo[3])

            while True:
                confirmacao = input("\nConfirma a exclusão da manifestação abaixo? S/N:").upper()
                if confirmacao == 'S':
                    sql = 'DELETE FROM ouvidoria WHERE id = ?'
                    c.execute(sql, (exclusao,))
                    con.commit()
                    resultado = "\nManifestação excluída com sucesso!\n"
                    break
                elif confirmacao == 'N':
                    resultado = "\nExclusão cancelada.\n"
                    break
                else:
                    print("\nOpção inválida. Digite novamente.")
        
        print(resultado)
        input("Pressione qualquer tecla para continuar...")
        os.system('clear')

# Alteração de manifestações existentes no sistema.
def alterarManifestacao():
    os.system('clear')
    cabecalho("Alteração de Manifestação")
    idAlteracao = lerInteiro("\nInsira o ID da manifestação que deseja alterar: ")
    try:
        c = con.cursor()
    except:
        print('\033[1;31mErro ao tentar conectar-se ao banco de dados.\033[m')
    else:
        try:
            sql = 'SELECT * FROM ouvidoria WHERE id = ?'
            c.execute(sql, (idAlteracao,))
            alterar = c.fetchall()
        except:
            print("Erro na busca pela manifestação.")
        else:
            try:
                while True:
                    cpfManifestante = leiaTexto("Insira seu CPF: ").strip()
                    break
                while True:
                    manifestante = leiaTexto("Insira seu nome: ").strip()
                    break
                while True:
                    manifestacao = leiaTexto("Insira o seu relato da manifestação: ").strip()
                    break
                while True:
                    telefone_1 = leiaTexto("Insira seu telefone para contato: ").strip()
                    break
            except:
                print("Erro na alteração de dados da manifestação.")
            else:
                asql = 'UPDATE ouvidoria SET cpfManifestante = ?, manifestante = ?, manifestacao = ?, telefone_1 = ? WHERE id = ?;'
                c.execute(asql, (cpfManifestante, manifestante, manifestacao, telefone_1, idAlteracao))
                con.commit()
                print("\nManifestação alterada com sucesso!")
                
def encerrarSistema():
    os.system('clear')
    print("\n\033[1;32mFinalizando...\033[m")
    con.close()
    exit()