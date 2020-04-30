# import libraries
from appJar import gui

# handle button events
def pressButton(button):
    if button == "Update":
        distance = app.getEntry("Dimension")
        app.clearCanvas("Canvas1")
        limits = app.addCanvasRectangle("Canvas1", x=0, y=0, w=260, h=260)
        rect = app.addCanvasRectangle("Canvas1", x=130-distance, y=130-distance, w=distance*2, h=distance*2)
    if button == "Point":
        x = app.getEntry("x")
        y = app.getEntry("y")
        point = app.addCanvasCircle("Canvas1", x, y, 5, fill='red')
        
distance = 50;

#Create a GUI variable called app
app = gui("Smart Notes",useTtk=True)

# add and configure widgets in the GUI
app.addLabel("title", "Welcome to canvas!")
app.addCanvas("Canvas1")
limits = app.addCanvasRectangle("Canvas1", x=0, y=0, w=260, h=260)
rect = app.addCanvasRectangle("Canvas1", x=130-distance/2, y=130-distance/2, w=distance, h=distance)
app.addNumericEntry("Dimension")
app.addNumericEntry("x")
app.addNumericEntry("y")
app.addButtons(["Update", "Point"], pressButton)

# start the GUI
app.go()