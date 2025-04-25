import customtkinter as ctk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class EditInfo:

    @property
    def caminhos(self):
        return {
            "excel": "Cantina\\db\\controle_estoque.xlsx",
            "database": "Cantina\\db\\database.db"
        }

    def __init__(self, tipo):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("Edição de informações")
        self.app.geometry("600x600")
        
        self.entry_data = self.create_entry("Data", 0)
        self.entry_nome = self.create_entry("Nome", 1)
        self.entry_produto = self.create_entry("Produto", 2)
        self.entry_debito = self.create_entry("Débito", 3)
        self.entry_credito = self.create_entry("Crédito", 4)
        self.entry_cargo = self.create_entry("Cargo", 5)
        self.entry_turma = self.create_entry("Turma", 6)

        self.botao_db = ctk.CTkButton(self.app, text="Editar informações", command=self.salvar_geral)
        self.botao_db.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.botao_erase = ctk.CTkButton(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.fgt_user = ctk.CTkButton(self.app, text="Logout", command=self.deslogar)
        self.fgt_user.grid(row=13, column=2, padx=10, pady=10, sticky="ew")

        self.back = ctk.CTkButton(self.app, text="Voltar", command=lambda: self.retornar(tipo))
        self.back.grid(row=13, column=0, padx=10, pady=10, sticky="ew")

        self.label_status = ctk.CTkLabel(self.app, text="")
        self.label_status.grid(row=12, column=0, columnspan=3, pady=5, sticky="ew")

        for i in range(14):
            self.app.grid_rowconfigure(i, weight=1)
            self.app.grid_columnconfigure(i % 3, weight=1)

    def retornar(self, tipo):
        if tipo.upper() == 'ADMIN':
            from InterationAdmin import InterationAdmin
            self.app.destroy()
            InterationAdmin(tipo).main()

        if tipo.upper() == 'USER':
            from InterationUser import InterationUser
            self.app.destroy()
            InterationUser(tipo).main()

    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        LoginService().main()

    def salvar_geral(self):
        self.salvar_xlsx()
        self.salvar_db()

    def create_entry(self, label, row, default_value=""):
        label_widget = ctk.CTkLabel(self.app, text=label + ":")
        label_widget.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        entry = ctk.CTkEntry(self.app)
        entry.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
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

        self.entry_data.delete(0, "end")
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
        else:
            df_final = novo_dado

        df_final.to_excel(arquivo_excel, index=False)
        self.label_status.configure(text="Dados salvos no Excel!")

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
                self.label_status.configure(text="Dados salvos no banco!")
            else:
                self.label_status.configure(text="Favor revisar as informações a serem alteradas!")
        except Exception as e:
            self.label_status.configure(text=str(e))

    def clear_fields(self):
        for entry in [self.entry_data, self.entry_nome, self.entry_produto, self.entry_debito,
                      self.entry_credito, self.entry_cargo, self.entry_turma]:
            entry.delete(0, "end")

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
        con.commit()
        con.close()

    def atualizar(self, data, nome, produto, debito, credito, cargo, turma):
        try:
            cursor, con = self.connect()
            data = datetime.strptime(data, '%d/%m/%Y')
            total = str(int(credito) - int(debito)) if credito and debito else "0"
            query = """
                UPDATE cantina 
                SET debito = ?, credito = ?, total = ?
                WHERE data = ? AND nome = ? AND produto = ? AND cargo = ? AND turma = ?
            """
            params = (debito, credito, total, data, nome, produto, cargo, turma)
            cursor.execute(query, params)
            atualizado = cursor.rowcount > 0
            con.commit()
            con.close()
            return atualizado
        except Exception as e:
            print(f"Erro: {e}")
            raise

    def main(self):
        self.entry_data_var = ctk.StringVar()
        self.entry_data.configure(textvariable=self.entry_data_var)
        self.entry_data_var.trace_add("write", self.formatar_data)
        self.app.mainloop()


if __name__ == '__main__':
    service = EditInfo()
    service.main()
