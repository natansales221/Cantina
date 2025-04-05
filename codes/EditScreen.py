import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class EditInfo:
    
    @property
    def caminhos(self):
        return {
            "excel":"db\\controle_estoque.xlsx",
            "database":"db\\database.db"
        }
    
    def __init__(self, tipo):
        self.app = tk.Tk()
        self.app.title("Edição de informações")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.entry_data = self.create_entry("Data", 0)
        self.entry_nome = self.create_entry("Nome", 1)
        self.entry_produto = self.create_entry("Produto", 2)
        self.entry_debito = self.create_entry("Débito", 3)
        self.entry_credito = self.create_entry("Crédito", 4)
        self.entry_cargo = self.create_entry("Cargo", 5)
        self.entry_turma = self.create_entry("Turma", 6)

        self.botao_db = ttk.Button(self.app, text="Editar informações", command=self.salvar_geral)
        self.botao_db.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.botao_erase = ttk.Button(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=10, column=2, sticky="ew", padx=5, pady=5)
        
        self.fgt_user = ttk.Button(self.app, text="Logout", command=self.deslogar)
        self.fgt_user.grid(row=15, column=2, sticky="ew", padx=5, pady=5)
        
        self.back = ttk.Button(self.app, text="Voltar", command=lambda: self.retornar(tipo))
        self.back.grid(row=15, column=0, sticky="ew", padx=5, pady=5)
        
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        for i in range(12):
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
        texto = self.entry_data.get().replace("/", "")
        if len(texto) > 8:
            texto = texto[:8]

        novo_texto = ""
        for i, char in enumerate(texto):
            if i in [2, 4]:
                novo_texto += "/"
            novo_texto += char

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
        novo_dado = pd.DataFrame([{
            "Data": datetime.strptime(data, '%d/%m/%Y'),
            "Nome": nome,
            "Produto": produto,
            "Débito": debito,
            "Crédito": 0 if credito == '' else credito,
            "Total": str(int(credito) - int(debito)),
            "Cargo": cargo,
            "Turma": turma,
        }])

        arquivo_excel = self.caminhos['excel']

        if os.path.exists(arquivo_excel):
            df_existente = pd.read_excel(arquivo_excel)
            filt_nome = df_existente[df_existente['Nome'] == nome]
            filt_prod = filt_nome[filt_nome['Produto'] == produto]
            filt_data = filt_prod[filt_prod['Data'] == datetime.strptime(data, '%d/%m/%Y')]
            filt_cargo = filt_data[filt_data['Cargo'] == cargo]
            filt_turma = filt_cargo[filt_cargo['Turma'] == turma]
            
            df_filtrado = df_existente[~(df_existente == filt_turma.iloc[0]).all(axis=1)]

            filt_turma['Débito'] = debito
            filt_turma['Crédito'] = 0 if credito == '' else credito
            filt_turma['Total'] = str(int(credito) - int(debito))

            novo_dado = filt_turma
            df_final = pd.concat([df_filtrado, novo_dado], ignore_index=True)
            df_final = df_final.reset_index(drop=True)
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
        try:
            if self.atualizar(data, nome, produto, debito, credito, cargo, turma):
                self.label_status.config(text="Dados salvos no banco!")
            else:
                self.label_status.config(text="Favor revisar as informações a serem alteradas!")
            
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

    def atualizar(self, data, nome, produto, debito, credito, cargo, turma):
        try:
            cursor, con = self.connect()
            data = datetime.strptime(data, '%d/%m/%Y')
            nome = nome
            produto = produto
            debito = debito
            credito = 0 if credito == '' else credito
            total = str(int(credito) - int(debito))
            cargo = cargo
            turma = turma 
            query = """
                UPDATE cantina 
                SET debito = (?),
                credito = (?),
                total = (?)
                WHERE data = (?)
                AND nome = (?)
                AND produto = (?)
                AND cargo = (?)
                AND turma = (?)
            """
            params = (debito, credito, total, data, nome, produto, cargo, turma)
            
            if cursor.execute(query, params).connection.in_transaction:
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
        self.entry_data_var = tk.StringVar()
        self.entry_data.config(textvariable=self.entry_data_var)
        self.entry_data_var.trace_add("write", self.formatar_data)
        
        self.app.mainloop()


if __name__ == '__main__':
    service = EditInfo()
    service.main()