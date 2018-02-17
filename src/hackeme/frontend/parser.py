from komparse.parser import Parser
from .grammar import Grammar

def make_parser():
    return Parser(Grammar())
