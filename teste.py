import sqlite3

    # Conectar ao banco de dados SQLite
conn = sqlite3.connect('clientes_2.db')
c = conn.cursor()

    # Criar tabelas
c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    estado_civil TEXT,
                    data_nascimento TEXT,
                    nome_pai TEXT,
                    nome_mae TEXT,
                    email TEXT,
                    grau_instrucao TEXT
                )''')

c.execute('''CREATE TABLE IF NOT EXISTS documentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    orgao_emissor TEXT,
                    data_emissao TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                )''')

c.execute('''CREATE TABLE IF NOT EXISTS telefones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    principal BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                )''')

conn.commit()

    # Funções de validação
def validar_opcao(opcao, opcoes_validas):
        while opcao not in opcoes_validas:
            print(f"Opção inválida! As opções válidas são: {', '.join(opcoes_validas)}")
            opcao = input("Digite novamente: ")
        return opcao

    # Função para cadastrar um cliente
def cadastrar_cliente():
        nome = input("Nome: ")
        cpf = input("CPF: ")
        
        c.execute("INSERT INTO clientes (nome, cpf) VALUES (?, ?)", (nome, cpf))
        cliente_id = c.lastrowid
        
        print("Cadastro de Documento")
        tipo = validar_opcao(input("Tipo (RG, CNH, Passaporte, CTPS, Identidade Funcional): "), 
                            ["RG", "CNH", "Passaporte", "CTPS", "Identidade Funcional"])
        numero = input("Número do Documento: ")
        orgao_emissor = input("Órgão Emissor: ")
        data_emissao = input("Data de Emissão (YYYY-MM-DD): ")
        
        c.execute("INSERT INTO documentos (cliente_id, tipo, numero, orgao_emissor, data_emissao) VALUES (?, ?, ?, ?, ?)",
                (cliente_id, tipo, numero, orgao_emissor, data_emissao))
        
        print("Cadastro de Telefone")
        tipo = validar_opcao(input("Tipo (Celular, Residencial, Comercial): "), 
                            ["Celular", "Residencial", "Comercial"])
        numero = input("Número: ")
        principal = input("É o telefone principal? (S/N): ").strip().lower() == 's'
        
        c.execute("INSERT INTO telefones (cliente_id, tipo, numero, principal) VALUES (?, ?, ?, ?)",
                (cliente_id, tipo, numero, principal))
        
        conn.commit()
        print("Cliente cadastrado com sucesso!")

    # Função para cadastrar telefone
def cadastrar_telefone():
        cpf = input("Digite o CPF do cliente: ")
        c.execute("SELECT id FROM clientes WHERE cpf = ?", (cpf,))
        cliente = c.fetchone()
        
        if cliente:
            cliente_id = cliente[0]
            tipo = validar_opcao(input("Tipo (Celular, Residencial, Comercial): "), 
                                ["Celular", "Residencial", "Comercial"])
            numero = input("Número: ")
            principal = input("É o telefone principal? (S/N): ").strip().lower() == 's'
            
            c.execute("INSERT INTO telefones (cliente_id, tipo, numero, principal) VALUES (?, ?, ?, ?)",
                    (cliente_id, tipo, numero, principal))
            conn.commit()
            print("Telefone cadastrado com sucesso!")
        else:
            print("Cliente não encontrado.")

    # Função para cadastrar dados adicionais
def cadastrar_dados_adicionais():
        cpf = input("Digite o CPF do cliente: ")
        c.execute("SELECT id FROM clientes WHERE cpf = ?", (cpf,))
        cliente = c.fetchone()
        
        if cliente:
            estado_civil = validar_opcao(input("Estado Civil (Casado, Solteiro, Divorciado, União Estável, Separado Judicialmente): "), 
                                        ["Casado", "Solteiro", "Divorciado", "União Estável", "Separado Judicialmente"])
            data_nascimento = input("Data de Nascimento (YYYY-MM-DD): ")
            nome_pai = input("Nome do Pai: ")
            nome_mae = input("Nome da Mãe: ")
            email = input("Email: ")
            grau_instrucao = validar_opcao(input("Grau de Instrução (Analfabeto, Ensino Fundamental Incompleto, Ensino Fundamental Completo, Ensino Médio Completo, Superior): "), 
                                        ["Analfabeto", "Ensino Fundamental Incompleto", "Ensino Fundamental Completo", "Ensino Médio Completo", "Superior"])
            
            c.execute("UPDATE clientes SET estado_civil = ?, data_nascimento = ?, nome_pai = ?, nome_mae = ?, email = ?, grau_instrucao = ? WHERE cpf = ?",
                    (estado_civil, data_nascimento, nome_pai, nome_mae, email, grau_instrucao, cpf))
            conn.commit()
            print("Dados adicionais cadastrados com sucesso!")
        else:
            print("Cliente não encontrado.")

    # Função para listar clientes cadastrados
def listar_clientes():
        c.execute("SELECT * FROM clientes")
        clientes = c.fetchall()
        
        if clientes:
            print("\nClientes Cadastrados:")
            for cliente in clientes:
                print(f"ID: {cliente[0]}, Nome: {cliente[1]}, CPF: {cliente[2]}, Estado Civil: {cliente[3]}, "
                    f"Data de Nascimento: {cliente[4]}, Nome do Pai: {cliente[5]}, Nome da Mãe: {cliente[6]}, "
                    f"Email: {cliente[7]}, Grau de Instrução: {cliente[8]}")
        else:
            print("Nenhum cliente cadastrado no banco de dados.")

    # Função para verificar telefone residencial
def verificar_telefone_residencial():
        c.execute("SELECT clientes.id, clientes.nome FROM clientes")
        clientes = c.fetchall()
        
        if clientes:
            print("\nVerificação de Telefone Residencial:")
            for cliente in clientes:
                cliente_id = cliente[0]
                c.execute("SELECT numero FROM telefones WHERE cliente_id = ? AND tipo = 'Residencial'", (cliente_id,))
                telefone_residencial = c.fetchone()
                
                if telefone_residencial:
                    print(f"Cliente ID {cliente[0]}, Nome: {cliente[1]} - Possui telefone residencial:{telefone_residencial[0]}.")
                else:
                    print(f"Cliente ID {cliente[0]}, Nome: {cliente[1]} - Não possui telefone residencial.")
        else:
            print("Nenhum cliente cadastrado no banco de dados.")

    # Menu principal
def menu():
        while True:
            print("\nMenu:")
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Telefone")
            print("3. Cadastrar Dados Adicionais")
            print("4. Listar Clientes")
            print("5. Verificar Telefone Residencial")
            print("6. Sair")
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                cadastrar_cliente()
            elif opcao == "2":
                cadastrar_telefone()
            elif opcao == "3":
                cadastrar_dados_adicionais()
            elif opcao == "4":
                listar_clientes()
            elif opcao == "5":
                verificar_telefone_residencial()
            elif opcao == "6":
                print("Saindo...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    # Executar menu
menu()

    # Fechar conexão com o banco de dados
conn.close()
