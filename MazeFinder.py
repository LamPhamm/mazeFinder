from tarfile import BLOCKSIZE
from turtle import color
import pygame
import MazeFinderAlgorithm
from tkinter import *
from tkinter import messagebox
import time

WHITE=(255, 255, 255)
BLACK=(0,0,0)
LIGHTBLUE=(0,191,255)
GRAY=(96,96,96)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
WINDOW_WIDTH=400
WINDOW_HEIGHT=420
BLOCKSIZE=40

def main():
    #Set up the board
    setBoard()
    
    # Variable to keep our game loop running
    running = True
    
    while running:
        #Display the grid lines
        displayGrids()
        #Display the title
        displayTitle()
        #Display the buttons
        displayMazeButton()
        displaySolveMazeButton()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

def setBoard():
    #Background color
    background_colour = WHITE
    global screen
    #Dimensions
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    #Set the caption of the screen
    pygame.display.set_caption('BFS MazeFinder-Designed by Lam Pham')
    
    #Fill the background colour to the screen
    screen.fill(background_colour)
    
    #Update the entire pygame window 
    pygame.display.update()

#Displays the black grid lines on the board
def displayGrids():
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(60, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.display.update()

def displayTitle():
    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Maze Finder', False, LIGHTBLUE)
    screen.blit(text_surface, (0,0))

def displayMazeButton():
    #Display the initial button
    rect=pygame.Rect(180, 10, 80, 30)
    pygame.draw.rect(screen, BLACK, rect)

    #Display the text for the button
    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 12)
    text_surface = my_font.render('Display Maze', False, WHITE)
    screen.blit(text_surface, (182,14))

    #Change the color when the user hovers over the button
    hover = rect.collidepoint(pygame.mouse.get_pos())
    if hover:
        pygame.draw.rect(screen,GRAY,rect)
        screen.blit(text_surface, (182,14))

    #Call the createMaze function when pressed
    events = pygame.event.get()
    #Loops through all events
    for event in events:
        #Create the maze if the mouse button was pressed
        if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(pygame.mouse.get_pos()):
                createMaze()

def displaySolveMazeButton():
    #Display the initial button
    rect=pygame.Rect(290, 10, 80, 30)
    pygame.draw.rect(screen, BLACK, rect)

    #Display the text for the button
    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 12)
    text_surface = my_font.render('Solve Maze', False, WHITE)
    screen.blit(text_surface, (296,14))

    #Change the color when the user hovers over the button
    hover = rect.collidepoint(pygame.mouse.get_pos())
    if hover:
        pygame.draw.rect(screen,GRAY,rect)
        screen.blit(text_surface, (296,14))

    #Call the solveMaze function when pressed
    events = pygame.event.get()
    #Loops through all events
    for event in events:
        #Create the maze if the mouse button was pressed
        if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(pygame.mouse.get_pos()):
                solveMaze()

#Creates a sample maze 
def createMaze():
    #Fill in the first row of the maze
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(60, 80, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)

            #Except for the second block
            if x!=80:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, BLUE, rect)

    #Fill in the far left and right columns
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(60, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            if x==0 or x==360:
                pygame.draw.rect(screen, BLACK, rect)

    #Fill in the last row except for third to last block
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(380, 420, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            
            if x!=280:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, RED, rect)

    #Freestyle fill in any other lines within maze
    for x in range(80,240,BLOCKSIZE):
        for y in range(140, 180, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect)

    for x in range(0,WINDOW_WIDTH,BLOCKSIZE):
        for y in range(220,WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(160, y, BLOCKSIZE, BLOCKSIZE)

            pygame.draw.rect(screen, BLACK, rect)

    for x in range(0,WINDOW_WIDTH,BLOCKSIZE):
        for y in range(140,WINDOW_HEIGHT-BLOCKSIZE*4, BLOCKSIZE):
            rect = pygame.Rect(280, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect)

    for x in range(BLOCKSIZE*6,WINDOW_WIDTH,BLOCKSIZE):
        for y in range(WINDOW_HEIGHT-BLOCKSIZE*3,WINDOW_HEIGHT-BLOCKSIZE*2, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect)

    for x in range(0,WINDOW_WIDTH,BLOCKSIZE):
        for y in range(180,WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(80, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect)

    for x in range(BLOCKSIZE*6,BLOCKSIZE*7,BLOCKSIZE):
        for y in range(WINDOW_HEIGHT-BLOCKSIZE*5,WINDOW_HEIGHT-BLOCKSIZE*3, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, BLACK, rect)

#Solves a given maze using BFS
def solveMaze():
    #Access the top left corner of each grid cell
    #Define the maze
    maze=[]
    #Coordinates of the top left corner of the blue square
    blue_square_coords=[]
    for y in range(60, WINDOW_HEIGHT, BLOCKSIZE):
        row=[]
        for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
            #Get the rgb color(tuple) of the cell
            colorCell=screen.get_at((x+1,y+1))[:3]

            #Convert rgb colors to their equivalence in the MazeFinderAlgorithm module
            if colorCell==BLACK:
                row.append("#")
            elif colorCell==WHITE:
                row.append(" ")
            elif colorCell==BLUE:
                row.append("O") 
                blue_square_coords.append(x)  
                blue_square_coords.append(y)  
            else:
                row.append("X")

        #Append row to maze
        maze.append(row)

    #Get the solution path of the maze and the removed_paths
    path,removed_paths=MazeFinderAlgorithm.BFS(maze)
    print(len(removed_paths))
    print(removed_paths[len(removed_paths)-1])
    #Visualize the algorithm running
    visualizeAlgorithm(removed_paths,blue_square_coords)
    #Show the solution of the maze
    showSolution(path,blue_square_coords)

#Shows the solution of the maze
def showSolution(path,blue_square_coords):
    #Make the path a list
    path_list=list(path)
    
    #The current position starts at the blue square's position
    current_pos=blue_square_coords
   
    #For each move, get the current position after move is performed
    for move in path_list:
        if move=="L":
            current_pos=[current_pos[0]-BLOCKSIZE,current_pos[1]]
        elif move=="R":
            current_pos=[current_pos[0]+BLOCKSIZE,current_pos[1]]
        elif move=="U":
            current_pos=[current_pos[0],current_pos[1]-BLOCKSIZE]
        else:
            current_pos=[current_pos[0],current_pos[1]+BLOCKSIZE]
        
        #Draw the rectangle
        rect = pygame.Rect(current_pos[0], current_pos[1], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, BLUE, rect)
        pygame.display.update()
        #Pause for a bit to show animation
        time.sleep(.25)

    #Display the path in a message box
    Tk().wm_withdraw() #To hide the main window
    messagebox.showinfo('Solution Path',path)
    

def drawPath(path,blue_square_coords):
    #Make the path a list
    path_list=list(path)
    
    #The current position starts at the blue square's position
    current_pos=blue_square_coords
   
    #For each move, get the current position after move is performed
    for move in path_list:
        if move=="L":
            current_pos=[current_pos[0]-BLOCKSIZE,current_pos[1]]
        elif move=="R":
            current_pos=[current_pos[0]+BLOCKSIZE,current_pos[1]]
        elif move=="U":
            current_pos=[current_pos[0],current_pos[1]-BLOCKSIZE]
        else:
            current_pos=[current_pos[0],current_pos[1]+BLOCKSIZE]
        
        #Draw the rectangle
        rect = pygame.Rect(current_pos[0], current_pos[1], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, GREEN, rect)
        #time.sleep(3)
    
    pygame.display.update()
    time.sleep(.0000000000000000000000000000000000000000001)

    #First reset the current position coordinates
    current_pos=blue_square_coords
    #Repaint over the green path
    for move in path_list:
        if move=="L":
            current_pos=[current_pos[0]-BLOCKSIZE,current_pos[1]]
        elif move=="R":
            current_pos=[current_pos[0]+BLOCKSIZE,current_pos[1]]
        elif move=="U":
            current_pos=[current_pos[0],current_pos[1]-BLOCKSIZE]
        else:
            current_pos=[current_pos[0],current_pos[1]+BLOCKSIZE]
        
        #Draw the rectangle
        rect = pygame.Rect(current_pos[0], current_pos[1], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, WHITE, rect)
    
    pygame.display.update()
    

#Visualizes the algorithm running by showing all of the possible moves in real time
def visualizeAlgorithm(removed_paths,blue_square_coords):
    for path in removed_paths[1:]:
        #Draw the path
        drawPath(path,blue_square_coords)
        
    
    
    
main()