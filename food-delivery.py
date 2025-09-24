# Sistema de Pedidos para Restaurante - FoodDelivery 6.0
# Desenvolvido por Maranhão - UNEX

itens = []
pedidos = []
fila_pendentes = []
fila_preparo = []
fila_prontos = []
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
        self.cupom_desconto = None  
        self.valor_original = valor_total  

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


def aplicar_desconto(valor_total, cupom):
    """Aplica desconto baseado no cupom informado"""
    cupons_validos = {
        "OFF5": 0.05,    
        "OFF10": 0.10,
        "OFF15": 0.15
    }
    
    if cupom in cupons_validos:
        desconto = cupons_validos[cupom]
        valor_com_desconto = valor_total * (1 - desconto)
        print(f"🎫 Cupom {cupom} aplicado! Desconto: {desconto*100}%")
        print(f"💵 Valor original: R$ {valor_total:.2f}")
        print(f"💰 Valor com desconto: R$ {valor_com_desconto:.2f}")
        return valor_com_desconto
    else:
        print("❌ Cupom inválido ou não encontrado!")
        return valor_total

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
    
    
    cupom = input("\n🎫 Cupom de desconto (digite OFF5, OFF10, OFF15 ou Enter para pular): ").strip().upper()
    valor_final = valor_total
    cupom_aplicado = None
    
    if cupom:
        valor_final = aplicar_desconto(valor_total, cupom)
        if valor_final != valor_total: 
            cupom_aplicado = cupom
    
    novo_pedido = Pedido(proximo_id_pedido, itens_pedido, valor_final)
    novo_pedido.cupom_desconto = cupom_aplicado
    novo_pedido.valor_original = valor_total
    
    pedidos.append(novo_pedido)
    fila_pendentes.append(novo_pedido)
    proximo_id_pedido += 1
    
    print(f"\n✅ Pedido #{novo_pedido.numero} criado com sucesso!")
    print(f"💵 Valor total: R$ {valor_final:.2f}")
    if cupom_aplicado:
        print(f"🎫 Cupom aplicado: {cupom_aplicado}")
        print(f"💰 Economia: R$ {(valor_total - valor_final):.2f}")
    print(f"📊 Status: {novo_pedido.status}")

def consultar_pedidos():
    print("\n--- Todos os Pedidos ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    for pedido in pedidos:
        cupom_info = f" | Cupom: {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
        print(f"Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}{cupom_info}")

def visualizar_filas():
    print("\n--- Situação das Filas ---")
    print(f"Pendentes (Aguardando aprovação): {len(fila_pendentes)} pedidos")
    print(f"Em preparo: {len(fila_preparo)} pedidos")
    print(f"Prontos: {len(fila_prontos)} pedidos")
    
    if fila_pendentes:
        print("\n📋 Pedidos Pendentes:")
        for pedido in fila_pendentes:
            cupom_info = f" [Cupom: {pedido.cupom_desconto}]" if pedido.cupom_desconto else ""
            print(f"  #{pedido.numero} - R$ {pedido.valor_total:.2f}{cupom_info}")
    
    if fila_preparo:
        print("\n👨‍🍳 Pedidos em Preparo:")
        for pedido in fila_preparo:
            cupom_info = f" [Cupom: {pedido.cupom_desconto}]" if pedido.cupom_desconto else ""
            print(f"  #{pedido.numero} - R$ {pedido.valor_total:.2f}{cupom_info}")
    
    if fila_prontos:
        print("\n✅ Pedidos Prontos:")
        for pedido in fila_prontos:
            cupom_info = f" [Cupom: {pedido.cupom_desconto}]" if pedido.cupom_desconto else ""
            print(f"  #{pedido.numero} - R$ {pedido.valor_total:.2f}{cupom_info}")


def detalhes_pedido_com_desconto(numero_pedido):
    """Mostra detalhes do pedido incluindo informações de desconto"""
    for pedido in pedidos:
        if pedido.numero == numero_pedido:
            print(f"\n📄 Detalhes do Pedido #{pedido.numero}")
            print(f"📊 Status: {pedido.status}")
            print("\n🛒 Itens do pedido:")
            for item, quantidade in pedido.itens:
                print(f"  - {item.nome} x{quantidade} - R$ {item.preço:.2f} cada")
            
            if pedido.cupom_desconto:
                print(f"\n🎫 Cupom aplicado: {pedido.cupom_desconto}")
                print(f"💵 Valor original: R$ {pedido.valor_original:.2f}")
                print(f"💰 Valor com desconto: R$ {pedido.valor_total:.2f}")
                economia = pedido.valor_original - pedido.valor_total
                print(f"💸 Economia: R$ {economia:.2f}")
            else:
                print(f"\n💵 Valor total: R$ {pedido.valor_total:.2f}")
            
            return True
    return False

def processar_pedidos_pendentes():
    print("\n--- Processar Pedidos Pendentes ---")
    
    if not fila_pendentes:
        print("Nenhum pedido pendente para processar!")
        return
    
    pedido = fila_pendentes[0]
    
    print(f"\n📄 Próximo pedido na fila: #{pedido.numero}")
    detalhes_pedido_com_desconto(pedido.numero)
    
    acao = input("\nAprovar pedido? (S/N): ").upper()
    
    if acao == "S":
        pedido.status = "EM PREPARACAO"
        fila_preparo.append(pedido)
        fila_pendentes.pop(0)
        print("✅ Pedido aprovado e movido para preparo!")
    else:
        pedido.status = "REJEITADO"
        fila_pendentes.pop(0)
        print("❌ Pedido rejeitado!")

def marcar_pedido_pronto():
    print("\n--- Marcar Pedido como Pronto ---")
    
    if not fila_preparo:
        print("Nenhum pedido em preparo!")
        return
    
    print("Pedidos em preparo:")
    for i, pedido in enumerate(fila_preparo, 1):
        cupom_info = f" [Cupom: {pedido.cupom_desconto}]" if pedido.cupom_desconto else ""
        print(f"{i}. Pedido #{pedido.numero} - R$ {pedido.valor_total:.2f}{cupom_info}")
    
    try:
        opcao = int(input("\nNúmero do pedido a marcar como pronto: ")) - 1
        
        if 0 <= opcao < len(fila_preparo):
            pedido = fila_preparo[opcao]
            pedido.status = "PRONTO"
            fila_prontos.append(pedido)
            fila_preparo.pop(opcao)
            print(f"✅ Pedido #{pedido.numero} marcado como pronto!")
        else:
            print("Opção inválida!")
            
    except ValueError:
        print("Valor inválido!")

def atualizar_status_pedido():
    print("\n--- Atualizar Status do Pedido ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    consultar_pedidos()
    
    try:
        numero = int(input("\nNúmero do pedido: "))
        
        if not detalhes_pedido_com_desconto(numero):
            print("Pedido não encontrado!")
            return
            
        print("\nStatus disponíveis:")
        print("1 - AGUARDANDO APROVACAO")
        print("2 - EM PREPARACAO")
        print("3 - PRONTO")
        print("4 - ENTREGUE")
        print("5 - CANCELADO")
        
        opcao = int(input("\nEscolha o novo status: "))
        
        for pedido in pedidos:
            if pedido.numero == numero:
                status_anterior = pedido.status
                
                if opcao == 1:
                    pedido.status = "AGUARDANDO APROVACAO"
                    if pedido not in fila_pendentes:
                        fila_pendentes.append(pedido)
                elif opcao == 2:
                    pedido.status = "EM PREPARACAO"
                    if pedido not in fila_preparo:
                        fila_preparo.append(pedido)
                elif opcao == 3:
                    pedido.status = "PRONTO"
                    if pedido not in fila_prontos:
                        fila_prontos.append(pedido)
                elif opcao == 4:
                    pedido.status = "ENTREGUE"
                elif opcao == 5:
                    pedido.status = "CANCELADO"
                else:
                    print("Opção inválida!")
                    return
                
                
                if status_anterior == "AGUARDANDO APROVACAO" and pedido in fila_pendentes:
                    fila_pendentes.remove(pedido)
                elif status_anterior == "EM PREPARACAO" and pedido in fila_preparo:
                    fila_preparo.remove(pedido)
                elif status_anterior == "PRONTO" and pedido in fila_prontos:
                    fila_prontos.remove(pedido)
                
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
            cupom_info = f" | Cupom: {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
            print(f"Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}{cupom_info}")
            encontrados = True
    
    if not encontrados:
        print(f"Nenhum pedido encontrado com status: {status}")


def consultar_pedidos_com_desconto():
    print("\n--- Pedidos com Cupom de Desconto ---")
    
    pedidos_com_desconto = [p for p in pedidos if p.cupom_desconto]
    
    if not pedidos_com_desconto:
        print("Nenhum pedido com cupom de desconto encontrado!")
        return
    
    for pedido in pedidos_com_desconto:
        economia = pedido.valor_original - pedido.valor_total
        print(f"Pedido #{pedido.numero} | Cupom: {pedido.cupom_desconto} | Valor: R$ {pedido.valor_total:.2f} | Economia: R$ {economia:.2f}")

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
        print("2. Consultar Todos os Pedidos")
        print("3. Visualizar Filas")
        print("4. Processar Pedidos Pendentes")
        print("5. Marcar Pedido como Pronto")
        print("6. Atualizar Status do Pedido")
        print("7. Filtrar Pedidos por Status")
        print("8. Consultar Pedidos com Desconto")  
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
                visualizar_filas()
            elif opcao == 4:
                processar_pedidos_pendentes()
            elif opcao == 5:
                marcar_pedido_pronto()
            elif opcao == 6:
                atualizar_status_pedido()
            elif opcao == 7:
                filtrar_pedidos_por_status()
            elif opcao == 8:
                consultar_pedidos_com_desconto()
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Por favor, digite um número válido!")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE PEDIDOS - FOODDELIVERY v6.0")
        print("=== SISTEMA DE CUPONS DE DESCONTO ===")
        print("Cupons disponíveis: OFF5 (5%), OFF10 (10%), OFF15 (15%)")
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
    print("Iniciando Sistema de Pedidos v6.0...")
    print("🎫 Sistema de Cupons de Desconto Ativado!")
    menu_principal()