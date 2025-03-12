produtos = {}

def cadastrar_produto():
    codigo = input("Digite o código do produto: ")
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    produtos[codigo] = {'nome': nome, 'preco': preco}
    print(f"Produto '{nome}' cadastrado com sucesso!")

def listar_produtos():
    print("\nLista de produtos cadastrados:")
    for codigo, info in produtos.items():
        print(f"Código: {codigo} | Nome: {info['nome']} | Preço: R$ {info['preco']:.2f}")

def vender_produto():
    codigo = input("Digite o código do produto que deseja vender: ")
    if codigo in produtos:
        produto = produtos[codigo]
        qtd = int(input("Informe a quantidade do produto vendido: "))
        valor_total = qtd * produto['preco']
        print(f"Produto vendido: {produto['nome']} - Quantidade: {qtd} - Total: R$ {valor_total:.2f}")
    else:
        print("Produto não encontrado!")

def menu():
    while True:
        print("\n1 - Cadastrar Produto")
        print("2 - Listar Produtos")
        print("3 - Vender Produto")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            vender_produto()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
