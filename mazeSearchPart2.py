from collections import deque
import heapq
import sys
import pygame


def layToMatrix(layPath):
    with open(layPath,'r') as f:
        matrix  =[list(line.strip()) for line in f.readlines()]
    return matrix


def closeFood(matrix, start):
    queue = deque([(start, 0)])  
    visited = set()  
    foodPos = [] 
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '.':
                foodPos.append((i, j))
    while queue:
        currPos, distance = queue.popleft()
        if currPos in foodPos:
            return currPos
        visited.add(currPos)
        neighbors = []
        for dr, dc in [(1, 0),(0, 1), (0, -1), (-1, 0)]:
            nr, nc = currPos[0] + dr, currPos[1] + dc
            if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] != '%' and (nr, nc) not in visited:
                neighbors.append((nr, nc))
        for neighbor in neighbors:
            queue.append((neighbor, distance + 1))
    return None

def display_info(screen, cost, maxDepth, nodesExpanded, maxFringe):
    font = pygame.font.SysFont('Verdana', 20,bold=True, italic=True)
    text1 = font.render("Path Cost: {}".format(cost), True, (255, 255, 255))
    text2 = font.render("Max Depth: {}".format(maxDepth), True, (255, 255, 255))
    text3 = font.render("Nodes Expanded: {}".format(nodesExpanded), True, (255, 255, 255))
    text4 = font.render("Max Fringe: {}".format(maxFringe), True, (255, 255, 255))
    h=screen.get_height()-120
    screen.blit(text1, (20, h))
    screen.blit(text2, (20, h+20))
    screen.blit(text3, (20, h+40))
    screen.blit(text4, (20, h+60))
    pygame.display.flip()

class dfs():
    
    def solve(mazeMat):
        node_expanded = 0
        max_depth = 0
        max_fringe = 0
        matrix = mazeMat
        
        def foodAndStart(matrix):
            start = None
            foodPos = []
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 'P':
                        start = (i, j)
                    elif matrix[i][j] == '.':
                        foodPos.append((i, j))
            return start, foodPos
        
        start, foodPos = foodAndStart(matrix)
        
        foodpath = []
        direction = [(1, 0),(0, 1), (-1, 0), (0, -1)]
        while foodPos:
            closestFood = closeFood(matrix, start)
            visitedSet = set()
            stack = [(start, 0, [])]
            
            while stack:
                pos, currdist, path = stack.pop(0)
                node_expanded += 1
                max_depth = max(max_depth, len(path))
                max_fringe = max(max_fringe, len(stack))
                
                if pos == closestFood:
                    foodpath.append(path + [pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start = pos
                    foodPos.remove(pos)
                    break
                
                if pos not in visitedSet:
                    visitedSet.add(pos)
                    for i, j in direction:
                        newRow = pos[0] + i
                        newCol = pos[1] + j
                        if (
                            0 <= newRow < len(matrix)
                            and 0 <= newCol < len(matrix[0])
                            and matrix[newRow][newCol] != '%'
                            and (newRow, newCol) not in visitedSet
                        ):
                            stack.append(((newRow, newCol), currdist + 1, path + [pos]))
        
        return foodpath, len(foodpath) - 1, node_expanded, max_depth, max_fringe


class bfs():
    def solve(mazeMat):
        node_expanded=0
        max_depth=0
        max_fringe=0
        matrix = mazeMat
        foodPos=[]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]=='P':
                    start = (i,j)
                elif matrix[i][j]=='.':
                    foodPos.append((i,j))
                    
        foodpath =[]
        direction = [(-1,0),(1,0),(0,-1),(0,1)]
        while foodPos:
            closetFood = closeFood(matrix,start)
            vistedSet=set()
            q = deque([(start,0,[])])
            while q:
                pos ,currdist, path = q.popleft()
                node_expanded+=1
                max_depth=max(max_depth,len(path))
                max_fringe=max(max_fringe,len(q))
                
                if(pos==closetFood):
                    foodpath.append(path+[pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start=pos
                    foodPos.remove(pos)
                    break
                if pos not in vistedSet:
                    vistedSet.add(pos)
                    for i,j in direction:
                        newRow = pos[0]+i
                        newCol = pos[1]+j
                        if 0<=newRow<len(matrix) and 0<=newCol<len(matrix[0]) and matrix[newRow][newCol]!='%' and (newRow,newCol) not in vistedSet:
                            q.append(((newRow,newCol),currdist+1,path+[pos]))
                            
        return foodpath,node_expanded,max_depth,max_fringe



class astar():
    def solve(mazeMat):
        node_expanded=0
        max_depth=0
        max_fringe=0
        matrix = mazeMat
        
        foodPos=[]
        start=None
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]=='P':
                    start = (i,j)
                elif matrix[i][j]=='.':
                    foodPos.append((i,j))
        foodpath =[]
        direction = [(-1,0),(1,0),(0,-1),(0,1)]
        
        while foodPos:
            
            closetFood = closeFood(matrix,start)
            vistedSet=set()
            heap = [(start,0,[])]
            while heap:
                pos, currdist, path = heapq.heappop(heap)
                node_expanded+=1
                max_depth=max(max_depth,len(path))
                max_fringe=max(max_fringe,len(heap))
                
                if(pos==closetFood):
                    foodpath.append(path+[pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start=pos
                    foodPos.remove(pos)
                    break
                if pos not in vistedSet:
                    vistedSet.add(pos)
                    for i,j in direction:
                        newRow = pos[0]+i
                        newCol = pos[1]+j
                        if 0<=newRow<len(matrix) and 0<=newCol<len(matrix[0]) and matrix[newRow][newCol]!='%' and (newRow,newCol) not in vistedSet:
                            heapq.heappush(heap,(((newRow,newCol),currdist+1+abs(newRow-closetFood[0])+abs(newCol-closetFood[1]),path+[pos])))
                            
        return foodpath,node_expanded,max_depth,max_fringe
    
    
class main():
    def main():
    
        print("Enter Input of LayOut File Choice: ")
        print("0 for trickySearch")
        print("1 for tinySearch ")
        print("2 for smallSearch")
        
        layChoice = int(input())
        
        layOutFiles =['trickySearch.lay','tinySearch.lay','smallSearch.lay']
        layPath = layOutFiles[layChoice]
        
        mazeMat =layToMatrix(layPath)
        
            
        
        print("Enter Input of Choice: ")
        print("0 for original matrix")
        print("1 for dfs Algo path ")
        print("2 for bfs Algo path")
        print("3 for A* Algo path")
        choice =int(input())

        
        pygame.init()
        cell=20
        BREATH=(len(mazeMat)*cell)*2
        LENGTH=len(mazeMat[0])*cell
        if layChoice!=1:
            screen = pygame.display.set_mode((LENGTH, BREATH),pygame.RESIZABLE)
        else:
            screen = pygame.display.set_mode((LENGTH*1.5, BREATH),pygame.RESIZABLE)
        pygame.display.set_caption("Maze Route with Multiple Targets")
        clock = pygame.time.Clock()
        flag=0
        while True:
            WALL_COLOR = (0,0,0)       
            START_COLOR = (255, 0, 0)    
            END_COLOR = (0, 255, 0)      
            EMPTY_COLOR = (178,159,126) 
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if flag==0:
                for i in range(len(mazeMat)):
                    for j in range(len(mazeMat[0])):
                        if mazeMat[i][j]=='%':
                            pygame.draw.rect(screen,WALL_COLOR,(j *cell, i * cell, cell, cell))
                        elif mazeMat[i][j]=='P':
                            pygame.draw.rect(screen,EMPTY_COLOR,(j *cell, i * cell, cell, cell))
                            pygame.draw.circle(screen,START_COLOR,(j * cell + cell // 2, i * cell + cell // 2), cell // 3)
                        elif mazeMat[i][j]=='.':
                            pygame.draw.rect(screen,EMPTY_COLOR,(j *cell, i * cell, cell, cell))
                            pygame.draw.circle(screen,END_COLOR,(j * cell + cell // 2, i * cell + cell // 2), cell // 3)                   
                        else:
                            pygame.draw.rect(screen,EMPTY_COLOR,(j *cell, i * cell, cell, cell))
                        
            
            if choice==0:     
                pygame.display.flip()
            if choice == 1 :
                path,cost,node_expanded,max_depth,max_fringe = dfs.solve(mazeMat)
                result_list = [tup for sublist in path for tup in sublist]
                prev=(1,1)
                for node in result_list:
                    pygame.display.set_caption("Maze Route DFS")
                    pygame.draw.rect(screen,EMPTY_COLOR,(prev[1] *cell, prev[0] * cell, cell, cell))
                    clock.tick(10)
                    pygame.draw.rect(screen,START_COLOR,(node[1] *cell, node[0] * cell, cell, cell),3)
                    prev=node
                    pygame.display.flip()
                    
                display_info(screen, cost,max_depth, node_expanded,max_fringe)
                choice=0
                print("DFS path:", path)
                
            
            if choice == 2 :
                path,node_expanded,max_depth,max_fringe = bfs.solve(mazeMat)
                cost=len(path)-1
                result_list = [tup for sublist in path for tup in sublist]
                prev=path[0][0]
                for node in result_list:
                    pygame.display.set_caption("Maze Route BFS")
                    pygame.draw.rect(screen,EMPTY_COLOR,(prev[1] *cell, prev[0] * cell, cell, cell))
                    clock.tick(10)
                    pygame.draw.rect(screen,START_COLOR,(node[1] *cell, node[0] * cell, cell, cell),3)
                    prev=node
                    pygame.display.flip()
                display_info(screen, cost,max_depth, node_expanded,max_fringe)
                choice=0
                print("BFS path:", path)
                
        
            if choice == 3 :
                path,node_expanded,max_depth,max_fringe  = astar.solve(mazeMat)
                cost=len(path)-1
                result_list = [tup for sublist in path for tup in sublist]
                prev=path[0][0]
                for node in result_list:
                    pygame.display.set_caption("Maze Route A*")
                    pygame.draw.rect(screen,EMPTY_COLOR,(prev[1] *cell, prev[0] * cell, cell, cell))
                    clock.tick(10)
                    pygame.draw.rect(screen,START_COLOR,(node[1] *cell, node[0] * cell, cell, cell),3)
                    prev=node
                    pygame.display.flip()
                display_info(screen, cost,max_depth, node_expanded,max_fringe)
                choice=0
                print("A* path:", path)
                
        
            
            pygame.display.flip()
            flag=flag+1
        
    main()
