import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

from InsertScreen import InsertInfo
from EditScreen import EditInfo
from DeleteScreen import DeleteInfo

class InterationAdmin: 
    
    def __init__(self, tipo):
        self.app = tk.Tk()
        self.app.title("Seleção de opções")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Criando os campos e armazenando em atributos da classe
        self.entry_login = self.create_entry("Olá Admin! O que deseja fazer?", 0)

        # Botões
        self.fgt_user = ttk.Button(self.app, text="Inserir informações", command=lambda: self.insert(tipo))
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Visualizar Dados Resumidos", command=self.view_resumo)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Editar Informações", command=lambda: self.edit_info(tipo))
        self.fgt_pswd.grid(row=11, column=0, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Visualizar Dados Completos", command=self.view_completo)
        self.fgt_user.grid(row=11, column=1, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Excluir Informações", command=lambda: self.excluir_info(tipo))
        self.fgt_pswd.grid(row=12, column=0, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Visualizar Dados Filtrados", command=self.view_filtro)
        self.fgt_user.grid(row=12, column=1, sticky="ew", padx=5, pady=5)
        
        self.back = ttk.Button(self.app, text="logout", command=self.deslogar)
        self.back.grid(row=15, column=1, sticky="ew", padx=5, pady=5)
        
        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=13, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()  
                                  
    def create_entry(self, label, row):
        tk.Label(self.app, text=label, anchor="center").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app)
        return entry

    def insert(self, tipo):
        self.app.destroy()
        insert_info = InsertInfo(tipo)
        insert_info.main()        

    def edit_info(self, tipo):
        self.app.destroy()
        edit_info = EditInfo(tipo)
        edit_info.main()  
        
    def excluir_info(self, tipo):
        self.app.destroy()
        edit_info = DeleteInfo(tipo)
        edit_info.main()  
        
    def view_resumo(self):
        print("view resumo")
        
    def view_completo(self):
        print("view resumo")
        
    def view_filtro(self):
        print("view resumo")
            
    def main(self):
        self.app.mainloop()
        
        
if __name__ == '__main__':
    service = InterationAdmin()
    service.main()
