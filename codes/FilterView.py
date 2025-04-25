import sqlite3
import pandas as pd
import customtkinter as ctk
import InterationAdmin


class Filter(ctk.CTk):
    def __init__(self, tipo):
        super().__init__()

        self.tipo = tipo
        self.title("Filtro de Produtos")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.nome_tabela = tipo

        self.criar_widgets()

    def criar_widgets(self):
        label = ctk.CTkLabel(self, text="Filtrar por Categoria:", font=("Calibri", 20))
        label.pack(pady=10)

        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=10)

        self.combo_categoria = ctk.CTkComboBox(frame_filtros, values=self.obter_categorias(), font=("Calibri", 13))
        self.combo_categoria.pack(side="left", padx=10)
        self.combo_categoria.set("Nome")

        self.entry_filtro = ctk.CTkEntry(frame_filtros, placeholder_text="Digite o valor a buscar...", font=("Calibri", 13))
        self.entry_filtro.pack(side="left", padx=10)
        self.entry_filtro.bind("<Return>", self.carregar_produtos)

        btn_filtrar = ctk.CTkButton(self, text="Filtrar", command=self.carregar_produtos, width=100)
        btn_filtrar.pack(padx=10, pady=10)

        btn_voltar = ctk.CTkButton(self, text="Voltar", command=self.voltar, width=100)
        btn_voltar.pack(padx=10, pady=10)

        self.listbox = ctk.CTkTextbox(self, wrap="none", font=("Courier New", 15))
        self.listbox.pack(expand=True, fill="both", padx=10, pady=10)
        

    def voltar(self):
        if self.tipo == 'admin':
            from InterationAdmin import InterationAdmin
            self.destroy()
            InterationAdmin(tipo=self.tipo).main()
        elif self.tipo == 'user':
            from InterationUser import InterationUser
            self.destroy()
            InterationUser(tipo=self.tipo).main()

    def obter_categorias(self):
        conn = sqlite3.connect(r"db\database.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM cantina LIMIT 1")
        nomes_colunas = [desc[0] for desc in cursor.description]
        conn.close()
        return nomes_colunas

    def carregar_produtos(self, event=None):
        filtro = self.entry_filtro.get()
        categoria = self.combo_categoria.get()
        conn = sqlite3.connect(r'db\database.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM cantina LIMIT 1')
        nomes_colunas = [descricao[0] for descricao in cursor.description]

        if categoria == "Todos":
            cursor.execute("SELECT * FROM cantina")
        else:
            cursor.execute(f"SELECT * FROM cantina WHERE {categoria} like ?", (f"%{filtro}%",))
        produtos = cursor.fetchall()
        df_base = pd.DataFrame(produtos, columns=nomes_colunas)
        self.listbox.tag_config("debito_color", foreground="#CD5C5C")
        self.listbox.tag_config("credito_color", foreground="#ADFF2F")
        self.listbox.tag_config("total_color", foreground="#87CEFA")

        # Não drope a coluna 'id'
        if 'data' in df_base.columns:
            df_base['data'] = pd.to_datetime(df_base['data'], errors='coerce').dt.strftime('%d-%m-%Y')
        colunas_monetarias = ['debito', 'credito', 'total']
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
        linha_total = {
            'data': '',
            'nome': '',
            'produto': 'SALDO DEVEDOR',
            'debito': f"$ {df_base['debito'].fillna(0).sum():.2f}",
            'credito': f"$ {df_base['credito'].fillna(0).sum():.2f}",
            'total': f"$ {df_base['total'].fillna(0).sum():.2f}",
            'cargo': '',
            'turma': '',
            'telefone': '',
            'observacao': ''
        }
        df_soma = pd.DataFrame([linha_vazia, linha_total])
        for coluna in colunas_monetarias:
            df_base[coluna] = df_base[coluna].apply(lambda x: f"R$ {float(x):.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else x)
            df_soma[coluna] = df_soma[coluna].apply(lambda x: f"R$ {float(x):.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else x)
        conn.close()
        df_final = pd.concat([df_base, df_soma], ignore_index=True)
        self.listbox.delete("0.0", "end")

        # Calcula o máximo comprimento para cada coluna
        larguras_colunas = [max(df_final[col].astype(str).str.len().max(), len(col)) for col in df_final.columns]

        # Insere o cabeçalho com o espaçamento calculado
        header = "  ".join(df_final.columns[i].ljust(larguras_colunas[i]) for i in range(len(df_final.columns)))
        self.listbox.insert("end", header + "\n")
        self.listbox.insert("end", "-" * len(header) + "\n")

        # Insere os dados com cores e espaçamento calculado
        for index, row in df_final.iterrows():
            for i, (col_name, value) in enumerate(row.items()):
                value_str = str(value).ljust(larguras_colunas[i])
                if col_name == "debito":
                    self.listbox.insert("end", value_str + "  ", "debito_color")
                elif col_name == "credito":
                    self.listbox.insert("end", value_str + "  ", "credito_color")
                elif col_name == "total":
                    self.listbox.insert("end", value_str + "  ", "total_color")
                else:
                    self.listbox.insert("end", value_str + "  ")
            self.listbox.insert("end", "\n")

            
    def main(self):
        self.mainloop()

if __name__ == "__main__":
    app = Filter(tipo="user")
    app.main()
