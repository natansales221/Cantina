import sqlite3

import tkinter as tk
from tkinter import ttk
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk


from InterationUser import InterationUser
from InterationAdmin import InterationAdmin

class LoginService: 
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue") 
        self.app = ctk.CTk()
        self.app.title("Cantina")
        self.app.geometry("700x400")
        self.app.iconbitmap(r"backup\teste\logo.ico")
        
        self.image = Image.open(r"backup\teste\45605.png")
        self.image_resized = self.image.resize((350, 350))
        self.img_tk = ImageTk.PhotoImage(self.image_resized)
        
        label_img = ctk.CTkLabel(master=self.app, image=self.img_tk, text="")
        label_img.place(x=30, y=55)
        label_img.image = self.img_tk
        
        frame = ctk.CTkFrame(master=self.app, width=350, height=396)
        frame.place(x=350, y=2)
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Login", width=300, font=("Arial", 14))
        self.user_entry.place(x=25, y=105)
        
        self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
        self.senha_entry.place(x=25, y=170)
        
        linkU = ctk.CTkLabel(master=frame, text="Recuperar usuário", font=("Arial", 12), text_color="lightblue", cursor="hand2")
        linkU.place(x=25, y=310)
        linkU.bind("<Button-1>", lambda event: self.lost_user())    
            
        linkS = ctk.CTkLabel(master=frame, text="Recuperar senha", font=("Arial", 12), text_color="lightblue", cursor="hand2")
        linkS.place(x=140, y=310)
        linkS.bind("<Button-1>", lambda event: self.lost_password())

        # Botões
        # self.fgt_pswd = ttk.Button(self.app, text="Esqueci a senha", command=self.lost_password)
        # self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        # self.fgt_user = ttk.Button(self.app, text="Esqueci o usuario", command=self.lost_user)
        # self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        # self.login_button = ttk.Button(self.app, text="Login", command=self.login_bt)
        # self.login_button.grid(row=10, column=2, sticky="ew", padx=5, pady=5)

        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
        
    def lost_password(self):
        # Open a new window for forgotten user
        self.forgot_pwd_window = tk.Toplevel(self.app)
        self.forgot_pwd_window.title("Recuperar Senha")

        # Create new fields for forgotten user window
        self.entry_forgot_name = self.create_entry_in_window("Confirme seu nome", 0, self.forgot_pwd_window)
        self.entry_forgot_last_name = self.create_entry_in_window("Confirme seu sobrenome", 1, self.forgot_pwd_window)
        self.entry_forgot_date = self.create_entry_in_window("Confirme sua data de nascimento", 2, self.forgot_pwd_window)
        self.entry_forgot_password = self.create_entry_in_window("Senha Nova", 3, self.forgot_pwd_window, is_password=True)
        
        self.submit_button = ttk.Button(self.forgot_pwd_window, text="Enviar", command=self.submit_forgot_password)
        self.submit_button.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
                    
    def lost_user(self):        
        # Open a new window for forgotten user
        self.forgot_user_window = tk.Toplevel(self.app)
        self.forgot_user_window.title("Recuperar Usuário")

        # Create new fields for forgotten user window
        self.entry_forgot_name = self.create_entry_in_window("Nome", 0, self.forgot_user_window)
        self.entry_forgot_last_name = self.create_entry_in_window("Sobrenome", 1, self.forgot_user_window)
        
        self.submit_button = ttk.Button(self.forgot_user_window, text="Enviar", command=self.submit_forgot_user)
        self.submit_button.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
    def create_entry_in_window(self, label, row, window, is_password=False):
        tk.Label(window, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(window, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        return entry

    def submit_forgot_user(self):
        cursor, con = self.connect()
        lost_name = self.entry_forgot_name.get()
        lost_sobrenome = self.entry_forgot_last_name.get()
        
        query = """
        SELECT login from login_cantina
        WHERE nome = (?)
        AND sobrenome = (?)
            """
        params = (lost_name, lost_sobrenome)
        
        if cursor.execute(query, params).rowcount != 0:
            con.commit()
            login_novo = cursor.fetchall()[0][0]

            self.label_status.config(text=f"Seu usuário é {login_novo}")
            self.forgot_user_window.destroy()
        else:
            self.label_status.config(text="Não foi possível encontrar um usuário")
            self.forgot_user_window.destroy()
            
    def login_bt(self):
        cursor, con = self.connect()
        login = self.entry_login.get()
        password = self.entry_pswd.get()
        
        query = """
                SELECT login, senha, tipo from login_cantina
                WHERE login = (?)
            """
        params = (login,)
        cursor.execute(query, params)
        try:
            login_valid, password_valid, tipo = cursor.fetchall()[0]

            if login == login_valid and password == password_valid:
                self.label_status.config(text="Login realizado com sucesso")
                if tipo.upper() == 'ADMIN':
                    self.app.destroy()
                    tela = InterationAdmin(tipo)
                    tela.main()
                elif tipo.upper() == 'USER':
                    self.app.destroy()
                    tela = InterationUser(tipo)
                    tela.main()
                
            else:
                self.label_status.config(text="Login ou senha inválido!")
        except:
            self.label_status.config(text="Login ou senha inválido!")
        
    def connect(self):
        conn = sqlite3.connect(r'db\database.db')
        cursor = conn.cursor()        
        return cursor, conn

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

        params = ('admin', 'admin', 'admin', 'admin', 'admin', '30/09/2000')
        
        cursor.execute(query, params)
        
        con.commit()
        
        # cursor.execute('drop table login_cantina')
        print("Tabela criada com sucesso")

    def main(self):
        self.app.mainloop()
        
    def submit_forgot_password(self):
        try:
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
                self.forgot_pwd_window.destroy()
            else:
                self.label_status.config(text="Não foi possível alterar a senha")
                self.forgot_pwd_window.destroy()
            con.close()
        except:
            self.label_status.config(text="Não foi possível alterar a senha")
            self.forgot_pwd_window.destroy()
            con.close()
        
        
if __name__ == '__main__':
    service = LoginService()
    service.main()
    