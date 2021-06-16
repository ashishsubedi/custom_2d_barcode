import os

from PIL import Image
from encoder import Encoder
from decoder import Decoder


from blessed import Terminal

if __name__ == '__main__':
    term = Terminal()
    run = True
    while run:
        print(term.on_snow4(term.clear()))
        print(term.darkred_on_snow4(term.center('Welcome to DxCode Client')))
        print(term.black_on_snow4("Use this program to encode or decode your message in DxCode "))
        print(term.blue_on_snow4("1=> Encode Message"))
        print(term.blue_on_snow4("2=> Decode Message"))
        print(term.darkred_on_snow4("Anything else=> Quit"))
        
        choice = input(term.darkgreen_on_snow4("=>"))

        if choice.isdigit():
            if choice == '1':
                # Encode
                enc = Encoder()
                print(term.on_snow4(term.clear()))

                print(term.indigo_on_snow4("Enter your message. Max length: 34 characters. More than that are ignored. Supports ascii only."))

                msg = input(term.darkgreen_on_snow4("=>"))

                if not msg:
                    print(term.darkred_on_snow4(term.center('Invald msg. Exiting application')))
                    run = False
                    break

                print(term.indigo_on_snow4("Enter output filename (default: generated.png)"))
                output = input(term.darkgreen_on_snow4("=>")) or 'generated.png'
                
                print(term.indigo_on_snow4("Output image size? (default: (256,256)"))
                _size  = input(term.darkgreen_on_snow4("=>")) or (256,256)
                
                print(term.indigo_on_snow4("Enter path to save (default: current location)"))
                location = input(term.darkgreen_on_snow4("=>")) or './'


                if enc.encode(msg):
                    if enc.matrix_to_image(_size,location,output):
                        print(term.black_on_snow4("Saved as ",os.path.join(os.path.abspath(location),output)))
                    run = False
                    break
                else:
                    print(term.black_on_snow4("Error Occured! Exiting!!"))

                    

            elif choice == '2':
                # Decode
                dec = Decoder()
                print(term.on_snow4(term.clear()))
                print(term.indigo_on_snow4("Enter path to save (default: ./generated.png)"))
                location = input(term.darkgreen_on_snow4("=>")) or './generated.png'
                dec.load_image(location)
                
                dec.image_to_matrix()
                msg = dec.decode()

                print(term.indigo_on_snow4("Your message is: "))
                print(term.black_on_snow4(msg))
                run = False
                break

            else:
                print(term.darkred_on_snow4("Exiting."))
                run = False
                break
        else:
            print(term.darkred_on_snow4("Exiting."))

            run = False
            break










