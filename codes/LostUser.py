import customtkinter as ctk
import sqlite3

from LoginScreen import LoginService

class LostUser: 
    
    def __init__(self):
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("Alteração de senha")
        
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.fgt_pswd = ctk.CTkButton(self.app, text="Recuperar Usuário", command=self.recovery_user)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.bck_btn = ctk.CTkButton(self.app, text="Voltar", command=self.deslogar)
        self.bck_btn.grid(row=10, column=0, sticky="ew", padx=5, pady=5)

        self.entry_forgot_name = self.create_entry_in_window("Confirme seu nome", 2, self.app)
        self.entry_forgot_last_name = self.create_entry_in_window("Confirme seu sobrenome", 3, self.app)
        
        self.label_status = ctk.CTkLabel(self.app, text="")
        self.label_status.grid(row=11, column=0, columnspan=3, sticky="ew")

        for i in range(12):
            self.app.rowconfigure(i, weight=1)
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()
    
                 
    def create_entry_in_window(self, label, row, window, is_password=False):
        ctk.CTkLabel(window, text=label + ":").grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        entry = ctk.CTkEntry(window, show="*" if is_password else "")
        entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        return entry

    def connect(self):
        con = sqlite3.connect(r'db\database.db')
        cursor = con.cursor()        
        return cursor, con

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

        params = ('natan', 'sales', 'natansales', 'natansales2', 'admin', '30/09/2000')
        
        cursor.execute(query, params)
        
        con.commit()

    def main(self):
        self.app.mainloop()
        
    def recovery_user(self):
        cursor, con = self.connect()
        lost_name = self.entry_forgot_name.get()
        lost_sobrenome = self.entry_forgot_last_name.get()
        
        query = "SELECT login FROM login_cantina WHERE nome = ? AND sobrenome = ?"
        params = (lost_name, lost_sobrenome)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        if result:
            self.label_status.configure(text=f"Seu usuário é {result[0]}")
        else:
            self.label_status.configure(text="Usuário não encontrado")
     
if __name__ == '__main__':
    service = LostUser()
    service.main()
    