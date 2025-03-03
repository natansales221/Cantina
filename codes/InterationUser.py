import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

from InsertScreen import InsertInfo

class InterationUser: 
    
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
        self.fgt_pswd = ttk.Button(self.app, text="Visualizar Resumo", command=self.view_resumed_info)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Inserir informações", command=self.insert)
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
        
    def view_resumed_info(self):
        print("view resumed info")
                    
    def create_entry(self, label, row):
        tk.Label(self.app, text=label, anchor="center").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        return entry

    def insert(self):
        self.app.destroy()
        insert_info = InsertInfo()
        insert_info.main()  
        
    def connect(self):
        con = sqlite3.connect(r'db\database.db')
        cursor = con.cursor()        
        return cursor, con

    def criar(self):
        con = sqlite3.connect(r'db\database.db')
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
        
if __name__ == '__main__':
    service = InterationUser()
    service.main()
