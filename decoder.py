from PIL import Image
import numpy as np
import cv2
import os

WIDTH = 20
HEIGHT = 20

BLACK ='0'
WHITE = '1'

encodingMappings = {
    '11': 'byte',
    '10':'numeric',
}

class Decoder:
    def __init__(self):
        
        # Full white matrix
        self.data_matrix = [[WHITE for j in range(WIDTH)] for i in range(HEIGHT)]
        self.image = None
        self.extracted = False
        
    def load_image(self, path):
        self.image = cv2.imread(path,0)
        if self.image is None:
            raise Exception("Error: Image not found")
        return self.image

    def image_to_matrix(self):
        '''
            Retrieves matrix from the given image
            Steps:
                - Find the correct orientation of the image
                - Figure out the block size. 
                    This can be done by measuring the distance between 
                    white and black blocsk of information blocks
                - Fill the data_matrix with values

        '''
        # cv2.imshow('image',self.image)
        # cv2.waitKey(0)
        
        # Binarize image to make sure light doesn't affect the data
        _,img = cv2.threshold(self.image,127,255,cv2.THRESH_BINARY)

        
        # Marker for top left, top right and bottom left
        tl,tr,bl = (0,0),(0,0),(0,0)

        
        h,w = img.shape[:2]

        # img = cv2.resize(img, (WIDTH,HEIGHT))
        # Find the orientation and rotate accordingly
        locatedFirstBlack = False
        startx,starty = 0,0
        # # pbr = pixels to block ratio. It gives how many pixels represents 1 block
        # pbr = -1
        # @TODO: Find the location of finder points and  correct the orientation and perspective
        for row in range(h):
            for col in range(w):
                # pbr += 1
                # Find the first black point
                if (not locatedFirstBlack and img[row,col] == 0):
                    startx,starty = row,col
                    pbr = 0
                    locatedFirstBlack = True
                    # print(row,col,img[row,col])
    

                # Find the no of pixels till next white 
                if(locatedFirstBlack and img[row,col] == 255):
                    # print("First white after black",row,col,img[row,col])
                    break
            if locatedFirstBlack:
                break
        

        tl = (startx,starty)

        # Find the last black pixel

        for col in range(w-1,starty,-1):
            # Find the first black point from back
            if (img[startx,col] == 0):
                break
        
        tr = (startx,col)
            
        
        # Calculate the distance(width) of two extreme ends of black points in code
        width_of_two_black = col - starty
        # print(width_of_two_black)


        # Move from down to up till you find black line till the end, mark the end and start position
        for row in range(h-1,startx,-1):
            # Find the first black point from back
            if (img[row,starty] == 0):
                break

        # Calculate the distance(height) of two extreme ends of black points in code
        height_of_two_black = row - startx
        # print(height_of_two_black)
 
        resize_factor = (round(width_of_two_black/(WIDTH-2)),round(height_of_two_black/(HEIGHT-2)))
        # print("Resize Factor",resize_factor)

        bl = (row,starty)   


        i,j=0,0
        # Now starting from top left, read block by block
        for row in range(0,h,resize_factor[1]):
            for col in range(0,w,resize_factor[0]):
                self.data_matrix[i][j] = '0' if img[row,col] == 0 else '1'
                j += 1
            i += 1
            j=0
        
        # self._print_data_matrix()
        self.extracted = True

    def decode(self):
        if not self.extracted:
            raise Exception("Error: Data Matrix not extracted. Extract data matrix from image before decoding")

        # Read the encoding 
        enc_type = encodingMappings[self.data_matrix[1][2]+self.data_matrix[1][3]]

        binary_len = ''.join(self.data_matrix[1][4:4+12])

        msg_len = int(binary_len,2)

        count = 0
        i,j = 2,2

        matrix_array_int = np.array(self.data_matrix).astype('uint8')
        msg = []
        while count < msg_len:
            # Extract a bit stored in a block
            # Binary is stored in reverse order (msd is stored in last position)
            val = 0
            for x in range(8): 
                
                val >>= 1
                val |=  (matrix_array_int[i,j]<<7)
       

                j += 1
                if j  == WIDTH-1:
                    j=2
                    i += 1
                    if i == HEIGHT - 1:
                        break  
            if i == HEIGHT - 1:
                break  


            msg.append(chr(int(val)))
      

            count += 1

        # print("Decoding Complete!")
        return ''.join(msg)
            

    def _print_data_matrix(self):
        for i in range(HEIGHT):
            print(' '.join(self.data_matrix[i]))

if __name__ == '__main__':
    # Can store upto 34 characters
    d = Decoder()
    d.load_image('/home/ash/Desktop/projects/custom_2d_barcode/generated')
    d.image_to_matrix()
    msg = d.decode()
    print("Message is",msg)
    cv2.destroyAllWindows()