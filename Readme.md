## Custom 2d Barcode
2D custom barcode like QR code with custom encoding and decoding algorithm.


### Description

1 block = 1 bit

Size: 13x13 blocks

Outside edge of code is white, and remaining 11x11 contains other information.

0 - Black
1 - White
- Outside blocks are all white.
- Remaining 11x11 blocks contains information. We assume our size as 11x11 now onwards
- Left and bottom edges are used for orientation information
- In the left edge, two blocks and one block are alternatively black and white.
- The bottom edge also has same pattern which extends from left to right.
- Block (17,2) and (19,19) are black.
- 2 blocks of top left after the identification column, contains information about encoding type. 
    - 00 - Byte mode ( Data are ascii character, each char uses 1 byte)
    - 01 - Numeric mode (All data are numeric, 1 byte for each number, represented as ascii)
    - 10 - Undefined
    - 11 - Undefined
- After these, 12 blocks contains the number of blocks where information are stored

- Remaining 275 blocks contains information sequentially. (34 bytes/characters of information)


### Algorithms

#### Encoding

    1. Split the message character by character and fill the data matrix in order.
    2. Represent the data in binary format and fill up the matrix. 
    3. Convert the matrix into an image using encoding information and correct values.


#### Decoding
    1. Read the image and find the correct orientation
    2. Approximate the  width of the block and use that as measure to find out block color.
    3. Starting from top left, decode the information using the encoding information.


