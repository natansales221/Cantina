import sqlite3
import pandas as pd
import customtkinter as ctk
import InterationAdmin


class Filter(ctk.CTk):
    def __init__(self, tipo):
        super().__init__()

        self.tipo = tipo  # guarda o tipo para uso posterior
        self.title("Filtro de Produtos")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.nome_tabela = tipo  # nome da tabela vindo de fora

        self.criar_widgets()

    def criar_widgets(self):
        label = ctk.CTkLabel(self, text="Filtrar por Categoria:", font=("Arial", 14))
        label.pack(pady=10)

        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=10)

        self.combo_categoria = ctk.CTkComboBox(frame_filtros, values=self.obter_categorias())
        self.combo_categoria.pack(side="left", padx=10)
        self.combo_categoria.set("nome")

        self.entry_filtro = ctk.CTkEntry(frame_filtros, placeholder_text="Digite o valor a buscar...")
        self.entry_filtro.pack(side="left", padx=10)

        btn_filtrar = ctk.CTkButton(self, text="Filtrar", command=self.carregar_cat_1)
        btn_filtrar.pack(padx=10, pady=10)

        btn_voltar = ctk.CTkButton(self, text="Voltar", command=self.voltar)
        btn_voltar.pack(padx=10, pady=15)

        self.listbox = ctk.CTkTextbox(self, wrap="none", font=("Courier", 12))
        self.listbox.pack(expand=True, fill="both", padx=10, pady=10)

    def voltar(self):
        # Corrigido: usar o tipo armazenado na classe
        if self.tipo == 'admin':
            from InterationAdmin import InterationAdmin
            self.destroy()  # Fecha a janela atual
            InterationAdmin(tipo=self.tipo).main()  # Chama a função principal para 'admin'
        elif self.tipo == 'user':
            from InterationUser import InterationUser
            self.destroy()  # Fecha a janela atual
            InterationUser(tipo=self.tipo).main()  # Chama a função principal para 'user'

    def obter_categorias(self):
        conn = sqlite3.connect(r"Cantina\db\database.db")
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.nome_tabela})")
        categorias = [coluna[1] for coluna in cursor.fetchall()]
        conn.close()
        return categorias

    def carregar_cat_1(self):
        categoria_um = self.combo_categoria.get()
        filtro = self.entry_filtro.get()

        conn = sqlite3.connect(r"Cantina\db\database.db")
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.nome_tabela})")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        df_base = pd.DataFrame(columns=colunas)

        if categoria_um in colunas:
            self.listbox.delete("0.0", "end")
            cursor.execute(f"SELECT * FROM {self.nome_tabela} WHERE {categoria_um} LIKE ?", (f"%{filtro}%",))
            produtos = cursor.fetchall()

            if produtos:
                df_base = pd.DataFrame(produtos, columns=colunas)
                self.listbox.insert("end", df_base.to_string(index=False))
            else:
                self.listbox.insert("end", "Nenhum resultado encontrado.")

        conn.close()

    def main(self):
        self.mainloop()


# Execução direta
if __name__ == "__main__":
    app = Filter("cantina")  # nome da tabela passado como argumento
    app.main()
