
import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3

class RecuperarSenha:
    def __init__(self, janela):
        self.janela = janela  # Armazena a referência da janela principal
        janela.withdraw()  # Esconde a janela principal

        self.senha = ctk.CTkToplevel()
        self.senha.geometry("700x400")
        self.senha.title("Cantina")
        self.senha.iconbitmap(r"C:\Users\renan\Downloads\Cantina\backup\teste\logo.ico")
        self.senha.resizable(False, False)

        frame = ctk.CTkFrame(master=self.senha, width=350, height=396)
        frame.place(x=350, y=2)

        image = Image.open(r"C:\Users\renan\Downloads\Cantina\backup\teste\45605.png")
        image_resized = image.resize((350, 350))
        img_tk = ImageTk.PhotoImage(image_resized)
        label_img = ctk.CTkLabel(master=self.senha, image=img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = img_tk  # Mantém a referência da imagem

        label = ctk.CTkLabel(master=frame, text="Recuperação de Senha", font=("Bebas Neue", 25), text_color="white")
        label.place(x=25, y=30)

        self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        self.senha_entry.place(x=25, y=105)

        self.passw1 = ctk.CTkEntry(master=frame, placeholder_text="Confirme sua senha", width=300, font=("Arial", 14), show="*")
        self.passw1.place(x=25, y=170)

        fechar_bt = ctk.CTkButton(frame, text="Confirmar", command=self.voltar_janela, width=300)
        fechar_bt.place(x=25, y=230)

    def voltar_janela(self):
        senha1 = self.senha_entry.get()
        senha2 = self.passw1.get()

        if senha1 != senha2:
            messagebox.showerror("Erro", "As senhas não coincidem!")
        else:
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
            self.senha.destroy()
            self.janela.deiconify()  # Reexibe a janela principal
