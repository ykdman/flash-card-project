from tkinter import *
import pandas as pd
import random

to_learn = {}

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
# ----- french_word Read ----
try:
    french_words_data = pd.read_csv("data/word_to_lean.csv")
except FileNotFoundError:
    orginal_data = pd.read_csv("data/french_words.csv")
    to_learn = orginal_data.to_dict(orient="records")
else:
    to_learn = french_words_data.to_dict(orient="records")

# ---------------------------card motion ---------

# ----- next card excute ----
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# ----- flip card method -----
def flip_card():

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# ----- is known -----
def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/word_to_lean.csv", index=False)
    next_card()


# ----- Basic Window Setting ------
window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# ----- Call Canvas -----
canvas = Canvas(width=800, height=526)


# ----- card front img setting-----
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# text setting
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

# ----- Button Setting -----

# Unknown Button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=next_card)
unknown_button.config(highlightthickness=0)
unknown_button.grid(row=1, column=0)

# Check Button
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.config(highlightthickness=0,)
known_button.grid(row=1, column=1)

next_card()  # 첫화면 부터 글자가 나오게
window.mainloop()
