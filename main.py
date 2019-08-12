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
ASK_DATE=3
ASK_MORE=4
THANK=5

policy_rules = {
    (INIT, "none"): (INIT, "I'm sorry but I'm not sure how to help you"),
    (INIT, "greet"): (INTRO,""),
    (INIT, "get_sth"): (ASK,""),
    (INIT, "get_history_price"): (ASK_DATE,""),
    (INIT, "get_current_price"): (ASK,""),
    (INIT, "get_volumn"): (ASK,""),
    (INIT, "get_cap"): (ASK,""),
    (INIT, "get_cap"): (ASK, ""),

    (ASK_DATE,None):(ASK_MORE,"What else do you want to know?",None),
}


