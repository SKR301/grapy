from tkinter import *

root = Tk()
root.state('zoomed')
root.title('grapy')

points = []

# func
def exportPoints():
    print(points)
    tempLabel.config(text='Exporting...')

def plotPoint(event):
    x, y = event.x-2, 1002-event.y
    if x<0 or x>1500 or y<0 or y>1000:
        return

    graph.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, width = 0, fill = 'blue')
    points.append({x, y})
    tempLabel.config(text=f'Plot at {x}, {y}')
    

# if __name__ == '__main__':
    # topBarFrame = Frame(root, bd=5)
    # topBarFrame.grid(row=0, column=0)

graphFrame = Frame(root, bd=5)
graphFrame.grid(row=1, column=0)

graph = Canvas(graphFrame, bg='white', height=1000, width=1500)
graph.bind('<Button-1>', plotPoint)
graph.grid(row=0, column=0)

menuBarFrame = Frame(root, bd=5)
menuBarFrame.grid(row=1, column=1)

tempLabel = Label(root, text='SKRinternationals 2022')
tempLabel.grid(row=2, column=0)

exportBtn = Button(root, text = 'Export', command=exportPoints, padx=150, bg='#0078d7', fg='white')
exportBtn.grid(row=2, column=1)

mainloop()
