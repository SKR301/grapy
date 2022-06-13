from tkinter import *
import csv

root = Tk()
root.state('zoomed')
root.title('grapy')

points = []
linRegSlope = DoubleVar()
linRegConstant = DoubleVar()
linRegSpread = DoubleVar()

# func -------------------------------------------------------------------------------------------------------------
def exportPoints():
    tempLabel.config(text='Exporting...')
    with open('points.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows([['x','y']])
        csvwriter.writerows(points)

def plotPoint(event):
    x, y = event.x-2, 1002-event.y
    if x<0 or x>1500 or y<0 or y>1000:
        return

    graph.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, width = 0, fill = 'blue')
    points.append([x, y])
    tempLabel.config(text=f'Plot at {x}, {y}')

def undoPlotPoint(event):
    if len(points) < 1:
        return

    lastPoint = points.pop(-1)
    x, y = lastPoint[0]+2, -1 * (lastPoint[1]-1002)
    graph.create_oval(x-3, y-3, x+3, y+3, width = 0, fill = 'white')

def hideLinRegOpt():
    linRegSlopeScale.grid_remove()
    linRegConstantScale.grid_remove()
    linRegSpreadScale.grid_remove()
    linRegBtn.config(command=showLinRegOpt)

def showLinRegOpt():
    linRegSlopeScale.grid(row=0, column=0)
    linRegConstantScale.grid(row=1, column=0)
    linRegSpreadScale.grid(row=2, column=0)
    linRegBtn.config(command=hideLinRegOpt)

def plotLinearRegPoints(event):
    tempLabel.config(text=f'{linRegSlope.get()}, {linRegConstant.get()}, {linRegSpread.get()}')

def showLogRegOpt():
    print('show logistic regression')


# if __name__ == '__main__': ----------------------------------------------------------------------------------------
topBarFrame = Frame(root, bd=5)
topBarFrame.grid(row=0, column=0)

graphFrame = Frame(root, bd=5)
graphFrame.grid(row=1, column=0)

graph = Canvas(graphFrame, bg='white', height=1000, width=1500)
graph.bind('<Button-1>', plotPoint)
graph.bind_all('<Control-z>', undoPlotPoint)
graph.grid(row=0, column=0)


menuBarFrame = Frame(root, bd=5)
menuBarFrame.grid(row=1, column=1)

linRegBtn = Button(menuBarFrame, text='Linear Reg', command=showLinRegOpt)
linRegBtn.grid(row=0, column=0)


linRegFrame = Frame(menuBarFrame, bd=5)
linRegFrame.grid(row=1, column=0)

linRegSlopeScale = Scale(linRegFrame, from_=0, to=90, orient=HORIZONTAL, length=300, variable=linRegSlope, command=plotLinearRegPoints)
linRegConstantScale = Scale(linRegFrame, from_=-1500, to=1500, orient=HORIZONTAL, length=300, variable=linRegConstant, command=plotLinearRegPoints)
linRegSpreadScale = Scale(linRegFrame, from_=0, to=100, orient=HORIZONTAL, length=300, variable=linRegSpread, command=plotLinearRegPoints)


# logRegnBtn = Button(menuBarFrame, text='Logistic Reg', command=showLogRegOpt)
# logRegnBtn.grid(row=1, column=0)


tempLabel = Label(root, text='SKRinternationals 2022')
tempLabel.grid(row=2, column=0)


exportBtn = Button(root, text='Export', command=exportPoints, padx=150, bg='#0078d7', fg='white')
exportBtn.grid(row=2, column=1)

mainloop()
