import customtkinter as ctk
import os
import pandas as pd
import sqlite3

from InsertScreen import InsertInfo
from EditScreen import EditInfo
from DeleteScreen import DeleteInfo

class InterationAdmin:
    
    def __init__(self, tipo):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("Seleção de opções")
        self.app.geometry("500x400")

        self.entry_login = ctk.CTkLabel(self.app, text="Olá Admin! O que deseja fazer?", font=("Helvetica", 16))
        self.entry_login.pack(pady=10)
        
        self.insert_button = ctk.CTkButton(self.app, text="Inserir informações", command=lambda: self.insert(tipo))
        self.insert_button.pack(pady=5)
        
        self.view_resumo_button = ctk.CTkButton(self.app, text="Visualizar Dados Resumidos", command=self.view_resumo)
        self.view_resumo_button.pack(pady=5)
        
        self.edit_button = ctk.CTkButton(self.app, text="Editar Informações", command=lambda: self.edit_info(tipo))
        self.edit_button.pack(pady=5)
        
        self.view_completo_button = ctk.CTkButton(self.app, text="Visualizar Dados Completos", command=self.view_completo)
        self.view_completo_button.pack(pady=5)
        
        self.delete_button = ctk.CTkButton(self.app, text="Excluir Informações", command=lambda: self.excluir_info(tipo))
        self.delete_button.pack(pady=5)
        
        self.view_filtro_button = ctk.CTkButton(self.app, text="Visualizar Dados Filtrados", command=self.view_filtro)
        self.view_filtro_button.pack(pady=5)
        
        self.logout_button = ctk.CTkButton(self.app, text="Logout", command=self.deslogar)
        self.logout_button.pack(pady=10)
        
        self.label_status = ctk.CTkLabel(self.app, text="", font=("Helvetica", 12))
        self.label_status.pack()

    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()
        
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
        print("view completo")
        
    def view_filtro(self):
        print("view filtro")
        
    def main(self):
        self.app.mainloop()
        
if __name__ == '__main__':
    service = InterationAdmin()
    service.main()
