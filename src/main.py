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
CANVAS_WIDTH, CANVAS_HEIGHT = 1500, 1000
linRegSlope = DoubleVar()
linRegConstant = DoubleVar()
linRegSpread = DoubleVar()

# functions -------------------------------------------------------------------------------------------------------------
def canvasToGraphPoint(canvasPoint):
    graphPoint = []
    for x,y in canvasPoint:
        graphPoint.append([x-CANVAS_WIDTH/2, CANVAS_HEIGHT/2-y])
    return graphPoint

def exportPoints():
    pointsToExp = canvasToGraphPoint(points)

    tempLabel.config(text='Exporting...')
    with open('points.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows([['x','y']])
        csvwriter.writerows(pointsToExp)

def plotPoint(x,y):
    graph.create_oval(x-3, y-3, x+3, y+3, width = 0, fill = 'blue')

def plotManualPoint(event):
    plotPoint(event.x, event.y)
    points.append([event.x, event.y])

def hideLinRegOpt():
    linRegSlopeLabel.grid_remove()
    linRegSlopeScale.grid_remove()
    linRegConstantLabel.grid_remove()
    linRegConstantScale.grid_remove()
    linRegSpreadLabel.grid_remove()
    linRegSpreadScale.grid_remove()
    linRegOptBtnFrame.grid_remove()
    linRegPointPlt.grid_remove()
    linRegPointSave.grid_remove()
    linRegBtn.config(command=showLinRegOpt)

def showLinRegOpt():
    linRegSlopeLabel.grid(row=0,column=0)
    linRegSlopeScale.grid(row=0, column=1)
    linRegConstantLabel.grid(row=1,column=0)
    linRegConstantScale.grid(row=1, column=1)
    linRegSpreadLabel.grid(row=2, column=0)
    linRegSpreadScale.grid(row=2, column=1)
    linRegOptBtnFrame.grid(row=3, columnspan=2)
    linRegPointPlt.grid(row=0, column=0)
    linRegPointSave.grid(row=0, column=1)
    linRegBtn.config(command=hideLinRegOpt)

# def clearCurr():
#     for x,y in currPoint:
#         plotX, plotY = x-2, -1*(y-1002)
#         graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'white')
    
#     currPoint.clear()

def randomSpread(spread):
    return (random() * spread) - spread/2

def plotLinearRegPoints():
    # clearCurr()
    # TODO HERE 
    # if linRegSlope.get() == 90:
    #     for a in range(0, CANVAS_HEIGHT, 10):
    #         y = a + (random() * linRegSpread.get()) - linRegSpread.get()/2
    #         x = (y - linRegConstant.get()) / math.tan(linRegSlope.get() * DEG_TO_RAD)
    #         plotX, plotY = x, 1002-y
    #         graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'blue')
    #         currPoint.append([x,y])
    # if linRegSlope.get() > 45 and linRegSlope.get() < 135:
    #     for a in range(0, CANVAS_HEIGHT, 10):
    #         y = a + (random() * linRegSpread.get()) - linRegSpread.get()/2
    #         x = (y - linRegConstant.get()) / math.tan(linRegSlope.get() * DEG_TO_RAD)
    #         plotX, plotY = x-2, 1002-y
    #         graph.create_oval(plotX-3, plotY-3, plotX+3, plotY+3, width = 0, fill = 'blue')
    #         currPoint.append([x,y])
    # else: 
    for a in range(int(-CANVAS_WIDTH/2), int(CANVAS_WIDTH/2), int(CANVAS_WIDTH/100)):
        x = a + randomSpread(linRegSpread.get())
        y = math.tan(linRegSlope.get() * DEG_TO_RAD) * x + linRegConstant.get() + randomSpread(linRegSpread.get())
        plotX,plotY = x+CANVAS_WIDTH/2, CANVAS_HEIGHT/2-y
        plotPoint(plotX,plotY)
        points.append([plotX, plotY])
            

def saveLinearRegPoints():
    global points
    points = points + currPoint

def showLogRegOpt():
    print('show logistic regression')

def displayCursorLocation(event):
    tempLabel.config(text=f'[{event.x-CANVAS_WIDTH/2},{CANVAS_HEIGHT/2-event.y}]')

def initGraph():
    graph.create_line(CANVAS_WIDTH/2, 0, CANVAS_WIDTH/2, CANVAS_HEIGHT, fill='#cccccc', width=2)
    graph.create_line(0, CANVAS_HEIGHT/2, CANVAS_WIDTH, CANVAS_HEIGHT/2, fill='#cccccc', width=2)
    for a in range(int(CANVAS_WIDTH/2), CANVAS_WIDTH, 50):
        graph.create_line(a, 0, a, CANVAS_HEIGHT, fill='#cccccc', width=1)
        graph.create_line(a-CANVAS_WIDTH/2, 0, a-CANVAS_WIDTH/2, CANVAS_HEIGHT, fill='#cccccc', width=1)
    for a in range(int(CANVAS_HEIGHT/2), CANVAS_HEIGHT, 50):
        graph.create_line(0, a, CANVAS_WIDTH, a, fill='#cccccc', width=1)
        graph.create_line(0, a-CANVAS_HEIGHT/2, CANVAS_WIDTH, a-CANVAS_HEIGHT/2, fill='#cccccc', width=1)

# MAIN---
    # TOP BAR---
topBarFrame = Frame(root, bd=5)
topBarFrame.grid(row=0, column=0)

#   GRAPH---
graphFrame = Frame(root, bd=5)
graphFrame.grid(row=1, column=0)

graph = Canvas(graphFrame, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
graph.grid(row=0, column=0)
initGraph()

graph.bind('<Button-1>', plotManualPoint)
graph.bind('<Motion>', displayCursorLocation)
# graph.bind_all('<Control-z>', undoPlotManualPoint)

#   RIGHT MENU---
menuBarFrame = Frame(root, bd=5)
menuBarFrame.grid(row=1, column=1)

        # LINEAR REGRESSION---
linRegBtn = Button(menuBarFrame, text='Linear Reg', width=40, command=showLinRegOpt)
linRegBtn.grid(row=0, column=0)

linRegFrame = Frame(menuBarFrame,highlightbackground='#aaa', highlightthickness=2, bd=10)
linRegFrame.grid(row=1, column=0)

linRegSlopeLabel = Label(linRegFrame, text='Slope')
linRegSlopeScale = Scale(linRegFrame, from_=0, to=180, orient=HORIZONTAL, length=200, variable=linRegSlope)
linRegConstantLabel = Label(linRegFrame, text='Y-intercept')
linRegConstantScale = Scale(linRegFrame, from_=-CANVAS_HEIGHT/2, to=CANVAS_HEIGHT/2, orient=HORIZONTAL, length=200, variable=linRegConstant)
linRegSpreadLabel = Label(linRegFrame, text='Spread')
linRegSpreadScale = Scale(linRegFrame, from_=0, to=200, orient=HORIZONTAL, length=200, variable=linRegSpread)
linRegOptBtnFrame = Frame(linRegFrame, bd=2)
linRegPointPlt = Button(linRegOptBtnFrame, text='Plot', command=plotLinearRegPoints)
linRegPointSave = Button(linRegOptBtnFrame, text='Save', command=saveLinearRegPoints)

    # BOTTOM LABEL---
tempLabel = Label(root, text='SKRinternationals 2022')
tempLabel.grid(row=2, column=0)

    # EXPORT---
exportBtn = Button(root, text='Export', command=exportPoints, padx=150, bg='#0078d7', fg='white')
exportBtn.grid(row=2, column=1)

mainloop()