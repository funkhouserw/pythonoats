from pymouse import PyMouse
import time
import math
import random

m = PyMouse()
left_up = [375,230]
right_down = [1250,700]
left_down = [375,700]
right_up = [1250,230]
#center = [845,500]
center = [792,470]

fs_center = (800, 445)
fs_left_up = (100, 100)
fs_left_down = (100, 800)
fs_right_up = (1500, 100)
fs_right_down = (1500, 800)
fs_radius = 440

def is_in_circle(coords):
  distance_to_center = math.hypot(coords[0]-fs_center[0],coords[1]-fs_center[1])
  return_vals = []
  if distance_to_center < fs_radius:
    return_vals = [True,coords]
  else:
    if coords[0] - fs_center[0] == 0:
      if coords[1] - fs_center[1] <= 0:
        angle = math.radians(90)
      else:
        angle = math.radians(-90)
    else: 
      angle = math.atan2((coords[1]-fs_center[1]),(coords[0]-fs_center[0]))
    y_val = fs_radius * math.sin(angle)
    x_val = fs_radius * math.cos(angle)
    return_vals = [False,int(fs_center[0]+x_val),int(fs_center[1]+y_val)]
  return return_vals

def change_command_to_radius(cmd,coords):
  if coords[0] - fs_center[0] == 0:
    if coords[1] - fs_center[1] <= 0:
      angle = math.radians(90)
    else:
      angle = math.radians(-90)
  else: 
    angle = math.atan2((coords[1]-fs_center[1]),(coords[0]-fs_center[0]))
  y_shift = fs_radius * math.sin(angle)
  x_shift = fs_radius * math.cos(angle)
  y_val = int(fs_center[1] + fs_radius * math.sin(angle))
  x_val = int(fs_center[0] + fs_radius * math.cos(angle))
  if "press" in cmd:
      return "m.press("+str(x_val)+","+str(y_val)+",1)"
  else:
      return "m.release("+str(x_val)+","+str(y_val)+",1)"


def run_commands(commands,release=True):
  wait = 0.04
  if release:
    last_x,last_y = commands[-1][1]
    commands.append(("m.release("+str(last_x)+","+str(last_y)+",1)",(last_x,last_y)))
  for (command,coords) in commands:
    if(is_in_circle(coords)[0]):
      time.sleep(wait)
      eval(command)
    else:
      time.sleep(wait)
      eval(change_command_to_radius(command,coords))

def square_slope(x,y,side,slope):
  points_raw = [(x,y),(x+side,y+side*slope),(x+side,y+side+side*slope),(x,y+side),(x,y),(x+side,y+side*slope)]
  points = [(int(a),int(b)) for (a,b) in points_raw]
  commands = [("m.press("+str(x)+","+str(y)+"),1",(x,y))]
  for my_x,my_y in points:
    if random.random() > 0 or True :
      commands.append(("m.press("+str(my_x)+","+str(my_y)+"),1",(my_x,my_y)))
  return commands


def test(back_square,front_square):
    sides = []
    for i in range(0,len(back_square)):
        r = (i+1)%4
        #sides.append((back_square[i],front_square[i],front_square[r],back_square[r],back_square[i],back_square[i]))
        sides.append((back_square[i],front_square[i],front_square[r],back_square[r]))
    for side in sides:
        commands = []
        commands.append(("m.press("+str(side[0][0])+","+str(side[0][1])+"),1",(side[0][0],side[0][1])))

        for (my_x,my_y) in side:
            commands.append(("m.press("+str(my_x)+","+str(my_y)+"),1",(my_x,my_y)))

        for (my_x,my_y) in side:
            commands.append(("m.press("+str(my_x)+","+str(my_y)+"),1",(my_x,my_y)))

        run_commands(commands,True)

def run_squares(xshift=-300,yshift=300,xshift2=0,yshift2=0):
    square1_vertex = (fs_center[0]+xshift2,fs_center[1]+yshift2)
    #starting_size = random.randrange(10,40,5)
    starting_size = 30
    back_square = [
            (square1_vertex[0],square1_vertex[1]),
            (square1_vertex[0]+starting_size,square1_vertex[1]),
            (square1_vertex[0]+starting_size,square1_vertex[1]+starting_size),
            (square1_vertex[0],square1_vertex[1]+starting_size),
            ]

    square2_vertex = (fs_center[0]+xshift,fs_center[1]+yshift)
    #ending_size = random.randrange(60,120,20)
    ending_size = 80
    front_square = [
            (square2_vertex[0],square2_vertex[1]),
            (square2_vertex[0]+ending_size,square2_vertex[1]),
            (square2_vertex[0]+ending_size,square2_vertex[1]+ending_size),
            (square2_vertex[0],square2_vertex[1]+ending_size),
            ]

    lines = []
    for i in range(0,len(back_square)):
        slope = (back_square[i][1]-front_square[i][1])/(back_square[i][0]-front_square[i][0])
        length = math.hypot(back_square[i][1]-front_square[i][1],back_square[i][0]-front_square[i][0])
        x_length= back_square[i][0]-front_square[i][0]
        lines.append([slope,length,x_length])

    steps = 3
    abs_dist = lines[0][-1]
    abs_change = ending_size - starting_size
    for line in lines:
        relative_distance = line[-1]/abs_dist
        line.append(relative_distance)
    for i in range(0,steps,1):
        coords = []
        for r in range(0,len(lines)):
            line = lines[r]
            x_change = line[-1]*abs_dist*i/steps
            y_change = x_change * line[0]
            x_full = int(front_square[r][0] + x_change)
            y_full = int(front_square[r][1] + y_change)
            coords.append((x_full,y_full))
        test(back_square,coords)



        
    test(back_square,front_square)

def multiple_squares():
    #sqrs = [(-250,250,-150,150),(-150,300,150,150),(-250,-50,-150,-150),(300,-250,150,-150),(10,30,0,0)]
    sqrs = [(-150,400-int((8/3)*i),50,250-i) for i in range(0,170,30)]
    for (a,b,c,d) in sqrs:
        run_squares(a,b,c,d)


multiple_squares()

def building():
    square2_vertex = (fs_center[0]+200,fs_center[1]+100)
    ending_size = 30
    starting_size = 130

    i = starting_size
    vertex = square2_vertex
    while i > ending_size:
      run_commands(square_slope(vertex[0],vertex[1],i,-1*(starting_size-i)/(3*starting_size)),False)
      i = i - 1
      if i%2 == 0:
        y_c = 1
        x_c = 2
      else:
        y_c = 1
        x_c = 1
      vertex = (vertex[0]-x_c,vertex[1]-y_c) 
