import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# class LoginService:
    
#     def __init__(self):
#         ctk.set_appearance_mode("dark")
#         ctk.set_default_color_theme("dark-blue")
        
#         self.app = ctk.CTk()
#         self.app.title("Login")
#         self.app.geometry("700x400")
#         self.app.iconbitmap(r"backup\teste\logo.ico")
        
#         # Adicionando a imagem
#         self.image = Image.open(r"backup\teste\45605.png")
#         self.image_resized = self.image.resize((350, 350))
#         self.img_tk = ImageTk.PhotoImage(self.image_resized)
        
#         label_img = ctk.CTkLabel(master=self.app, image=self.img_tk, text="")
#         label_img.place(x=30, y=55)
#         label_img.image = self.img_tk
        
#         # Criando o frame
#         frame = ctk.CTkFrame(master=self.app, width=350, height=396)
#         frame.place(x=350, y=2)

#         # Título do frame
#         label = ctk.CTkLabel(master=frame, text="Gerenciamento de Vendas", font=("Bebas Neue", 25), text_color="white")
#         label.place(x=25, y=30)

#         # Campos de entrada
#         self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira seu usuário", width=300, font=("Arial", 14))
#         self.user_entry.place(x=25, y=105)

#         self.senha_entry = ctk.CTkEntry(master=frame, placeholder_text="Insira sua senha", width=300, font=("Arial", 14), show="*")
#         self.senha_entry.place(x=25, y=170)

#         # Checkbox para manter conectado
#         checkbox = ctk.CTkCheckBox(master=frame, text="Mantenha-me Conectado")
#         checkbox.place(x=25, y=235)

#         # Botão de login
#         loginBt = ctk.CTkButton(master=frame, text="Login", width=300, command=self.login_bt)
#         loginBt.place(x=25, y=280)

#         # Links para recuperação de usuário e senha
#         linkU = ctk.CTkLabel(master=frame, text="Recuperar usuário", font=("Arial", 12), text_color="lightblue", cursor="hand2")
#         linkU.place(x=25, y=310)
#         linkU.bind("<Button-1>", lambda e: self.lost_user())

#         linkS = ctk.CTkLabel(master=frame, text="Recuperar senha", font=("Arial", 12), text_color="lightblue", cursor="hand2")
#         linkS.place(x=140, y=310)
#         linkS.bind("<Button-1>", lambda e: self.lost_password())

#     def login_bt(self):
#         # Recupera os valores de login e senha
#         user = self.user_entry.get()
#         password = self.senha_entry.get()
        
#         # Aqui você pode adicionar a lógica de validação, como a verificação no banco de dados
#         if user == "admin" and password == "1234":  # Exemplo de validação
#             messagebox.showinfo("Login", "Login bem-sucedido!")
#         else:
#             messagebox.showerror("Erro", "Usuário ou senha inválidos.")

#     def lost_user(self):
#         # Exemplo de ação para recuperação de usuário
#         messagebox.showinfo("Recuperação de Usuário", "Instruções para recuperar o usuário serão enviadas para seu e-mail.")

#     def lost_password(self):
#         # Exemplo de ação para recuperação de senha
#         messagebox.showinfo("Recuperação de Senha", "Instruções para recuperar a senha serão enviadas para seu e-mail.")
    
#     def main(self):
#         self.app.mainloop()

# if __name__ == '__main__':
#     service = LoginService()
#     service.main()



# Definir nome da tabela e pegar colunas
# Criar DataFrame vazio

# # Verifica se a coluna existe na tabela
# if categoria_um in colunas:
#     cursor.execute(f"SELECT * FROM {nome_tabela} WHERE {categoria_um} LIKE ?", (f"%{filtro}%",))
#     produtos = cursor.fetchall()

#     # Criar DataFrame a partir dos dados recuperados
#     if produtos:
#         df_base = pd.DataFrame(produtos, columns=colunas)

# # Fechar conexão com o banco
# conn.close()

# # Exibir o DataFrame
# print(df_base)

# # Exportar para Excel
# df_base.to_excel("resultado.xlsx", index=False)
# print("Dados exportados para 'resultado.xlsx'")


import sqlite3
import pandas as pd
import customtkinter as ctk

# Função para carregar produtos filtrados
def carregar_cat_1():
    categoria_um = combo_categoria.get()  # Pega a categoria escolhida (ex: nome, valor, tipo)
    filtro = entry_filtro.get() 
    teste = pd.read_excel(r'db\controle_estoque.xlsx')

    conn = sqlite3.connect(r"db\database.db")
    cursor = conn.cursor()
    
    nome_tabela = 'cantina'
    cursor.execute(f"PRAGMA table_info({nome_tabela})")
    colunas = [coluna[1] for coluna in cursor.fetchall()]
    
    df_base = pd.DataFrame(columns=colunas)

    if categoria_um in colunas:
        # Limpa a listbox antes de inserir os novos itens
        listbox.delete("0.0", "end")

        # Se for nome, traz só os nomes dos produtos filtrados
        cursor.execute(f"SELECT * FROM cantina WHERE {categoria_um} LIKE ?", (f"%{filtro}%",))
        produtos = cursor.fetchall()
        
        if produtos:
            df_base = pd.DataFrame(produtos, columns=colunas)
        # for v, produto in enumerate(produtos[0]):
            

        #     listbox.insert("end", f"{colunas[v]} - {produto}\n")
            
        listbox.insert("end", df_base.to_string(index=False))
            

    conn.close()

# Criar janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("500x400")
root.title("Filtro de Produtos")

conn = sqlite3.connect(r"db\database.db")
cursor = conn.cursor()
nome_tabela = 'cantina'

cursor.execute(f"PRAGMA table_info({nome_tabela})")
categorias = [coluna[1] for coluna in cursor.fetchall()]

# Criar Label
label = ctk.CTkLabel(root, text="Filtrar por Categoria:", font=("Arial", 14))
label.pack(pady=10)

# Criar Frame para alinhar os widgets lado a lado
frame_filtros = ctk.CTkFrame(root)
frame_filtros.pack(pady=10)

# Criar ComboBox com as opções de filtro
combo_categoria = ctk.CTkComboBox(frame_filtros, values=categorias)
combo_categoria.pack(side="left", padx=10)
combo_categoria.set("nome")  # Definir um valor padrão

# Criar um campo de entrada para o nome do produto
entry_filtro = ctk.CTkEntry(frame_filtros, placeholder_text="Digite o nome...")
entry_filtro.pack(side="left", padx=10)

# Criar um botão para carregar produtos
btn_filt_1 = ctk.CTkButton(root, text="Filtrar Nome", command=carregar_cat_1)
btn_filt_1.pack(padx=10, pady=5)

btn_filt_1 = ctk.CTkButton(root, text="Filtrar Data", command=carregar_cat_1)
btn_filt_1.pack(padx=10, pady=5)


btn_filt_1 = ctk.CTkButton(root, text="Filtrar Produto", command=carregar_cat_1)
btn_filt_1.pack(padx=10, pady=5)

# Criar uma listbox para exibir os produtos
listbox = ctk.CTkTextbox(root, wrap="none")
listbox.pack(expand=True, fill="both", padx=10, pady=10)

# Rodar aplicação
root.mainloop()
