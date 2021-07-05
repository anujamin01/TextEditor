import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
class Menubar:
    def __init__(self, parent):
        font_specs = ("Arial", 14)

        menubar = tk.Menu(parent.master, font = font_specs)
        parent.master.config(menu = menubar)

        file_dropdown = tk.Menu(menubar, font = font_specs, tearoff = 0)
        file_dropdown.add_command(label = "New File",
                                  accelerator = "Ctrl+N",
                                  command = parent.new_file)
        file_dropdown.add_command(label="Open File",
                                  accelerator = "Ctrl+O",
                                  command = parent.open_file)
        file_dropdown.add_command(label="Save",
                                  accelerator="Ctrl+S",
                                  command = parent.save)
        file_dropdown.add_command(label="Save As",
                                  accelerator="Ctrl+Shift+S",
                                  command = parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                  command = parent.master.destroy)

        about_dropdown = tk.Menu(menubar,  font = font_specs, tearoff = 0)
        about_dropdown.add_command(label = "Release Notes", command = self.show_release_notes)

        about_dropdown.add_separator()
        about_dropdown.add_command(label = "About", command = self.show_about_message)

        menubar.add_cascade(label = "File", menu = file_dropdown)
        menubar.add_cascade(label = "About", menu = about_dropdown)

    def show_about_message(self):
        box_title = "About Discount Notepad"
        box_message = "A simplified version of notepad written in python 3.7"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "V0.1"
        messagebox.showinfo(box_title, box_message)

class Statusbar:

    def __init__(self, parent):

        font_specs = ("Arial", 12)

        self.status = tk.StringVar()
        self.status.set("Discount Notepad - v0.1")

        label = tk.Label(parent.textArea, textvariable = self.status, fg = "black",
                         bg="lightgrey", anchor = 'sw', font= font_specs)

        label.pack(side = tk.BOTTOM, fill = tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your File Has Been Saved!")
        else:
            self.status.set("Discount Notepad V0.1")


class Notepad:

    def __init__(self, master):
        master.title("Untitled - Discount Notepad")
        master.geometry("900x600")

        font_specs = ("Arial", 18)

        self.master = master
        self.filename = None;

        self.textArea = tk.Text(master, font = font_specs)
        self.scroll = tk.Scrollbar(master, command = self.textArea.yview)
        self.textArea.configure(yscrollcommand = self.scroll.set)
        self.textArea.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.scroll.pack(side = tk.RIGHT, fill = tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.bind_shortcuts()

    def set_window_title(self, name = None):
        if name:
            self.master.title(name + " - Discount Notepad")
        else:
            self.master.title("Untitled - Discount Notepad")

    def new_file(self):
        self.textArea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension = ".txt", filetypes = [("All Files", "*.*"),
                                                    ("Text Files" "*.txt*"),
                                                    ("Python Scripts" "*.py*")])

        if self.filename:
            self.textArea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textArea.insert(1.0, f.read())
            self.set_window_title(self.filename)


    def save(self, *args):
        if self.filename:
            try:
                textArea_content = self.textArea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textArea_content)
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self):
        try:
            new_file = filedialog.askopenfilename(
                defaultextension = ".txt",
                filetypes = [("All Files", "*.*"),
                            ("Text Files" "*.txt*"),
                            ("Python Scripts" "*.py*")])
            textArea_content = self.textArea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textArea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def bind_shortcuts(self):
        self.textArea.bind('<Control-n>', self.new_file)
        self.textArea.bind('<Control-o>', self.open_file)
        self.textArea.bind('<Control-s>', self.save)
        self.textArea.bind('<Control-S>', self.save_as)
        self.textArea.bind('<Key>', self.statusbar.update_status)


if __name__ == "__main__":
    master = tk.Tk()
    pt = Notepad(master)
    master.mainloop()