import customtkinter as ctk
import sqlite3
from InterationUser import InterationUser
from InterationAdmin import InterationAdmin

class LoginService:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Cantina")
        self.app.minsize(600, 400)

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)

        # Frame da esquerda (logo)
        self.left_frame = ctk.CTkFrame(self.app)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.left_frame, text="🍴", font=("Arial", 120))
        self.logo_label.grid(row=0, column=0, sticky="nsew")

        # Frame da direita (login)
        self.right_frame = ctk.CTkFrame(self.app)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.right_frame, text="🍴 Cantina", font=("Arial Black", 30))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.entry_login = self.create_entry(self.right_frame, "Login", 1)
        self.entry_pswd = self.create_entry(self.right_frame, "Senha", 2, is_password=True)
        self.entry_pswd.bind("<Return>", self.login_bt)

        self.button_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.button_frame.grid(row=5, column=0, pady=10, padx=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.login_button = ctk.CTkButton(self.button_frame, text="Login", command=self.login_bt)
        self.login_button.grid(row=0, column=0, padx=(0, 10))
        self.login_button.configure(width=100)

        self.forgot_button = ctk.CTkButton(self.button_frame, text="Esqueci a senha", command=self.lost_password)
        self.forgot_button.grid(row=0, column=1,)
        self.forgot_button.configure(width=50)

        self.lost_user = ctk.CTkButton(self.button_frame, text="Esqueci o usuário", command=self.lost_user)
        self.lost_user.grid(row=0, column=2, padx=10, pady=1,)
        self.lost_user.configure(width=50)

        self.label_status = ctk.CTkLabel(self.right_frame, text="", text_color="red", font=("Arial", 12))
        self.label_status.grid(row=6, column=0, pady=(10, 5))

        self.copyright_label = ctk.CTkLabel(
            self.right_frame, text="©copyright - 2025", font=("Arial", 10)
        )
        self.label_status.grid(row=6, column=0, pady=(0, 10))
        self.right_frame.grid_rowconfigure(7, weight=1)

    def create_entry(self, parent, placeholder, row, is_password=False):
        label = ctk.CTkLabel(parent, text=f"{placeholder}:", font=("Arial", 14))
        label.grid(row=row * 2 - 1, column=0, sticky="w", padx=20)

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, show="*" if is_password else "")
        entry.grid(row=row * 2, column=0, padx=20, pady=(0, 10), sticky="ew")
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

    def login_bt(self, event=None):
        login = self.entry_login.get()
        senha = self.entry_pswd.get()

        # Login hardcoded (apenas para testes)
        if login == "admin" and senha == "123":
            self.label_status.configure(text="Login bem-sucedido!", text_color="green")
            self.app.destroy()
            tela = InterationAdmin("ADMIN")
            tela.main()
            return

        # Conecta ao banco
        cursor, conn = self.connect()
        query = """
            SELECT login, senha, tipo FROM login_cantina
            WHERE login = ?
        """
        params = (login,)
        try:
            cursor.execute(query, params)
            resultado = cursor.fetchone()

            if resultado:
                login_valid, senha_valid, tipo = resultado
                if senha == senha_valid:
                    self.label_status.configure(text="Login realizado com sucesso!", text_color="green")
                    self.app.destroy()
                    if tipo.upper() == 'ADMIN':
                        tela = InterationAdmin(tipo)
                    else:
                        tela = InterationUser(tipo)
                    tela.main()
                else:
                    self.label_status.configure(text="Senha incorreta!", text_color="red")
            else:
                self.label_status.configure(text="Usuário não encontrado!", text_color="red")

        except Exception as e:
            print(f"Erro ao tentar login: {e}")
            self.label_status.configure(text="Erro ao tentar realizar o login!", text_color="red")
        finally:
            conn.close()

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

        # Verifica se o usuário admin já existe antes de inserir
        cursor.execute("SELECT * FROM login_cantina WHERE login = 'admin'")
        if not cursor.fetchone():
            query = """
                INSERT INTO login_cantina (nome, sobrenome, login, senha, tipo, nascimento)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = ('admin', 'admin', 'admin', 'admin', 'admin', '30/09/2000')
            cursor.execute(query, params)
            print("Usuário admin criado com sucesso")

        con.commit()
        con.close()

    def main(self):
        self.app.mainloop()

if __name__ == '__main__':
    service = LoginService()
    service.main()
