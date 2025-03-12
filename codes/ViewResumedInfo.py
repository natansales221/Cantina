import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import sqlite3

from InsertScreen import InsertInfo
from EditScreen import EditInfo
from DeleteScreen import DeleteInfo

class ViewResumedInfo: 
    
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Seleção de opções")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.entry_login = self.create_entry("Olá Admin! O que deseja fazer?", 0)

        self.fgt_user = ttk.Button(self.app, text="Inserir informações", command=self.view_resumo)
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Visualizar Dados Resumidos", command=self.view_resumo)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Editar Informações", command=self.view_resumo)
        self.fgt_pswd.grid(row=11, column=0, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Visualizar Dados Completos", command=self.view_completo)
        self.fgt_user.grid(row=11, column=1, sticky="ew", padx=5, pady=5)
        
        self.fgt_pswd = ttk.Button(self.app, text="Excluir Informações", command=self.view_resumo)
        self.fgt_pswd.grid(row=12, column=0, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Visualizar Dados Filtrados", command=self.view_filtro)
        self.fgt_user.grid(row=12, column=1, sticky="ew", padx=5, pady=5)
        
        self.back = ttk.Button(self.app, text="logout", command=self.deslogar)
        self.back.grid(row=15, column=1, sticky="ew", padx=5, pady=5)
        
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=13, column=0, columnspan=3, sticky="ew")

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

    def view_resumo(self):
        print("view resumo")
        
    def view_completo(self):
        print("view resumo")
        
    def view_filtro(self):
        print("view resumo")
            
    def main(self):
        self.app.mainloop()
        
        
if __name__ == '__main__':
    service = ViewResumedInfo()
    service.main()

    import sqlite3
    import customtkinter as ctk


    def carregar_produtos():
        categoria = combo_categoria.get()  # Pegando valor do ComboBox
        conn = sqlite3.connect("mercado.db")
        cursor = conn.cursor()

        # Se a categoria for "Todos", busca tudo, senão filtra pela categoria escolhida
        if categoria == "Todos":
            cursor.execute("SELECT nome, preco FROM produtos")
        else:
            cursor.execute("SELECT nome, preco FROM produtos WHERE categoria = ?", (categoria,))

        produtos = cursor.fetchall()
        conn.close()

        # Limpar a lista antes de adicionar os novos itens
        listbox.delete("0.0", "end")

        # Adicionar os produtos na listbox
        for produto in produtos:
            listbox.insert("end", f"{produto[0]} - R$ {produto[1]:.2f}\n")


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("400x350")
    root.title("Filtro de Produtos")


    label = ctk.CTkLabel(root, text="Filtrar por Categoria:", font=("Arial", 14))
    label.pack(pady=10)

    combo_categoria = ctk.CTkComboBox(root, values=["Todos", "Alimentos", "Limpeza", "Bebidas"], command=lambda event: carregar_produtos())
    combo_categoria.pack()
    combo_categoria.set("Todos")  # Define a opção inicial como "Todos"

    btn_carregar = ctk.CTkButton(root, text="Filtrar", command=carregar_produtos)
    btn_carregar.pack(pady=10)

    listbox = ctk.CTkTextbox(root, width=350, height=200)
    listbox.pack(pady=10)


    root.mainloop()