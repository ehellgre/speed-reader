import tkinter as tk
import PyPDF2
import time
import threading

# read text from pdf file and return it as words
def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in (reader.pages):
            text += page.extract_text()
        return text.split()
    
# class to control the reading + words display
class SpeedReader:
    def __init__(self, root, words):
        self.root = root
        self.words = words
        self.label = tk.Label(root, text='', font=('Helvetica', 18))
        self.label.pack()
        self.speed = 200 # default speed 200 words / min
        self.running = False # control flag

    # func for starting the reading
    def start(self):
        self.running = True
        threading.Thread(target=self.display_words).start()

    # func for stopping the reading
    def stop(self):
        self.running = False

    # func for updating the displayed words at the wanted speed
    def display_words(self):
        for word in self.words:
            if not self.running:
                break
            self.label.config(text=word)
            time.sleep(60 / self.speed) # calculate delay based on words per minute
            self.root.update() # update the gui with new word

    # func for adjusting reading speed
    def set_speed(self, speed):
        self.speed = speed

# set up the gui
def main():
    root = tk.Tk()
    root.title('Speed Reader')

    words = read_pdf_file('rikosoikeudenyleinenosa.pdf')
    reader = SpeedReader(root, words)

    # setting up gui controls aka start/stop btns + speed
    start_btn = tk.Button(root, text='START', command=reader.start)
    stop_btn = tk.Button(root, text='STOP', command=reader.stop)
    read_speed = tk.Scale(root, from_=100, to=250, orient='horizontal', label='Speed', command=lambda v: reader.set_speed(int(v)))

    start_btn.pack()
    stop_btn.pack()
    read_speed.pack()

    root.mainloop()

# entry
if __name__ == '__main__':
    main()
