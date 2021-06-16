from PIL import Image
import numpy as np
import os

WIDTH = 20
HEIGHT = 20

BLACK ='0'
WHITE = '1'

encodingMappings = {
    'byte': '11',
    'numeric': '10',
}

class Encoder:
    def __init__(self):
        self.encoded = False
        # Full white matrix
        self.data_matrix = [[WHITE for j in range(WIDTH)] for i in range(HEIGHT)]
        # Bottom row except for edge all black
        self.data_matrix[-2] = [WHITE]+[BLACK for i in range(WIDTH-2)] + [WHITE]
        # Left column except for edge all black
        for i in range(1,HEIGHT-1):
            self.data_matrix[i][1] = BLACK


        # Fill Top Right in white,black,black
        self.data_matrix[1][WIDTH-4:WIDTH-1] = [WHITE,BLACK,BLACK]



    def encode(self,msg,encoding_type='byte'):
        self.message = msg
        self.encoding_type = encoding_type


        msg_len = len(msg)
        print(msg_len)
    

        # Fill the first two block with encoding type code
        self.data_matrix[1][2] = encodingMappings[self.encoding_type][0]
        self.data_matrix[1][3] = encodingMappings[self.encoding_type][1]

        # Fill the 12 blocks with length information
 
        binary_len = format(msg_len,'012b') # Length with 12 0 padding
        
        for j in range(12):
            self.data_matrix[1][j+4] = binary_len[j]
            


        
        # Fill the remainig 272 blocks with data
        count = 0
        i,j = 2,2
        print("Filling the data_matrix")
        while (count < msg_len and i<HEIGHT-2):
            
            current_character = msg[count]

            curr_char_int = ord(current_character)

            # Extract a bit and store it in block
            # Binary is stored in reverse order (msd is stored in last position)
            for _ in range(8): 
                val = 1 & curr_char_int
                curr_char_int >>= 1

                self.data_matrix[i][j] = str(val)

                j += 1
                if j  == WIDTH-1:
                    j=2
                    i += 1
                    if i == HEIGHT - 1:
                        break    
            
            # Increase the character count
            count += 1
            
        # Store random information in remaining spaces
        # remaining_spaces  = (HEIGHT-4) * (WIDTH-3) - msg_len

        while (i<HEIGHT-2):
            self.data_matrix[i][j] = str(np.random.randint(0,2))

            j += 1
            if j  == WIDTH-1:
                j=2
                i += 1
                if i == HEIGHT - 1:
                    break    
            
            # Increase the character count
            count += 1

        self._print_data_matrix()
        
        self.encoded = True

    def matrix_to_image(self,size = (256,256),location='./',filename='generated',file_format='png'):
        if not self.encoded:
            raise Exception("Error: Message not encoded. Encode message before converting to image")
        matrix_array_int = np.array(self.data_matrix).astype('uint8')
        img = Image.fromarray(matrix_array_int*255,'L')
        
        img = img.resize(size, Image.NEAREST)
        img.save(os.path.join(os.path.abspath(location),filename),file_format)
        print("Saved as ",os.path.join(os.path.abspath(location),filename))

    def _print_data_matrix(self):
        for i in range(HEIGHT):
            print(' '.join(self.data_matrix[i]))

if __name__ == '__main__':
    # Can store upto 34 characters
    e = Encoder()
    e.encode("My name is Anthony Gonzalvez. And I am in America!!")
    e.matrix_to_image()