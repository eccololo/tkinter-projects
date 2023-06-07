# TODO:
#    1. Dodać wykres funkcji używając biblioteki matplotlib


from tkinter import *
from tkinter.ttk import Label, Button, Entry


def calc_equation():
    user_input_a = entry_a.get()
    user_input_b = entry_b.get()
    user_input_c = entry_c.get()

    if user_input_a.isdigit() and user_input_a.isdigit() and user_input_a.isdigit():
        user_input_a = float(user_input_a)
        user_input_b = float(user_input_b)
        user_input_c = float(user_input_c)

        delta = (user_input_b ** 2) - (4 * user_input_a * user_input_c)
        print(delta)

        if delta < 0:
            output["text"] = ""
            label_msg["text"] = "Delta < 0. No solutions."
        elif delta > 0:
            root_1 = round(-user_input_b + (delta ** 0.5) / (2 * user_input_a), 2)
            root_2 = round(-user_input_b - (delta ** 0.5) / (2 * user_input_a), 2)
            output["text"] = f"x1 = {root_1}\nx2 = {root_2}"
            label_msg["text"] = f"Delta > 0. Solutions is {root_1} and {root_2}."
        else:
            root_1 = round(-user_input_b / (2 * user_input_a), 2)
            output["text"] = f"x = {root_1}"
            label_msg["text"] = f"Delta = 0. Solutions is {root_1}."
    else:
        output["text"] = ""
        label_msg["text"] = f"Parameters a, b and c must be digits."


def reset():
    entry_a.delete(0, END)
    entry_a.insert(0, "")
    entry_b.delete(0, END)
    entry_b.insert(0, "")
    entry_c.delete(0, END)
    entry_c.insert(0, "")
    output["text"] = "x = ?"
    label_msg["text"] = "Message:"

root = Tk()
root.title("Quadratic Equation Root.")
root.minsize(height=200, width=350)
root.config(padx=25, pady=25)

label_a = Label(root, text="a =", font=("Arial", 14))
label_a.grid(row=0, column=0)
label_a.config(padding=10)

label_b = Label(root, text="b =", font=("Arial", 14))
label_b.grid(row=1, column=0)
label_b.config(padding=10)

label_b = Label(root, text="c =", font=("Arial", 14))
label_b.grid(row=2, column=0)
label_b.config(padding=10)

entry_a = Entry(width=10)
entry_a.grid(column=1, row=0)

entry_b = Entry(width=10)
entry_b.grid(column=1, row=1)

entry_c = Entry(width=10)
entry_c.grid(column=1, row=2)

output = Label(root, text="x = ?", font=("Arial", 20))
output.grid(row=0, column=2)
output.config(padding=(80, 0))

calc_btn_img = PhotoImage(file='../assets/images/calc_btn_80x80.png')
button_calc = Button(image=calc_btn_img, command=calc_equation)
button_calc.grid(column=2, row=1, rowspan=2, columnspan=2)

label_msg = Label(root, text="Message:", font=("Arial", 14))
label_msg.grid(row=3, column=0, columnspan=3)
label_msg.config(padding=10)

reset_btn = Button(text="Reset", command=reset)
reset_btn.grid(column=0, row=4, columnspan=4)

root.mainloop()
