import tkinter as tk
from tkinter import ttk
import sqlite3

from InterationUser import InterationUser
from InterationAdmin import InterationAdmin

class LoginScreen: 
    
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Login")
        
        style = ttk.Style()
        style.configure("TButton", foreground="black", font=("Helvetica", 12))

        # Configura as colunas para expandirem horizontalmente
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        # Criando os campos e armazenando em atributos da classe
        self.entry_login = self.create_entry("Login", 0)
        self.entry_pswd = self.create_entry("Senha", 1, is_password=True)

        # Botões
        self.fgt_pswd = ttk.Button(self.app, text="Esqueci a senha", command=self.lost_password)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.fgt_user = ttk.Button(self.app, text="Esqueci o usuario", command=self.lost_user)
        self.fgt_user.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        self.login_button = ttk.Button(self.app, text="Login", command=self.login_bt)
        self.login_button.grid(row=10, column=2, sticky="ew", padx=5, pady=5)

        # Label de status
        self.label_status = tk.Label(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        # Configura todas as linhas para expandirem verticalmente
        for i in range(12):
            self.app.rowconfigure(i, weight=1)
        
    def lost_password(self):
        login = self.entry_login.get()
        password = self.entry_pswd.get()
        print(f"Usuário: {login}, Senha: {password}")
        
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
                    
    def create_entry(self, label, row, is_password=False):
        tk.Label(self.app, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = tk.Entry(self.app, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        return entry

    def lost_user(self):
        
        login = self.entry_login.get()
        password = self.entry_pswd.get()
        print(f"Usuário: {login}, Senha: {password}")
        
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
        
        if cursor.execute(query, params).rowcount == 1:
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
   
        login_valid, password_valid, tipo = cursor.fetchall()[0]

        if login == login_valid and password == password_valid:
            self.label_status.config(text="Login realizado com sucesso")
            if tipo.upper() == 'ADMIN':
                self.app.destroy()
                tela = InterationAdmin()
                tela.main()
            elif tipo.upper() == 'USER':
                self.app.destroy()
                tela = InterationUser()
                tela.main()
            
        else:
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
        
        
if __name__ == '__main__':
    service = LoginScreen()
    service.main()
    