import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from add_produtos import AddProd
import sqlite3

class PainelAdmin:
    def __init__(self, janela):
        janela.withdraw()  # Esconde a janela principal
        self.painel_adm = ctk.CTkToplevel()  # Janela de administração
        self.painel_adm.geometry("700x400")
        self.painel_adm.title("Cantina")
        self.painel_adm.iconbitmap(r"C:\Users\renan\Downloads\Cantina\backup\teste\logo.ico")
        self.painel_adm.resizable(False, False)

        self.frame = ctk.CTkFrame(master=self.painel_adm, width=350, height=396)
        self.frame.place(x=350, y=2)

        image = Image.open(r"C:\Users\renan\Downloads\Cantina\backup\teste\45605.png")
        image_resized = image.resize((300, 300))
        img_tk = ImageTk.PhotoImage(image_resized)

        label_img = ctk.CTkLabel(master=self.painel_adm, image=img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = img_tk

        label = ctk.CTkLabel(master=self.frame, text="Acesso Admins", font=("Bebas Neue", 25), text_color="white")
        label.place(x=25, y=30)

        self.admin_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Insira seu usuário", width=300, font=("Arial", 14))
        self.admin_entry.place(x=25, y=105)

        self.senha_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        self.senha_entry.place(x=25, y=170)

        confirmar_bt = ctk.CTkButton(self.frame, text="Confirmar", command=self.validar_admin, width=300)
        confirmar_bt.place(x=25, y=230)

    def validar_admin(self):
        adm = self.admin_entry.get()
        pssw = self.senha_entry.get()

        if adm == "admin" and pssw == "0000":
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.painel_adm.withdraw()  # Esconde a janela de login do administrador
            self.add_prod_window = AddProd()  # Cria a janela para adicionar produtos
            self.add_prod_window.run()  # Executa a janela de adicionar produtos
        elif not adm or not pssw:
            messagebox.showerror("Erro", "Os campos de usuário e senha não podem estar vazios!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")