#Image Smashing -- Project 1
#Alec Webb
#This project is based on a project (http://nifty.stanford.edu/2015/hug-seam-carving/) shown at
#the SIG-CSE conference on "nifty assignments." This is based on a SIGGRAPH paper
#and video (https://www.youtube.com/watch?v=6NcIJXTlugc), which you should definitely watch! (4:27).
#It’s apparently also a photoshop tool now, too!

import sys

#globals helpful for finding shortest paths
trackheat = float('inf')
trackleast = 0

def width(grid):
#Given a grid, determine how wide it is (how many columns there are). You may assume
#it’s rectangular (you don’t have to check every single row’s width)
    return len(grid[0])

def height(grid):
#Given a grid, determine how tall it is (how many rows there are). You may assume it’s rectangular
    return len(grid)

def calc_nrg(left, up, right, down):
#this function calculates the energy based on the surrounding cells
    red = 0
    green = 1
    blue = 2
    dRx = (left[red] - right[red])**2
    dGx = (left[green] - right[green])**2
    dBx = (left[blue] - right[blue])**2
    dX  = dRx + dGx + dBx
    dRy = (up[red] - down[red])**2
    dGy = (up[green] - down[green])**2
    dBy = (up[blue] - down[blue])**2
    dY  = dRy + dGy + dBy
    energy = dX + dY
    return energy

def energy_at(grid, r, c):
#given a grid of RGB triplets calculate the energy gradient at that location
    cols = width(grid)
    rows = height(grid)
    if(r < (rows-1) and c < (cols-1) and r>0 and c>0):
        #for inner cells    
        left = grid[r][c-1]
        right = grid[r][c+1]
        up = grid[r-1][c]
        down = grid[r+1][c]
        return calc_nrg(left, up, right, down)
    elif(c == 0 and r < (rows-1) and r!=0):
        #for left edge but not corner
        left = grid[r][cols-1]
        right = grid[r][c+1]
        up = grid[r-1][c]
        down = grid[r+1][c]
        return calc_nrg(left, up, right, down)
    elif(c == (cols-1) and r<(rows-1) and r!=0):
        #for right edge but not corner
        left = grid[r][c-1]
        right = grid[r][0]
        up = grid[r-1][c]
        down = grid[r+1][c] 
        return calc_nrg(left, up, right, down)
    elif(r == 0 and c!=0 and c<(cols-1)):
        #top row but not corners
        left = grid[r][c-1]
        right = grid[r][c+1]
        up = grid[rows-1][c]
        down = grid[r+1][c]
        return calc_nrg(left, up, right, down)
    elif(r == (rows-1) and c!=0 and c<(cols-1)):
        #bottom row but not corners
        left = grid[r][c-1]
        right = grid[r][c+1]
        up = grid[r-1][c]
        down = grid[0][c]
        return calc_nrg(left, up, right, down)
    elif(r==0 and c==0):
        #topleft
        left = grid[r][cols-1]
        right = grid[r][c+1]
        up = grid[rows-1][c]
        down = grid[r+1][c]
        return calc_nrg(left, up, right, down)
    elif(r==(rows-1) and c==0):
        #bottomleft
        left = grid[r][cols-1]
        right = grid[r][c+1]
        up = grid[r-1][c]
        down = grid[0][c]
        return calc_nrg(left, up, right, down)
    elif(r==0 and c == (cols-1)):
        #topright
        left = grid[r][c-1]
        right = grid[r][0]
        up = grid[rows-1][c]
        down = grid[r+1][c]
        return calc_nrg(left, up, right, down)
    else:
        #bottomright
        left = grid[r][c-1]
        right = grid[r][0]
        up = grid[r-1][c]
        down = grid[0][c]
        return calc_nrg(left, up, right, down)

def energy(grid):
#given a grid of RGB triplets, create and return a grid storing the energy at each point
#in the argument grid. Do not modify the given grid when constructing the return grid
    rows = height(grid)
    cols = width(grid)
    heatgrid = []
    for i in range(0,rows):
        heatgrid.append([])
        for j in range(0,cols):
            heatgrid[i].append(energy_at(grid,i,j))

    return heatgrid

def find_path(grid,c):
    pathheat = 0
    position = c
    rows = height(grid)
    cols = width(grid)
    r=0
    path = []
    start = grid[r][c]

    pathheat+=start
    path.append((r,c))
    for i in range(0,rows):
        if(c==0 and r<(rows-1)):
            #on left border, check down and downright
            down = grid[r+1][c]
            downright = grid[r+1][c+1]
            if(down <= downright):
                pathheat+=down
                path.append((r+1,c))
                r = r+1
            else:
                pathheat+=downright
                path.append((r+1,c+1))
                r = r+1
                c = c+1

        if(c!=0 and c<(cols-1) and r<(rows-1)):
            #somewhere in the middle check downleft, down, downright
            downleft = grid[r+1][c-1]
            down = grid[r+1][c]
            downright = grid[r+1][c+1]
            if(downleft <= down and downleft <= downright):
                pathheat+=downleft
                path.append((r+1,c-1))
                r = r+1
                c = c-1
            if(down < downleft and down <= downright):
                pathheat+=down
                path.append((r+1,c))
                r = r+1
            if(downright < down and downright < downleft):
                pathheat+=downright
                path.append((r+1,c+1))
                r = r+1
                c = c+1

        if(c==(cols-1) and r<(rows-1)):
            #on right border, check downleft and down
            downleft = grid[r+1][c-1]
            down = grid[r+1][c]
            if(downleft <= down):
                pathheat+=downleft
                path.append((r+1,c-1))
                r = r+1
                c = c-1
            else:
                pathheat+=down
                path.append((r+1,c))
                r = r+1

    find_least(position, pathheat, rows, cols)
    return path

def find_least(vectorpos, heat,rows,cols):
#this function manipulates globals so the path with the least heat can be found
    global trackheat
    global trackleast
    if(heat < trackheat):
        trackheat = heat
        trackleast = vectorpos

def find_vertical_path(grid):
    global trackheat
    global trackleast
    #reset the globals
    trackheat = float('inf')
    trackleast = 0

    cols = width(grid)
    grid_nrg = energy(grid)
    pathlist = []
    #build a list of the paths in the energy grid
    for i in range(0,cols):
        pathlist.append(find_path(grid_nrg,i))
    
    #return the lowest energy path
    return pathlist[trackleast]

def find_horizontal_path(grid):
    #transpose grid for use in find vertical path
    transpose = [list(i) for i in zip(*grid)]
    result = find_vertical_path(transpose)

    #reverse the row col tuples
    adjusted = [(b,a) for a,b in result]
    return adjusted

def remove_vertical_path(grid, path):
    rows = height(grid)
    #traverse the path in reverse and delete the item
    for i in range(rows-1, -1,-1):
        delete = path[i]
        r = delete[0]
        c = delete[1]
        item = grid[r][c]
        grid[i].remove(item)

    return grid

def remove_horizontal_path(grid, path):
    #transpose and reverse row col tuples in path for use in remove vertical path
    transpose = [list(i) for i in zip(*grid)]
    adjusted = [(b,a) for a,b in path]
    transform = remove_vertical_path(transpose, adjusted)

    #transpose the returned grid
    transpose_transformed = [list(i) for i in zip(*transform)]
    return transpose_transformed

def ppm_to_grid(filename):
    # Open the input file
    ppm = open(filename,"r")

    # verify p3 file type
    filetype = ppm.readline()
    if (filetype != "P3\n"):
        sys.exit('invalid file')

    #read width and height, convert to integers
    width = ppm.readline()
    height = ppm.readline()
    width = int(width)
    height = int(height)

    #check if a grid exists
    if (width <= 0) or (height <= 0):
        sys.exit('width or height is 0, invalid file size')

    #read maximum value, should always be 255 
    max = int(ppm.readline())
    if (max != 255):
        sys.exit('invalid maximum')

    #Create a list of the rgb values
    rgb_list = []
    for line in ppm:
        rgb_list += line.split(" ")

    #close the file
    ppm.close() 

    grid = []
    #by rows top to bottom convert to a grid
    for x in range(0,height):
        grid.append([])
        for y in range(0,width):
            grid[x].append((int(rgb_list[(y * 3 + (x*(width*3))) ]), 
                            int(rgb_list[(y * 3 + (x*(width*3))) + 1]),
                            int(rgb_list[(y * 3 + (x*(width*3))) + 2])))

    return grid

def grid_to_ppm(grid, filename):
    #write type max width and height to file
    w = str(width(grid))
    h = str(height(grid))
    ty = 'P3\n'
    mx = '255\n'
    out = open(filename, 'w')
    out.write(ty)
    out.write(w + '\n')
    out.write(h + '\n')
    out.write(mx)
    #write the rgb values to the file
    list = flatten(grid)
    for item in list:
        out.write("%s %s %s " % (item[0] ,item[1] ,item[2]))

    #close the file
    out.close()

def flatten(grid):
#this function flattens a list
    return sum(grid, [])


#DEBUG


