import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from add_produtos import AddProd
from painel_admin import PainelAdmin
from usuario import RecuperarUsuario
from senha import RecuperarSenha
import sqlite3

class JanelaPrincipal:
    def __init__(self, janela):
        self.janela = janela
        self.janela.geometry("700x400")
        self.janela.title("Cantina")
        self.janela.iconbitmap(r"C:\Users\renan\Downloads\Cantina\backup\teste\logo.ico")
        self.janela.resizable(False, False)

        self.image = Image.open(r"C:\Users\renan\Downloads\Cantina\backup\teste\45605.png")
        self.image_resized = self.image.resize((300, 300))
        self.img_tk = ImageTk.PhotoImage(self.image_resized)

        label_img = ctk.CTkLabel(master=self.janela, image=self.img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = self.img_tk

        frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        frame.place(x=350, y=2)

        label = ctk.CTkLabel(master=frame, text="Gerenciamento de Vendas", font=("Bebas Neue", 25), text_color="white")
        label.place(x=25, y=30)

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira seu usuário", width=300, font=("Arial", 14))
        self.user_entry.place(x=25, y=105)

        self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        self.senha_entry.place(x=25, y=170)

        checkbox = ctk.CTkCheckBox(master=frame, text="Mantenha-me Conectado")
        checkbox.place(x=25, y=235)

        loginBt = ctk.CTkButton(master=frame, text="Login", width=300, command=self.verificar_login)
        loginBt.place(x=25, y=280)

        # Links
        linkU = ctk.CTkLabel(master=frame, text="Recuperar usuário", font=("Arial", 12), text_color="lightblue", cursor="hand2")
        linkU.place(x=25, y=310)
        linkU.bind("<Button-1>", lambda e: self.abrir_recuperar_usuario())

        linkS = ctk.CTkLabel(master=frame, text="Recuperar senha", font=("Arial", 12), text_color="lightblue", cursor="hand2")
        linkS.place(x=140, y=310)
        linkS.bind("<Button-1>", lambda e: self.abrir_recuperar_senha())

        linkA = ctk.CTkLabel(master=frame, text="Acesso Admin", font=("Arial", 12), text_color="lightblue", cursor="hand2")
        linkA.place(x=250, y=310)
        linkA.bind("<Button-1>", lambda e: self.abrir_painel_admin())

    def verificar_login(self):
        """ Verifica se o usuário e senha estão corretos no banco de dados """
        usuario = self.user_entry.get()
        senha = self.senha_entry.get()

        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        # Conectar ao banco de dados
        con = sqlite3.connect("cantina.db")
        cur = con.cursor()

        # Buscar usuário no banco
        cur.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
        usuario_encontrado = cur.fetchone()
        con.close()

        if usuario_encontrado:
            messagebox.showinfo("Seja Bem-Vindo", f"Login realizado com sucesso!")
            # Aqui você pode abrir a próxima tela
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_recuperar_usuario(self):
        RecuperarUsuario(self.janela)

    def abrir_recuperar_senha(self):
        RecuperarSenha(self.janela)

    def abrir_painel_admin(self):
        PainelAdmin(self.janela)
    
# Iniciar a aplicação
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    janela = ctk.CTk()
    app = JanelaPrincipal(janela)
    janela.mainloop()
