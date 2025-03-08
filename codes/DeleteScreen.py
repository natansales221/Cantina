import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class DeleteInfo():
    
    @property
    def caminhos(self):
        return {
            "excel":"db\\controle_estoque.xlsx",
            "database":"db\\database.db"
        }
    
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Exclusão de informações")
        
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
        self.entry_cargo = self.create_entry("Cargo", 3)
        self.entry_turma = self.create_entry("Turma", 4)

        # Botões
        self.botao_db = ttk.Button(self.app, text="Apagar informações", command=self.exclusao)
        self.botao_db.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.botao_erase = ttk.Button(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=10, column=2, sticky="ew", padx=5, pady=5)
        
        self.fgt_user = ttk.Button(self.app, text="logout", command=self.deslogar)
        self.fgt_user.grid(row=15, column=2, sticky="ew", padx=5, pady=5)
        
        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):  # Garante que todas as linhas se ajustem
            self.app.rowconfigure(i, weight=1)
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()  
               
    def exclusao(self):
        self.apagar()
        self.apagar_xlsx()
        
    def create_entry(self, label, row, default_value=""):
        tk.Label(self.app, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        entry.insert(0, default_value)  # Insere o valor padrão
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

    def apagar_xlsx(self):
        data = self.entry_data.get()
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()
        produto = self.entry_produto.get()
        turma = self.entry_turma.get()

        arquivo_excel = self.caminhos['excel']

        if os.path.exists(arquivo_excel):
            df_existente = pd.read_excel(arquivo_excel)
            filt_nome = df_existente[df_existente['Nome'].str.upper() == nome.upper()]
            filt_prod = filt_nome[filt_nome['Produto'].str.upper() == produto.upper()]
            filt_data = filt_prod[filt_prod['Data'] == datetime.strptime(data, '%d/%m/%Y')]
            filt_cargo = filt_data[filt_data['Cargo'].str.upper() == cargo.upper()]
            filt_turma = filt_cargo[filt_cargo['Turma'].str.upper() == turma.upper()]
            
            df_filtrado = df_existente[~df_existente.index.isin(filt_turma.index)]

            df_final = df_filtrado
            df_final = df_final.reset_index(drop=True)
        else:
            df_final = pd.DataFrame([{
                "Data": datetime.strptime(data, '%d/%m/%Y'),
                "Nome": nome,
                "Produto": produto,
                "Cargo": cargo,
                "Turma": turma,
            }])

        df_final.to_excel(arquivo_excel, index=False)
        self.label_status.config(text="Dados apagados no Excel!")

    def apagar(self):
        data = self.entry_data.get()
        nome = self.entry_nome.get()
        produto = self.entry_produto.get()
        cargo = self.entry_cargo.get()
        turma = self.entry_turma.get()
        try:
            if self.apagar_db(datetime.strptime(data, '%d/%m/%Y'), nome, produto, cargo, turma):
                self.label_status.config(text="Dados apagados no banco!")
            else:
                self.label_status.config(text="Favor revisar as informações a serem excluídas!")
            
        except Exception as e:
            self.label_status.config(text=e)

    def clear_fields(self):
        """Limpa todos os campos de entrada."""
        self.entry_data.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_produto.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_turma.delete(0, tk.END)

    def connect(self):
        con = sqlite3.connect(self.caminhos['database'])
        cursor = con.cursor()        
        return cursor, con

    def criar(self):
        cursor, con = self.connect()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS cantina (
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
        );''')
        print("Tabela criada com sucesso")

    def apagar_db(self, data, nome, produto, cargo, turma):
        try:
            cursor, con = self.connect()  # Obtém o cursor e a conexão
            query = """
                DELETE FROM cantina
                WHERE data = ?
                AND nome = ?
                AND produto = ?
                AND cargo = ?
                AND turma = ?
            """
            params = (data, nome, produto, cargo, turma)
            
            if cursor.execute(query, params).rowcount == 1:
                con.commit()
                con.close()
                return True
            else:
                con.close()
                return False
            
                
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
    service = DeleteInfo()
    service.main()
