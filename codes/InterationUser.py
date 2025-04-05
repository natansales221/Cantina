import customtkinter as ctk
import sqlite3
from InsertScreen import InsertInfo

class InterationUser: 
    
    def __init__(self, tipo):
        ctk.set_appearance_mode("dark")  # Define o tema escuro
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Seleção de opções")
        self.app.geometry("400x300")

        self.label_title = ctk.CTkLabel(self.app, text="Olá Usuário! O que deseja fazer?", font=("Helvetica", 14))
        self.label_title.pack(pady=10)

        self.view_button = ctk.CTkButton(self.app, text="Visualizar Resumo", command=self.view_resumed_info)
        self.view_button.pack(pady=5)
        
        self.insert_button = ctk.CTkButton(self.app, text="Inserir informações", command=lambda: self.insert(tipo))
        self.insert_button.pack(pady=5)
        
        self.logout_button = ctk.CTkButton(self.app, text="Logout", command=self.deslogar)
        self.logout_button.pack(pady=5)
        
        self.label_status = ctk.CTkLabel(self.app, text="", fg_color="transparent")
        self.label_status.pack(pady=5)
    
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()
    
    def view_resumed_info(self):
        print("Visualizando resumo de informações")
    
    def insert(self, tipo):
        self.app.destroy()
        insert_info = InsertInfo(tipo)
        insert_info.main()
    
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
        con.close()
        
        # cursor.execute('drop table login_cantina')
        print("Tabela criada com sucesso")

    def main(self):
        self.app.mainloop()
                
if __name__ == '__main__':
    service = InterationUser()
    service.main()
