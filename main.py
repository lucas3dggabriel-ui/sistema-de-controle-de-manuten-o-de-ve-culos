import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT,
    placa TEXT UNIQUE,
    ano INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS manutencoes (
    id_manutencao INTEGER PRIMARY KEY AUTOINCREMENT,
    veiculo_id INTEGER,
    descricao TEXT,
    valor REAL,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
)
""")

while True:
    print("\n" + "="*30)
    print("   SISTEMA DE MANUTENÇÃO")
    print("="*30)
    print("1. Cadastrar Veículo")
    print("2. Listar Veículos")
    print("4. Registrar Manutenção")
    print("5. Ver Histórico de Manutenção")
    print("3. Sair")
    print("-"*30)
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        try:
            modelo = input("Modelo do veículo: ")
            placa = input("Placa: ")
            ano = int(input("Ano: "))
            
            cursor.execute("INSERT INTO veiculos (modelo, placa, ano) VALUES (?, ?, ?)", 
                           (modelo, placa, ano))
            conn.commit()
            print(f"\n✅ Sucesso: {modelo} cadastrado!")
        except sqlite3.IntegrityError:
            print("\n❌ Erro: Esta placa já está cadastrada no sistema.")
        except ValueError:
            print("\n❌ Erro: No campo 'Ano', digite apenas números.")

    elif opcao == "2":
        cursor.execute("SELECT * FROM veiculos")
        veiculos = cursor.fetchall()
        
        print("\n--- Frota de Veículos ---")
        if not veiculos:
            print("Nenhum veículo cadastrado.")
        for v in veiculos:
            print(f"ID: {v[0]} | Carro: {v[1]} | Placa: {v[2]} | Ano: {v[3]}")

    elif opcao == "4":
        try:
            print("\n(Dica: Consulte o ID do carro na opção 2)")
            v_id = int(input("Digite o ID do veículo: "))
            desc = input("Descrição do serviço: ")
            val = float(input("Valor do serviço (ex: 150.50): "))
            
            cursor.execute("INSERT INTO manutencoes (veiculo_id, descricao, valor) VALUES (?, ?, ?)", 
                           (v_id, desc, val))
            conn.commit()
            print("\n✅ Manutenção registrada com sucesso!")
        except ValueError:
            print("\n❌ Erro: Digite números válidos para ID e Valor.")

    elif opcao == "5":
        try:
            v_id = int(input("Digite o ID do veículo para ver o histórico: "))
            
            cursor.execute("SELECT modelo FROM veiculos WHERE id = ?", (v_id,))
            carro = cursor.fetchone()
            
            if carro:
                cursor.execute("SELECT descricao, valor FROM manutencoes WHERE veiculo_id = ?", (v_id,))
                servicos = cursor.fetchall()
                
                print(f"\n--- Histórico: {carro[0]} (ID: {v_id}) ---")
                if not servicos:
                    print("Nenhum serviço registrado para este carro.")
                for s in servicos:
                    print(f"• {s[0]} | R$ {s[1]:.2f}")
            else:
                print("\n❌ Erro: Veículo não encontrado.")
        except ValueError:
            print("\n❌ Erro: Digite um ID válido.")

    elif opcao == "3":
        print("\nEncerrando o sistema... Até logo!")
        break

    else:
        print("\n⚠️ Opção inválida. Tente novamente.")

conn.close()
