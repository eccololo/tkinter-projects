from tkinter import *
from tkinter.ttk import *
from playsound import playsound
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#11009E"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 10
WORK_SOUND = "../assets/sounds/notification.mp3"
SHORT_BREAK_SOUND = "../assets/sounds/ping.mp3"
LONG_BREAK_SOUND = "../assets/sounds/ding.mp3"
reps = 1
timer_1 = None
timer_2 = None


def fix_count_numbers(count):
    return "0" + str(count) if count < 10 else count


# ---------------------------- TIMER MECHANISM ------------------------------- #

def count_down(count):
    global reps
    global timer_1
    global timer_2

    count_min = math.floor(count / 60)
    count_second = count % 60
    count_min = fix_count_numbers(count_min)
    count_second = fix_count_numbers(count_second)
    canvas.itemconfigure(timer_text, text=f"{count_min}:{count_second}")
    if count > 0:
        timer_1 = root.after(1000, count_down, count - 1)
    else:
        reps += 1
        timer_2 = root.after(1000, start)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def start():
    global reps
    check_str = checkmark.cget("text")
    if reps % 8 == 0:
        window_focus()
        label_1["text"] = "Break"
        play_sound(LONG_BREAK_SOUND)
        label_1.config(foreground=GREEN)
        count_down(LONG_BREAK_MIN * 60)
    elif reps % 2 == 0:
        label_1["text"] = "Break"
        play_sound(SHORT_BREAK_SOUND)
        label_1.config(foreground=BLUE)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        label_1["text"] = "Work"
        play_sound(WORK_SOUND)
        if len(check_str) >= 4:
            check_str = ""
        else:
            check_str += "✔"
        checkmark["text"] = check_str
        label_1.config(foreground=RED)
        count_down(WORK_MIN * 60)


# ---------------------------- TIMER RESET ------------------------------- #

def reset():
    global reps
    reps = 1
    try:
        root.after_cancel(timer_1)
        root.after_cancel(timer_2)
    except ValueError:
        pass
    label_1["text"] = "Focus"
    canvas.itemconfigure(timer_text, text=f"00:00")
    checkmark["text"] = ""


# ---------------------------- MUSIC SETUP ------------------------------- #

def play_sound(track):
    playsound(track)


# ---------------------------- HELPER FUNC ------------------------------- #

def window_focus():
    root.lift()
    root.attributes("-topmost", True)
    root.focus_force()


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Pomodoro App")
root.config(pady=50, padx=100, bg=YELLOW)

label_1 = Label(text="Timer", font=(FONT_NAME, 25, "bold"), background=YELLOW, foreground=GREEN)
label_1.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

style = Style()
style.configure('Action.TButton', font=(FONT_NAME, 11, 'bold'), foreground=BLUE)

start_btn = Button(text="Start", command=start, style="Action.TButton")
start_btn.grid(row=2, column=0)

start_btn = Button(text="Reset", command=reset, style="Action.TButton")
start_btn.grid(row=2, column=2)

checkmark = Label(font=(FONT_NAME, 25, "bold"), background=YELLOW, foreground=GREEN)
checkmark.grid(row=3, column=1)

root.mainloop()
