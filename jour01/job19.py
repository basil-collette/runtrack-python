print("JOB 19 ###################################################################################################################")

def draw_rectangle(width, height):
    for x in range(height):
        line = '|'
        for y in range(width):
            line += '-' if (x == 0 or x == height-1) else ' '
        line += '|'
        print(line)

draw_rectangle(10, 3)
