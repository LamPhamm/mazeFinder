#Maze Finder Console Program
import queue
import pdb

#Creates a maze using lists
def create_maze():
    maze=[]
    maze.append(["#","#","O","#","#"])
    maze.append(["#"," "," "," ","#"])
    maze.append(["#"," ","#"," ","#"])
    maze.append(["#"," "," "," ","#"])
    maze.append(["#","#","X","#","#"])
    return maze

#Determines if the x character is reached; returns true or false
def x_reached(maze,path):
    current_pos=find_O_position(maze)                                                                 
    X_pos=find_X_position(maze)

    #Convert the path string into a list
    path_list=list(path)

    #Check if the path is empty, then the X hasn't been reached
    if len(path_list)==0:
        return False
        
    for move in path_list:
        #Depending on the move in the path, update the current position
        if move=="L":
            current_pos=[current_pos[0],current_pos[1]-1]
        elif move=="R":
            current_pos=[current_pos[0],current_pos[1]+1]
        elif move=="U":
            current_pos=[current_pos[0]-1,current_pos[1]]
        else:
            current_pos=[current_pos[0]+1,current_pos[1]]

    #Determine if the X_pos has been reached
    if current_pos==X_pos:
        return True
    return False


#Determines if the path is valid; returns true or false
def is_valid_move(maze,path):
    current_pos=find_O_position(maze)

    #Convert the path into a list
    path_list=list(path)
    for move in path_list:
        #Check bound cases
        if current_pos[0]==len(maze)-1:#End of the maze where the O reaches the X. Don't want the O to move down
            return False
        elif current_pos[0]==0 and move=="U":#Start of the maze at the top row at the current position. Don't want the O to move up
            return False

        #For each move, determine if the move doesn't hit the # key. If it doesn't hit the # key, update the current position and continue
        #If it hits the # key, return False as it's not a valid move
        elif move=="L" and maze[current_pos[0]][current_pos[1]-1]!="#":
            current_pos=[current_pos[0],current_pos[1]-1]
        elif move=="L":
            return False

        elif move=="R" and maze[current_pos[0]][current_pos[1]+1]!="#":
            current_pos=[current_pos[0],current_pos[1]+1]
        elif move=="R":
            return False

        elif move=="U" and maze[current_pos[0]-1][current_pos[1]]!="#":
            current_pos=[current_pos[0]-1,current_pos[1]]

        elif move=="U":
            return False
        elif move=="D" and maze[current_pos[0]+1][current_pos[1]]!="#":
            current_pos=[current_pos[0]+1,current_pos[1]]
        else:
            return False
        
    #Return True, as the path has not hit the pound key
    return True

def display_maze_solution(maze,path):
    current_pos=find_O_position(maze)

    #Convert path string into a list
    path_list=list(path)

    #For each move, determine the current position of the O and update the maze
    for move in path_list:
        if move=="L":
            current_pos=[current_pos[0],current_pos[1]-1]
        elif move=="R":
            current_pos=[current_pos[0],current_pos[1]+1]
        elif move=="U":
            current_pos=[current_pos[0]-1,current_pos[1]]
        else:
            current_pos=[current_pos[0]+1,current_pos[1]]

        maze[current_pos[0]][current_pos[1]]="$"

    #Return the maze with the path
    return maze
        
#Function that finds the O position
def find_O_position(maze):
    for row_index in range(len(maze)):
        for col_index in range(len(maze[row_index])):
            if maze[row_index][col_index]=="O":
                O_pos=[row_index,col_index]
    
    return O_pos

#Function that finds the X position
def find_X_position(maze):
    for row_index in range(len(maze)):
        for col_index in range(len(maze[row_index])):
            if maze[row_index][col_index]=="X":
                X_pos=[row_index,col_index]

    return X_pos

#BFS Algorithm
def BFS(maze):
    #Possible moves
    moves=["L","R","D","U"]

    #Create a queue
    paths=queue.Queue()

    #Represents a path of the object thus far
    path=""
    paths.put(path)
    removed=""
    removed_paths=[]
    #Iterate while the X hasn't been reached
    while x_reached(maze,removed)==False:
        #Dequeue from the queue
        removed=paths.get()
        removed_paths.append(removed)

        #For each move, determine if possible move is valid
        for move in moves:
            #The new path is the removed move plus the individual move(L,R,U,D)
            path=removed+move
            #Determine if the move is valid(doesn't hit #)
            if is_valid_move(maze,path):
                #Add the item to the queue when valid
                paths.put(path)
                
    #Once the X is reached, we can return the shortest path
    return removed, removed_paths

"""
maze=create_maze()
path,removed_paths=BFS(maze)
print(path)
print(removed_paths)
"""


    


