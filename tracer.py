from pymouse import PyMouse
from PIL import Image
import time
import numpy as np
import math
import random
m = PyMouse()
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
  wait = 0.02
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

def PointsInCircum(r,n=100,xskew=1,yskew=1):
  return [(math.cos(2*math.pi/n*x)*r*(xskew),math.sin(2*math.pi/n*x)*r*(yskew)) for x in range(0,n+1)]

def get_colors():
    im = Image.open('./circles.jpg')
    width,height = im.size
    pixel_values = im.load() 
    return (pixel_values,width,height)

def is_white(rgb):
    if rgb[0] > 200 and rgb[1] > 200 and rgb[2] > 200:
        return True
    else:
        return False


def run_everything():
  pixels,width,height = get_colors()
  desired_x = 700
  desired_y = 700
  xscale = width/desired_x 
  yscale = height/desired_y
  cmds = []

  for h in range(1,desired_y,2):
    number_releases = 0
    number_presses = 0
    for w in range(1,desired_x,2):
      act_x = int(w * xscale) - 1
      act_y = int(h * yscale) - 1
      if is_white(pixels[act_x,act_y]) or w > desired_x-10:
        if not number_releases > 3:
          cmds.append(((w,h),"release"))
        number_releases += 1
      else:
        cmds.append(((w,h),"press"))
        number_releases = 0
  commands = []
  for (coord,cmd) in cmds: 
    x = coord[0]+450
    y = coord[1]+200
    foo = "m."+cmd+"("+str(x)+","+str(y)+",1)"
    commands.append((foo,(x,y)))
  run_commands(commands,True)

run_everything()
