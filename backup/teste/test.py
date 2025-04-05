import sqlite3
import customtkinter as ctk

# Função para carregar produtos filtrados
def carregar_produtos():
    tipo_prod = combo_categoria.get()  # Pegando valor do ComboBox
    conn = sqlite3.connect("cantina.db")
    cursor = conn.cursor()

    # Se a categoria for "Todos", busca tudo, senão filtra pela categoria escolhida
    if tipo_prod == "Todos":
        cursor.execute("SELECT nome_prod, valor_prod FROM produtos")
    else:
        cursor.execute("SELECT nome_prod, valor_prod FROM produtos WHERE tipo_prod = ?", (tipo_prod,))
    
    produtos = cursor.fetchall()
    conn.close()

    # Limpar a lista antes de adicionar os novos itens
    listbox.delete("0.0", "end")

    # Adicionar os produtos na listbox
    for produto in produtos:
        listbox.insert("end", f"{produto[0]} - R$ {produto[1]:.2f}\n")

# Criar janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x350")
root.title("Filtro de Produtos")

# Criar Label
label = ctk.CTkLabel(root, text="Filtrar por Categoria:", font=("Arial", 14))
label.pack(pady=10)

# Criar ComboBox com as opções de filtro
combo_categoria = ctk.CTkComboBox(root, values=["Todos", "Alimentos", "Limpeza", "Bebidas"], command=lambda _: carregar_produtos())
combo_categoria.pack()
combo_categoria.set("Todos")  # Define a opção inicial como "Todos"

# Criar um botão para carregar produtos
btn_carregar = ctk.CTkButton(root, text="Filtrar", command=carregar_produtos)
btn_carregar.pack(pady=10)

# Criar uma listbox para exibir os produtos
listbox = ctk.CTkTextbox(root, width=350, height=200)
listbox.pack(pady=10)

# Rodar aplicação
root.mainloop()
