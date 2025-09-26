# Sistema de Pedidos para Restaurante - FoodDelivery 7.0
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

# NOVO: Função completa de cancelamento de pedidos
def cancelar_pedido():
    print("\n--- Cancelar Pedido ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    # Mostra apenas pedidos que podem ser cancelados
    pedidos_cancelaveis = [p for p in pedidos if p.status in ["AGUARDANDO APROVACAO", "EM PREPARACAO"]]
    
    if not pedidos_cancelaveis:
        print("Nenhum pedido disponível para cancelamento.")
        print("Apenas pedidos com status 'AGUARDANDO APROVACAO' ou 'EM PREPARACAO' podem ser cancelados.")
        return
    
    print("\n📋 Pedidos disponíveis para cancelamento:")
    for pedido in pedidos_cancelaveis:
        cupom_info = f" [Cupom: {pedido.cupom_desconto}]" if pedido.cupom_desconto else ""
        print(f"#{pedido.numero} - Status: {pedido.status} - Valor: R$ {pedido.valor_total:.2f}{cupom_info}")
    
    try:
        numero = int(input("\nNúmero do pedido a cancelar: "))
        
        pedido_encontrado = None
        for pedido in pedidos:
            if pedido.numero == numero:
                pedido_encontrado = pedido
                break
        
        if not pedido_encontrado:
            print("❌ Pedido não encontrado!")
            return
        
        # Verifica se o pedido pode ser cancelado
        if pedido_encontrado.status not in ["AGUARDANDO APROVACAO", "EM PREPARACAO"]:
            print(f"❌ Este pedido não pode ser cancelado.")
            print(f"   Status atual: {pedido_encontrado.status}")
            print("   Apenas pedidos 'AGUARDANDO APROVACAO' ou 'EM PREPARACAO' podem ser cancelados.")
            return
        
        print(f"\n📄 Detalhes do Pedido #{pedido_encontrado.numero}:")
        print(f"   Status: {pedido_encontrado.status}")
        print(f"   Valor: R$ {pedido_encontrado.valor_total:.2f}")
        if pedido_encontrado.cupom_desconto:
            print(f"   Cupom aplicado: {pedido_encontrado.cupom_desconto}")
        
        print("\nItens do pedido:")
        for item, quantidade in pedido_encontrado.itens:
            print(f"   - {item.nome} x{quantidade}")
        
        # Confirmação de cancelamento
        confirmacao = input("\n🚨 TEM CERTEZA que deseja cancelar este pedido? (S/N): ").upper()
        
        if confirmacao == "S":
            # Remove o pedido das filas
            if pedido_encontrado in fila_pendentes:
                fila_pendentes.remove(pedido_encontrado)
            if pedido_encontrado in fila_preparo:
                fila_preparo.remove(pedido_encontrado)
            if pedido_encontrado in fila_prontos:
                fila_prontos.remove(pedido_encontrado)
            
            # Atualiza status para cancelado
            pedido_encontrado.status = "CANCELADO"
            
            print(f"✅ Pedido #{pedido_encontrado.numero} cancelado com sucesso!")
            
            # Mostra resumo do cancelamento
            if pedido_encontrado.cupom_desconto:
                economia = pedido_encontrado.valor_original - pedido_encontrado.valor_total
                print(f"💸 Valor reembolsado: R$ {pedido_encontrado.valor_total:.2f}")
                print(f"🎫 Cupom {pedido_encontrado.cupom_desconto} foi invalidado")
            else:
                print(f"💸 Valor reembolsado: R$ {pedido_encontrado.valor_total:.2f}")
        else:
            print("❌ Cancelamento não realizado. O pedido permanece ativo.")
            
    except ValueError:
        print("❌ Número de pedido inválido!")

def consultar_pedidos():
    print("\n--- Todos os Pedidos ---")
    
    if not pedidos:
        print("Nenhum pedido cadastrado!")
        return
    
    for pedido in pedidos:
        status_icon = "✅" if pedido.status == "ENTREGUE" else "❌" if pedido.status == "CANCELADO" else "⏳"
        cupom_info = f" | Cupom: {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
        print(f"{status_icon} Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}{cupom_info}")

def visualizar_filas():
    print("\n--- Situação das Filas ---")
    print(f"📋 Pendentes: {len(fila_pendentes)} pedido(s)")
    print(f"👨‍🍳 Em preparo: {len(fila_preparo)} pedido(s)")
    print(f"✅ Prontos: {len(fila_prontos)} pedido(s)")
    
    # Conta pedidos cancelados e entregues
    cancelados = len([p for p in pedidos if p.status == "CANCELADO"])
    entregues = len([p for p in pedidos if p.status == "ENTREGUE"])
    print(f"❌ Cancelados: {cancelados} pedido(s)")
    print(f"📦 Entregues: {entregues} pedido(s)")
    
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
            status_icon = "✅" if pedido.status == "ENTREGUE" else "❌" if pedido.status == "CANCELADO" else "⏳"
            print(f"\n{status_icon} Detalhes do Pedido #{pedido.numero}")
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
                    # Remove de todas as filas quando é entregue
                    if pedido in fila_prontos:
                        fila_prontos.remove(pedido)
                elif opcao == 5:
                    # NOVO: Usa a função de cancelamento para consistência
                    print("\n🔔 Use a opção 'Cancelar Pedido' para cancelamentos!")
                    return
                else:
                    print("Opção inválida!")
                    return
                
                # Remove das filas antigas
                if status_anterior == "AGUARDANDO APROVACAO" and pedido in fila_pendentes:
                    fila_pendentes.remove(pedido)
                elif status_anterior == "EM PREPARACAO" and pedido in fila_preparo:
                    fila_preparo.remove(pedido)
                elif status_anterior == "PRONTO" and pedido in fila_prontos:
                    fila_prontos.remove(pedido)
                
                print("✅ Status atualizado com sucesso!")
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
            status_icon = "✅" if status == "ENTREGUE" else "❌" if status == "CANCELADO" else "⏳"
            cupom_info = f" | Cupom: {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
            print(f"{status_icon} Pedido #{pedido.numero} | Valor: R$ {pedido.valor_total:.2f} | Status: {pedido.status}{cupom_info}")
            encontrados = True
    
    if not encontrados:
        print(f"Nenhum pedido encontrado com status: {status}")

def consultar_pedidos_com_desconto():
    print("\n--- Pedidos com Cupom de Desconto ---")
    
    pedidos_com_desconto = [p for p in pedidos if p.cupom_desconto]
    
    if not pedidos_com_desconto:
        print("Nenhum pedido com cupom de desconto encontrado!")
        return
    
    total_economia = 0
    for pedido in pedidos_com_desconto:
        economia = pedido.valor_original - pedido.valor_total
        total_economia += economia
        status_icon = "✅" if pedido.status == "ENTREGUE" else "❌" if pedido.status == "CANCELADO" else "⏳"
        print(f"{status_icon} Pedido #{pedido.numero} | Cupom: {pedido.cupom_desconto} | Valor: R$ {pedido.valor_total:.2f} | Economia: R$ {economia:.2f}")
    
    print(f"\n💰 Total de economia com cupons: R$ {total_economia:.2f}")

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
        print("6. Cancelar Pedido")  # NOVO: Opção de cancelamento
        print("7. Atualizar Status do Pedido")
        print("8. Filtrar Pedidos por Status")
        print("9. Consultar Pedidos com Desconto")
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
                cancelar_pedido()
            elif opcao == 7:
                atualizar_status_pedido()
            elif opcao == 8:
                filtrar_pedidos_por_status()
            elif opcao == 9:
                consultar_pedidos_com_desconto()
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Por favor, digite um número válido!")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE PEDIDOS - FOODDELIVERY v7.0")
        print("=== SISTEMA DE CANCELAMENTO ===")
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
    print("Iniciando Sistema de Pedidos v7.0...")
    print("🚨 Sistema de Cancelamento Ativado!")
    menu_principal()
