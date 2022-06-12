from tkinter import *

root = Tk()

root.title('grapy')

if __name__ == '__main__':
    graph = Canvas(root, bg = 'white', bd = 2)
    graph.grid(row = 0, column = 1)

    exportBtn = Button(root, text = 'Export')
    exportBtn.grid(row = 1, column = 0)

    mainloop()