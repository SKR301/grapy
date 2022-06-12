from tkinter import *

root = Tk()
root.state('zoomed')
root.title('grapy')

if __name__ == '__main__':
    topBarFrame = Frame(root, bd=5)
    topBarFrame.grid(row=0, column=0)

    graphFrame = Frame(root, bd=5)
    graphFrame.grid(row=1, column=0)

    graph = Canvas(graphFrame, bg='white', bd=2, height=1000, width=1500)
    graph.grid(row=0, column=0)

    menuBarFrame = Frame(root, bd=5)
    menuBarFrame.grid(row=1, column=1)
    
    exportBtn = Button(root, text = 'Export')
    exportBtn.grid(row=2, column=1)

    mainloop()