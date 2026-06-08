from ast import Lambda
import tkinter as tk
import os 
import yt_dlp
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

        #Conversion variables
        self.convertMaster = None
        self.convertType = ""

        #for file and directory paths
        self.filePath = ""
        self.directoryPath = ""

        #colours
        self.lightDark = "#202024"
        self.dark = "#18181b"
        self.green = "#90fc03"

        #creating the GUI
        self.canvas = tk.Canvas(self.root, width = 1920, height = 1080, bg = "#202024", highlightthickness=0)
        self.canvas.pack(padx = 10, pady = 10)

        #background rectangle
        self.canvas.create_rectangle(
            0, 100, 1920, 1080,
            fill=self.dark,
            outline = "black"
        )

        #input rectangle
        self.canvas.create_rectangle(
            150, 150, 1770, 350,
            fill = self.lightDark,
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
            bg = self.green,
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
            bg = self.lightDark,
            font = ("Arial", 40),
            fg = "white"
        )
        self.optionTwo = tk.Entry(
            self.root, 
            width = 10,
            bg = self.lightDark,
            font = ("Arial", 40),
            fg = "white"
        )

        self.canvas.create_window(550, 250, window = self.optionOne)
        self.canvas.create_window(1370, 250, window = self.optionTwo)

        #background rectangle two
        self.canvas.create_rectangle(
            30, 425, 1870, 980,
            fill = self.lightDark,
            outline = "white"
        )

        self.root.mainloop()

    def confirmPressed(self):
        if self.optionOne.get().lower() == "mp4" and self.optionTwo.get().lower() == "mp3":
            self.mp4ToMp3()
        elif self.optionOne.get().lower() == "youtube" and self.optionTwo.get().lower() == "mp3":
            self.youtubeToMp3()
        else:
            messagebox.showerror(title = "Error!!!!!!", message = "You did something wrong bozo")

    def createFirstLabel(self, master, type):
        #the text
        tk.Label(
            master,
            text=type + ": ",
            fg ="white",
            bg=self.lightDark,
            font=("Arial", 30)
        ).grid(row=0, column=0, padx=10)

        if type != "url":
            #Select files button
            self.selectFiles = tk.Button(
                master,
                width=20,
                height=1,
                bg=self.green,
                relief="solid",
                bd=2,
                text="Select file",
                font=("Arial", 20, "bold"),
                fg="white",
                command=lambda: self.selectFile(type, master)
            )

            self.selectFiles.grid(row=0, column=1, padx=10)
        else:
            self.urlBox = tk.Entry(
                master, 
                width = 20,
                bg = self.lightDark,
                font = ("Arial", 30),
                fg = "white"
            )

            self.urlBox.grid(row=0, column=1, padx = 10)

    def createSecondLabel(self, master, type):
        #label
        tk.Label(
            master,
            text=type + " name: ",
            fg ="white",
            bg=self.lightDark,
            font=("Arial", 30)
        ).grid(row=1, column=0, padx=10)

        #entering label name
        self.entryBox = tk.Entry(
            master, 
            width = 20,
            bg = self.lightDark,
            font = ("Arial", 30),
            fg = "white"
        )

        self.entryBox.grid(row=1, column=1, pady=(20, 0))

    def createDirectory(self, master):
        #text for location of file
        tk.Label(
            master,
            text = "Destination: ",
            fg = "white",
            bg=self.lightDark,
            font=("Arial", 30)
        ).grid(row=2, column=0, padx=10)

        #button for the location of file
        self.selectDirectory = tk.Button(
            master,
            width=20,
            height=1,
            bg=self.green,
            relief="solid",
            bd=2,
            text="Select directory",
            font=("Arial", 20, "bold"),
            fg="white",
            command=lambda:self.selectFile("location", master)
        )

        self.selectDirectory.grid(row=2, column=1, padx=10, pady=(20, 0))

    def createConversionButton(self, type, master):
        return tk.Button(
            master,
            width = 50,
            height = 3,
            bg=self.green,
            relief="solid",
            bd=2,
            text="Converttttttttttt",
            font=("Arial", 20, "bold"),
            fg="white",
            command = lambda:self.convert(type)
        )

    def youtubeToMp3(self):
        #sets up frame
        self.youtubeMp3Frame = tk.Frame(self.canvas, bg=self.lightDark)
        self.canvas.create_window(950,650,window=self.youtubeMp3Frame)
        self.youtubeMp3Frame.columnconfigure(2, minsize=1080)

        self.createFirstLabel(self.youtubeMp3Frame, "url")
        self.createSecondLabel(self.youtubeMp3Frame, "mp3")
        self.createDirectory(self.youtubeMp3Frame)

        self.convertYoutubeMP3 = self.createConversionButton("youtubeMP3", self.youtubeMp3Frame)
        self.convertYoutubeMP3.grid(row=5, column=0, columnspan=3, padx=0, pady=(70,0), sticky="")

    def mp4ToMp3(self):
        #sets up frame
        self.mp4Frame = tk.Frame(self.canvas, bg=self.lightDark)
        self.canvas.create_window(950, 700, window=self.mp4Frame)
        self.mp4Frame.columnconfigure(2, minsize=1080)

        self.createFirstLabel(self.mp4Frame, "mp4")
        self.createSecondLabel(self.mp4Frame, "mp3")
        self.createDirectory(self.mp4Frame)

        #convert button 
        self.convertMP4 = self.createConversionButton("mp4", self.mp4Frame)
        self.convertMP4.grid(row=5, column=0, columnspan=3, padx=0, pady=(70,0), sticky="")

    def selectFile(self, type, master):
        if type == "mp4":
            if hasattr(self, "mp4Path"):
                self.mp4Path.destroy()
            self.filePath = askopenfilename()
            if self.filePath[len(self.filePath) - 3:len(self.filePath)] == "mp4":
                self.mp4Path = tk.Label(
                    master,
                    text = self.filePath,
                    fg = "white",
                    bg = self.lightDark,
                    font = ("Arial", 10)
                )
                self.fileClearToGo = True
            elif self.filePath == "":
                self.mp4Path = tk.Label(
                    master,
                    text = "Input something.",
                    fg = "red",
                    bg = self.lightDark,
                    font = ("Arial", 10)
                )
                self.fileClearToGo = False
            else:
                self.mp4Path = tk.Label(
                    master,
                    text = "That's not a mp4 file. Try again.",
                    fg = "red",
                    bg = self.lightDark,
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
                    master,
                    text = self.directoryPath,
                    fg = "white",
                    bg = self.lightDark,
                    font = ("Arial", 10)
                )
                self.directoryClearToGo = True
            else:
                self.directoryPathText = tk.Label(
                    master,
                    text = "Input something.",
                    fg = "red",
                    bg = self.lightDark,
                    font = ("Arial", 10)
                )
                self.directoryClearToGo = False
            self.directoryPathText.grid(row=2, column=2)

    def convert(self, type):
        if type == "mp4":
            if self.fileClearToGo and self.directoryClearToGo and self.entryBox.get() != "":
                self.video = self.filePath
                self.directory = self.directoryPath
                self.audioName = self.entryBox.get()
                self.outputFile = os.path.join(self.directory, self.audioName + ".mp3")

                #the actual conversion
                self.audio = AudioSegment.from_file(self.video, format="mp4")
                self.audio.export(self.outputFile, format="mp3")
                messagebox.showinfo(title = "Success!!!!", message = "MP4 - MP3 conversion complete!")

                #reset
                self.directoryPathText.destroy()
                self.mp4Path.destroy()
                self.directoryPath = None
                self.filePath = None
                self.fileClearToGo = False
                self.directoryClearToGo = False
            else:
                messagebox.showerror(title = "Error!!!!!", message = "Information missing. Go and see what you did.")
        elif type == "youtubeMP3":
            if self.urlBox.get() != "" and self.entryBox.get() != "" and self.directoryClearToGo:
                self.youtubeURl = self.urlBox.get()
                self.directory = self.directoryPath
                self.audioName = self.entryBox.get()
                self.outputFile = os.path.join(self.directory, self.audioName + ".mp3")

                #actual conversion
                self.ydl_opts = {
                    "format" : "bestaudio/best",
                    "outtmpl" : self.outputFile,
                    "noplaylist" : True,
                    "postprocessors" : [{
                        "key" : "FFmpegExtractAudio",
                        "preferredcodec" : "mp3",
                        "preferredquality" : "192"
                    }]
                }
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([self.youtubeURl])
                messagebox.showinfo(title = "Sucess!!!", message = "Youtube - MP3 conversion complete!")

                self.directoryPathText.destroy()
                self.directoryPath = None
                self.directoryClearToGo = False
            else:
                messagebox.showerror(title = "Error!!!!!", message = "Information missing. Go and see what you did.")
theGUI()