import customtkinter as ctk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class InsertInfo():
    
    @property
    def caminhos(self):
        return {
            "excel": "db\\controle_estoque.xlsx",
            "database": "db\\database.db"
        }
    
    def __init__(self, tipo):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("Inserção de informações")
        self.app.geometry("500x400")

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=2)
        self.app.grid_columnconfigure(2, weight=1)

        self.entry_data = self.create_entry("Data", 0)
        self.entry_nome = self.create_entry("Nome", 1)
        self.entry_produto = self.create_entry("Produto", 2)
        self.entry_debito = self.create_entry("Débito", 3)
        self.entry_credito = self.create_entry("Crédito", 4)
        self.entry_cargo = self.create_entry("Cargo", 5)
        self.entry_turma = self.create_entry("Turma", 6)
        self.entry_telefone = self.create_entry("Telefone", 7)
        self.entry_obs = self.create_entry("Observação", 8)

        self.botao_db = ctk.CTkButton(self.app, text="Salvar Database", command=self.salvar_geral, font=("Calibri", 15))
        self.botao_db.grid(row=10, column=0, padx=5, pady=5)
        self.botao_db.configure(width=200, hover_color="#228B22")

        self.botao_excel = ctk.CTkButton(self.app, text="Salvar Excel", command=self.salvar_geral, font=("Calibri", 15))
        self.botao_excel.grid(row=10, column=1, padx=5, pady=5)
        self.botao_excel.configure(width=200, hover_color="#228B22")

        self.botao_erase = ctk.CTkButton(self.app, text="Limpar campos", command=self.clear_fields, font=("Calibri", 15))
        self.botao_erase.grid(row=10, column=2, padx=5, pady=5)
        self.botao_erase.configure(width=200, hover_color="#A0522D")

        self.fgt_user = ctk.CTkButton(self.app, text="Logout", command=self.deslogar, font=("Calibri",15))
        self.fgt_user.grid(row=15, column=2, padx=5, pady=5)
        self.fgt_user.configure(width=200, hover_color="Dark Red")

        self.back = ctk.CTkButton(self.app, text="Voltar", command= lambda: self.retornar(tipo), font=("Calibri", 15))
        self.back.grid(row=15, column=0, padx=5, pady=5)
        self.back.configure(width=200, hover_color="Dark Red")

        self.label_status = ctk.CTkLabel(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        for i in range(12):
            self.app.grid_rowconfigure(i, weight=1)

    def retornar(self, tipo):
        tipo_str = tipo() if callable(tipo) else tipo

        if tipo_str == 'admin':
            from InterationAdmin import InterationAdmin
            self.app.destroy()
            InterationAdmin(tipo_str).main()

        elif tipo_str == 'user':
            from InterationUser import InterationUser
            self.app.destroy()
            InterationUser(tipo_str).main() 


    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        LoginService().main()

    def salvar_geral(self):
        self.salvar_xlsx()
        self.salvar_db()

    def create_entry(self, label, row, default_value=""):
        ctk.CTkLabel(self.app, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = ctk.CTkEntry(self.app)
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        entry.insert(0, default_value)
        return entry

    def formatar_data(self, *args):
        texto = self.entry_data.get().replace("/", "")
        if len(texto) > 8:
            texto = texto[:8]

        novo_texto = ""
        for i, char in enumerate(texto):
            if i in [2, 4]:
                novo_texto += "/"
            novo_texto += char

        self.entry_data.delete(0, 'end')
        self.entry_data.insert(0, novo_texto)

    def salvar_xlsx(self):
        data = self.entry_data.get()
        nome = self.entry_nome.get()
        produto = self.entry_produto.get()
        debito = 0 if self.entry_debito.get() == '' else self.entry_debito.get()
        credito = 0 if self.entry_credito.get() == '' else self.entry_credito.get()
        cargo = self.entry_cargo.get()
        turma = self.entry_turma.get()
        telefone = self.entry_telefone.get()
        observacao = self.entry_obs.get()

        novo_dado = pd.DataFrame([{
            "Data": datetime.strptime(data, '%d/%m/%Y'),
            "Nome": nome,
            "Produto": produto,
            "Débito": debito,
            "Crédito": credito,
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
        self.label_status.configure(text="Dados salvos no Excel!")

    def salvar_db(self):
        try:
            self.inserir(
                data = self.entry_data.get(),
                nome = self.entry_nome.get(),
                produto = self.entry_produto.get(),
                debito = self.entry_debito.get(),
                credito = self.entry_credito.get() if self.entry_credito.get() > '0' else 0,
                cargo = self.entry_cargo.get(),
                turma = self.entry_turma.get(),
                telefone = self.entry_telefone.get(),
                observacao = self.entry_obs.get()
            )
            self.label_status.configure(text="Dados salvos no banco!")
        except Exception as e:
            self.label_status.configure(text=str(e))

    def clear_fields(self):
        for entry in [self.entry_data, self.entry_nome, self.entry_produto,
                      self.entry_debito, self.entry_credito, self.entry_cargo,
                      self.entry_turma, self.entry_telefone, self.entry_obs]:
            entry.delete(0, 'end')

    def connect(self):
        con = sqlite3.connect(self.caminhos['database'])
        return con.cursor(), con

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
        con.close()

    def inserir(self, data, nome, produto, debito, credito, cargo, turma, telefone, observacao):
        try:
            cursor, con = self.connect()
            data = datetime.strptime(data, '%d/%m/%Y')
            total = str(int(credito) - int(debito))
            cursor.execute("""
                INSERT INTO cantina (data, nome, produto, debito, credito, total, cargo, turma, telefone, observacao)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (data, nome, produto, debito, credito, total, cargo, turma, telefone, observacao))
            con.commit()
            con.close()
        except Exception as e:
            raise Exception(f"Erro ao inserir no banco: {e}")

    def main(self):
        self.entry_data.bind("<KeyRelease>", lambda e: self.formatar_data())
        self.app.mainloop()


if __name__ == '__main__':
    service = InsertInfo()
    service.main()
