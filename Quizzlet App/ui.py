from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from quiz_brain import QuizBrain
import settings
import random

THEME_COLOR = "#375362"


class QuizModeInterface:

    def __init__(self):
        self.root = Tk()
        self.root.title("Choose Mode")
        self.root.config(pady=20, padx=20, bg=THEME_COLOR)
        self.root.geometry("230x100")

        self.true_btn = Button(text="Ease Mode",
                               width=30,
                               cursor="hand2",
                               command=self.set_easy_mode)
        self.true_btn.grid(row=0, column=0)

        self.false_btn = Button(text="Hard Mode",
                                width=30,
                                cursor="hand2",
                                command=self.set_hard_mode)
        self.false_btn.grid(row=1, column=0, pady=5)

        self.root.mainloop()

    def set_hard_mode(self):
        settings.MODE = "hard"
        settings.API_DATA_TYPE = "multiple"
        settings.API_DATA_AMOUNT = 50
        self.root.destroy()

    def set_easy_mode(self):
        settings.MODE = "easy"
        settings.API_DATA_TYPE = "boolean"
        settings.API_DATA_AMOUNT = 20
        self.root.destroy()


class QuizEasyModeInterface:

    def __init__(self, quiz_brain: QuizBrain):

        self.quiz = quiz_brain

        self.root = Tk()
        self.root.title("Quizzlet")
        self.root.config(pady=20, padx=20, bg=THEME_COLOR)
        self.root.geometry("400x500")

        self.score_label = Label(self.root, text="Score: 0", background=THEME_COLOR,
                                 font=("Arial", 12, "bold"), foreground="white")
        self.score_label.grid(row=0, column=1, sticky='E', pady=10)

        self.question_canvas = Canvas(width=360, height=250, bg="white", highlightthickness=0)
        self.question_text = self.question_canvas.create_text(180,
                                                              110,
                                                              text="Question 1",
                                                              fill="black",
                                                              font=("Arial", 18, "italic"),
                                                              width=300)
        self.question_canvas.grid(row=1, column=0, columnspan=2, pady=5)

        self.true_btn_img = PhotoImage(file="./images/true.png")
        self.true_btn = Button(text="True", width=13, image=self.true_btn_img,
                               cursor="hand2", command=self.check_answer_true)
        self.true_btn.grid(row=2, column=0, pady=25)

        self.false_btn_img = PhotoImage(file="./images/false.png")
        self.false_btn = Button(text="False", width=13, image=self.false_btn_img,
                                cursor="hand2", command=self.check_answer_false)
        self.false_btn.grid(row=2, column=1, pady=25)

        self.show_next_question()

        self.root.mainloop()

    def show_next_question(self):
        self.question_canvas.configure(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.question_canvas.itemconfig(self.question_text, text=q_text)
        else:
            end_text = "There is no more questions. Congratulations!"
            self.question_canvas.itemconfig(self.question_text, text=end_text)
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def check_answer_true(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def check_answer_false(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        self.root.after(1000, self.show_next_question)
        if is_right:
            self.question_canvas.configure(bg="green")
        else:
            self.question_canvas.configure(bg="red")


class QuizHardModeInterface:

    def __init__(self, quiz_brain: QuizBrain):

        self.quiz = quiz_brain
        self.incorrect_answers = self.quiz.incorrect_answers
        self.correct_answer = self.quiz.correct_answer

        self.root = Tk()
        self.root.title("Quizzlet")
        self.root.config(pady=20, padx=20, bg=THEME_COLOR)
        self.root.geometry("660x400")

        self.score_label = Label(self.root, text="Score: 0", background=THEME_COLOR,
                                 font=("Arial", 12, "bold"), foreground="white")
        self.score_label.grid(row=0, column=2, sticky='E', pady=10)

        self.question_canvas = Canvas(width=360, height=250, bg="white", highlightthickness=0)
        self.question_text = self.question_canvas.create_text(180,
                                                              110,
                                                              text="Question 1",
                                                              fill="black",
                                                              font=("Arial", 18, "italic"),
                                                              width=300)
        self.question_canvas.grid(row=1, column=1, columnspan=2, pady=5)

        self.one_btn = Button(text="1", width=20,
                               cursor="hand2")
        self.one_btn.grid(row=2, column=0, pady=25)

        self.two_btn = Button(text="2", width=20,
                                cursor="hand2")
        self.two_btn.grid(row=2, column=1, pady=25)

        self.three_btn = Button(text="3", width=20,
                                cursor="hand2")
        self.three_btn.grid(row=2, column=2, pady=25)

        self.four_btn = Button(text="2", width=20,
                              cursor="hand2")
        self.four_btn.grid(row=2, column=4, pady=25)

        self.shuffle_and_show_answers()
        self.show_next_question()

        self.root.mainloop()

    def show_next_question(self):
        self.question_canvas.configure(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.question_canvas.itemconfig(self.question_text, text=q_text)
        else:
            end_text = "There is no more questions. Congratulations!"
            self.question_canvas.itemconfig(self.question_text, text=end_text)
            self.one_btn.config(state="disabled")
            self.two_btn.config(state="disabled")
            self.three_btn.config(state="disabled")
            self.four_btn.config(state="disabled")

    def check_answer_true(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def check_answer_false(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        self.root.after(1000, self.show_next_question)
        if is_right:
            self.question_canvas.configure(bg="green")
        else:
            self.question_canvas.configure(bg="red")

    def shuffle_and_show_answers(self):
        answer_btn_list = [self.one_btn, self.two_btn, self.three_btn, self.four_btn]
        random.shuffle(answer_btn_list)
        answers_txt_list = [self.correct_answer].extend(self.incorrect_answers)

        for idx, item in enumerate(answer_btn_list):
            item.config(text=answers_txt_list[idx])

