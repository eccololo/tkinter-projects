from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


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


