from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizEasyModeInterface
from ui import QuizModeInterface
from ui import QuizHardModeInterface
import settings

# quiz_mode = QuizModeInterface()

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    if settings.MODE == "hard":
        question_false_answers = question["incorrect_answers"]
        new_question = Question(question_text, question_answer, question_false_answers)
    else:
        new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz = QuizBrain(question_bank)
quiz_hard_ui = QuizHardModeInterface(quiz)
# if settings.MODE == "easy":
#     quiz_easy_ui = QuizEasyModeInterface(quiz)
# else:
#     quiz_hard_ui = QuizHardModeInterface(quiz)

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
