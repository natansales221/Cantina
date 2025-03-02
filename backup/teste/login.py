import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from add_produtos import AddProd




class JanelaPrincipal:

    def __init__(self, janela):
        self.janela = janela
        self.janela.geometry("700x400")
        self.janela.title("Cantina")
        self.janela.iconbitmap("logo.ico")
        self.janela.resizable(False, False)

        self.image = Image.open("45605.png")
        self.image_resized = self.image.resize((350, 350))
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

        self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14))
        self.senha_entry.place(x=25, y=170)

        checkbox = ctk.CTkCheckBox(master=frame, text="Mantenha-me Conectado")
        checkbox.place(x=25, y=235)

        loginBt = ctk.CTkButton(master=frame, text="Login", width=300)
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

    def abrir_recuperar_usuario(self):
        RecuperarUsuario(self.janela)

    def abrir_recuperar_senha(self):
        RecuperarSenha(self.janela)

    def abrir_painel_admin(self):
        PainelAdmin(self.janela)


class PainelAdmin:
    def __init__(self, janela):
        janela.withdraw()  # Esconde a janela principal
        self.painel_adm = ctk.CTkToplevel()  # Janela de administração
        self.painel_adm.geometry("700x400")
        self.painel_adm.title("Cantina")
        self.painel_adm.iconbitmap("logo.ico")
        self.painel_adm.resizable(False, False)

        self.frame = ctk.CTkFrame(master=self.painel_adm, width=350, height=396)
        self.frame.place(x=350, y=2)

        image = Image.open("45605.png")
        image_resized = image.resize((350, 350))
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


class RecuperarUsuario:
    def __init__(self, janela):
        janela.withdraw()
        self.usuario = ctk.CTkToplevel()
        self.usuario.geometry("700x400")
        self.usuario.title("Cantina")
        self.usuario.iconbitmap("logo.ico")
        self.usuario.resizable(False, False)

        frame = ctk.CTkFrame(master=self.usuario, width=350, height=396)
        frame.place(x=350, y=2)

        image = Image.open("45605.png")
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


class RecuperarSenha:
    def __init__(self, janela):
        janela.withdraw()
        self.senha = ctk.CTkToplevel()
        self.senha.geometry("700x400")
        self.senha.title("Cantina")
        self.senha.iconbitmap("logo.ico")
        self.senha.resizable(False, False)

        frame = ctk.CTkFrame(master=self.senha, width=350, height=396)
        frame.place(x=350, y=2)

        image = Image.open("45605.png")
        image_resized = image.resize((350, 350))
        img_tk = ImageTk.PhotoImage(image_resized)
        label_img = ctk.CTkLabel(master=self.senha, image=img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = img_tk

        label = ctk.CTkLabel(master=frame, text="Recuperação de Senha", font=("Bebas Neue", 25), text_color="white")
        label.place(x=25, y=30)

        self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        self.senha_entry.place(x=25, y=105)

        passw1 = ctk.CTkEntry(master=frame, placeholder_text="Confirme sua senha", width=300, font=("Arial", 14), show="*")
        passw1.place(x=25, y=170)

        fechar_bt = ctk.CTkButton(frame, text="Confirmar", command=self.voltar_janela, width=300)
        fechar_bt.place(x=25, y=230)

    def voltar_janela(self):
        senha1 = self.senha_entry.get()
        senha2 = self.passw1.get()

        if senha1 != senha2:
            messagebox.showerror("Erro", "As senhas não coincidem!")
        else:
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")


# Iniciar a aplicação
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    janela = ctk.CTk()
    app = JanelaPrincipal(janela)
    janela.mainloop()
