import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class InsertInfo():
    
    @property
    def caminhos(self):
        return {
            "excel":"db\\controle_estoque.xlsx",
            "database":"db\\database.db"
        }
    
    def __init__(self, tipo):
        self.app = tk.Tk()
        self.app.title("Inserção de informações")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Criando os campos e armazenando em atributos da classe
        self.entry_data = self.create_entry("Data", 0)
        self.entry_nome = self.create_entry("Nome", 1)
        self.entry_produto = self.create_entry("Produto", 2)
        self.entry_debito = self.create_entry("Débito", 3)
        self.entry_credito = self.create_entry("Crédito", 4)
        self.entry_cargo = self.create_entry("Cargo", 5)
        self.entry_turma = self.create_entry("Turma", 6)
        self.entry_telefone = self.create_entry("Telefone", 7)
        self.entry_obs = self.create_entry("Observação", 8)

        # Botões
        self.botao_excel = ttk.Button(self.app, text="Salvar Excel", command=self.salvar_geral)
        self.botao_excel.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.botao_db = ttk.Button(self.app, text="Salvar Database", command=self.salvar_geral)
        self.botao_db.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.botao_erase = ttk.Button(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=10, column=2, sticky="ew", padx=5, pady=5)
        
        self.fgt_user = ttk.Button(self.app, text="logout", command=self.deslogar)
        self.fgt_user.grid(row=15, column=2, sticky="ew", padx=5, pady=5)
        
        self.back = ttk.Button(self.app, text="Voltar", command=lambda: self.retornar(tipo))
        self.back.grid(row=15, column=0, sticky="ew", padx=5, pady=5)

        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):  # Garante que todas as linhas se ajustem
            self.app.rowconfigure(i, weight=1)
            
    def retornar(self, tipo):
        if tipo.upper() == 'ADMIN':
            from InterationAdmin import InterationAdmin
            self.app.destroy()
            logout = InterationAdmin(tipo)
            logout.main() 

        if tipo.upper() == 'USER':
            from InterationUser import InterationUser
            self.app.destroy()
            logout = InterationUser(tipo)
            logout.main() 
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()   
        
    def salvar_geral(self):
        self.salvar_xlsx()
        self.salvar_db()
    
    def create_entry(self, label, row, default_value=""):
        tk.Label(self.app, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        entry.insert(0, default_value)
        return entry

    def formatar_data(self, *args):
        """ Formata a entrada da data automaticamente (dd/mm/yyyy). """
        texto = self.entry_data.get().replace("/", "")  # Remove barras existentes
        if len(texto) > 8:
            texto = texto[:8]  # Garante que não ultrapasse o formato correto

        novo_texto = ""
        for i, char in enumerate(texto):
            if i in [2, 4]:  # Insere a barra nas posições corretas
                novo_texto += "/"
            novo_texto += char

        # Atualiza o campo sem perder a posição do cursor
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, novo_texto)

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
            "Data": datetime.strptime(data, '%d/%m/%Y'),
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

        arquivo_excel = self.caminhos['excel']

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

    def connect(self):
        con = sqlite3.connect(self.caminhos['database'])
        cursor = con.cursor()        
        return cursor, con

    def criar(self):
        cursor, con = self.connect()
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS cantina (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                nome VARCHAR(30),
                produto TEXT,
                debito TEXT,
                credito TEXT,
                total TEXT,
                cargo TEXT,
                turma TEXT,
                telefone TEXT,
                observacao TEXT
            );
        ''')
        print("Tabela criada com sucesso")
        con.close()

    def inserir(self, data, nome, produto, debito, credito, cargo, turma, telefone, observacao):
        try:
            cursor, con = self.connect()  # Obtém o cursor e a conexão
            data = datetime.strptime(data, '%d/%m/%Y')
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
            con.close()
            print("Finalizado com sucesso")
        except Exception as e:
            print(f"Erro: {e}")
            raise

    def main(self):
        # Adicionando o 'trace' para formatação de data
        self.entry_data_var = tk.StringVar()
        self.entry_data.config(textvariable=self.entry_data_var)
        self.entry_data_var.trace_add("write", self.formatar_data)
        
        self.app.mainloop()


if __name__ == '__main__':
    service = InsertInfo()
    service.main()
