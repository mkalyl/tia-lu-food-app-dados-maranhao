# Sistema de Pedidos para Restaurante - FoodDelivery Final 
# Desenvolvido por Maranhão - UNEX

itens = []          
pedidos = []
fila_pendentes = []
fila_aceitos = []
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
    def __init__(self, numero, itens, valor_total, status):
        self.numero = numero
        self.itens = itens  
        self.valor_total = valor_total
        self.status = status
        self.cupom_desconto = None

def cadastrar_item():
    global proximo_id_item
    print("\n🎯 --- Cadastrar Novo Item ---")
    
    nome = input("📝 Nome do item: ")
    descricao = input("📄 Descrição: ")
    preço = float(input("💵 Preço: R$ "))
    estoque = int(input("📦 Estoque inicial: "))
    
    novo_item = Item(proximo_id_item, nome, descricao, preço, estoque)
    itens.append(novo_item)
    proximo_id_item += 1
    
    print(f"✅ Item '{nome}' cadastrado com sucesso! Código: {novo_item.codigo}")

def consultar_itens():
    print("\n📋 --- Itens do Cardápio ---")
    if not itens:
        print("❌ Nenhum item cadastrado.")
        return
    
    for item in itens:
        print(f"🔸 Código: {item.codigo} | Nome: {item.nome} | Preço: R$ {item.preço:.2f} | Estoque: {item.estoque}")

def atualizar_item():
    print("\n✏️ --- Atualizar Item ---")
    consultar_itens()
    
    if not itens:
        return
    
    try:
        codigo = int(input("\n🔢 Código do item a atualizar: "))
        item_encontrado = None
        
        for item in itens:
            if item.codigo == codigo:
                item_encontrado = item
                break
        
        if item_encontrado:
            print(f"\n📝 Editando item: {item_encontrado.nome}")
            item_encontrado.nome = input(f"🆕 Novo nome ({item_encontrado.nome}): ") or item_encontrado.nome
            item_encontrado.descricao = input(f"📄 Nova descrição ({item_encontrado.descricao}): ") or item_encontrado.descricao
            item_encontrado.preço = float(input(f"💵 Novo preço ({item_encontrado.preço}): ") or item_encontrado.preço)
            item_encontrado.estoque = int(input(f"📦 Novo estoque ({item_encontrado.estoque}): ") or item_encontrado.estoque)
            print("✅ Item atualizado com sucesso!")
        else:
            print("❌ Item não encontrado!")
            
    except ValueError:
        print("❌ Código inválido!")

def criar_pedido():
    global proximo_id_pedido
    print("\n🆕 --- Criar Novo Pedido ---")
    
    if not itens:
        print("❌ Não há itens disponíveis no cardápio!")
        return
    
    consultar_itens()
    itens_pedido = []
    valor_total = 0.0
    
    while True:
        try:
            codigo = int(input("\n🔢 Código do item (0 para finalizar): "))
            if codigo == 0:
                break
            
            quantidade = int(input("📦 Quantidade: "))
            
            item_encontrado = None
            for item in itens:
                if item.codigo == codigo:
                    item_encontrado = item
                    break
            
            if item_encontrado and item_encontrado.estoque >= quantidade:
                itens_pedido.append((item_encontrado, quantidade))
                valor_total += item_encontrado.preço * quantidade
                print(f"✅ Item '{item_encontrado.nome}' adicionado ao pedido!")
            else:
                print("❌ Item não encontrado ou estoque insuficiente!")
                
        except ValueError:
            print("❌ Valor inválido!")
    
    if not itens_pedido:
        print("❌ Pedido vazio! Cancelando operação.")
        return
    
    # 🎫 Sistema de Cupons
    cupom = input("\n🎫 Cupom de desconto (OFF5, OFF10, OFF15 ou Enter para pular): ").upper()
    if cupom == "OFF5":
        desconto = 0.05
        valor_total *= (1 - desconto)
        print("🎉 Desconto de 5% aplicado!")
    elif cupom == "OFF10":
        desconto = 0.10
        valor_total *= (1 - desconto)
        print("🎉 Desconto de 10% aplicado!")
    elif cupom == "OFF15":
        desconto = 0.15
        valor_total *= (1 - desconto)
        print("🎉 Desconto de 15% aplicado!")
    elif cupom:
        print("❌ Cupom inválido! Nenhum desconto aplicado.")
    
    novo_pedido = Pedido(proximo_id_pedido, itens_pedido, valor_total, "AGUARDANDO APROVACAO")
    pedidos.append(novo_pedido)
    fila_pendentes.append(novo_pedido)
    proximo_id_pedido += 1
    
    print(f"\n✅ Pedido #{novo_pedido.numero} criado com sucesso!")
    print(f"💵 Valor total: R$ {valor_total:.2f}")
    if cupom in ["OFF5", "OFF10", "OFF15"]:
        print(f"🎫 Cupom aplicado: {cupom}")
    print("📊 Status: AGUARDANDO APROVACAO")

def processar_pedidos_pendentes():
    print("\n⚡ --- Processar Pedidos Pendentes ---")
    
    if not fila_pendentes:
        print("✅ Nenhum pedido pendente!")
        return
    
    pedido = fila_pendentes[0]
    
    print(f"\n📄 Pedido #{pedido.numero}")
    print("🛒 Itens do pedido:")
    for item, quantidade in pedido.itens:
        print(f"  - {item.nome} x{quantidade}")
    print(f"💵 Valor total: R$ {pedido.valor_total:.2f}")
    
    acao = input("\n✅ Aceitar pedido? (S/N): ").upper()
    
    if acao == "S":
        pedido.status = "ACEITO"
        fila_aceitos.append(pedido)
        print("✅ Pedido aceito e movido para preparo!")
    else:
        pedido.status = "REJEITADO"
        print("❌ Pedido rejeitado!")
    
    fila_pendentes.pop(0)

def cancelar_pedido():
    print("\n🚨 --- Cancelar Pedido ---")
    
    if not pedidos:
        print("❌ Nenhum pedido cadastrado!")
        return
    
    try:
        numero = int(input("🔢 Número do pedido a cancelar: "))
        pedido_encontrado = None
        
        for pedido in pedidos:
            if pedido.numero == numero:
                pedido_encontrado = pedido
                break
        
        if not pedido_encontrado:
            print("❌ Pedido não encontrado!")
            return
        
        print(f"\n📄 Pedido #{pedido_encontrado.numero}")
        print(f"📊 Status atual: {pedido_encontrado.status}")
        
        if pedido_encontrado.status in ["AGUARDANDO APROVACAO", "ACEITO"]:
            confirmacao = input("⚠️ Tem certeza que deseja cancelar este pedido? (S/N): ").upper()
            if confirmacao == "S":
                pedido_encontrado.status = "CANCELADO"
                
                if pedido_encontrado in fila_pendentes:
                    fila_pendentes.remove(pedido_encontrado)
                if pedido_encontrado in fila_aceitos:
                    fila_aceitos.remove(pedido_encontrado)
                
                print("✅ Pedido cancelado com sucesso!")
            else:
                print("❌ Cancelamento não realizado.")
        else:
            print("❌ Este pedido não pode ser cancelado.")
            print("   Apenas pedidos 'AGUARDANDO APROVACAO' ou 'ACEITO' podem ser cancelados.")
            
    except ValueError:
        print("❌ Valor inválido!")

def atualizar_status_pedido():
    print("\n🔄 --- Atualizar Status do Pedido ---")
    
    if not pedidos:
        print("❌ Nenhum pedido cadastrado!")
        return
    
    try:
        numero = int(input("🔢 Número do pedido: "))
        pedido_encontrado = None
        
        for pedido in pedidos:
            if pedido.numero == numero:
                pedido_encontrado = pedido
                break
        
        if not pedido_encontrado:
            print("❌ Pedido não encontrado!")
            return
        
        print(f"\n📄 Pedido #{pedido_encontrado.numero}")
        print(f"📊 Status atual: {pedido_encontrado.status}")
        print("\n🔄 Status disponíveis:")
        print("1 - ⏳ FAZENDO (em preparação)")
        print("2 - 👨‍🍳 FEITO (preparo finalizado)")
        print("3 - 🚗 ESPERANDO ENTREGADOR")
        print("4 - 🚀 SAÍDA PARA ENTREGA")
        print("5 - ✅ ENTREGUE")
        
        opcao = int(input("\n🎯 Escolha o novo status: "))
        
        if opcao == 1:
            pedido_encontrado.status = "FAZENDO"
        elif opcao == 2:
            pedido_encontrado.status = "FEITO"
            fila_prontos.append(pedido_encontrado)
        elif opcao == 3:
            pedido_encontrado.status = "ESPERANDO ENTREGADOR"
        elif opcao == 4:
            pedido_encontrado.status = "SAÍDA PARA ENTREGA"
        elif opcao == 5:
            pedido_encontrado.status = "ENTREGUE"
        else:
            print("❌ Opção inválida!")
            return
        
        print("✅ Status atualizado com sucesso!")
            
    except ValueError:
        print("❌ Valor inválido!")

def exibir_todos_pedidos():
    print("\n📊 --- Todos os Pedidos ---")
    
    if not pedidos:
        print("❌ Nenhum pedido cadastrado!")
        return
    
    for pedido in pedidos:
        status_icon = "✅" if pedido.status == "ENTREGUE" else "❌" if pedido.status == "CANCELADO" else "⏳"
        cupom_info = f" | 🎫 {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
        print(f"{status_icon} Pedido #{pedido.numero} | 💵 R$ {pedido.valor_total:.2f} | 📊 {pedido.status}{cupom_info}")

def filtrar_pedidos_por_status():
    print("\n🔍 --- Filtrar Pedidos por Status ---")
    
    if not pedidos:
        print("❌ Nenhum pedido cadastrado!")
        return
    
    status = input("🎯 Digite o status para filtrar: ").upper()
    encontrados = False
    
    for pedido in pedidos:
        if pedido.status == status:
            status_icon = "✅" if status == "ENTREGUE" else "❌" if status == "CANCELADO" else "⏳"
            cupom_info = f" | 🎫 {pedido.cupom_desconto}" if pedido.cupom_desconto else ""
            print(f"{status_icon} Pedido #{pedido.numero} | 💵 R$ {pedido.valor_total:.2f} | 📊 {pedido.status}{cupom_info}")
            encontrados = True
    
    if not encontrados:
        print(f"❌ Nenhum pedido encontrado com status: {status}")

def menu_principal():
    while True:
        print("\n" + "="*60)
        print("🏪 SISTEMA DE PEDIDOS - FOODDELIVERY v8.0")
        print("🎨Desenvolvido por Maranhão - UNEX")
        print("="*60)
        print("1. 📋 Gerenciar Menu de Itens")
        print("2. 🛒 Gerenciar Menu de Pedidos")
        print("3. 📊 Consultas e Relatórios")
        print("0. 🚪 Sair")
        
        try:
            opcao = int(input("\n🎯 Escolha uma opção: "))
            
            if opcao == 0:
                print("👋 Saindo do sistema... Até logo!")
                break
            elif opcao == 1:
                menu_itens()
            elif opcao == 2:
                menu_pedidos()
            elif opcao == 3:
                menu_consultas()
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Por favor, digite um número válido!")

def menu_itens():
    while True:
        print("\n📋 --- Gerenciar Itens ---")
        print("1. 🆕 Cadastrar Item")
        print("2. ✏️ Atualizar Item")
        print("3. 👀 Consultar Itens")
        print("0. ↩️ Voltar")
        
        try:
            opcao = int(input("\n🎯 Escolha uma opção: "))
            
            if opcao == 0:
                break
            elif opcao == 1:
                cadastrar_item()
            elif opcao == 2:
                atualizar_item()
            elif opcao == 3:
                consultar_itens()
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Por favor, digite um número válido!")

def menu_pedidos():
    while True:
        print("\n🛒 --- Gerenciar Pedidos ---")
        print("1. 🆕 Criar Pedido")
        print("2. ⚡ Processar Pedidos Pendentes")
        print("3. 🔄 Atualizar Status de Pedido")
        print("4. 🚨 Cancelar Pedido")
        print("0. ↩️ Voltar")
        
        try:
            opcao = int(input("\n🎯 Escolha uma opção: "))
            
            if opcao == 0:
                break
            elif opcao == 1:
                criar_pedido()
            elif opcao == 2:
                processar_pedidos_pendentes()
            elif opcao == 3:
                atualizar_status_pedido()
            elif opcao == 4:
                cancelar_pedido()
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Por favor, digite um número válido!")

def menu_consultas():
    while True:
        print("\n📊 --- Consultas e Relatórios ---")
        print("1. 👀 Exibir Todos os Pedidos")
        print("2. 🔍 Filtrar Pedidos por Status")
        print("0. ↩️ Voltar")
        
        try:
            opcao = int(input("\n🎯 Escolha uma opção: "))
            
            if opcao == 0:
                break
            elif opcao == 1:
                exibir_todos_pedidos()
            elif opcao == 2:
                filtrar_pedidos_por_status()
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Por favor, digite um número válido!")

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Pedidos v8.0 Emojizado...")
    print("🎨 Interface melhorada com emojis e cores!")
    menu_principal()