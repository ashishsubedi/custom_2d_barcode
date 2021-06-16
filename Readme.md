## Custom 2d Barcode (DxCode))
2D custom barcode like QR code with custom encoding and decoding algorithm.

Message = Hello World!!!
![DxCode Sample: message = Hello World!!!](https://raw.githubusercontent.com/ashishsubedi/custom_2d_barcode/main/generated.png)

20x20 blocks can store upto 34 bytes/characters.

### Description

1 block = 1 bit

Size: 20x20 blocks

Outside edge of code is white, and remaining 19x19 contains other information.

0 - Black
1 - White
- Outside blocks are all white.
- Remaining 19x19 blocks contains information. We assume our size as 11x11 now onwardsLeft and bottom edges are used for orientation
-  information
- In the left edge, all blocks are black.
- The bottom edge also has same pattern which extends from left to right.
- Top Right blocks are white, black,black

- 2 blocks of top left after the identification column, contains information about encoding type. 
    - 11 - Byte mode ( Data are ascii character, each char uses 1 byte)
    - 10 - Numeric mode (All data are numeric, 1 byte for each number, represented as ascii)
    - 01 - Undefined
    - 00 - Undefined
- After these, 12 blocks contains the number of blocks where information are stored
- Remainig blocks in the row are empty

- Remaining 272 blocks contains information sequentially. (34 bytes/characters of information)


### Algorithms

#### Encoding

    1. Split the message character by character and fill the data matrix in order.
    2. Represent the data in binary format and fill up the matrix. 
    3. Convert the matrix into an image using encoding information and correct values.


#### Decoding
    1. Read the image and find the location of extremes
    2. Approximate the  width and height of the block and use that as measure to find out block value.
    3. Starting from top left, decode the information using the encoding information.

### How to run

- Run <code> pip install -r requirements.txt </code>
- Run <code> python main.py </code>

