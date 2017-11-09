'''
Created on 10-Nov-2013

@author: raghavan
'''
import os

from color import Color
from pyimage import PyImage
from graph import Graph

class FaceDetector(object):
    '''
    classdocs
    '''

    def __init__(self, filename, block_size = 5, min_component_size = 15, majority = 0.5):
        '''
        Constructor - keeps input image filename, image read from the file as a PyImage object, block size (in pixels),
        threshold to decide how many skin color pixels are required to declare a block as a skin-block
        and min number of blocks required for a component. The majority argument says what fraction of
        the block pixels must be skin/hair colored for the block to be a skin/hair block - the default value is
        0.5 (half).
        '''
        # Your code
        self.filename = filename
        self.block_size = block_size
        self.min_component_size = min_component_size
        self.majority = majority
        self.skin = Graph()
        self.hair = Graph()
        self.pyim = PyImage(filename)

    def skin_green_limits(self, red):
        '''
        Return the limits of normalized green given the normalized red component as a tuple (min, max)
        '''
        return ((-0.776*red*red + 0.5601*red + 0.1766), (-1.376*red*red + 1.0743*red + 0.1452))


    def is_skin(self, pixel_color):
        '''
        Given the pixel color (as a Color object) return True if it represents the skin color
        Color is skin if hue in degrees is (> 240 or less than or equal to 20) and 
        green is in the green limits and it is not white
        '''
        # Your code
        color = Color(pixel_color)
        hue = color.hue_degrees()
        W = (color.R - 0.33)*(color.R - 0.33) + (color.G - 0.33)*(color.G - 0.33)
        green_limits = self.skin_green_limits(color.R)
        cond1 = (hue > 240 or hue <= 20)
        cond2 = green_limits[0] < color.G and color.G < green_limits[1]
        cond3 = color.rgb_abs()[0] < 230 and color.rgb_abs()[1] < 230 and color.rgb_abs()[2] < 230
        cond4 = 0.6 > color.R and color.R > 0.2
        if cond1 and cond2 and cond3 and cond4 and W > 0.0004:
            return True
        return False
    
            
    def is_hair(self, pixel_color):
        '''
        Return True if the pixel color represents hair - it is if intensity < 80 and ((B-G)<15 or (B-R)<15 or
        hue is between 20 and 40)
        '''
        # Your code
        color = Color(pixel_color)
        hue = color.hue_degrees()
        R = pixel_color[0]
        G = pixel_color[1]
        B = pixel_color[2]
        if ((20 <= hue and hue <= 40) or (B - G) < 15 or (B - R) < 15) and color.intensity < 80 :
            return True
        return False

    def is_skin_hair_block(self, block, block_type):
        '''
        Return true if the block (given by the argument 'block' which is the coordinate-tuple for the top-left corner)
        is a skin/hair-block - it is if a majority (as per the threshold attribute) of the pixels in the block are
        skin/hair colored. 'block_type' says whether we are testing for a skin block ('s') or a hair block ('h).
        '''
        # Your code
        count_pixels = 0
        for pixely in range(block[1], block[1] + self.block_size):
            for pixelx in range(block[0], block[0] + self.block_size):
                if pixelx < self.pyim.size()[0] and pixely < self.pyim.size()[1]:
                    color = self.pyim.get_rgba(pixelx, pixely)
                    if block_type == 's' and self.is_skin(color):
                        count_pixels +=1
                    elif block_type == 'h' and self.is_hair(color):
                        count_pixels +=1
        if ((count_pixels * 1.0)/(self.block_size * self.block_size * 1.0)) >= self.majority:
            return True
        return False
            
                
        
        

    def add_neighbour_blocks(self, block, graph):
        '''
        Given a block (given by the argument 'block' which is the coordinate-tuple for the top-left corner)
        and a graph (could be a hair or a skin graph), add edges from the current block to its neighbours
        on the image that are already nodes of the graph
        Check blocks to the left, top-left and top of the current block and if any of these blocks is in the
        graph (means the neighbour is also of the same type - skin or hair) add an edge from the current block
        to the neighbour.
        '''
        # Your code
        valid_rangeX = range(self.pyim.size()[0])
        valid_rangeY = range(self.pyim.size()[1])
        length = self.block_size
        
        if self.is_skin_hair_block(block, 's'):
            if (block[0] -length) in valid_rangeX and self.is_skin_hair_block((block[0]-length,block[1]), 's'):
                self.skin.add_edge((block[0]-length, block[1]), block)
            if (block[0] -length) in valid_rangeX and (block[1] - length) in valid_rangeY and self.is_skin_hair_block((block[0]-length,block[1]-length), 's'):
                self.skin.add_edge((block[0]-length,block[1]-length), block)
            if (block[1] -length) in valid_rangeY and self.is_skin_hair_block((block[0], block[1] -length), 's'):
                self.skin.add_edge((block[0], block[1] - length), block)
            if (block[0] + length) in valid_rangeX and (block[1] - length) in valid_rangeY and self.is_skin_hair_block((block[0]+length,block[1]-length), 's'):
                self.skin.add_edge((block[0] + length, block[1] - length), block)
        
        elif self.is_skin_hair_block(block, 'h'):
            #self.hair.add_node(block)
            if (block[0] -length) in valid_rangeX and self.is_skin_hair_block((block[0]-length,block[1]), 'h'):
                self.hair.add_edge((block[0]-length,block[1]), block)
            if (block[0] -length) in valid_rangeX and (block[1] - length) in valid_rangeY and self.is_skin_hair_block((block[0]-length,block[1]-length), 'h'):
                self.hair.add_edge((block[0]-length,block[1]-length), block)
            if (block[1] -length) in valid_rangeY and self.is_skin_hair_block((block[0], block[1] -length), 'h'):
                self.hair.add_edge((block[0],block[1]-length), block)
            if (block[0]+length) in valid_rangeX and (block[1] - length) in valid_rangeY and self.is_skin_hair_block((block[0]+length,block[1]-length), 'h'):
                self.hair.add_edge((block[0]+length,block[1]-length), block)
            
                
        
        
    def make_block_graph(self):
        '''
        Return the skin and hair graphs - nodes are the skin/hair blocks respectively
        Initialize skin and hair graphs. For every block if it is a  skin(hair) block
        add edges to its neighbour skin(hair) blocks in the corresponding graph
        For this to work the blocks have to be traversed in the top->bottom, left->right order
        '''
        # Your code

        for col in range(0, self.pyim.size()[1], self.block_size):
            for row in range(0, self.pyim.size()[0], self.block_size):
                if self.is_skin_hair_block((row, col), 's'):
                    self.skin.add_node((row,col))
                    self.add_neighbour_blocks((row,col), self.skin.adjacency)
                elif self.is_skin_hair_block((row, col), 'h'):
                    self.hair.add_node((row,col))
                    self.add_neighbour_blocks((row,col), self.hair.adjacency)
                

    def find_bounding_box(self, component):
        '''
        Return the bounding box - a box is a pair of tuples - ((minx, miny), (maxx, maxy)) for the component
        Argument 'component' - is just the list of blocks in that component where each block is represented by the
        coordinates of its top-left pixel.
        '''
        # Your code
        minx = miny = maxx = maxy = component[0][0]
        for tup in component:
            if tup[0] > maxx:
                maxx = tup[0]
            if tup[0] < minx:
                minx = tup[0]
            if tup[1] > maxy:
                maxy = tup[1]
            if tup[1] < miny:
                miny = tup[1]
            
        return ((minx, miny), (maxx, maxy))
    
    
    def skin_hair_match(self, skin_box, hair_box):
        '''
        Return True if the skin-box and hair-box given are matching according to one of the pre-defined patterns
        '''
        # Your code
        hair_minx = hair_box[0][0]
        hair_miny = hair_box[0][1]
        hair_maxx = hair_box[1][0]
        hair_maxy = hair_box[1][1]
        skin_minx = skin_box[0][0]
        skin_miny = skin_box[0][1]
        skin_maxx = skin_box[1][0]
        skin_maxy = skin_box[1][1]
        '''if skin_miny == hair_maxy :
            return True
        if skin_miny > hair_miny and skin_minx > hair_minx and skin_maxy < hair_maxy and skin_maxx > hair_maxx:
            return True
        if hair_miny < skin_miny and skin_miny < hair_maxy:
            return True
        if hair_maxy == skin_maxy :
            return True
        if skin_miny <= hair_miny and hair_maxy <= skin_maxy:
            return True'''
        return True
        

    def detect_faces(self):
        '''
        Main method - to detect faces in the image that this class was initialized with
        Return list of face boxes - a box is a pair of tuples - ((minx, miny), (maxx, maxy))
        Algo: (i) Make block graph (ii) get the connected components of the graph (iii) filter the connected components
        (iv) find bounding box for each component (v) Look for matches between face and hair bounding boxes
        Return the list of face boxes that have matching hair boxes
        '''
        # Your code
        index = 0
        self.make_block_graph()
        skin_components = self.skin.get_connected_components()
        hair_components = self.hair.get_connected_components()
        skin_components = skin_components[::-1]
        hair_components = hair_components[::-1]
        for comp in skin_components:
            if len(comp) >= self.min_component_size:
                break
            index +=1
        skin_components = skin_components[index:]
        
        index = 0
        for comp in hair_components:
            if len(comp) >= self.min_component_size:
                break
            index +=1
        hair_components = hair_components[index:]
        
        skin_boxes = []
        hair_boxes = []
        for component in skin_components:
            skin_boxes.append(self.find_bounding_box(component))
            
        for component in hair_components:
            hair_boxes.append(self.find_bounding_box(component))
        
        faces = []
        for skin_box in skin_boxes:
            for hair_box in hair_boxes:
                if self.skin_hair_match(skin_box, hair_box):
                    faces.append(skin_box)
          
        return faces, hair_boxes
                    
    def mark_box(self, box, color):
        '''
        Mark the box (same as in the above methods) with a given color (given as a raw triple)
        This is just a one-pixel wide line showing the box.
        '''
        # Your code
        minx = box[0][0]
        miny = box[0][1]
        maxx = box[1][0]
        maxy = box[1][1]
        if minx > self.pyim.size()[0]:
            minx = self.pyim.size()[0] - 1
        if maxx > self.pyim.size()[0]:
            maxx = self.pyim.size()[0] - 1
        if miny > self.pyim.size()[1]:
            miny = self.pyim.size()[1] - 1
        if maxy > self.pyim.size()[1]:
            maxy = self.pyim.size()[1] - 1
        
        for pixel in range(minx, maxx + 1):
            self.pyim.set(pixel, miny, color)
        for pixel in range(minx, maxx + 1):
            self.pyim.set(pixel, maxy, color)
        for pixel in range(miny, maxy + 1):
            self.pyim.set(minx, pixel, color)
        for pixel in range(miny, maxy + 1):
            self.pyim.set(maxx, pixel, color)
 
        


    def mark_faces(self, marked_file):
        '''
        Detect faces and mark each face detected -- mark the bounding box of each face in red
        and save the marked image in a new file
        '''
        # Your code
        faces, hair = self.detect_faces()
        for box in faces:
            self.mark_box(box, (255, 0, 0))
        '''for box in hair:
            self.mark_box(box, (0, 255, 0))'''
        self.pyim.save(marked_file)  
              

if __name__ == '__main__':
    pass
    detect_face_in = FaceDetector('/testcase/faces-01.jpeg')
    detect_face_in.mark_faces('/testresult/try3.jpeg')
    #fd = FaceDetector('faces-01.jpeg')
    #print fd.is_skin_hair_block((35,75), 'h')
