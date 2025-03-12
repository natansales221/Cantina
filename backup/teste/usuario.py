import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3

class RecuperarUsuario:
    def __init__(self, janela):
        janela.withdraw()
        self.usuario = ctk.CTkToplevel()
        self.usuario.geometry("700x400")
        self.usuario.title("Cantina")
        self.usuario.iconbitmap(r"C:\Users\renan\Downloads\Cantina\backup\teste\logo.ico")
        self.usuario.resizable(False, False)

        frame = ctk.CTkFrame(master=self.usuario, width=350, height=396)
        frame.place(x=350, y=2)

        image = Image.open(r"C:\Users\renan\Downloads\Cantina\backup\teste\45605.png")
        image_resized = image.resize((350, 350))
        img_tk = ImageTk.PhotoImage(image_resized)
        label_img = ctk.CTkLabel(master=self.usuario, image=img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = img_tk

        label = ctk.CTkLabel(master=frame, text="Recuperação de Usuário", font=("Bebas Neue", 25), text_color="white")
        label.place(x=25, y=30)

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira seu usuário", width=300, font=("Arial", 14))
        self.user_entry.place(x=25, y=105)

        passw1 = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        passw1.place(x=25, y=170)

        passw2 = ctk.CTkEntry(master=frame, placeholder_text="Confirme sua senha", width=300, font=("Arial", 14), show="*")
        passw2.place(x=25, y=230)

        fechar_bt = ctk.CTkButton(frame, text="Confirmar", command=self.voltar_janela, width=300)
        fechar_bt.place(x=25, y=300)

    def voltar_janela(self):
        user = self.user_entry.get()
        senha1 = self.passw1.get()
        senha2 = self.passw2.get()

        if not user:
            messagebox.showerror("Erro", "O campo de usuário não pode estar vazio!")
        elif not senha1 or not senha2:
            messagebox.showerror("Erro", "Os campos de senha não podem estar vazios!")
        elif senha1 != senha2:
            messagebox.showerror("Erro", "As senhas não coincidem!")
        else:
            messagebox.showinfo("Sucesso", "Senha cadastrada com sucesso!")