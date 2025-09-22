# Sistema de Pedidos para Restaurante - FoodDelivery
# Desenvolvido por Maranhão - UNEX

itens = []
pedidos = []

proximo_id_item = 1
proximo_id_pedido = 1

class Item:
    def _init_(self, codigo, nome, descricao, preço, estoque):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.preço = preço
        self.estoque = estoque

class Pedido:
    def _init_(self, numero, itens, valor_total, status):
        self.numero = numero
        self.itens = itens
        self.valor_total = valor_total
        self.status = status

def cadastrar_item():
    global proximo_id_item
    print("\n--- Cadastrar Novo Item ---")
    nome = input("Nome do item: ")
    descricao = input("Descrição: ")
    preço = float(input("Preço: R$ "))
    estoque = int(input("Estoque inicial: "))
    novo_item = Item(proximo_id_item, nome, descricao, preço, estoque)
    itens.append(novo_item)
    proximo_id_item += 1
    print(f"Item '{nome}' cadastrado com sucesso! Código: {novo_item.codigo}")

def consultar_itens():
    print("\n--- Itens do Cardápio ---")
    if not itens:
        print("Nenhum item cadastrado.")
        return
    for item in itens:
        print(f"Código: {item.codigo} | Nome: {item.nome} | Preço: R$ {item.preço:.2f} | Estoque: {item.estoque}")

def criar_pedido():
    global proximo_id_pedido
    print("\n--- Criar Novo Pedido ---")
    if not itens:
        print("Não há itens disponíveis no cardápio!")
        return
    consultar_itens()
    itens_pedido = []
    valor_total = 0.0
    while True:
        try:
            codigo = int(input("\nCódigo do item (0 para finalizar): "))
            if codigo == 0:
                break
            quantidade = int(input("Quantidade: "))
            item_encontrado = None
            for item in itens:
                if item.codigo == codigo:
                    item_encontrado = item
                    break
            if item_encontrado and item_encontrado.estoque >= quantidade:
                itens_pedido.append((item_encontrado, quantidade))
                valor_total += item_encontrado.preço * quantidade
                print(f"Item '{item_encontrado.nome}' adicionado ao pedido!")
            else:
                print("Item não encontrado ou estoque insuficiente!")
        except ValueError:
            print("Valor inválido!")
    if not itens_pedido:
        print("Pedido vazio! Cancelando operação.")
        return
    novo_pedido = Pedido(proximo_id_pedido, itens_pedido, valor_total, "NOVO")
    pedidos.append(novo_pedido)
    proximo_id_pedido += 1
    print(f"\nPedido #{novo_pedido.numero} criado com sucesso!")
    print(f"Valor total: R$ {valor_total:.2f}")

def menu_principal():
    while True:
        print("\n--- SISTEMA DE PEDIDOS ---")
        print("1. Cadastrar Item")
        print("2. Consultar Itens")
        print("3. Criar Pedido")
        print("0. Sair")
        try:
            opcao = int(input("\nEscolha uma opção: "))
            if opcao == 0:
                print("Saindo do sistema...")
                break
            elif opcao == 1:
                cadastrar_item()
            elif opcao == 2:
                consultar_itens()
            elif opcao == 3:
                criar_pedido()
            else:
                print("Opção inválida!")
        except ValueError:
            print("Por favor, digite um número válido!")
            
if __name__ == "__main__":
    menu_principal()
