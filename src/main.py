from tkinter import *
from random import *
from os.path import exists
import csv
import math

root = Tk()
root.state('zoomed')
root.title('grapy')

p1 = PhotoImage(file = "./src/assets/grapy_logo.png")
root.iconphoto(False, p1)

points = []
pointCountList = []
currPoint = []
DEG_TO_RAD = 0.01745329
CANVAS_WIDTH, CANVAS_HEIGHT = 1500, 1000
GRAPH_WIDTH, GRAPH_HEIGHT = 30, 20
CANVAS_GRAPH_RATIO = 50
linRegSlope = DoubleVar()
linRegConstant = DoubleVar()
linRegSpread = DoubleVar()
logRegSlope = DoubleVar()
logRegConstant = DoubleVar()
logRegSpread = DoubleVar()
clusterRadius = DoubleVar()
clusterPointsCount = DoubleVar()

# functions -------------------------------------------------------------------------------------------------------------
def canvasToGraphPoint(canvasX, canvasY):
    x, y = canvasX-CANVAS_WIDTH/2, CANVAS_HEIGHT/2-canvasY
    x, y = x/50, y/50
    graphX, graphY = round(x, 10), round(y, 10)
    return graphX, graphY

def graphToCanvasPoints(graphX, graphY):
    x, y = graphX*50, graphY*50
    x, y = x+CANVAS_WIDTH/2, CANVAS_HEIGHT/2-y
    canvasX, canvasY = round(x, 10), round(y, 10)
    return canvasX, canvasY

def getOutputFileName():
    count = 0
    fileName = 'points_'+str(count)+'.csv'
    while exists(fileName):
        count += 1
        fileName = 'points_'+str(count)+'.csv'

    return fileName

def exportPoints():
    pointsToExp = []
    for x, y in points:
        pointsToExp.append(canvasToGraphPoint(x, y))
    
    filename = getOutputFileName()

    tempLabel.config(text='Exporting...')
    isSaved = True
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerows([['x','y']])
            csvwriter.writerows(pointsToExp)
    except Exception as e:
        print(e)
        isSaved = False

    tempLabel.config(text=f'Exported as {filename}') if isSaved else tempLabel.config(text='Cannot export successfully!')

def undoPlotPoint(event):
    if len(pointCountList) <= 0:
        return
    ptsToUndo = pointCountList.pop(-1)
    
    for a in range(ptsToUndo):
        x,y = points.pop(-1)
        plotPoint(x, y, 'white')

    initGraph()
    initPoints()
        
def plotPoint(x,y,colour):
    graph.create_oval(x-3, y-3, x+3, y+3, width = 0, fill = colour)

def plotManualPoint(event):
    plotPoint(event.x, event.y, 'blue')
    points.append([event.x, event.y])
    pointCountList.append(1)

def clickedGraph(event):
    if clusterPointsCount.get() > 0 and clusterRadius.get() > 0.0:
        plotClusterPoints(event)
    else:
        plotManualPoint(event)

def hideLinRegOpt():
    linRegFrame.grid_remove()
    linRegSlopeLabel.grid_remove()
    linRegSlopeScale.grid_remove()
    linRegConstantLabel.grid_remove()
    linRegConstantScale.grid_remove()
    linRegSpreadLabel.grid_remove()
    linRegSpreadScale.grid_remove()
    linRegOptBtnFrame.grid_remove()
    # linRegPointPlt.grid_remove()
    linRegPointSave.grid_remove()
    linRegBtn.config(command=showLinRegOpt)

def showLinRegOpt():
    linRegFrame.grid(row=1, column=0)
    linRegSlopeLabel.grid(row=0,column=0)
    linRegSlopeScale.grid(row=0, column=1)
    linRegConstantLabel.grid(row=1,column=0)
    linRegConstantScale.grid(row=1, column=1)
    linRegSpreadLabel.grid(row=2, column=0)
    linRegSpreadScale.grid(row=2, column=1)
    linRegOptBtnFrame.grid(row=3, columnspan=2)
    # linRegPointPlt.grid(row=0, column=0)
    linRegPointSave.grid(row=0, column=0)
    linRegBtn.config(command=hideLinRegOpt)

def hideLogRegOpt():
    logRegFrame.grid_remove()
    logRegSlopeLabel.grid_remove()
    logRegSlopeScale.grid_remove()
    logRegConstantLabel.grid_remove()
    logRegConstantScale.grid_remove()
    logRegSpreadLabel.grid_remove()
    logRegSpreadScale.grid_remove()
    logRegOptBtnFrame.grid_remove()
    # logRegPointPlt.grid_remove()
    logRegPointSave.grid_remove()
    logRegBtn.config(command=showLogRegOpt)

def showLogRegOpt():
    logRegFrame.grid(row=3, column=0)
    logRegSlopeLabel.grid(row=0,column=0)
    logRegSlopeScale.grid(row=0, column=1)
    logRegConstantLabel.grid(row=1,column=0)
    logRegConstantScale.grid(row=1, column=1)
    logRegSpreadLabel.grid(row=2, column=0)
    logRegSpreadScale.grid(row=2, column=1)
    logRegOptBtnFrame.grid(row=3, columnspan=2)
    # logRegPointPlt.grid(row=0, column=0)
    logRegPointSave.grid(row=0, column=1)
    logRegBtn.config(command=hideLogRegOpt)

def hideClusterOpt():
    clusterFrame.grid_remove()
    clusterPointsCountLabel.grid_remove()
    clusterPointsCountScale.grid_remove()
    clusterRadiusLabel.grid_remove()
    clusterRadiusScale.grid_remove()
    clusterBtnFrame.grid_remove()
    clusterBtn.config(command=showClusterOpt)

def showClusterOpt():
    clusterFrame.grid(row=5, column=0)
    clusterPointsCountLabel.grid(row=0, column=0)
    clusterPointsCountScale.grid(row=0, column=1)
    clusterRadiusLabel.grid(row=1, column=0)
    clusterRadiusScale.grid(row=1, column=1)
    clusterBtnFrame.grid(row=3, columnspan=2)
    clusterBtn.config(command=hideClusterOpt)

def initPoints():
    for x,y in points:
        plotPoint(x, y, 'blue')

def clearCurr():
    for x,y in currPoint:
        plotPoint(x, y, 'white')
    currPoint.clear()
    initGraph()
    initPoints()

def randomSpread(spread):
    return (random() * spread) - spread/2

def plotLinearRegPoints(event):
    clearCurr()
    tempLabel.config(text=f'y = {round(math.tan(linRegSlope.get()),2)}x + {linRegConstant.get()}')

    if linRegSlope.get() > 45 and linRegSlope.get() < 135:
        a = -GRAPH_HEIGHT/2
        while a < GRAPH_HEIGHT/2:
            y = a
            x = (y - linRegConstant.get())/(math.tan(linRegSlope.get() * DEG_TO_RAD))
            x, y = x + randomSpread(linRegSpread.get()), y + randomSpread(linRegSpread.get())
            plotX, plotY = graphToCanvasPoints(x, y)
            plotPoint(plotX, plotY, 'blue')
            currPoint.append([plotX, plotY])
            a += GRAPH_HEIGHT/100
    else: 
        a = -GRAPH_WIDTH/2
        while a < GRAPH_WIDTH/2:
            x = a
            y = math.tan(linRegSlope.get() * DEG_TO_RAD) * x + linRegConstant.get()
            x, y = x + randomSpread(linRegSpread.get()), y + randomSpread(linRegSpread.get())
            plotX, plotY = graphToCanvasPoints(x, y)
            plotPoint(plotX, plotY, 'blue')
            currPoint.append([plotX, plotY])
            a += GRAPH_WIDTH/100
          
def saveLinearRegPoints():
    global points
    points = points + currPoint
    pointCountList.append(100)
    currPoint.clear()

def plotLogisticRegPoints(event):
    clearCurr()
    tempLabel.config(text=f'y = 1/(1+e^({logRegSlope.get()}x + {logRegConstant.get()}))')
    
    theta = logRegSlope.get()
    if theta == 89:
        theta = 88
    if theta == 91:
        theta = 92

    if theta == 90:
        a = -GRAPH_WIDTH/2
        while a < GRAPH_WIDTH/2:
            x = a
            y = 0 if a < 0 else 1
            x, y = x + randomSpread(logRegSpread.get()), y + randomSpread(logRegSpread.get())
            plotX,plotY = graphToCanvasPoints(x, y)
            plotPoint(plotX, plotY, 'blue')
            currPoint.append([plotX, plotY])
            a += GRAPH_WIDTH/100
    else:    
        a = -GRAPH_WIDTH/2
        while a < GRAPH_WIDTH/2:
            x = a
            z = math.tan(theta * DEG_TO_RAD) * x + logRegConstant.get()
            y = 1/(1+pow(math.e,-z))
            x, y = x + randomSpread(logRegSpread.get()), y + randomSpread(logRegSpread.get())
            plotX, plotY = graphToCanvasPoints(x, y)
            plotPoint(plotX, plotY, 'blue')
            currPoint.append([plotX, plotY])
            a += GRAPH_WIDTH/100
          
def saveLogisticRegPoints():
    global points
    points = points + currPoint
    pointCountList.append(100)
    currPoint.clear()

def savePts(pointsCount=0):
    global points
    points = points + currPoint
    if pointsCount == 0:
        pointCountList.append(len(currPoint))
    else:
        pointCountList.append(pointsCount)
    currPoint.clear()

def plotClusterPoints(event):
    for a in range(int(clusterPointsCount.get())):
        xOffset, yOffset = randomSpread(2 * clusterRadius.get()) * CANVAS_GRAPH_RATIO, randomSpread(2 * clusterRadius.get()) * CANVAS_GRAPH_RATIO
        plotX, plotY = event.x + xOffset, event.y + yOffset
        plotPoint(plotX, plotY, 'blue')
        points.append([plotX, plotY])
    pointCountList.append(int(clusterPointsCount.get()))

def displayCursorLocation(event):
    # x1, y1 = canvasToGraphPoint(event.x, event.y)
    # x2, y2 = graphToCanvasPoints(x1, y1)
    # tempLabel.config(text=f'[{event.x},{event.y}]=>[{x1},{y1}]=>[{x2},{y2}]')
    x, y = canvasToGraphPoint(event.x, event.y)
    tempLabel.config(text=f'[{x},{y}]')

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

graph.bind('<Button-1>', clickedGraph)
graph.bind('<Motion>', displayCursorLocation)
graph.bind_all('<Control-z>', undoPlotPoint)

#   RIGHT MENU---
menuBarFrame = Frame(root, bd=5)
menuBarFrame.grid(row=1, column=1)  

        # LINEAR REGRESSION---
linRegBtn = Button(menuBarFrame, text='Linear Reg', width=40, command=showLinRegOpt)
linRegBtn.grid(row=0, column=0)

linRegFrame = Frame(menuBarFrame, highlightbackground='#aaa', highlightthickness=2, bd=10)

linRegSlopeLabel = Label(linRegFrame, text='Elevation')
linRegSlopeScale = Scale(linRegFrame, from_=0, to=180, orient=HORIZONTAL, length=200, variable=linRegSlope, command=plotLinearRegPoints)
linRegConstantLabel = Label(linRegFrame, text='Y-intercept')
linRegConstantScale = Scale(linRegFrame, from_=-GRAPH_HEIGHT/2, to=GRAPH_HEIGHT/2, orient=HORIZONTAL, length=200, variable=linRegConstant, command=plotLinearRegPoints)
linRegSpreadLabel = Label(linRegFrame, text='Spread')
linRegSpreadScale = Scale(linRegFrame, from_=0, to=5, orient=HORIZONTAL, length=200, variable=linRegSpread, command=plotLinearRegPoints)
linRegOptBtnFrame = Frame(linRegFrame, bd=2)
linRegPointSave = Button(linRegOptBtnFrame, text='Save', command=lambda: savePts(100))

        # LINEAR REGRESSION---
logRegBtn = Button(menuBarFrame, text='Logistic Reg', width=40, command=showLogRegOpt)
logRegBtn.grid(row=2, column=0)

logRegFrame = Frame(menuBarFrame, highlightbackground='#aaa', highlightthickness=2, bd=10)

logRegSlopeLabel = Label(logRegFrame, text='Elevation')
logRegSlopeScale = Scale(logRegFrame, from_=0, to=180, orient=HORIZONTAL, length=200, variable=logRegSlope, command=plotLogisticRegPoints)
logRegConstantLabel = Label(logRegFrame, text='X-offset')
logRegConstantScale = Scale(logRegFrame, from_=-GRAPH_WIDTH/2, to=GRAPH_WIDTH/2, orient=HORIZONTAL, length=200, variable=logRegConstant, command=plotLogisticRegPoints)
logRegSpreadLabel = Label(logRegFrame, text='Spread')
logRegSpreadScale = Scale(logRegFrame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL, length=200, variable=logRegSpread, command=plotLogisticRegPoints)
logRegOptBtnFrame = Frame(logRegFrame, bd=2)
logRegPointSave = Button(logRegOptBtnFrame, text='Save', command=lambda: savePts(100))

        # CLUSTERING---
clusterBtn = Button(menuBarFrame, text='Cluster', width=40, command=showClusterOpt)
clusterBtn.grid(row=4, column=0)

clusterFrame = Frame(menuBarFrame, highlightbackground='#aaa', highlightthickness=2, bd=10)

clusterPointsCountLabel = Label(clusterFrame, text='# points')
clusterPointsCountScale = Scale(clusterFrame, from_=1, to=30, orient=HORIZONTAL, length=200, variable=clusterPointsCount)
clusterRadiusLabel = Label(clusterFrame, text='Radius')
clusterRadiusScale = Scale(clusterFrame, from_=0, to=3, resolution=0.1, orient=HORIZONTAL, length=200, variable=clusterRadius)
clusterBtnFrame = Frame(clusterFrame, bd=2)

    # BOTTOM LABEL---
tempLabel = Label(root, text='SKRinternationals 2022')
tempLabel.grid(row=2, column=0)

    # EXPORT---
exportBtn = Button(root, text='Export', command=exportPoints, padx=150, bg='#0078d7', fg='white')
exportBtn.grid(row=2, column=1)

mainloop()
