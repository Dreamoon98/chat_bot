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
ASK_COMPANY=2
ASK_SPE=3
THANK=4

policy_rules = {
    '''
    (INIT, "none"): (INIT, "I'm sorry but I'm not sure how to help you"),
    (INIT, "greet"): (INTRO,""),
    (INIT, "get_company"): (ASK_SPE,""),
    (INIT, "get_stock"): (ASK_SPE,""),
    (INIT, "tks"): (THANK,"I'm glad to help you!"),

    (INTRO, "none"):(INIT, "I'm sorry but I'm not sure how to help you"),
    (INTRO, "greet"): (INTRO,""),
    (INTRO, "get_company"): (ASK_COMPANY,""),
    (INTRO, "get_stock"): (ASK_SPE,""),
    (INTRO, "tks"): (THANK, "I'm glad to help you!"),
    '''

    (INIT, "none"): INIT,
    (INIT, "greet"): INTRO,
    (INIT, "tks"): THANK,

    (INTRO, "get_company"): ASK_COMPANY,
    (INTRO, "get_stock"): ASK_SPE,
    (INTRO, "tks"): THANK,

    (ASK_COMPANY, "get_company"): ASK_SPE,
    (ASK_COMPANY, "get_stock"): ASK_SPE,
    (ASK_COMPANY, "tks"): THANK,

    (ASK_SPE, "get_stock"): ASK_SPE,
    (ASK_SPE, "get_company"): ASK_SPE,
    (ASK_COMPANY, "tks"): THANK,

}
bot_re = {
    'intro':"I'm the robot that can get stock information to you!",
    'get_company':"Which stock do you want to know?",
    'thank':"I'm glad to help you!",
    'open':"Open price on {}: {}",
    'volume':"Volume on {}: {}",
    'cap':"Market cap on {}: {}",
    'current_price':"Current price on {}: {}",
    'default':"I'm sorry but I'm not sure how to help you"
}

def interpret(message):
    intent=interpreter.parse(message)
    entities = interpreter.parse(message)["entities"]
    return ''
def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

def respond(policy, state, message):
    pass


