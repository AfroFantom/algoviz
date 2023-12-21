from collections import deque
import pygame
import math
from queue import PriorityQueue

WIDTH=800
WIN=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("AlgoViz")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self,r,c,width,tot_rows):
        self.r=r
        self.c=c
        self.x=c*width
        self.y=r*width
        self.color=WHITE
        self.width=width
        self.tot_rows=tot_rows
    
    def get_pos(self):
        return self.r,self.c
    
    def is_closed(self):
        return self.color==RED

    def is_open(self):
        return self.color==GREEN

    def is_barrier(self):
        return self.color==BLACK
    
    def is_start(self):
        return self.color==ORANGE
    
    def is_end(self):
        return self.color==PURPLE
    
    def reset(self):
        self.color=WHITE
    
    def make_start(self):
        self.color=ORANGE
    def make_closed(self):
        self.color=RED
    def make_open(self):
        self.color=GREEN
    def make_barrier(self):
        self.color=BLACK
    def make_end(self):
        self.color=TURQUOISE
    def make_path(self):
        self.color=PURPLE
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def update_neighbours(self,grid):
        self.neighbours=[]
        if self.r < self.tot_rows - 1 and not grid[self.r+1][self.c].is_barrier():#down
            self.neighbours.append(grid[self.r+1][self.c])

        if self.r > 0 and not grid[self.r-1][self.c].is_barrier():#up
            self.neighbours.append(grid[self.r-1][self.c])
        
        if self.c < self.tot_rows - 1 and not grid[self.r][self.c+1].is_barrier():#right
            self.neighbours.append(grid[self.r][self.c+1])
        
        if self.c > 0 and not grid[self.r][self.c-1].is_barrier():#left
            self.neighbours.append(grid[self.r][self.c-1])

    def __lt__(self,other):
        return False
    
def manahattanDistance(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

#impl a-star
def algo(draw,grid,start,end):
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    origin_dict={}
    #setting up g and f scores for a star
    g_score={node:float("inf") for row in grid for node in row}
    g_score[start]=0
    f_score={node:float("inf") for row in grid for node in row}
    f_score[start]=manahattanDistance(start.get_pos(),end.get_pos())
    open_set_hash={start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = open_set.get()[2]
        open_set_hash.remove(curr)

        if curr== end: #makePath
            make_path(draw,end,origin_dict)
            end.make_end()
            return True

        for nnodes in curr.neighbours:
            temp_g=g_score[curr]+1
            if temp_g<g_score[nnodes]:
                origin_dict[nnodes]=curr
                g_score[nnodes]=temp_g
                f_score[nnodes]=temp_g+manahattanDistance(nnodes.get_pos(),end.get_pos())
                if nnodes not in open_set_hash:
                    count+=1
                    open_set.put((f_score[nnodes],count,nnodes))
                    open_set_hash.add(nnodes)
                    nnodes.make_open()

        draw()

        if curr!=start:
            curr.make_closed()
    return False

def bfs(draw,graph, start, end):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        current, path = queue.popleft()

        if current == end:
            make_path_bfs(draw,end,path)
            end.make_end()
            return True  # Return the path if the goal is reached

        if current not in visited:
            visited.add(current)
            for neighbor in current.neighbours:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        draw()
        if current!=start:
            current.make_closed()
    return False  # Return False if there is no path from start to end

def make_path_bfs(draw,end,path):
    for i in range(len(path)-1,0,-1):
        path[i].make_path()
        draw()
        #nodes.pop()



def make_path(draw,end,origin_set):
    while end in origin_set:
        end=origin_set[end]
        end.make_path()
        draw()

def make_grid(r,width):
    grid=[]
    gap=width//r
    for i in range(r):
        grid.append([])
        for j in range(r):
            node=Node(i,j,gap,r)
            grid[i].append(node)
    
    return grid

def draw_grid(win,r,width):
    gap=width//r
    for i in range(r):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(r):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))

def draw(win,grid,r,width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win,r,width)
    pygame.display.update()

def get_clck_pstn(pos,r,width):
    gap=width//r
    x,y=pos
    row=y//gap
    col=x//gap
    return row, col

def main(win,width):
    ROWS=50
    grid= make_grid(ROWS,width)
    start,end=None,None
    run,started=True,False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_TAB:
                    run == False
    
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:#left
                pos=pygame.mouse.get_pos()
                row,col=get_clck_pstn(pos,ROWS,width)
                node=grid[row][col]
                if not start and node!=end:
                    start=node
                    start.make_start()
                elif not end and node!=start:
                    end = node
                    end.make_end()
                elif node!=end and node!=start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:#right
                pos=pygame.mouse.get_pos()
                row,col=get_clck_pstn(pos,ROWS,width)
                node=grid[row][col]
                if node==start:
                    start=None 
                elif node==end:
                    end=None
                node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    #algo(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    bfs(lambda: draw(win,grid,ROWS,width),grid,start,end)        
            


    pygame.quit()

main(WIN,WIDTH)


