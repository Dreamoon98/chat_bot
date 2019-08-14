from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import re
import random
from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
def trainer():
    trainer = Trainer(config.load("config_spacy.yml"))
    training_data = load_data('training_data_rasa.json')
    interpreter = trainer.train(training_data)
    return interpreter

interpreter=trainer()

#state
INIT=0
INTRO=1
ASK=2

THANK=3

bot_re = {
    'greet':"Nice to meet you! I'm the robot that can get stock information to you! Which stock do you want to know?",
#    'get_company':"Which stock do you want to know?",
    'get_detail':"What do you want to know about the stock, price, volume or market cap?",
    'thank':"I'm glad to help you!",
    'open':"Open price on {}: {}",
    'volume':"Volume on {}: {}",
    'cap':"Market cap on {}: {}",
    'current_price':"Current price on {}: {}",
    'default':"I'm sorry but I'm not sure how to help you."
}

policy_rules = {

    (INIT, "none"): (INIT, bot_re['default']),
    (INIT, "greet"): (INTRO,bot_re['greet']),
    (INIT, "get_stock"): (ASK,bot_re['get_detail']),
    (INIT, "open"): (ASK, bot_re['open']),
    (INIT, "volume"): (ASK, bot_re['volume']),
    (INIT, "cap"): (ASK, bot_re['cap']),
    (INIT, "current_price"): (ASK, bot_re['current_price']),
    (INIT, "thank"): (THANK,bot_re['thank']),

    (INTRO, "greet"): (INTRO,bot_re['greet']),
    (INTRO, "get_stock"): (ASK,bot_re['get_detail']),
    (INTRO, "open"): (ASK, bot_re['open']),
    (INTRO, "volume"): (ASK, bot_re['volume']),
    (INTRO, "cap"): (ASK, bot_re['cap']),
    (INTRO, "current_price"): (ASK, bot_re['current_price']),
    (INTRO, "thank"): (THANK, bot_re['thank']),

    (ASK, "greet"): (ASK, bot_re['default']),
    (ASK, "get_stock"): (ASK, bot_re['get_detail']),
    (ASK, "open"): (ASK, bot_re['open']),
    (ASK, "volume"): (ASK, bot_re['volume']),
    (ASK, "cap"): (ASK, bot_re['cap']),
    (ASK, "current_price"): (ASK, bot_re['current_price']),
    (ASK, "thank"): (THANK, bot_re['thank']),

    (THANK, "greet"): (INTRO,bot_re['greet']),
    (THANK, "get_stock"): (ASK,bot_re['get_detail']),
    (THANK, "open"): (ASK, bot_re['open']),
    (THANK, "volume"): (ASK, bot_re['volume']),
    (THANK, "cap"): (ASK, bot_re['cap']),
    (THANK, "current_price"): (ASK, bot_re['current_price']),
    (THANK, "thank"): (THANK, bot_re['thank']),


}


def get_entity(self, message):
    if not self.interpreter.parse(message)['entities'] is None:
        return None

    if self.interpreter.parse(message)['entities'][0]['entity'] == 'company':
        return self.interpreter.parse(message)['entities'][0]['value']

def get_intent(message):
    return interpreter.parse(message)['intent']['name']
def interpret(message):
    i_p=interpreter.parse(message)["intent"]["name"]
    intent=i_p["intent"]["name"]
    entities=i_p["entities"]


    msg=message.lower()
    if 'open'in msg:
        return 'open'
    if 'volume'or 'vol' in msg:
        return 'volume'
    if 'cap' or 'market cap' or'marketcap' or 'capacity' or 'market capacity'in msg:
        return 'cap'
    if 'price' in msg:
        return 'current_price'
    return 'none'
def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

def respond(policy, state, message):
    pass


