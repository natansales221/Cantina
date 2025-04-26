import customtkinter as ctk
import os
import pandas as pd
import sqlite3
from datetime import datetime

class DeleteInfo:
    
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
        self.app.title("Exclusão de Informações")
        self.app.geometry("600x400")

        self.entry_data_var = ctk.StringVar()
        self.entry_data_var.trace_add("write", self.formatar_data)

        self.create_entry("Data", 0, self.entry_data_var)
        self.entry_nome = self.create_entry("Nome", 1)
        self.entry_produto = self.create_entry("Produto", 2)
        self.entry_cargo = self.create_entry("Cargo", 3)


        self.botao_db = ctk.CTkButton(self.app, text="Apagar dados acima", command=self.exclusao)
        self.botao_db.grid(row=10, column=0, padx=5, pady=5, sticky="ew")
        self.botao_db.configure(fg_color="#993e02")
        
        self.botao_erase = ctk.CTkButton(self.app, text="Limpar campos", command=self.clear_fields)
        self.botao_erase.grid(row=10, column=1, padx=5, pady=5, sticky="ew")
        
        self.botao_erase_all = ctk.CTkButton(self.app, text="APAGAR TODAS AS INFORMAÇÕES", command=self.exclusao_geral)
        self.botao_erase_all.grid(row=10, column=2, padx=5, pady=5, sticky="ew")
        self.botao_erase_all.configure(width=200, fg_color="#990202")
        
        self.botao_voltar = ctk.CTkButton(self.app, text="Voltar", command=lambda: self.retornar(tipo))
        self.botao_voltar.grid(row=15, column=0, padx=5, pady=5, sticky="ew")

        self.botao_logout = ctk.CTkButton(self.app, text="Logout", command=self.deslogar)
        self.botao_logout.grid(row=15, column=1, padx=5, pady=5, sticky="ew")

        self.label_status = ctk.CTkLabel(self.app, text="", fg_color="transparent")
        self.label_status.grid(row=12, column=0, columnspan=2, sticky="ew")

        for i in range(12):
            self.app.rowconfigure(i, weight=1)

    def create_entry(self, label, row, var=None):
        label_widget = ctk.CTkLabel(self.app, text=label + ":")
        label_widget.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

        entry_var = var if var else ctk.StringVar()
        entry = ctk.CTkEntry(self.app, textvariable=entry_var, width=200)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        return entry

    def formatar_data(self, *args):
        """ Formata a entrada da data automaticamente (dd/mm/yyyy). """
        texto = self.entry_data_var.get().replace("/", "")
        if len(texto) > 8:
            texto = texto[:8]

        novo_texto = ""
        for i, char in enumerate(texto):
            if i in [2, 4]:
                novo_texto += "/"
            novo_texto += char

        self.entry_data_var.set(novo_texto)

    def exclusao(self):
        self.apagar()
        self.apagar_xlsx()

    def apagar_xlsx(self):
        data = self.entry_data_var.get()
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()
        produto = self.entry_produto.get()


        arquivo_excel = self.caminhos['excel']

        if os.path.exists(arquivo_excel):
            df_existente = pd.read_excel(arquivo_excel)
            filt_nome = df_existente[df_existente['Nome'].str.upper() == nome.upper()]
            filt_prod = filt_nome[filt_nome['Produto'].str.upper() == produto.upper()]
            filt_data = filt_prod[filt_prod['Data'] == datetime.strptime(data, '%d/%m/%Y')]
            filt_cargo = filt_data[filt_data['Cargo'].str.upper() == cargo.upper()]
  
            df_filtrado = df_existente[~df_existente.index.isin(filt_cargo.index)]
            df_final = df_filtrado.reset_index(drop=True)
        else:
            df_final = pd.DataFrame([{
                "Data": datetime.strptime(data, '%d/%m/%Y'),
                "Nome": nome,
                "Produto": produto,
                "Cargo": cargo,
            }])

        df_final.to_excel(arquivo_excel, index=False)
        self.label_status.configure(text="Dados apagados no Excel!")

    def apagar(self):
        data = self.entry_data_var.get()
        nome = self.entry_nome.get()
        produto = self.entry_produto.get()
        cargo = self.entry_cargo.get()

        try:
            if self.apagar_db(data, nome, produto, cargo):
                self.label_status.configure(text="Dados apagados no banco!")
            else:
                self.label_status.configure(text="Favor revisar as informações a serem excluídas!")
        except Exception as e:
            self.label_status.configure(text=str(e))

    def clear_fields(self):
        """Limpa todos os campos de entrada."""
        self.entry_data_var.set("")
        self.entry_nome.delete(0, "end")
        self.entry_produto.delete(0, "end")
        self.entry_cargo.delete(0, "end")


    def connect(self):
        con = sqlite3.connect(self.caminhos['database'])
        cursor = con.cursor()        
        return cursor, con

    def apagar_db(self, data, nome, produto, cargo):
        try:
            data = datetime.strptime(data, '%d/%m/%Y')
            cursor, con = self.connect()
            query = """
                DELETE FROM cantina
                WHERE data = ?
                AND nome = ?
                AND produto = ?
                AND cargo = ?
            """
            params = (data, nome, produto, cargo)
            
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
        
    def exclusao_geral(self):
        try:
            cursor, con = self.connect()
            query = "DELETE FROM cantina"
            cursor.execute(query)
            con.commit()
            return True
        except Exception as e:
            print(f"Erro ao limpar tabela: {e}")
            raise
        finally:
            if con:
                con.close()
                
    def retornar(self, tipo):
        if tipo.upper() == 'ADMIN':
            from InterationAdmin import InterationAdmin
            self.app.destroy()
            InterationAdmin(tipo).main()
        elif tipo.upper() == 'USER':
            from InterationUser import InterationUser
            self.app.destroy()
            InterationUser(tipo).main()

    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        LoginService().main()

    def main(self):
        self.app.mainloop()

if __name__ == '__main__':
    service = DeleteInfo()
    service.main()
