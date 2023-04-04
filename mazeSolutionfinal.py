from collections import deque
import heapq
import sys
import pygame


red=(255,0,0)
green =(0,255,0)
screen=''
cell=''
BREATH=''
LENGTH=''
clock=''


print("Enter Input of LayOut File Choice: ")
print("0 for bigMaze")
print("1 for mediunMaze ")
print("2 for smallMaze")
print("3 for openMaze")
layChoice = int(input())

#    all .lay files are stored in the layOutFiles

layOutFiles = ['bigMaze.lay','mediumMaze.lay','smallMaze.lay','openMaze.lay']


# layToMatrix function uses to convert .lay files to matrix

def layToMatrix(path):
    with open(path, 'r') as f:
        maze =  [list(line.strip()) for line in f.readlines()]
    return maze


mazeMat=layToMatrix(layOutFiles[layChoice])

# findStartAndEnd function helps to find the starting "PACMAN" position and ending position

def findStartAndEnd(mat):
    for i in range(len(mat)):
        for j in  range(len(mat[i])):
            if mat[i][j]=='P':
                start = (i,j)
            elif mat[i][j]=='.':
                end = (i,j)
    return start,end

# direction consists of direction of node to find neighbours

direction = [(0, 1), (0, -1), (-1, 0), (1, 0)]

#neighbours function helps to visit neighbour node i.e up ,down, left, right

def neighbours(mazeMat,node):
    neighbors = []
    for x,y in direction:
        xx=node[0]+x
        yy=node[1]+y
        if 0 <= xx < len(mazeMat) and 0 <= yy < len(mazeMat[0]) and mazeMat[xx][yy] != '%':
            neighbors.append((xx, yy))
    return neighbors
    
# findPathUsingDFS helps to find path using depth first search Algo
    
def findPathUsingDFS(mazeMat):
    node_expanded=0
    max_depth=0
    max_fringe=0
    start,end = findStartAndEnd(mazeMat)
    stack = [(start,[start])]
    vistedPath = set()
    while stack:
        node, path = stack.pop()
        node_expanded+=1
        max_depth=max(max_depth,len(path))
        max_fringe=max(max_fringe,len(stack))
        draw(path,red)
        
        if node ==end:
            return path,len(path)-1,node_expanded,max_depth,max_fringe
        
        if node not in vistedPath:
            vistedPath.add(node)
            for _ in neighbours(mazeMat , node):
                if _ not in vistedPath:
                    stack.append((_ , path+[_]))
    return None,None, None,None,None

# findPathUsingBFS helps to find path using breath first search Algo

def findPathUsingBFS(mazeMat):
    node_expanded=0
    max_depth=0
    max_fringe=0
    start,end = findStartAndEnd(mazeMat)
    q = deque([(start,[start])])
    vistedSet = set()

    while q:
        node ,path = q.popleft()
        node_expanded+=1
        max_depth=max(max_depth,len(path))
        max_fringe=max(max_fringe,len(q))
        draw(path,red)
        if node == end:
            return path , len(path)-1,node_expanded,max_depth,max_fringe
        if node not in vistedSet:
            vistedSet.add(node)
            for _ in neighbours(mazeMat,node):
                if _ not in vistedSet:
                    q.append((_ , path+[_]))
    
    return None,None,None,None,None

# findPathUsingAstar helps to find path using A* Algo

def findPathUsingAStar(mazeMat):
    node_expanded=0
    max_depth=0
    max_fringe=0
    start,end = findStartAndEnd(mazeMat)
    heap  = [(0,start,[start])]
    vistedSet = set()
    
    while heap:
        K, node, path = heapq.heappop(heap)
        node_expanded+=1
        max_depth=max(max_depth,len(path))
        max_fringe=max(max_fringe,len(heap))
        draw(path,red)
        if node == end:
            return path , len(path)-1,node_expanded,max_depth,max_fringe
        if node not in vistedSet:
            vistedSet.add(node)
            for _ in neighbours(mazeMat,node):
                if _ not in vistedSet:
                    
                    cost  =len(path)+1
                    cost += abs(_[0]-end[0])+abs(_[1]-end[1])
                    heapq.heappush(heap,(cost, _ ,path+[_]))
    return None,None,None,None,None       

# draw function helps in draw the path of visted nodes 

def draw(path,color):
    global screen,cell,BREATH,LENGTH,clock
    for node in path:
        pygame.display.set_caption("Maze Route")
        pygame.draw.rect(screen,color,(node[1] *cell, node[0] * cell, cell, cell),3)
        pygame.display.flip()
        clock.tick(120)


# main function helps to run the program using the input given by the user this 
# function creates a pygame frame to visilatize the matrix if the 
# choice is 0 to show original matrix
# choice is 1 dfs Algo runs
# choice is 2  bfs Algo runs
# choice is 3 a* Algo runs

def main():
    
    global screen,cell,BREATH,LENGTH,clock
    
    print("Enter Input of Choice: ")
    print("0 for original matrix")
    print("1 for DFS Algo path ")
    print("2 for BFS Algo path")
    print("3 for A* Algo path")
    choice =int(input())
    
    
    pygame.init()
    cell=20
    BREATH=len(mazeMat)*cell
    LENGTH=len(mazeMat[0])*cell
    screen = pygame.display.set_mode((LENGTH, BREATH),pygame.RESIZABLE)

    clock = pygame.time.Clock()
    flag=True
    pygame.display.set_caption("Maze Route")
    
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if flag:
            for i in range(len(mazeMat)):
                for j in range(len(mazeMat[0])):
                    if mazeMat[i][j]=='%':
                        pygame.draw.rect(screen,(0,0,0),(j *cell, i * cell, cell, cell))
                    elif mazeMat[i][j]=='P':
                        pygame.draw.rect(screen,(255,0,0),(j *cell, i * cell, cell, cell))
                    elif mazeMat[i][j]=='.':
                        pygame.draw.rect(screen,(0,255,0),(j *cell, i * cell, cell, cell))
                    else:
                        pygame.draw.rect(screen,(112,128,144),(j *cell, i * cell, cell, cell))
                    
         
        
        if choice==0:
            pygame.display.flip()
        
        if choice == 1 :
            dfs_path,dfs_cost,nodeExpanded,maxDepth,maxFringe = findPathUsingDFS(mazeMat)
            print("DFS path:", dfs_path)
            print("DFS cost:", dfs_cost)
            print("DFS nodeExpanded:", nodeExpanded)
            print("DFS maxDepth:", maxDepth)
            print("DFS maxFringe:", maxFringe)
            draw(dfs_path,green)
            pygame.display.flip()
            choice=0
        
        if choice == 2 :
            bfs_path,bfs_cost,nodeExpanded,maxDepth,maxFringe  = findPathUsingBFS(mazeMat)
            print("BFS path:", bfs_path)
            print("BFS cost:", bfs_cost)
            print("BFS nodeExpanded:", nodeExpanded)
            print("BFS maxDepth:", maxDepth)
            print("BFS maxFringe:", maxFringe)
            draw(bfs_path,green)
            pygame.display.flip()
            choice=0
    
        if choice == 3 :
            Astar_path,Astar_cost,nodeExpanded,maxDepth,maxFringe  = findPathUsingAStar(mazeMat)
            print("A* path:", Astar_path)
            print("A* cost:", Astar_cost)
            print("A* nodeExpanded:", nodeExpanded)
            print("A* maxDepth:", maxDepth)
            print("A* maxFringe:", maxFringe)
            
            draw(Astar_path,green)
            pygame.display.flip()
            choice=0
        
        pygame.display.flip() 
        flag=False
        
        
        
        
main()