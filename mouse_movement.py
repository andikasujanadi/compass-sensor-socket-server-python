import pyautogui
import math

init_x=960
init_y=540
boundary = 200

x0, y0 = init_x, init_y
x, y = 0, 0
angle = 90


angle_in_degrees = 90
angle_in_radians = math.radians(angle_in_degrees)
result = math.cos(angle_in_radians)
rounded_result = round(result, 15)  # Round to 15 decimal places

print(rounded_result)

try:
    pyautogui.moveTo(init_x, init_y)
    while True:
        x1, y1 = pyautogui.position()
        if x1 < (init_x-boundary):
            pyautogui.moveTo(init_x+boundary, y1)
            x -= boundary*2
        elif x1 > (init_x+boundary):
            pyautogui.moveTo(init_x-boundary, y1)
            x += boundary*2
        if y1 < (init_y-boundary):
            pyautogui.moveTo(x1, init_y+boundary)
            y -= boundary*2
        elif y1 > (init_y+boundary):
            pyautogui.moveTo(x1, init_y-boundary)
            y += boundary*2
    
        x += (x1 - x0)*round(math.cos(math.radians(angle)),15) + (y1 - y0)*round(math.sin(math.radians(angle)),15)
        y += (y1 - y0)*round(math.cos(math.radians(angle)),15) + (x1 - x0)*round(math.sin(math.radians(angle)),15)

        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        
        x0, y0 = x1, y1
except KeyboardInterrupt:
    print()