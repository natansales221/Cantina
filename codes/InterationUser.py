import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

from InsertScreen import InsertInfo

class InterationUser: 
    
    def __init__(self, tipo):
        self.app = tk.Tk()
        self.app.title("Seleção de opções")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.entry_login = self.create_entry("Olá Usuário! O que deseja fazer?", 0)

        self.fgt_pswd = ttk.Button(self.app, text="Visualizar Resumo", command=self.view_resumed_info)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Inserir informações", command=lambda: self.insert(tipo))
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.back = ttk.Button(self.app, text="logout", command=self.deslogar)
        self.back.grid(row=15, column=1, sticky="ew", padx=5, pady=5)

        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        for i in range(12):
            self.app.rowconfigure(i, weight=1)
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()  
           
    def view_resumed_info(self):
        print("view resumed info")
                    
    def create_entry(self, label, row):
        tk.Label(self.app, text=label, anchor="center").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        return entry

    def insert(self, tipo):
        self.app.destroy()
        insert_info = InsertInfo(tipo)
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
        con.close()
        
        # cursor.execute('drop table login_cantina')
        print("Tabela criada com sucesso")

    def main(self):
        self.app.mainloop()
                
if __name__ == '__main__':
    service = InterationUser()
    service.main()
