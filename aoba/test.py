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
