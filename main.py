from PIL import Image
from encoder import Encoder
from decoder import Decoder

from blessed import Terminal

if __name__ == '__main__':
    term = Terminal()
    
    print(term.on_darkkhaki(term.clear()))
    print(term.darkred_on_darkkhaki(term.center('Welcome')))
    print(term.black_on_darkkhaki("Use this program to encode or decode your message in  "))











