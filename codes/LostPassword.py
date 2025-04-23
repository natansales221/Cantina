import customtkinter as ctk
import sqlite3

from LoginScreen import LoginService

class LostPassword: 
    
    def __init__(self):
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("Alteração de senha")
        
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=2)
        self.app.columnconfigure(2, weight=1)

        self.fgt_pswd = ctk.CTkButton(self.app, text="Alterar Senha", command=self.submit_forgot_password)
        self.fgt_pswd.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.bck_btn = ctk.CTkButton(self.app, text="Voltar", command=self.deslogar)
        self.bck_btn.grid(row=10, column=0, sticky="ew", padx=5, pady=5)

        self.entry_forgot_name = self.create_entry_in_window("Confirme seu nome", 2, self.app)
        self.entry_forgot_last_name = self.create_entry_in_window("Confirme seu sobrenome", 3, self.app)
        self.entry_forgot_date = self.create_entry_in_window("Confirme sua data de nascimento", 4, self.app)
        self.entry_forgot_password = self.create_entry_in_window("Senha Nova", 5, self.app, is_password=True)
        
        self.label_status = ctk.CTkLabel(self.app, text="")
        self.label_status.grid(row=15, column=1, sticky="ew")

        for i in range(12):
            self.app.rowconfigure(i, weight=1)
            
    def deslogar(self):
        from LoginScreen import LoginService
        self.app.destroy()
        logout = LoginService()
        logout.main()
    
    def formatar_data(self, *args):
        """ Formata a entrada da data automaticamente (dd/mm/yyyy). """
        texto = self.entry_forgot_date.get().replace("/", "")
        if len(texto) > 8:
            texto = texto[:8]

        novo_texto = ""
        for i, char in enumerate(texto):
            if i in [2, 4]:
                novo_texto += "/"
            novo_texto += char

        self.entry_forgot_date.delete(0, ctk.END)
        self.entry_forgot_date.insert(0, novo_texto)
                 
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
        
        try:
            if cursor.execute(query, params).connection.total_changes != 0:
                con.commit()
                self.label_status.configure(text="Senha alterada!")

            else:
                self.label_status.configure(text="Não foi possível alterar a senha")
        except:
            self.label_status.configure(text="Não foi possível alterar a senha")
       
if __name__ == '__main__':
    service = LostPassword()
    service.main()
    