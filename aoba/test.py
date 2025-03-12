import sqlite3
import customtkinter as ctk

# Função para carregar produtos filtrados
def carregar_produtos():
    categoria = combo_categoria.get()  # Pega a categoria escolhida (ex: codigo, nome, valor, tipo)
    filtro = combo_categoria_dois.get()  # Pega o valor do filtro
    
    conn = sqlite3.connect(r"db\database.db")
    cursor = conn.cursor()

    # Mapeando a categoria para o nome correto da coluna no banco
    colunas = {"codigo": "cod_prod", "nome": "nome_prod", "valor": "valor_prod", "tipo": "tipo_prod"}
    
    if categoria in colunas:
        coluna_banco = colunas[categoria]

        # Limpa a listbox antes de inserir os novos itens
        listbox.delete("0.0", "end")

        # Se for nome, traz só os nomes dos produtos
        if categoria == "nome":
            cursor.execute(f"SELECT nome_prod FROM produtos WHERE {coluna_banco} LIKE ?", (f"%{filtro}%",))
            produtos = cursor.fetchall()
            for produto in produtos:
                listbox.insert("end", f"{produto[0]}\n")

        # Para outras categorias, traz nome e valor
        else:
            cursor.execute(f"SELECT nome_prod, valor_prod FROM produtos WHERE {coluna_banco} LIKE ?", (f"%{filtro}%",))
            produtos = cursor.fetchall()
            for produto in produtos:
                listbox.insert("end", f"{produto[0]} - R$ {produto[1]:.2f}\n")
    
    conn.close()


# Criar janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x350")
root.title("Filtro de Produtos")

# Criar Label
label = ctk.CTkLabel(root, text="Filtrar por Categoria:", font=("Arial", 14))
label.pack(pady=10)

# Criar Frame para alinhar os widgets lado a lado
frame_filtros = ctk.CTkFrame(root)
frame_filtros.pack(pady=10)

# Criar ComboBox com as opções de filtro
combo_categoria = ctk.CTkComboBox(frame_filtros, values=["nome"])
combo_categoria.pack(side="left", padx=10)
combo_categoria.set("nome")  # Definir um valor padrão

combo_categoria_dois = ctk.CTkComboBox(frame_filtros, values=["codigo", "nome", "valor", "tipo"])
combo_categoria_dois.pack(side="left", padx=10)
combo_categoria_dois.set("nome")  # Definir um valor padrão

# Criar um botão para carregar produtos
btn_carregar = ctk.CTkButton(root, text="Filtrar", command=carregar_produtos)
btn_carregar.pack(pady=10)

# Criar uma listbox para exibir os produtos
listbox = ctk.CTkTextbox(root, width=350, height=200)
listbox.pack(pady=10)

# Rodar aplicação
root.mainloop()
