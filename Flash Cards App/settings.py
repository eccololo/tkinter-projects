from tkinter import messagebox
import csv
import sys


def return_number_of_questions():
    """This function returns the number of questions from DB file for settings purposes."""
    csvfile = None
    reader = None
    try:
        csvfile = open(DATA_FILE_PATH, "r", encoding='utf-8')
        reader = csv.reader(csvfile, delimiter=',')
    except FileNotFoundError:
        messagebox.showinfo("Error.", "Sorry, but DB file with answers and question was not found.\nContact developer.")
        sys.exit()
    finally:
        counter = len(list(csvfile))
        csvfile.close()
        return counter


DATA_FILE_PATH = "assets/data/300_italian_polish_most_common_words.csv"
DATA_SET = None
FONT_NAME = "Courier"
CANVAS_BG_COLOR = "#74b291"
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 550
TIMER = None
QUESTION_NO = None
QUESTION_NO_MAX = return_number_of_questions()
QUESTION_NO_LIST = list(range(2, QUESTION_NO_MAX))
TITLE = None
QA = None
CANVAS = None
IMAGE_TAG = None
COUNT_DOWN_TIME = 5500
SHOW_NEXT_QUESTION_AFTER = 4000