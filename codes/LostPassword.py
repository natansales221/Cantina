import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

from LoginScreen import login_screen


class LostPassword: 
    
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Alteração de senha")
        
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Botões
        self.fgt_pswd = ttk.Button(self.app, text="Alterar Senha", command=self.submit_forgot_password)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.entry_forgot_name = self.create_entry_in_window("Confirme seu nome", 2, self.app)
        self.entry_forgot_last_name = self.create_entry_in_window("Confirme seu sobrenome", 3, self.app)
        self.entry_forgot_date = self.create_entry_in_window("Confirme sua data de nascimento", 4, self.app)
        self.entry_forgot_password = self.create_entry_in_window("Senha Nova", 5, self.app, is_password=True)
        
        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
                            
    def create_entry_in_window(self, label, row, window, is_password=False):
        tk.Label(window, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(window, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        return entry

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

        else:
            self.label_status.config(text="Não foi possível alterar a senha")
       
if __name__ == '__main__':
    service = LostPassword()
    service.main()
    