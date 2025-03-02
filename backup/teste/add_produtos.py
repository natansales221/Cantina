import customtkinter as ctk
from tkinter import messagebox

class AddProd:
    def __init__(self):
        # Configuração principal da janela
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("blue")  # Tema padrão

        self.add_prod = ctk.CTk()  
        self.add_prod.geometry("700x400")
        self.add_prod.title("Cantina")

        # Definir ícone com tratamento de erro
        try:
            self.add_prod.iconbitmap("logo.ico")
        except Exception as e:
            print(f"Erro ao carregar o ícone: {e}")

        self.add_prod.resizable(False, False)

        # Lista para armazenar os produtos adicionados
        self.produtos_adicionados = []

        # Título principal
        label_title = ctk.CTkLabel(master=self.add_prod, text="Acesso Admins", font=("Bebas Neue", 25), text_color="white")
        label_title.place(x=20, y=15)

        # Campos de entrada
        ctk.CTkLabel(master=self.add_prod, text="Cód. Produto", font=("Bebas Neue", 15), text_color="white").place(x=20, y=75)
        self.cod_prod = ctk.CTkEntry(master=self.add_prod, placeholder_text="Código do produto", width=150, font=("Arial", 14))
        self.cod_prod.place(x=20, y=100)

        ctk.CTkLabel(master=self.add_prod, text="Nome Produto", font=("Bebas Neue", 15), text_color="white").place(x=20, y=135)
        self.nome_prod = ctk.CTkEntry(master=self.add_prod, placeholder_text="Nome do Produto", width=300, font=("Arial", 14))
        self.nome_prod.place(x=20, y=160)

        ctk.CTkLabel(master=self.add_prod, text="Valor Produto", font=("Bebas Neue", 15), text_color="white").place(x=20, y=195)
        self.valor_prod = ctk.CTkEntry(master=self.add_prod, placeholder_text="Valor do Produto", width=300, font=("Arial", 14))
        self.valor_prod.place(x=20, y=220)

        ctk.CTkLabel(master=self.add_prod, text="Tipo Produto", font=("Bebas Neue", 14), text_color="white").place(x=20, y=250)
        self.tipo_prod = ctk.CTkComboBox(master=self.add_prod, values=["Selecione", "Bebida", "Comida", "Doces"], width=300)
        self.tipo_prod.place(x=20, y=275)
        self.tipo_prod.set("Selecione")  # Define a opção inicial como "placeholder"

        # Botão para confirmar
        confirmar_bt = ctk.CTkButton(master=self.add_prod, text="Adicionar", command=self.confirm, width=150)
        confirmar_bt.place(x=20, y=325)

        # Botão para voltar
        voltar_bt = ctk.CTkButton(master=self.add_prod, text="Voltar", command=self.voltar, width=150)
        voltar_bt.place(x=180, y=325)

        # Criando um frame lateral para exibir os produtos adicionados
        self.frame = ctk.CTkFrame(master=self.add_prod, width=350, height=400)
        self.frame.place(x=350, y=2)

        self.label_lista = ctk.CTkLabel(master=self.frame, text="Produtos Adicionados:\n", font=("Arial", 16), text_color="white", justify="left")
        self.label_lista.pack(pady=10, padx=10)

    def atualizar_lista(self):
        # Atualiza a lista de produtos no frame
        nova_lista = "Produtos Adicionados:\n" + "\n".join(self.produtos_adicionados)
        self.label_lista.configure(text=nova_lista)

    def confirm(self):
        # Função de confirmação
        cod = self.cod_prod.get()
        nome = self.nome_prod.get()
        valor = self.valor_prod.get()
        tipo = self.tipo_prod.get()

        if not cod or not nome or not valor:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")
        elif tipo == "Selecione":
            messagebox.showwarning("Atenção", "Selecione um tipo de produto válido!")
        else:
            # Adiciona o produto à lista
            self.produtos_adicionados.append(f"{cod} - {nome} ({tipo}) R$ {valor}")

            # Atualiza a lista de produtos no frame
            self.atualizar_lista()

            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso!")

            # Limpa os campos de entrada
            self.cod_prod.delete(0, "end")
            self.nome_prod.delete(0, "end")
            self.valor_prod.delete(0, "end")
            self.tipo_prod.set("Selecione")

    def voltar(self):
        # Função para fechar a janela
        self.add_prod.destroy()

    def run(self):
        # Iniciar a aplicação
        self.add_prod.mainloop()


# Criar e executar a aplicação
if __name__ == "__main__":
    app = AddProd()
    app.run()
