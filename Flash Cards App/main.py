from functools import partial
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from settings import *
import random
import csv
import sys

root = Tk()
root.title("Flash Cards App")
center_the_project_window(root)
root.config(pady=40, padx=40)
root.configure(bg='#B1DDC6')

DATA_SET = return_question_answer_from_data_set()

# ======================= UI ===========================
CANVAS = Canvas(root, width=625, height=395, bg=CANVAS_BG_COLOR, highlightthickness=0)
flash_card_image = PhotoImage(file="./assets/images/card_front.png")
IMAGE_TAG = CANVAS.create_image(230, 140, image=flash_card_image)
CANVAS.grid(column=0, row=0, columnspan=2)
TITLE = CANVAS.create_text(290, 100, text="Italian", fill="black", font=(FONT_NAME, 30, "bold"))
QA = CANVAS.create_text(300, 210, text="Question", fill="black", font=(FONT_NAME, 55, "bold"))

false_image = PhotoImage(file="./assets/images/wrong.png")
show_next_question_if_false = partial(show_next_question_if_false, root)
false_btn = Button(image=false_image, command=show_next_question_if_false)
false_btn.grid(row=1, column=0)

right_image = PhotoImage(file="./assets/images/right.png")
proceed_to_next_question = partial(proceed_to_next_question, root)
right_btn = Button(image=right_image, command=proceed_to_next_question)
right_btn.grid(row=1, column=1)

show_next_question(root)
count_down(root)

root.mainloop()
