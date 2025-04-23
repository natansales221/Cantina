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

        btn_filtrar = ctk.CTkButton(self, text="Filtrar", command=self.carregar_produtos)
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
        conn = sqlite3.connect(r"db\database.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM cantina LIMIT 1")
        nomes_colunas = [desc[0] for desc in cursor.description]
        conn.close()
        return nomes_colunas

    def carregar_produtos(self):
        filtro = self.entry_filtro.get()
        categoria = self.combo_categoria.get()  # Pegando valor do ComboBox
        conn = sqlite3.connect(r'db\database.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM cantina LIMIT 1')

        # Extrai os nomes das colunas do cursor.description
        nomes_colunas = [descricao[0] for descricao in cursor.description]

        # Se a categoria for "Todos", busca tudo, senão filtra pela categoria escolhida
        if categoria == "Todos":
            cursor.execute("SELECT * FROM cantina")
        else:
            cursor.execute(f"SELECT * FROM cantina WHERE {categoria} like ?", (f"%{filtro}%",))

        produtos = cursor.fetchall()
        df_base = pd.DataFrame(produtos, columns=nomes_colunas)

        # Remove a coluna ID se existir
        if 'id' in df_base.columns:
            df_base = df_base.drop(columns=["id"])

        # Formata a coluna de data
        if 'data' in df_base.columns:
            df_base['data'] = pd.to_datetime(df_base['data'], errors='coerce').dt.strftime('%d-%m-%Y')

        # Colunas monetárias
        colunas_monetarias = ['debito', 'credito', 'total']
        
        # Converte colunas monetárias para número antes da soma
        for coluna in colunas_monetarias:
            if coluna in df_base.columns:
                df_base[coluna] = pd.to_numeric(df_base[coluna], errors='coerce')
        linha_vazia = {
            'data': '-',
            'nome': '-',
            'produto': '-',
            'debito': '-',
            'credito': '-',
            'total': '-',
            'cargo': '-',
            'turma': '-',
            'telefone': '-',
            'observacao': '-'
        }
        # Cria uma linha de totais
        linha_total = {
            'data': '',
            'nome': '',
            'produto': 'TOTAL',
            'debito': df_base['debito'].sum(),
            'credito': df_base['credito'].sum(),
            'total': df_base['total'].sum(),
            'cargo': '',
            'turma': '',
            'telefone': '',
            'observacao': ''
        }

        # Cria DataFrame de soma com a linha total
        df_soma = pd.DataFrame([linha_vazia, linha_total])

        # Formata os campos monetários com R$
        for coluna in colunas_monetarias:
            df_base[coluna] = df_base[coluna].apply(lambda x: f"R$ {float(x):.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else x)
            df_soma[coluna] = df_soma[coluna].apply(lambda x: f"R$ {float(x):.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else x)


        conn.close()
        df_final = pd.concat([df_base, df_soma], ignore_index=True)

        # Mostra tudo junto na interface
        self.listbox.delete("0.0", "end")
        self.listbox.insert("end", df_final.to_string(index=False))
        
    def main(self):
        self.mainloop()


# Execução direta
if __name__ == "__main__":
    app = Filter(tipo='admin')
    app.main()
