from pymouse import PyMouse
import time
import math
import random


### Change these to the relevant coordinates of your screen! 
### I use "fullscreen" mode on myoats.com, giving more room for real estate. 
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
  #change the command to fall within the radius.
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
  if release:
    last_x,last_y = commands[-1][1]
    commands.append(("m.release("+str(last_x)+","+str(last_y)+",1)",(last_x,last_y)))
  for (command,coords) in commands:
    if(is_in_circle(coords)[0]):
      time.sleep(0.03)
      eval(command)
    else:
      time.sleep(0.03)
      eval(change_command_to_radius(command,coords))

def PointsInCircum(r,n=100,xskew=1,yskew=1):
  return [(math.cos(2*math.pi/n*x)*r*(xskew),math.sin(2*math.pi/n*x)*r*(yskew)) for x in range(0,n+1)]


def draw_circle(s_x,s_y,radius,np=50,xskew=1,yskew=1,percent_draw_start=0,percent_draw_end=1):
  all_points = PointsInCircum(radius,n=np,xskew=xskew,yskew=yskew) 
  points = all_points[int((len(all_points)-1)*percent_draw_start):int((len(all_points)-1)*percent_draw_end)]
  begin_x = s_x + int(points[0][0])
  begin_y = s_y + int(points[0][1])
  commands = [("m.press("+str(begin_x)+","+str(begin_y)+",1)",(begin_x,begin_y))]
  for point in points:
    new_x = s_x + int(point[0])
    new_y = s_y + int(point[1])
    commands.append(("m.press("+str(new_x)+","+str(new_y)+")",(new_x,new_y)))
  return(commands)

def squiggles(s_x,s_y,s_y2,x_distance,n):
  commands = [("m.press("+str(s_x)+","+str(s_y)+",1)",(s_x,s_y))]
  x = s_x
  y = s_y
  for i in range(1,n,1):
    x = s_x + x_distance*i
    y = s_y if i%2 ==0 else s_y2
    commands.append(("m.press("+str(x)+","+str(y)+")",(x,y)))
  return commands

def square(x,y,side):
  points = [(x,y),(x+side,y),(x+side,y+side),(x,y+side),(x,y),(x+side,y)]
  commands = [("m.press("+str(x)+","+str(y)+"),1",(x,y))]
  for my_x,my_y in points:
    commands.append(("m.press("+str(my_x)+","+str(my_y)+"),1",(my_x,my_y)))
  return commands

def square_slope(x,y,side,slope):
  points_raw = [(x,y),(x+side,y+side*slope),(x+side,y+side+side*slope),(x,y+side),(x,y),(x+side,y+side*slope)]
  points = [(int(a),int(b)) for (a,b) in points_raw]
  commands = [("m.press("+str(x)+","+str(y)+"),1",(x,y))]
  for my_x,my_y in points:
    if random.random() > 0.4 :
      commands.append(("m.press("+str(my_x)+","+str(my_y)+"),1",(my_x,my_y)))
  return commands

def percent_of_cmds(commands,start_pct,step_pct):
  if not start_pct == 0:
    # get the index of the first desired command based on percent
    start_index = int(start_pct*len(commands))
    # make that the first element. 
    commands = commands[start_index:] + commands[:start_index]
  # how many commands should we return
  commands = commands[:min(int(step_pct*len(commands)),len(commands))]
  return commands




def square_grid(sx,sy,slope,side,space,yrepeat,mainrepeat,goleft=False):
  for x in range(0,yrepeat,1):
    x_start = sx
    y_start = sy + int((side+space)*x)
    for i in range(0,mainrepeat,1):
      if goleft:
        addx = -1*int(i*(side+space))
        addy = -1*int(i*(side+space)*slope)
      else:
        addx = int(i*(side+space))
        addy = int(i*(side+space)*slope)
      nx_start = x_start + addx 
      ny_start = y_start + addy 
      if random.random() > 0.75 or True:
          run_commands(square_slope(nx_start,ny_start,side,slope),True)

#run_commands(square(center[0]+200,center[1]-100,50),True)
#run_commands(square_slope(center[0]+200,center[1]-100,50,-0.5),True)
#square_grid(fs_center[0]+150,fs_center[1]-250,0,20,5,5,15,False)
#square_grid(center[0]+320,center[1]-250,-1/3,20,5,5,10,True)
#square_grid(center[0]-320,center[1]-250,0,20,4,19,25,False)
#######################
#square_grid(left_up[0]-40,center[1]-260,0,25,10,14,27,False)
#bottom = center[1]-260 + (25+10)*14
#square_grid(left_up[0]-80,top,0,10,5,10,65)
#square_grid(left_up[0]-80,bottom,0,10,5,10,55)
################

def square_changes():
  screen_width = right_up[0] - left_up[0] 
  top = center[1]-260 - (5+10)*10 - 10
  last_top = top
  space = 10
  starting_width = 10
  max_width = 80
  while last_top < (fs_center[1] + fs_radius - 70):
    width = int(5*random.randrange(2,5))
    if width < 40:
      y_loop = 2
    else:
      y_loop = 1
    number_of_repeats = int(screen_width/(space+width)) + 5
    square_grid(left_up[0]-80,last_top,0,width,space,y_loop,number_of_repeats) 
    last_top = last_top + (space + width)*y_loop
    
#square_changes()
#square_grid(center[0],center[1]-250,0,30,10,1,12,False)


#for i in range(1,11,1):
#  x_start = left_up[0]+100
#  y_start = left_up[1]-100
#  y_shift = i*20
#  x_distance = 10
#  n = 20
#  rightmost_x = x_start + n*x_distance
#  if i%2 == 1:
#    run_commands(squiggles(x_start,y_start+y_shift,y_start+35+y_shift,x_distance,n),False)
#  else:
#    run_commands(squiggles(rightmost_x,y_start+y_shift,y_start+35+y_shift,x_distance*-1,n),True)


###### PARABOLASSSS
#for z in range(0,1,1):
#  add_x = 20*z
#  for n in range(0,15,1):
#    commands = []
#    x_start = left_up[0]+100 + add_x
#    y_start = left_up[1]-100 + 10*n
#    for i in range(-10,10,1):
#      x = x_start+5*int(i) 
#      y = y_start+int((1+(abs(i)/10))*(i**2))
#      print(x,y)
#      commands.append(("m.press("+str(x)+","+str(y)+")",(x,y)))
#    run_commands(commands,False)




def random():
  max_range = 200
  step=5
  for i in range(80,max_range,step):
    commands = draw_circle(center[0], center[1], i, 100, xskew=1, yskew=1, percent_draw_start=0, percent_draw_end=1)
    #commands = percent_of_cmds(commands,i/max_range,.1)
    #run_commands(commands,i>=(max_range-step-1))
    commands = percent_of_cmds(commands,0,(max_range-(i))/max_range)
    run_commands(commands,True)
    #run_commands(commands,i%10==5)


def hemispheres():
  radius=10
  origy = center[1]-75
  origx = center[0]+350
  for i in range(0,60,radius):
    if i == 0 or i%(2*radius) ==0:
      origy = origy + radius*2 + radius
    else:
      origy = origy - radius//2
    newx,newy = origx,origy
    for _ in range(1,10,1):
      commands = draw_circle(newx, newy, radius, 50, xskew=1, yskew=1, percent_draw_start=0, percent_draw_end=1)
      if i == 0 or i%(2*radius) ==0:
        commands = percent_of_cmds(commands,0,0.53)
        newx=commands[-1][-1][0]-radius
        #newy=commands[-1][-1][1]
      else: 
        commands = percent_of_cmds(commands,0.5,0.53)
        newx=commands[-1][-1][0]-3*radius
        #newy=commands[-1][-1][1]
      run_commands(commands,True)

#max_range = 220
#for i in range(150,max_range,15):
#  percent_start = max(i/max_range,1-0.14)
#  percent_end = max(i/max_range + 0.14,1)
#  run_commands(draw_circle(center[0],center[1],i,100,xskew=1,yskew=1,percent_draw_start=percent_start,percent_draw_end=percent_end),i==160)

#angles are always 60
#length is always side / iteration

def triangle_from_points(points):
  sx,sy = points[0]
  commands= [("m.press("+str(sx)+","+str(sy)+"),1",(sx,sy))]
  commands.append(("m.press("+str(sx)+","+str(sy)+"),1",(sx,sy)))
  for (x,y) in points:
    commands.append(("m.move("+str(x)+","+str(y)+"),1",(x,y)))
  for (x,y) in points:
    commands.append(("m.press("+str(x)+","+str(y)+"),1",(x,y)))
  cut = True # if random.random() > 0.9 else False
  run_commands(commands,cut)

def triangle(x,y,side,upsidedown=False):
  sides = side
  x_shift = int((math.sin(math.radians(30))*sides)) #opposite
  y_shift = int(math.cos(math.radians(30))*sides) #adjacent
  if upsidedown:
    y_shift = y_shift*-1
  sx = x
  sy = y 
  starting_points = [(sx,sy),(sx+x_shift,sy+y_shift),(sx-x_shift,sy+y_shift)] 
  return starting_points


def midpoint(tuple1,tuple2):
  x1,y1 = tuple1
  x2,y2 = tuple2
  return (int((x1 + x2)/2), int((y1 + y2)/2))
import random
def serpinski(data,steps,k):
  # get initial points
  sp = data
  if random.random() > 0: # min(0.9,0.2*k): 
    triangle_from_points(sp)
  midpoints = [midpoint(sp[0],sp[1]),midpoint(sp[1],sp[2]),midpoint(sp[2],sp[0])]
  k += 1
  if k <= steps:
    cutoff = 0.5
    if random.random() > cutoff: 
      serpinski([sp[0],midpoints[0],midpoints[2]],steps,k)
    if random.random() > cutoff: 
      serpinski([sp[1],midpoints[0],midpoints[1]],steps,k)
    if random.random() > cutoff: 
      serpinski([sp[2],midpoints[1],midpoints[2]],steps,k)

## FULL SCREEN ONLY
#serpinski(triangle(center[0]-120,center[1]+160,1050,True),5,0)
#serpinski(triangle(center[0]+120,center[1]-200,750),5,0)

def random_triangles():
  #angle = math.radians(random.random()*360)
  angle = math.radians(random.randrange(-90,220))
  radius_length = random.random()*(fs_radius - 300) + 200
  x_point =  fs_center[0] + int(math.sin(angle)*radius_length)
  y_point =  fs_center[1] + int(math.cos(angle)*radius_length)
  triangle_size = int(random.randrange(50,300,20))
  if triangle_size < 150:
    depth = random.randrange(1,2) 
  else:
    depth = random.randrange(2,4) 
  upsidedown = y_point >= fs_center[1]
  if random.random() > 0.8:
    upsidedown = not upsidedown
  serpinski(triangle(x_point,y_point,triangle_size,upsidedown),depth,0)

#for _ in range(0,12):
#  random_triangles()


#serpinski(triangle(center[0],center[1]-430,900),6,0)
#serpinski(triangle(center[0]-260,center[1]-50,700),5,0)


#serpinski(triangle(center[0]+320,center[1]+160,550,True),4,0)
