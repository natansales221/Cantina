import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

class Cantininha: 
    
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Seleção de opções")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Criando os campos e armazenando em atributos da classe
        self.entry_login = self.create_entry("Olá Usuário! O que deseja fazer?", 0)

        # Botões
        self.fgt_pswd = ttk.Button(self.app, text="Visualizar Resumo", command=self.view)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Inserir informações", command=self.insert)
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
        
    def view(self):
        login = self.entry_login.get()
        # Open a new window for forgotten user
        self.forgot_pwd_window = tk.Toplevel(self.app)
        self.forgot_pwd_window.title("Recuperar Senha")

        # Create new fields for forgotten user window
        self.entry_forgot_name = self.create_entry_in_window("Confirme seu nome", 0, self.forgot_pwd_window)
        self.entry_forgot_last_name = self.create_entry_in_window("Confirme seu sobrenome", 1, self.forgot_pwd_window)
        self.entry_forgot_date = self.create_entry_in_window("Confirme sua data de nascimento", 2, self.forgot_pwd_window)
        self.entry_forgot_password = self.create_entry_in_window("Senha Nova", 3, self.forgot_pwd_window, is_password=True)
        
        self.submit_button = ttk.Button(self.forgot_pwd_window, text="Enviar", command=self.submit_forgot_password)
        self.submit_button.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
                    
    def create_entry(self, label, row):
        tk.Label(self.app, text=label, anchor="center").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        return entry

    def insert(self):
        
        self.app = tk.Tk()
        self.app.title("Formulário de Casos Abertos")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Criando os campos e armazenando em atributos da classe
        self.entry_data = self.create_entry_insert("Data", 0)
        self.entry_nome = self.create_entry_insert("Nome", 1)
        self.entry_produto = self.create_entry_insert("Produto", 2)
        self.entry_debito = self.create_entry_insert("Débito", 3)
        self.entry_credito = self.create_entry_insert("Crédito", 4)
        self.entry_cargo = self.create_entry_insert("Cargo", 5)
        self.entry_turma = self.create_entry_insert("Turma", 6)
        self.entry_telefone = self.create_entry_insert("Telefone", 7)
        self.entry_obs = self.create_entry_insert("Observação", 8)

        # Botões
        self.botao_excel = ttk.Button(self.app, text="Salvar Excel", command=self.salvar_geral)
        self.botao_excel.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.botao_db = ttk.Button(self.app, text="Salvar Database", command=self.salvar_geral)
        self.botao_db.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.botao_erase = ttk.Button(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=10, column=2, sticky="ew", padx=5, pady=5)

        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):  # Garante que todas as linhas se ajustem
            self.app.rowconfigure(i, weight=1)
        
    def create_entry_in_window(self, label, row, window, is_password=False):
        tk.Label(window, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(window, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        return entry

    def submit_forgot_user(self):
        cursor, con = self.connect()
        lost_name = self.entry_forgot_name.get()
        lost_sobrenome = self.entry_forgot_last_name.get()
        
        query = """
        SELECT login from login_cantina
        WHERE nome = (?)
        AND sobrenome = (?)
            """
        params = (lost_name, lost_sobrenome)
        cursor.execute(query, params)
        
        login_novo = cursor.fetchall()[0][0]

        self.label_status.config(text=f"Seu usuário é {login_novo}")

        # Close the forgotten user window
        self.forgot_user_window.destroy()

    def login_bt(self):
        cursor, con = self.connect()
        login = self.entry_login.get()
        query = """
                SELECT login, senha from login_cantina
            """
        cursor.execute(query)
        
        login_valid, password_valid = cursor.fetchall()[0]
  
    def connect(self):
        con = sqlite3.connect('db\database.db')
        cursor = con.cursor()        
        return cursor, con

    def criar(self):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_cantina (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                sobrenome TEXT,
                login TEXT,
                senha TEXT,
                tipo TEXT,
                nascimento TEXT
            );
        ''')

        query = """
                INSERT INTO login_cantina (nome, sobrenome, login, senha, tipo, nascimento)
                VALUES (?,?,?,?,?,?)
            """

        params = ('natan', 'sales', 'natansales', 'natansales2', 'admin', '30/09/2000')
        
        cursor.execute(query, params)
        
        con.commit()
        
        # cursor.execute('drop table login_cantina')
        print("Tabela criada com sucesso")

    def main(self):
        self.app.mainloop()
        
    def submit_forgot_password(self):
        cursor, con = self.connect()
        lost_name = self.entry_forgot_name.get()
        lost_sobrenome = self.entry_forgot_last_name.get()
        date = self.entry_forgot_date.get()
        pwd = self.entry_forgot_password.get()
        
        query = """
        UPDATE login_cantina
        SET senha = ?
        WHERE nome = ?
        AND sobrenome = ? 
        AND nascimento = ?
        """
        params = (pwd, lost_name, lost_sobrenome, date)
        
        if cursor.execute(query, params).rowcount == 1:
            con.commit()
            self.label_status.config(text="Senha alterada!")
            self.forgot_pwd_window.destroy()
        else:
            self.label_status.config(text="Não foi possível alterar a senha")
            self.forgot_pwd_window.destroy()
     
    def create_entry_insert(self, label, row):
        tk.Label(self.app, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)  # Ocupa 2 colunas
        return entry
    
    def salvar_xlsx(self):
        
        data = self.entry_data.get()
        nome = self.entry_nome.get()
        credito = self.entry_credito.get()
        cargo = self.entry_cargo.get()
        produto = self.entry_produto.get()
        debito = self.entry_debito.get()
        turma = self.entry_turma.get()
        telefone = self.entry_telefone.get()
        observacao = self.entry_obs.get()

        novo_dado = pd.DataFrame([{
            "Data": data,
            "Nome": nome,
            "Produto": produto,
            "Débito": debito,
            "Crédito": 0 if credito == '' else credito,
            "Total": str(int(credito) - int(debito)),
            "Cargo": cargo,
            "Turma": turma,
            "Telefone": telefone,
            "Observacao": observacao
        }])

        arquivo_excel = "db\controle_estoque.xlsx"

        if os.path.exists(arquivo_excel):
            df_existente = pd.read_excel(arquivo_excel)
            df_final = pd.concat([df_existente, novo_dado], ignore_index=True)
        else:
            df_final = novo_dado

        df_final.to_excel(arquivo_excel, index=False)

        self.label_status.config(text="Dados salvos no Excel!")
        
    def salvar_db(self):
        data = self.entry_data.get()
        nome = self.entry_nome.get()
        produto = self.entry_produto.get()
        debito = self.entry_debito.get()
        credito = self.entry_credito.get()
        cargo = self.entry_cargo.get()
        turma = self.entry_turma.get()
        telefone = self.entry_telefone.get()
        observacao = self.entry_obs.get()
        try:
            self.inserir(data, nome, produto, debito, credito, cargo, turma, telefone, observacao)
            print("Dados salvos no banco!")
            self.label_status.config(text="Dados salvos no banco!")
        except Exception as e:
            self.label_status.config(text= e)
          
    def salvar_geral(self):
        self.salvar_xlsx()
        self.salvar_db()
        self.clear_fields()
    
    def clear_fields(self):
        """Limpa todos os campos de entrada."""
        self.entry_data.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_produto.delete(0, tk.END)
        self.entry_debito.delete(0, tk.END)
        self.entry_credito.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_turma.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_obs.delete(0, tk.END)

    def inserir(self, data, nome, produto, debito, credito, cargo, turma, telefone, observacao):
        try:
            cursor, con = self.connect()  # Obtém o cursor e a conexão
            data = data
            nome = nome
            produto = produto
            debito = debito
            credito = 0 if credito == '' else credito
            total = str(int(credito) - int(debito))
            cargo = cargo
            turma = turma
            telefone = telefone        
            observacao = observacao
            
            query = """
                INSERT INTO cantina (data, nome, produto, debito, credito, total, cargo, turma, telefone, observacao)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """
            params = (data, nome, produto, debito, credito, total, cargo, turma, telefone, observacao)
            
            cursor.execute(query, params)
            con.commit()
            print("Finalizado com sucesso")
        except Exception as e:
            print(f"Erro: {e}")
            raise
        
if __name__ == '__main__':
    service = Cantininha()
    service.main()
