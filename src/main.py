from tkinter import *
from random import *
import csv
import math

root = Tk()
root.state('zoomed')
root.title('grapy')

points = []
currPoint = []
DEG_TO_RAD = 0.01745329
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

def plotManualPoint(event):
    x, y = event.x-2, 1002-event.y
    if x<0 or x>1500 or y<0 or y>1000:
        return

    graph.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, width = 0, fill = 'blue')
    points.append([x, y])
    tempLabel.config(text=f'Plot at {x}, {y}')

def undoPlotManualPoint(event):
    if len(points) < 1:
        return

    lastPoint = points.pop(-1)
    x, y = lastPoint[0]+2, -1 * (lastPoint[1]-1002)
    graph.create_oval(x-3, y-3, x+3, y+3, width = 0, fill = 'white')

def hideLinRegOpt():
    linRegSlopeScale.grid_remove()
    linRegConstantScale.grid_remove()
    linRegSpreadScale.grid_remove()
    linRegOptBtnFrame.grid_remove()
    linRegPointPlt.grid_remove()
    linRegPointSave.grid_remove()
    linRegBtn.config(command=showLinRegOpt)

def showLinRegOpt():
    linRegSlopeScale.grid(row=0, column=0)
    linRegConstantScale.grid(row=1, column=0)
    linRegSpreadScale.grid(row=2, column=0)
    linRegOptBtnFrame.grid(row=3, column=0)
    linRegPointPlt.grid(row=0, column=0)
    linRegPointSave.grid(row=0, column=1)
    linRegBtn.config(command=hideLinRegOpt)

def clearCurr():
    for x,y in currPoint:
        plotX, plotY = x-2, -1*(y-1002)
        graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'white')
    
    currPoint.clear()

def plotLinearRegPoints():
    clearCurr()
    
    tempLabel.config(text=f'Plotting {linRegSlope.get()}x + {linRegConstant.get()} : [{linRegSpread.get()}]')

    if linRegSlope.get() == 90:
        for a in range(0, 1000, 10):
            y = a + (random() * linRegSpread.get()) - linRegSpread.get()/2
            x = (y - linRegConstant.get()) / math.tan(linRegSlope.get() * DEG_TO_RAD)
            plotX, plotY = x, 1002-y
            graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'blue')
            currPoint.append([x,y])
    if linRegSlope.get() > 45 and linRegSlope.get() < 135:
        for a in range(0, 1000, 10):
            y = a + (random() * linRegSpread.get()) - linRegSpread.get()/2
            x = (y - linRegConstant.get()) / math.tan(linRegSlope.get() * DEG_TO_RAD)
            plotX, plotY = x-2, 1002-y
            graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'blue')
            currPoint.append([x,y])
    else: 
        for a in range(0, 1500, 15):
            x = a + (random() * linRegSpread.get()) - linRegSpread.get()/2
            y = math.tan(linRegSlope.get() * DEG_TO_RAD) * x + linRegConstant.get() + (random() * linRegSpread.get()) - linRegSpread.get()/2
            plotX, plotY = x-2, 1002-y
            graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'blue')
            currPoint.append([x,y])

def saveLinearRegPoints():
    global points
    points = points + currPoint

def showLogRegOpt():
    print('show logistic regression')



# if __name__ == '__main__': ----------------------------------------------------------------------------------------
topBarFrame = Frame(root, bd=5)
topBarFrame.grid(row=0, column=0)

graphFrame = Frame(root, bd=5)
graphFrame.grid(row=1, column=0)

graph = Canvas(graphFrame, bg='white', height=1000, width=1500)
graph.bind('<Button-1>', plotManualPoint)
graph.bind_all('<Control-z>', undoPlotManualPoint)
graph.grid(row=0, column=0)


menuBarFrame = Frame(root, bd=5)
menuBarFrame.grid(row=1, column=1)

linRegBtn = Button(menuBarFrame, text='Linear Reg', command=showLinRegOpt)
linRegBtn.grid(row=0, column=0)


linRegFrame = Frame(menuBarFrame, bd=5)
linRegFrame.grid(row=1, column=0)

linRegSlopeScale = Scale(linRegFrame, from_=0, to=180, orient=HORIZONTAL, length=300, variable=linRegSlope)
linRegConstantScale = Scale(linRegFrame, from_=-1500, to=1500, orient=HORIZONTAL, length=300, variable=linRegConstant)
linRegSpreadScale = Scale(linRegFrame, from_=0, to=200, orient=HORIZONTAL, length=300, variable=linRegSpread)
linRegOptBtnFrame = Frame(linRegFrame, bd=2)
linRegPointPlt = Button(linRegOptBtnFrame, text='Plot', command=plotLinearRegPoints)
linRegPointSave = Button(linRegOptBtnFrame, text='Save', command=saveLinearRegPoints)

# logRegnBtn = Button(menuBarFrame, text='Logistic Reg', command=showLogRegOpt)
# logRegnBtn.grid(row=1, column=0)


tempLabel = Label(root, text='SKRinternationals 2022')
tempLabel.grid(row=2, column=0)


exportBtn = Button(root, text='Export', command=exportPoints, padx=150, bg='#0078d7', fg='white')
exportBtn.grid(row=2, column=1)

mainloop()
