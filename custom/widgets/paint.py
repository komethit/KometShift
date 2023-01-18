from tkinter import *
import tkinter.ttk as ttk
from tkinter import colorchooser

class PaintWidget(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.brush_color = "black"
        self.my_canvas = Canvas(self, width=440, height=220, bg="white")
        self.my_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        self.my_canvas.bind('<B1-Motion>', self.paint)

        self.brush_options_frame = Frame(self)
        self.brush_options_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.brush_size_frame = LabelFrame(self.brush_options_frame, text="Brush Size")
        self.brush_size_frame.grid(row=0, column=0)
        self.my_slider = ttk.Scale(self.brush_size_frame, from_=1, to=100, command=self.change_brush_size, orient=VERTICAL, value=10)
        self.my_slider.grid(row=0, column=0)
        self.slider_label = Label(self.brush_size_frame, text=self.my_slider.get())
        self.slider_label.grid(row=1, column=0)
        self.brush_type_frame = LabelFrame(self.brush_options_frame, text="Brush Type", height=400)
        self.brush_type_frame.grid(row=1, column=0)

        self.brush_type = StringVar()
        self.brush_type.set("round")

        self.brush_type_radio1 = Radiobutton(self.brush_type_frame, text="Round", variable=self.brush_type, value="round")
        self.brush_type_radio2 = Radiobutton(self.brush_type_frame, text="Slash", variable=self.brush_type, value="butt")
        self.brush_type_radio3 = Radiobutton(self.brush_type_frame, text="Diamond", variable=self.brush_type, value="projecting")
        self. brush_type_radio1.grid(row=0, column=0)
        self.brush_type_radio2.grid(row=1, column=0)
        self.brush_type_radio3.grid(row=2, column=0)

        self.change_colors_frame = LabelFrame(self.brush_options_frame, text="Change Colors")
        self.change_colors_frame.grid(row=2, column=0)
        self.brush_color_button = Button(self.change_colors_frame, text="Brush Color", command=self.change_brush_color)
        self.brush_color_button.grid(row=0, column=0)
        self.canvas_color_button = Button(self.change_colors_frame, text="Canvas Color", command=self.change_canvas_color)
        self.canvas_color_button.grid(row=1, column=0)

        self.options_frame = LabelFrame(self.brush_options_frame, text="Program Options")
        self.options_frame.grid(row=3, column=0)
        self.clear_button = Button(self.options_frame, text="Clear Screen", command=self.clear_screen)
        self.clear_button.grid(row=0, column=0)

    def paint(self, e):
        brush_width = '%0.0f' %  float(self.my_slider.get())
        brush_type2 = self.brush_type.get()
        x1 = e.x - 1
        y1 = e.y - 1
        x2 = e.x + 1
        y2 = e.y + 1
        self.my_canvas.create_line(x1, y1, x2, y2, fill=self.brush_color, width=brush_width, capstyle=brush_type2, smooth=True)

    def change_brush_size(self, thing):
        self.slider_label.config(text='%0.0f' %  float(self.my_slider.get()))

    def change_brush_color(self):
        brush_color = "black"
        brush_color = colorchooser.askcolor(color=brush_color)[1]
    
    def change_canvas_color(self):
        bg_color = "black"
        bg_color = colorchooser.askcolor(color=bg_color)[1]
        self.my_canvas.config(bg=bg_color)

    def clear_screen(self):
        self.my_canvas.delete(ALL)
        self.my_canvas.config(bg="white")