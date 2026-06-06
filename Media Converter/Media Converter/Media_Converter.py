import tkinter as tk
import os 
from tkinter import messagebox
from tkinter.filedialog import askopenfile, askopenfilename, askdirectory
from pydub import AudioSegment
from time import sleep

class theGUI:

    def __init__(self):
        #initialisation
        self.root = tk.Tk()
        self.root.geometry("1920x1080")
        self.root.title("Media Converter")
        self.root.configure(bg = "#202024")

        #checking conditions
        self.fileClearToGo = False
        self.directoryClearToGo = False

        #Determine conversion's master
        self.convertMaster = None
        self.convertType = ""

        #for file and directory paths
        self.filePath = ""
        self.directoryPath = ""

        #creating the GUI
        self.canvas = tk.Canvas(self.root, width = 1920, height = 1080, bg = "#202024", highlightthickness=0)
        self.canvas.pack(padx = 10, pady = 10)

        #background rectangle
        self.canvas.create_rectangle(
            0, 100, 1920, 1080,
            fill="#18181b",
            outline = "black"
        )

        #input rectangle
        self.canvas.create_rectangle(
            150, 150, 1770, 350,
            fill = "#202024",
            outline = "white"
        )

        #the big text
        self.canvas.create_text(
            960, 50,
            text="--MEDIA CONVERTER--",
            fill="white",
            font=("Arial", 50, "bold")
        )

        #the TO text
        self.canvas.create_text(
            960, 250,
            text = "TO",
            fill = "white",
            font = ("Arial", 35)
        )

        #confirm button
        self.confirm = tk.Button(
            self.root, 
            width = 20, 
            height = 2, 
            bg = "#90fc03",
            relief = "solid",
            bd = 2,
            text = "Confirm", 
            font = ("Arial", 20, "bold"),
            fg = "white",
            command = self.confirmPressed
         )
        self.canvas.create_window(960, 355, window = self.confirm)

        #the options
        self.optionOne = tk.Entry(
            self.root, 
            width = 10,
            bg = "#202024",
            font = ("Arial", 40),
            fg = "white"
        )
        self.optionTwo = tk.Entry(
            self.root, 
            width = 10,
            bg = "#202024",
            font = ("Arial", 40),
            fg = "white"
        )

        self.canvas.create_window(550, 250, window = self.optionOne)
        self.canvas.create_window(1370, 250, window = self.optionTwo)

        #background rectangle two
        self.canvas.create_rectangle(
            30, 425, 1870, 980,
            fill = "#202024",
            outline = "white"
        )

        self.root.mainloop()

    def confirmPressed(self):
        if self.optionOne.get().lower() == "mp4" and self.optionTwo.get().lower() == "mp3":
            self.mp4ToMp3()
        else:
            messagebox.showerror(title = "Error!!!!!!", message = "You did something wrong bozo")

    def mp4ToMp3(self):
        #sets up frame
        self.mp4Frame = tk.Frame(self.canvas, bg="#202024")
        self.canvas.create_window(950, 700, window=self.mp4Frame)
        self.mp4Frame.columnconfigure(2, minsize=1080)

        #mp4 label
        tk.Label(
            self.mp4Frame,
            text="mp4: ",
            fg ="white",
            bg="#202024",
            font=("Arial", 30)
        ).grid(row=0, column=0, padx=10)

        #Select files button
        self.selectFiles = tk.Button(
            self.mp4Frame,
            width=20,
            height=1,
            bg="#90fc03",
            relief="solid",
            bd=2,
            text="Select file",
            font=("Arial", 20, "bold"),
            fg="white",
            command=lambda: self.selectFile("mp4")
        )

        self.selectFiles.grid(row=0, column=1, padx=10)

        #mp3 label
        tk.Label(
            self.mp4Frame,
            text="mp3 name: ",
            fg ="white",
            bg="#202024",
            font=("Arial", 30)
        ).grid(row=1, column=0, padx=10)

        #entering mp3 name
        self.mp3Name = tk.Entry(
            self.mp4Frame, 
            width = 20,
            bg = "#202024",
            font = ("Arial", 30),
            fg = "white"
        )

        self.mp3Name.grid(row=1, column=1, pady=(20, 0))

        #text for location of file
        tk.Label(
            self.mp4Frame,
            text = "Destination: ",
            fg = "white",
            bg="#202024",
            font=("Arial", 30)
        ).grid(row=2, column=0, padx=10)

        #button for the location of file
        self.selectDirectory = tk.Button(
            self.mp4Frame,
            width=20,
            height=1,
            bg="#90fc03",
            relief="solid",
            bd=2,
            text="Select directory",
            font=("Arial", 20, "bold"),
            fg="white",
            command=lambda:self.selectFile("location")
        )

        self.selectDirectory.grid(row=2, column=1, padx=10, pady=(20, 0))

        #convert button 
        self.convertMP4 = self.createConversionButton("mp4")
        self.convertMP4.grid(row=5, column=0, columnspan=3, padx=0, pady=(70,0), sticky="")

    def createConversionButton(self, type):
        if type == "mp4":
            self.convertMaster = self.mp4Frame
            self.convertType = "mp4"
        return tk.Button(
            self.convertMaster,
            width = 50,
            height = 3,
            bg="#90fc03",
            relief="solid",
            bd=2,
            text="Converttttttttttt",
            font=("Arial", 20, "bold"),
            fg="white",
            command = self.convert
        )

    #add processing text bum
    def createProcessingLabel(self):
        return tk.Label(
            self.convertMaster,
            text = "Processing...",
            fg = "white",
            bg="#202024",
            font=("Arial", 50)
        )

    def selectFile(self, type):
        if type == "mp4":
            if hasattr(self, "mp4Path"):
                self.mp4Path.destroy()
            self.filePath = askopenfilename()
            #filename[:-3] didn't work for some reason. idk if I'm just being dumb or not but this will do
            if self.filePath[len(self.filePath) - 3:len(self.filePath)] == "mp4":
                self.mp4Path = tk.Label(
                    self.mp4Frame,
                    text = self.filePath,
                    fg = "white",
                    bg = "#202024",
                    font = ("Arial", 10)
                )
                self.fileClearToGo = True
            elif self.filePath == "":
                self.mp4Path = tk.Label(
                    self.mp4Frame,
                    text = "Input something.",
                    fg = "red",
                    bg = "#202024",
                    font = ("Arial", 10)
                )
                self.fileClearToGo = False
            else:
                self.mp4Path = tk.Label(
                    self.mp4Frame,
                    text = "That's not a mp4 file. Try again.",
                    fg = "red",
                    bg = "#202024",
                    font = ("Arial", 10)
                )
                self.fileClearToGo = False
            self.mp4Path.grid(row=0, column=2)
        else:
            if hasattr(self, "directoryPathText"):
                self.directoryPathText.destroy()
            self.directoryPath = askdirectory()
            if self.directoryPath != "":
                self.directoryPathText = tk.Label(
                    self.mp4Frame,
                    text = self.directoryPath,
                    fg = "white",
                    bg = "#202024",
                    font = ("Arial", 10)
                )
                self.directoryClearToGo = True
            else:
                self.directoryPathText = tk.Label(
                    self.mp4Frame,
                    text = "Input something.",
                    fg = "red",
                    bg = "#202024",
                    font = ("Arial", 10)
                )
                self.directoryClearToGo = False
            self.directoryPathText.grid(row=2, column=2)

    def convert(self):
        self.convertMP4.destroy()
        self.processingText = self.createProcessingLabel()
        self.processingText.grid(row=5, column=0, columnspan=3, padx=0, pady=(70,0), sticky="")

        if self.convertType == "mp4":
            if self.fileClearToGo and self.directoryClearToGo and self.mp3Name.get() != "":
                self.video = self.filePath
                self.directory = self.directoryPath
                self.audioName = self.mp3Name.get()
                self.outputFile = os.path.join(self.directory, self.audioName + ".mp3")

                #the actual conversion
                self.audio = AudioSegment.from_file(self.video, format="mp4")
                self.audio.export(self.outputFile, format="mp3")
                messagebox.showinfo(title = "Success!!!!", message = "MP4 - MP3 conversion complete!")

                #reset
                self.processingText.destroy()
                self.convertMP4 = self.createConversionButton("mp4")
                self.convertMP4.grid(row=5, column=0, columnspan=3, padx=0, pady=(70,0), sticky="")
                self.directoryPathText.destroy()
                self.mp4Path.destroy()
                self.directoryPath = None
                self.filePath = None
                self.fileClearToGo = False
                self.directoryClearToGo = False
            else:
                messagebox.showerror(title = "Error!!!!!", message = "Information missing. Go and see what you did.")

theGUI()

# #removes quotation because i'm lazyyyyy
# def removequotation(string):
#     return string.replace('"', "")

# # function to... says it in the name
# def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
#     audio = audiosegment.from_file(mp4_file_path, format="mp4")
    
#     audio.export(mp3_file_path, format="mp3")
    
#     print(f"converted '{mp4_file_path}' to '{mp3_file_path}' successfully.")

# # get user input for the mp4 file path and the desired mp3 file name
# video = input("enter the path of the mp4 file you want to convert: ")
# newvideo = removequotation(video)

# audioname = input("enter the name of the output mp3 file (without extension): ")
# outputfile = os.path.join(download, audioname + ".mp3")

# convert_mp4_to_mp3(newvideo, outputfile)

