#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    #Variabili Parole
    LettoSwitch=["switch","bedroom","light"]
    DeskSwitch=["switch","desk","light"]

    #Variabili Pin

    #Variabili Debug
    inizio=0
    GiaUsate=[]
    frase=[]
    tot=0
    trovato=0

    #INIZIO PROGRAMA
    #Sarà readable_results
    Parole = re.split(" ",intentMessage.input)
    answer = intentMessage.input
    idh = intentMessage.session_id
    hermes.publish_end_session(idh, answer)

    for w in range(inizio,len(Parole)):
        frase.insert(len(frase),Parole[w])
    #------------------------------------ LettoSwitch
        for i in range(0,len(frase)):
            if(frase[i] in LettoSwitch and frase[i] not in GiaUsate):
                GiaUsate.insert(0,frase[i])
                tot=tot+1
            if(tot==len(LettoSwitch)):
                trovato=1
                answer = "Ok,I switched bedroon light"
                idh = intentMessage.session_id
                hermes.publish_end_session(idh, answer)
                break
        tot=0
        GiaUsate=[]
    #------------------------------------ DeskSwitch
        for i in range(0,len(frase)):
            if(frase[i] in DeskSwitch and frase[i] not in GiaUsate):
                GiaUsate.insert(0,frase[i])
                tot=tot+1
            if(tot==len(DeskSwitch)):
                trovato=1
                answer = "Ok,I switched desk light"
                idh = intentMessage.session_id
                hermes.publish_end_session(idh, answer)
                break
        tot=0
        GiaUsate=[]
    #--------
        if trovato==1:
            frase=[]
            trovato=0
    #fine

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Ricky7714:On-Off_light_room", subscribe_intent_callback) \
         .start()
         
