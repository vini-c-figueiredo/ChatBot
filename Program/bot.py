import telebot
import requests, json
import os
from dotenv import load_dotenv 
from datetime import datetime, timedelta, time

load_dotenv()

tot_preco = 0
count = 0
user = None
Finaliza_user = None
Lista_pedidos = []

CHAVE_API = os.getenv("chave_api")

bot = telebot.TeleBot(CHAVE_API)

@bot.message_handler(commands=["sim"])
def sim(mensagem):
    texto1 = "Que ótimo!!"
    texto2 = """Clique no sabor que deseja!
    
    /opcao1 presunto e queijo
    
    /opcao2 Frango com catupiry
    
    /opcao3 Portuguesa 
    """
    bot.reply_to(mensagem, texto1)
    bot.send_message(mensagem.chat.id, texto2)
    
@bot.message_handler(commands=["nao"])
def nao(mensagem):
    texto1 = "Poxa, que pena! Mas se precisar estamos aqui!" 
    bot.reply_to(mensagem, texto1)
    global count, user
    Finaliza_user = mensagem.chat.id
    Lista_pedidos.remove(Finaliza_user)    
    count = 0

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    texto1 = """Deseja mais algo?
    Clique no sabor que deseja!
    
    /opcao1 presunto e queijo
    
    /opcao2 Frango com catupiry
    
    /opcao3 Portuguesa
    
    /opcao4 Fechar pedido
    
    /opcao5 Cancelar"""
    bot.send_message(mensagem.chat.id, texto1)
    
    global tot_preco    
    preco = 40
    tot_preco = tot_preco + preco
    
    with open ('nota.txt', 'a') as arquivo:
        texto_nota = """Presunto e queijo.................R$40,00\n"""
        arquivo.write(texto_nota)
    
@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    texto1 = """Deseja mais algo?
    Clique no sabor que deseja!
    
    /opcao1 presunto e queijo
    
    /opcao2 Frango com catupiry
    
    /opcao3 Portuguesa
    
    /opcao4 Fechar Pedido
    
    /opcao5 Cancelar"""
    bot.send_message(mensagem.chat.id, texto1)

    global tot_preco
    preco = 40
    tot_preco = tot_preco + preco
    
    with open ('nota.txt', 'a') as arquivo:
        texto_nota = """Frango com catupiry...............R$40,00\n"""
        arquivo.write(texto_nota)
    
@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    texto1 = """Deseja mais algo?
    Clique no sabor que deseja!
    
    /opcao1 presunto e queijo
    
    /opcao2 Frango com catupiry
    
    /opcao3 Portuguesa
    
    /opcao4 Fechar Pedido
    
    /opcao5 Cancelar"""
    bot.send_message(mensagem.chat.id, texto1)
    
    global tot_preco    
    preco = 40
    tot_preco = tot_preco + preco
    
    with open ('nota.txt', 'a') as arquivo:
        texto_nota = """Portuguesa........................R$40,00\n"""
        arquivo.write(texto_nota)
    
@bot.message_handler(commands=["opcao4"])
def opcao4(mensagem):    
    global tot_preco, count
    preco_total = f"{tot_preco:_.2f}"
    preco_total = preco_total.replace('.', ',').replace('_', '.')
    
    texto1 = """Compra finalizada, o valor total foi de R${}""".format(preco_total)
   
    
    data_ped = datetime.now()
    tempo_entrega = timedelta(minutes = 40)
    data_entrega = (data_ped + tempo_entrega)
    data = ("{}").format(time(data_entrega.hour, data_entrega.minute))
        
    bot.send_message(mensagem.chat.id, texto1)
    texto2 = "A pizza chega em 40 minutos, horário de previsão {}".format(data)
    bot.send_message(mensagem.chat.id, texto2)
    
    with open ('nota.txt', 'a') as arquivo:
        texto_nota = f"""\nValor Total.......................R${preco_total}"""
        arquivo.write(texto_nota)
        
    preco_total = 0
    tot_preco = 0 
    
    texto3 = """Qual a forma de pagamento?
    /cartao 
    
    /dinheiro
    
    /PIX"""
    
    bot.send_message(mensagem.chat.id, texto3)
    
@bot.message_handler(commands=["opcao5"])
def opcao5(mensagem):
    texto1 = "Seu pedido foi cancelado!"
    bot.send_message(mensagem.chat.id, texto1)
    
    if (os.path.exists("nota.txt")):
        os.remove("nota.txt")
    
    global count, tot_preco, user
    count = 0
    Finaliza_user = mensagem.chat.id
    Lista_pedidos.remove(Finaliza_user)
    tot_preco = 0
    
@bot.message_handler(commands=["cartao"])
def cartao(mensagem):
    global count
    
    texto1 = """E qual o CEP de entrega?"""
    
    bot.send_message(mensagem.chat.id, texto1)
    
    count = 2

@bot.message_handler(commands=["dinheiro"])
def dinheiro(mensagem):
    global count
    
    texto1 = """E qual o CEP de entrega?"""
    
    bot.send_message(mensagem.chat.id, texto1)
    
    count = 2

@bot.message_handler(commands=["PIX"])
def pix(mensagem):
    global count
    
    texto1 = """E qual o CEP de entrega?"""
    
    bot.send_message(mensagem.chat.id, texto1)
    
    count = 2

def retorna(mensagem):
    return True

@bot.message_handler(func=retorna)
def verificar(mensagem):
    global count, user
    user = mensagem.chat.id
    
    if (count == 0 or count == 1):
        responder(mensagem)
    elif (count == 2):
        endereco(mensagem)
    
def endereco(mensagem):
    global count, user
    while True:        
        endereco_entrega = mensagem.text
        Finaliza_user = mensagem.chat.id
            
        dados = requests.get(f"https://cep.awesomeapi.com.br/json/{endereco_entrega}")
        formatado = json.loads(dados.text)
            
        try:
            endereco_rua = formatado['address']
        except:
            texto2 = """O cep não existe! Digite novamente!"""
            bot.send_message(mensagem.chat.id, texto2)
            break    
            
        texto1 = f"""ótimo, o pedido será entregue no endereço: {endereco_rua}"""
        bot.send_message(mensagem.chat.id, texto1)
        with open('nota.txt', 'rb') as arquivo:
            bot.send_document(mensagem.chat.id, arquivo)
                    
        if (os.path.exists("nota.txt")):
            os.remove("nota.txt")

        count = 0
        Lista_pedidos.remove(Finaliza_user)
        break

def responder(mensagem):
    global count, user
    
    user = mensagem.chat.id
    
    if (user not in Lista_pedidos):
        cliente = mensagem.from_user.first_name
        Lista_pedidos.append(user)
        texto = """
        Bem-Vindo a pizzaria, {}""".format (cliente)
        fazer_pedido = """Você gostaria de fazer um pedido?
        /sim
        /nao"""
        bot.reply_to(mensagem, texto)
        bot.send_message(mensagem.chat.id, fazer_pedido)       
    elif (user in Lista_pedidos and count != 2):
        texto1 = "Você já tem um pedido pendente, finalize ele para continuar!"
        
        bot.send_message(mensagem.chat.id, texto1)

bot.polling()