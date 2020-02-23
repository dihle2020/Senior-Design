# import the library
from appJar import gui

from PIL import Image, ImageTk
# handle button events

# define functionalit
def press(button):
    app.stop()



#functionality for clicking the train button
def launch(btn):    
    #open new window to indicate training session in progress
    app.startSubWindow("Demo",modal=True)
    app.emptyCurrentContainer()
    app.setSize("400x400")
    #load the training inputs into variables
    homeTeam = app.getEntry("Home Team" )
    homeScore = int(app.getEntry("Home Score"))
    awayTeam = app.getEntry("Away Team")
    awayScore = app.getEntry("Away Score")
    quarter = app.getEntry("Quarter")
    timeRemaining = app.getEntry("Time Remaining")

    
    app.addLabel("Home Score ", "Home Score: " + str(homeScore)) 
    
    app.addLabel("Away Score ", "Away Score: " + str(awayScore)) 
    app.addLabel("Live Quarter", "Quarter: " + str(quarter)) 
    app.showSubWindow("Demo", hide=False)
    app.stopSubWindow() 



# create a GUI variable called app
app = gui("Scenario Customization", "600x500  ")
app.setBg("grey")
app.setFont(18)



# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to BuzzerBeater Live")
app.setLabelBg("title", "red")


photo = ImageTk.PhotoImage(Image.open("buzzerBeater.jpg"))
app.addImageData("pic", photo, fmt="PhotoImage")


app.addLabelEntry("Home Team")
app.addLabelEntry("Away Team")
app.setLabelBg("Home Team", "red")
app.setLabelBg("Away Team", "blue")

app.addLabelEntry("Home Score")
app.addLabelEntry("Away Score")
app.setLabelBg("Home Score", "red")
app.setLabelBg("Away Score", "blue")


app.addLabelEntry("Time Remaining")
app.setLabelBg("Time Remaining", "white")

app.addLabelEntry("Quarter")
app.setLabelBg("Quarter", "white")

app.addLabelOptionBox("Crowd Capacity", ["Poor Crowd", "Average Crowd", "Good Turnout","Big Game Turnout", "Championship Game"])
app.setLabelBg("Crowd Capacity", "white")




# link the buttons to the function called press
app.addButton("Cancel", press)
app.addButton("Train", launch)


# start the GUI
app.go()
