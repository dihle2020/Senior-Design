import tkinter as tk
from tkinter.filedialog import askopenfilename



#global filename 
# defining open_file_chooser function
def open_file_chooser():
    filename = askopenfilename()
    child = tk.Tk()
    child.geometry("500x200")
    child.title("Video Classifer")
    label = tk.Label(child, fg="dark green")
    label.pack()
    label.config(text=str(filename))
    label2 = tk.Label(child, fg="dark blue",font=("Helvetica", 32))
    label2.pack()
    label2.config(text=str("Results:"))
    # code goes here
    label2.config(text=str("Results:"))



# creating an instance of Tk
root = tk.Tk()
root.geometry("300x100")
root.title("Video Classifer")


# Button : Open
open = tk.Button(root, text = "Open and Train", command = open_file_chooser)
open.pack()
label = tk.Label(root, fg="dark green")
label.pack()
label.config(text=str("Please choose a file."))

# Starting the Application
root.mainloop()