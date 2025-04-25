import customtkinter as ctk
import sqlite3
from InterationUser import InterationUser
from InterationAdmin import InterationAdmin

class LoginService:
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Login")
        self.app.geometry("450x150")

        self.entry_login = self.create_entry("Login", 0)
        self.entry_pswd = self.create_entry("Senha", 1, is_password=True)
        self.entry_pswd.bind("<Return>", self.login_bt)


        self.fgt_pswd = ctk.CTkButton(self.app, text="Esqueci a senha", command=self.lost_password)
        self.fgt_pswd.grid(row=10, column=1, padx=5, pady=5)
        
        self.fgt_user = ctk.CTkButton(self.app, text="Esqueci o usuário", command=self.lost_user)
        self.fgt_user.grid(row=10, column=0, padx=5, pady=5)
        
        self.login_button = ctk.CTkButton(self.app, text="Login", command=self.login_bt)
        self.login_button.grid(row=10, column=2, padx=5, pady=5)
        
        self.label_status = ctk.CTkLabel(self.app, text="", fg_color="transparent")
        self.label_status.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

    def create_entry(self, label, row, is_password=False):
        ctk.CTkLabel(self.app, text=label + ":").grid(row=row, column=0, padx=5, pady=5)
        entry = ctk.CTkEntry(self.app, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
        return entry

    def lost_password(self):
        from LostPassword import LostPassword
        self.app.destroy()
        lost_password = LostPassword()
        lost_password.main()
    
    def lost_user(self):    
        from LostUser import LostUser 
        self.app.destroy()
        lost_password = LostUser()
        lost_password.main()
        
    def connect(self):
        conn = sqlite3.connect(r'db\database.db')
        cursor = conn.cursor()        
        return cursor, conn
            
    def login_bt(self, event=True):
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
            login_valid, password_valid, tipo = cursor.fetchone()

            if login == login_valid and password == password_valid:
                self.label_status.configure(text="Login realizado com sucesso")
                if tipo.upper() == 'ADMIN':
                    self.app.destroy()
                    tela = InterationAdmin(tipo)
                    tela.main()
                elif tipo.upper() == 'USER':
                    self.app.destroy()
                    tela = InterationUser(tipo)
                    tela.main()
            else:
                self.label_status.configure(text="Login ou senha inválido!")
        except:
            self.label_status.configure(text="Login ou senha inválido!")
            
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
        
        print("Tabela criada com sucesso")

    def main(self):
        self.app.mainloop()
             
if __name__ == '__main__':
    service = LoginService()
    service.main()
    