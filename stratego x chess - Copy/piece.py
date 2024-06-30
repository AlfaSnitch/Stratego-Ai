import os

class Piece:
    
    def __init__(self,name,color,value,texture=None, texture_rect = None):
        self.color = color
        self.name = name
        
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        
        self.moves = []
        self.moved = False
        
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self):
        self.texture = os.path.join(
            f'assests/img/{self.name}_{self.color}.png'
        )
    
    def add_moves(self,move):
        self.moves.append(move)

class Spy(Piece):

    def __init__(self, color):
        super().__init__('spy', color, 1.0)
        
class Scout(Piece): # like a rook

    def __init__(self, color):
        super().__init__('scout', color, 2.0)
        
class Miner(Piece):

    def __init__(self, color):
        super().__init__('miner', color, 3.0)
      
      
class Sergeant(Piece):

    def __init__(self, color):
        super().__init__('sergeant', color, 4.0)
     

class Lieutenant(Piece):

    def __init__(self, color):
        super().__init__('lieutenant', color, 5.0)
      
      
class Captain(Piece):

    def __init__(self, color):
        super().__init__('captain', color, 6.0)
        
class Major(Piece):

    def __init__(self, color):
        super().__init__('major', color, 7.0)

class Colonel(Piece):

    def __init__(self, color):
        super().__init__('colonel', color, 8.0)

class General(Piece):

    def __init__(self, color):
        super().__init__('general', color, 9.0)

class Marshal(Piece):

    def __init__(self, color):
        super().__init__('marshal', color, 10.0)
        
class Flag(Piece):

    def __init__(self, color):
        super().__init__('flag', color, 10000.0)

class Bomb(Piece):

    def __init__(self, color):
        super().__init__('bomb', color, 13.0)
            
      
      
      
      
                 
      