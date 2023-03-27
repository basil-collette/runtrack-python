print("JOB 23 ###################################################################################################################")

def draw_triangle(height):
    for x in range(height):
        print((' ' * (height-x-1)) + '/' + (' ' * (2*x)) + '\\')
    print('/' + ('_' * (2 * height-2)) + '\\')
        
draw_triangle(5)