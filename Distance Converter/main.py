from tkinter import *
from tkinter.ttk import Label, Button, Entry

SWITCH_FLAG = False
MILES_KM_RATIO = 1.609
KM_MILES_RATIO = 0.621


def miles_to_km_convert():
    user_input = float(entry.get())
    output_txt = 0
    if user_input < 0:
        output_label["text"] = "Error: Number < 0"
    else:
        if not SWITCH_FLAG:
            output_txt = round(user_input * MILES_KM_RATIO, 2)
        else:
            output_txt = round(user_input * KM_MILES_RATIO, 2)

    output_label["text"] = output_txt


def switch():
    global SWITCH_FLAG
    if not SWITCH_FLAG:
        SWITCH_FLAG = True
        label_2["text"] = "km"
        label_3["text"] = "miles"
        temp = output_label.cget("text")
        output_label["text"] = entry.get()
        entry.delete(0, END)
        entry.insert(0, temp)

    else:
        SWITCH_FLAG = False
        label_2["text"] = "miles"
        label_3["text"] = "km"
        temp = output_label.cget("text")
        output_label["text"] = entry.get()
        entry.delete(0, END)
        entry.insert(0, temp)


root = Tk()
root.title("Distance Converter.")
root.minsize(height=200, width=350)
root.config(padx=25, pady=25)

switch_btn_img = PhotoImage(file='../assets/images/switch_icon_60x20.png')
switch_btn = Button(root, image=switch_btn_img, command=switch)
switch_btn.grid(column=0, row=0)

label_1 = Label(root, text="is equal to", font=("Arial", 14))
label_1.grid(row=1, column=0)
label_1.config(padding=10)

entry = Entry(width=20)
entry.insert(0, "")
entry.grid(column=1, row=0)

output_label = Label(root, text="0", font=("Arial", 14))
output_label.grid(row=1, column=1)
output_label.config(padding=10)

button_calc = Button(text="Calculate", command=miles_to_km_convert)
button_calc.grid(column=1, row=3)

label_2 = Label(root, text="miles", font=("Arial", 14))
label_2.grid(row=0, column=2)
label_2.config(padding=10)

label_3 = Label(root, text="km", font=("Arial", 14))
label_3.grid(row=1, column=2)
label_3.config(padding=10)

root.mainloop()
