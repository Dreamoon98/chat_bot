from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import re
import random
from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import yfinance as yf
from datetime import datetime
def trainer():
    trainer = Trainer(config.load("config_spacy.yml"))
    training_data = load_data('training.md')
    interpreter = trainer.train(training_data)
    return interpreter

interpreter=trainer()
g_detail=None
g_company=None
#state
INIT=0
INTRO=1
ASK_COMPANY=2
ASK_DETAIL=3
THANK=4

bot_re = {
    'greet':"Nice to meet you! I'm the robot that can get stock information to you! Which stock do you want to know?",
#    'get_company':"Which stock do you want to know?",
    'get_detail':"What do you want to know about the stock, price, volume or market cap?",
    'thank':"I'm glad to help you!",
    'open':"Open price: {} ",
    'volume':"Volume on {0[0]} UTC: {0[1]} ",
    'cap':"Market cap on {0[0]} UTC: {0[1]} ",
    'current_price':"Current price on {0[0]} UTC: {0[1]} ",
    'default':"I'm sorry but I'm not sure how to help you."
}

policy_rules={
    (INIT, "none"): INIT,
    (INIT, "greet"): INTRO,
    (INIT, "get_company"):ASK_COMPANY,
    (INIT, "get_detail"):ASK_DETAIL,
    (INIT, "thank"):THANK,

    (INTRO, "greet"):INTRO,
    (INTRO, "get_company"): ASK_COMPANY,
    (INTRO, "get_detail"): ASK_DETAIL,
    (INTRO, "thank"): THANK,

    (ASK_COMPANY, "get_company"): ASK_DETAIL,
    (ASK_COMPANY, "get_detail"): ASK_DETAIL,
    (ASK_COMPANY, "thank"): THANK,

    (ASK_DETAIL, "get_detail"): ASK_DETAIL,
    (ASK_COMPANY, "thank"): THANK,

}


'''
policy_rules_TMP = {
    
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
    
    
    (INIT, "none"): (INIT, bot_re['default']),
    (INIT, "greet"): (INTRO,bot_re['greet']),   
}
'''


def get_entity(message):
    entities = interpreter.parse(message)['entities']
    params = {}
    # Fill the dictionary with entities
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])
    return params


def get_intent(message):
    intent = interpreter.parse(message)['intent']
    params = {}
    params[intent['name']] = intent['confidence']
    return params
def interpret(message):
    intent=get_intent(message)
    if 'greet' in intent:
        return 'greet'
    ents = get_entity(message)
    if 'company' in ents:
        global g_company
        g_company = ents['company']
        return 'get_company'
    if 'details'in ents:
        global g_detail
        g_detail=ents['detail']
        return 'get_detail'

    return 'none'

def get_open(company):
    a = yf.Ticker(company)
    return a.info['regularMarketOpen']

def get_c_price(company):
    a = yf.Ticker(company)
    i = a.info
    p = i['regularMarketPrice']
    t = i['regularMarketTime']
    utc_time = datetime.utcfromtimestamp(t)
    return utc_time, p

def get_volume(company):
    a = yf.Ticker(company)
    i = a.info
    v = i['regularMarketVolume']
    t = i['regularMarketTime']
    utc_time = datetime.utcfromtimestamp(t)
    return utc_time, v

def get_cap(company):
    a = yf.Ticker(company)
    i = a.info
    c = i['marketCap']
    t = i['regularMarketTime']
    utc_time = datetime.utcfromtimestamp(t)
    return utc_time, c

def send_message(policy, state, message):
    print("USER : {}".format(message))
    new_state, response = respond(policy, state, message)
    print("BOT : {}".format(response))
    return new_state

def respond(policy, state, message):
    it=interpret(message)
    new_state=policy[(state,it)]

    if it=='greet':
        res=bot_re['greet']
    if it=='thank':
        res=bot_re['thank']
    if it=='get_company':
        res=bot_re['get_detail']
    if it=='get_detail':
        if g_detail=='open' or g_detail=='open price' or g_detail== 'open_price':
            res=bot_re['open'].format(get_open(g_company))
        if g_detail=='price' or g_detail=='current price':
            res=bot_re['current_price'].format(get_c_price(g_company))
        if g_detail=='volume' :
            res=bot_re['volume'].format(get_volume(g_company))
        if g_detail=='cap' or g_detail=='market cap' or g_detail== 'market_cap':
            res=bot_re['cap'].format(get_cap(g_company))
    if it=='none':
        res=bot_re['default']

    return new_state, res
