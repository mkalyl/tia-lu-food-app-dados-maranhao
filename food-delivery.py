# Sistema de Pedidos para Restaurante - FoodDelivery
# Desenvolvido por Maranhão - UNEX

itens = []
pedidos = []
proximo_id_item = 1
proximo_id_pedido = 1

class Item:
    def __init__(self, codigo, nome, descricao, preço, estoque):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.preço = preço
        self.estoque = estoque

class Pedido:
    def __init__(self, numero, itens, valor_total):
        self.numero = numero
        self.itens = itens
        self.valor_total = valor_total
        self.status = "AGUARDANDO APROVACAO" 

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

def atualizar_item():
    print("\n--- Atualizar Item ---")
    consultar_itens()
    
    if not itens:
        return
    
    try:
        codigo = int(input("\nCódigo do item a atualizar: "))
        
        for item in itens:
            if item.codigo == codigo:
                print(f"\nEditando item: {item.nome}")
                item.nome = input(f"Novo nome ({item.nome}): ") or item.nome
                item.descricao = input(f"Nova descrição ({item.descricao}): ") or item.descricao
                item.preço = float(input(f"Novo preço ({item.preço}): ") or item.preço)
                item.estoque = int(input(f"Novo estoque ({item.estoque}): ") or item.estoque)
                print("Item atualizado com sucesso!")
                return
        
        print("Item não encontrado!")
            
    except ValueError:
        print("Código inválido!")

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
            
            for item in itens:
                if item.codigo == codigo:
                    if item.estoque >= quantidade:
                        itens_pedido.append((item, quantidade))
                        valor_total += item.preço * quantidade
                        print(f"Item '{item.nome}' adicionado ao pedido!")
                    else:
                        print("Estoque insuficiente!")
                    break
            else:
                print("Item não encontrado!")
                
        except ValueError:
            print("Valor inválido!")
    
    if not itens_pedido:
        print("Pedido vazio! Cancelando operação.")
        return
    
    novo_pedido = Pedido(proximo_id_pedido, itens_pedido, valor_total)
    pedidos.append(novo_pedido)
    proximo_id_pedido += 1
    
    print(f"\nPedido #{novo_pedido.numero} criado com sucesso!")
    print(f"Valor total: R$ {valor_total:.2f}")
    print(f"Status: {novo_pedido.status}")  

def consultar_pedidos():
    print("\n--- Todos os Pedidos ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    for pedido in pedidos:
        print(f"Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}")


def atualizar_status_pedido():
    print("\n--- Atualizar Status do Pedido ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    consultar_pedidos()
    
    try:
        numero = int(input("\nNúmero do pedido: "))
        
        for pedido in pedidos:
            if pedido.numero == numero:
                print(f"\nPedido #{pedido.numero}")
                print(f"Status atual: {pedido.status}")
                print("\nStatus disponíveis:")
                print("1 - AGUARDANDO APROVACAO")
                print("2 - EM PREPARACAO")
                print("3 - PRONTO")
                print("4 - ENTREGUE")
                print("5 - CANCELADO")
                
                opcao = int(input("\nEscolha o novo status: "))
                
                if opcao == 1:
                    pedido.status = "AGUARDANDO APROVACAO"
                elif opcao == 2:
                    pedido.status = "EM PREPARACAO"
                elif opcao == 3:
                    pedido.status = "PRONTO"
                elif opcao == 4:
                    pedido.status = "ENTREGUE"
                elif opcao == 5:
                    pedido.status = "CANCELADO"
                else:
                    print("Opção inválida!")
                    return
                
                print("Status atualizado com sucesso!")
                return
        
        print("Pedido não encontrado!")
            
    except ValueError:
        print("Valor inválido!")


def filtrar_pedidos_por_status():
    print("\n--- Filtrar Pedidos por Status ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    print("Status disponíveis: AGUARDANDO APROVACAO, EM PREPARACAO, PRONTO, ENTREGUE, CANCELADO")
    status = input("Digite o status para filtrar: ").upper()
    encontrados = False
    
    for pedido in pedidos:
        if pedido.status == status:
            print(f"Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}")
            encontrados = True
    
    if not encontrados:
        print(f"Nenhum pedido encontrado com status: {status}")

def menu_itens():
    while True:
        print("\n--- Gerenciar Itens ---")
        print("1. Cadastrar Item")
        print("2. Atualizar Item")
        print("3. Consultar Itens")
        print("0. Voltar")
        
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 0:
                break
            elif opcao == 1:
                cadastrar_item()
            elif opcao == 2:
                atualizar_item()
            elif opcao == 3:
                consultar_itens()
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Por favor, digite um número válido!")

def menu_pedidos():
    while True:
        print("\n--- Gerenciar Pedidos ---")
        print("1. Criar Pedido")
        print("2. Consultar Pedidos")
        print("3. Atualizar Status do Pedido")   
        print("4. Filtrar Pedidos por Status")  
        print("0. Voltar")
        
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 0:
                break
            elif opcao == 1:
                criar_pedido()
            elif opcao == 2:
                consultar_pedidos()
            elif opcao == 3:
                atualizar_status_pedido()
            elif opcao == 4:
                filtrar_pedidos_por_status()
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Por favor, digite um número válido!")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE PEDIDOS - FOODDELIVERY v4.0")
        print("="*50)
        print("1. Gerenciar Itens")
        print("2. Gerenciar Pedidos")
        print("0. Sair")
        
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 0:
                print("Saindo do sistema...")
                break
            elif opcao == 1:
                menu_itens()
            elif opcao == 2:
                menu_pedidos()
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Por favor, digite um número válido!")

if __name__ == "__main__":
    print("Iniciando Sistema de Pedidos v4.0...")
    menu_principal()