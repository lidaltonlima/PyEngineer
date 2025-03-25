class Node:
    def __init__(self, name: str, x: float, y: float, z: float):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.dx = False
        self.dy = False
        self.dz = False
        self.rx = False
        self.ry = False
        self.rz = False
    
    def support(self,
                dx: bool = False, dy: bool = False, dz: bool = False,
                rx: bool = False, ry: bool = False, rz: bool = False,) -> None:
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        
    def coordinates(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        
        

if __name__ == '__main__':
    n = Node('N1', 1, 2, 3)
    n.support(dx=True)
    print(n.rx)