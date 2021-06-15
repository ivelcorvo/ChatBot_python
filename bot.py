from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.trainers import ListTrainer
import re  # regular expression
 
# static_url_path='/static' para poder trazaer a imagem da pasta 'icon'
app = Flask(__name__,static_url_path='/static') 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  
# ===============================   
# instânciando um objeto ChatBot
bot = ChatBot('Jason', read_only=True, 
              response_selection_method=get_most_frequent_response,     
              storage_adapter="chatterbot.storage.SQLStorageAdapter",
              database_uri='sqlite:///database.sqlite3'
              )

# ================  
# treinando o bot 
treinador = ListTrainer(bot)

conversa = open("conversa.txt", encoding="utf-8", errors="ignore").read().split("\n") 
treinador.train(conversa)

# ======================  
# retorna a página html
@app.route("/")
def home():
    return render_template("index.html")

# =================================== 
# limpa o texto. arruma alguns erros
def limpa_texto(texto):
  texto = texto.lower()
  texto = re.sub("vc","você",texto)
  texto = re.sub("td","tudo",texto)
  texto = re.sub("xau","tchau",texto)
  texto = re.sub("proposito","propósito",texto)
  return texto

# =======================================================
# pega a mensagem do usuário e devolve a resposta do bot
@app.route("/get")
def get_bot_response():
    while True:
        try:
            pergunta = userText = request.args.get('msg')      
            pergunta = limpa_texto(pergunta)
            resposta = bot.get_response(pergunta)
            if float(resposta.confidence) > 0.5:
                return str(resposta)
            else:
                return str(' Desculpe . . . Ainda não sei responder esta pergunta.') 
            return str(resposta)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
        
# ==================
# inicia o programa
if __name__ == "__main__":
    app.run()      