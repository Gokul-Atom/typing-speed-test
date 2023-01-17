import sys
from random import choice
from tkinter import Tk, Button, Entry, Label, Text, Frame, Scale, Scrollbar, Toplevel
from tkinter import CENTER, DISABLED, E, END, N, NORMAL, S, W, WORD

paragraphs = [
    "Finance is the soul and blood of any business and no firm can survive without finance. It concerns itself with the management of monetary affairs of the firm and how money can be raised on the best terms available.",
    "Proper mental health is essential in every stage of life - from childhood and teenager to adulthood. Throughout a lifetime, an individual can experience mental health issues at any point.",
    "Today Startups are being widely recognized as important engines for growth and job generation. Through innovation and scalable technology, startups can generate impactful solutions, and thereby act as vehicles for socio-economic development and transformation.",
    "Global warming is the latest alarm bell for the earth's environment. Global warming refers to the increase in the average temperature of the earth's surface during the last century.",
    "A cryptocurrency is a virtual or digital currency that is highly secured by cryptography or encryption techniques which makes it nearly impossible to counterfeit such cryptocurrency.",
    "An electric vehicle uses one or more electric motors or traction motors for propulsion. The power of a vehicle's electric motor, as in other vehicles, is measured in kilowatts (kW).",
    "Debit cards eliminate the need to carry cash or physical checks to make purchases, and they can also be used at ATMs to withdraw cash.",
    "Business plays a major role within our society. It is a creative and competitive activity that continuously contributes to the shaping of our society. By satisfying their needs and wants people cannot satisfy themselves."
    "Racism was something that he was acutely aware of as he grew up. Right from the age of six, his friendship with a white boy was taken away when his parents decided that they did not want their son to associate with a black boy.",
    "Born on April 14th, 1891, Bhimrao Ramji Ambedkar was an Indian nationalist, jurist, Dalit leader, and Buddhist revivalist. But most importantly, he was the chief architect of the Indian constitution.",
    "Born into a Jewish family on 14th March 1879 in Germany, Einstein had early speech difficulties, still he was a topper at elementary school. His father, Hermann Einstein was a salesman and engineer.",
    "The American entrepreneur, philanthropist, and the Chairman of Microsoft was born on 28th October 1955 into a wealthy Seattle family. As a student, Gates excelled in elementary school, particularly in Mathematics and Sciences.",
    "The Taj Mahal is the materialized vision of love and marks a perfect indelible remark on its Mughal Architecture. This historical monument is the mausoleum of Emperor Shan Jahan's beloved wife, Empress Arjuman Banu Begum, most commonly known as Mumtaz Mahal.",
    "Having a healthy lifestyle is all about choosing to live your life in the healthiest way possible. There are a few things you have to do to start living your life in this way, i.e., the healthy way. This means doing some amount of exercise daily.",
    "Self-confidence is a state of mind where someone pushes their boundaries and encourages belief from the very beginning, and this comes from a place of self-love. You ought to love yourself to gain that freedom from doubting your actions."
]

POSITION_LIST = None
TAG_IDS = 1
TAG_ID = 0
WORDS = []
CORRECT_WORDS = []
INCORRECT_WORDS = []
COUNTDOWN = 60
TIMER = None
WPM = 0
ACCURACY = 0

root = Tk()
root.title("Typing Speed Test")
root.resizable(False, False)

mainframe = Frame(root)
top_frame = Frame(root)
result = Toplevel(root)
result.title("Typing Speed Results")
result.resizable(False, False)


def start_timer():
    global COUNTDOWN, TIMER
    if COUNTDOWN:
        TIMER = root.after(1000, start_timer)
        COUNTDOWN -= 1
        label_timer.config(text=f"Time Left: {COUNTDOWN // 60:02d}:{COUNTDOWN % 60:02d}")
        progress_bar_timer.config(state=NORMAL)
        progress_bar_timer.set(COUNTDOWN)
        progress_bar_timer.config(state=DISABLED)
        calculate_wpm()
        label_wpm.config(text=f"WPM: {WPM} wpm\nAccuracy: {ACCURACY}%")
    else:
        stop_test()


def reset_timer():
    global TIMER, COUNTDOWN
    root.after_cancel(TIMER)
    COUNTDOWN = 60
    label_timer.config(text=f"Time Left: {COUNTDOWN // 60:02d}:{COUNTDOWN % 60:02d}")
    progress_bar_timer.config(state=NORMAL)
    progress_bar_timer.set(COUNTDOWN)
    progress_bar_timer.config(state=DISABLED)


def begin_test(*args):
    global TAG_ID, CORRECT_WORDS, INCORRECT_WORDS, WPM, ACCURACY
    for tag in range(TAG_ID):
        text_typing_content.tag_config(tag, background="white", foreground="black")
    TAG_ID = 0
    CORRECT_WORDS, INCORRECT_WORDS = [], []
    WPM, ACCURACY = 0, 0
    text_typing_content.config(state=NORMAL)
    text_typing_content.delete(1.0, END)
    text_typing_content.insert(END, choice(paragraphs))
    text_typing_content.config(state=DISABLED)
    get_spaces()
    highlight()
    entry_typed_text.focus()
    entry_typed_text.config(state=NORMAL)
    if TIMER:
        reset_timer()
    start_timer()
    button_begin_test.config(text="Restart Test", width=20)
    button_begin_test.grid_configure(columnspan=1, sticky=E)
    button_stop_test.grid(row=1, column=1, pady=(20, 0), sticky=W)
    label_correct_words.config(text=f"Correct Words: {len(CORRECT_WORDS)}")
    label_incorrect_words.config(text=f"Incorrect Words: {len(INCORRECT_WORDS)}")


def stop_test(*args):
    global COUNTDOWN
    show_result()
    reset_timer()
    entry_typed_text.config(state=DISABLED)
    COUNTDOWN = 60
    button_begin_test.config(text="Start Test", width=40)
    button_begin_test.grid_configure(columnspan=2, sticky=N)
    button_stop_test.grid_forget()
    text_typing_content.config(state=NORMAL)
    text_typing_content.delete(1.0, END)
    text_typing_content.insert(END, 'Press "Enter" or Click "Begin Test" to Begin Test.')
    text_typing_content.config(state=DISABLED)


def evaluate(*args):
    global TAG_ID
    if 0 <= TAG_ID <= TAG_IDS:
        typed_text = entry_typed_text.get().strip()
        correct_word = WORDS[TAG_ID - 1]
        if typed_text == correct_word:
            CORRECT_WORDS.append(typed_text)
            highlight()
        else:
            word = {"correct word": correct_word,
                    "typed text": typed_text}
            INCORRECT_WORDS.append(word)
            highlight(correct=False)
        entry_typed_text.delete(0, END)

    label_correct_words.config(text=f"Correct Words: {len(CORRECT_WORDS)}")
    label_incorrect_words.config(text=f"Incorrect Words: {len(INCORRECT_WORDS)}")

    if TAG_ID > TAG_IDS:
        text_typing_content.focus()
        entry_typed_text.config(state=DISABLED)
        stop_test()


def get_spaces():
    global POSITION_LIST, TAG_IDS, WORDS
    TAG_IDS = 0
    line_number = 1
    POSITION_LIST = []
    WORDS.clear()
    line_list = text_typing_content.get(1.0, END).split("\n")
    for line in line_list:
        position = 0
        length = len(line)
        if length:
            individual_list = [f"{line_number}.-1"]
            WORDS.append(line.split(" "))
            while True:
                position = line.find(" ", position)
                if position >= 0:
                    individual_list.append(f"{line_number}.{position}")
                    position += 1
                else:
                    individual_list.append(f"{line_number}.{length}")
                    POSITION_LIST.append(individual_list)
                    break
        line_number += 1

    WORDS = sum(WORDS, [])

    for i in POSITION_LIST:
        for tag in range(len(i[:-1])):
            start_position = f'{i[tag].split(".")[0]}.{int(i[tag].split(".")[1]) + 1}'
            end_position = f'{i[tag + 1].split(".")[0]}.{int(i[tag + 1].split(".")[1])}'
            text_typing_content.tag_add(TAG_IDS, start_position, end_position)
            TAG_IDS += 1


def highlight(*args, correct: bool = True):
    global TAG_ID
    text_typing_content.tag_config(TAG_ID, background="green", foreground="white")
    if correct:
        text_typing_content.tag_config(TAG_ID - 1, background="white", foreground="black")
    else:
        text_typing_content.tag_config(TAG_ID - 1, background="red", foreground="white")
    if TAG_ID + 3 < TAG_IDS:
        text_typing_content.yview_pickplace(text_typing_content.tag_ranges(TAG_ID + 3)[0])
    TAG_ID += 1


def calculate_wpm():
    global WPM, ACCURACY
    characters = sum([len(word) for word in CORRECT_WORDS]) + len(CORRECT_WORDS)
    incorrect_characters = sum([len(word) for word in INCORRECT_WORDS]) + len(INCORRECT_WORDS)
    time_in_minute = (60 - COUNTDOWN) / 60
    try:
        WPM = round(characters / 5 / time_in_minute, 2)
        gwpm = round((incorrect_characters + characters) / 5 / time_in_minute, 2)
    except ZeroDivisionError:
        WPM = round(characters / 5, 2)
        gwpm = round((incorrect_characters + characters) / 5, 2)
    if WPM:
        ACCURACY = round(WPM / gwpm * 100, 2)


def show_result():
    result.deiconify()
    result.wm_transient(root)
    result.lift()
    if INCORRECT_WORDS:
        label_info.config(text=f"Congratulations! You 've completed the test in {60 - COUNTDOWN} seconds.\n"
                               f"You 've got {len(CORRECT_WORDS)} words correct out of {len(WORDS)} words.\n\n"
                               f"Your speed is {WPM} words per minute with {ACCURACY}% accuracy.\n\n"
                               f"Now let's see some mistyped words.")
    else:
        label_info.config(text=f"Congratulations! You 've completed the test in {60 - COUNTDOWN} seconds.\n"
                               f"You 've got {len(CORRECT_WORDS)} words correct out of {len(WORDS)} words.\n\n"
                               f"Your speed is {WPM} words per minute with {ACCURACY}% accuracy.\n\n")
    for word in INCORRECT_WORDS:
        text_typed_words.insert(END, f"{word['typed text']}\n")
        text_correct_words.insert(END, f"{word['correct word']}\n")


def scroll_typed_words(*args):
    text_typed_words.yview_moveto(text_correct_words.yview()[0])
    scrollbar_result.set(*args)


def scroll_correct_words(*args):
    text_correct_words.yview_moveto(text_typed_words.yview()[0])
    scrollbar_result.set(*args)


def scroll_both(*args):
    text_typed_words.yview(*args)
    text_correct_words.yview(*args)


button_begin_test = Button(mainframe, text="Begin Test", command=begin_test, font=("Times New Roman", 20, "bold"), width=40)
button_stop_test = Button(mainframe, text="Stop Test", command=stop_test, font=("Times New Roman", 20, "bold"), width=20)

button_okay = Button(result, text="Okay", command=lambda: [result.withdraw(), mainframe.focus()], font=("Times New Roman", 20, "bold"), width=20)

entry_typed_text = Entry(mainframe, font=("", 25), justify=CENTER, width=60, state=DISABLED)

label_timer = Label(top_frame, text=f"Time Left: {COUNTDOWN // 60:02d}:{COUNTDOWN % 60:02d}", font=("", 15))
label_correct_words = Label(top_frame, text=f"Correct Words: {len(CORRECT_WORDS)}", font=("", 14, "bold"))
label_incorrect_words = Label(top_frame, text=f"Incorrect Words: {len(INCORRECT_WORDS)}", font=("", 14, "bold"))
label_wpm = Label(top_frame, text="WPM: 0", font=("", 16, "bold"))

label_result = Label(result, text="Test Results", font=("", 20, "bold"))
label_result_incorrect_words = Label(result, text="Incorrect Words", font=("", 18, "bold"))
label_result_correct_words = Label(result, text="Correct Words", font=("", 14, "bold"))
label_typed_words = Label(result, text="Typed Words", font=("", 14, "bold"))
label_info = Label(result, font=("", 14, "bold"))

progress_bar_timer = Scale(top_frame, from_=0, to=COUNTDOWN, orient="horizontal", width=5, length=600, fg="green",
                           font=("", 14, "bold"))
progress_bar_timer.set(COUNTDOWN)

scrollbar_typing_content = Scrollbar(mainframe, width=20)
scrollbar_result = Scrollbar(result, width=20)

text_typing_content = Text(mainframe, width=70, height=10, wrap=WORD, font=("Calibri", 25))
text_typing_content.insert(END, 'Press "Enter" or Click "Begin Test" to Begin Test.')
text_typing_content.config(state=DISABLED, yscrollcommand=scrollbar_typing_content.set)
scrollbar_typing_content.config(command=text_typing_content.yview)

text_correct_words = Text(result, width=40, height=8, wrap=WORD, font=("Calibri", 14))
text_typed_words = Text(result, width=40, height=8, wrap=WORD, font=("Calibri", 14))
text_correct_words.config(yscrollcommand=scroll_typed_words)
text_typed_words.config(yscrollcommand=scroll_correct_words)
scrollbar_result.config(command=scroll_both)

top_frame.grid(row=0, column=0, columnspan=2)
label_timer.grid(row=0, column=0, columnspan=2)
progress_bar_timer.grid(row=1, column=0, columnspan=2)
label_correct_words.grid(row=2, column=0, sticky=E, padx=20)
label_incorrect_words.grid(row=2, column=1, sticky=W, padx=20)
label_wpm.grid(row=3, column=0, columnspan=2)

mainframe.grid(row=1, column=0, padx=40, pady=10, columnspan=2)
text_typing_content.grid(row=0, column=0, columnspan=2)
scrollbar_typing_content.grid(row=0, column=1, sticky=N + S, columnspan=2)
button_begin_test.grid(row=1, column=0, pady=(20, 0), columnspan=2)
entry_typed_text.grid(row=2, column=0, ipady=20, pady=20, columnspan=2)

label_result.grid(row=0, column=0, columnspan=2, pady=(50, 0))
label_info.grid(row=1, column=0, columnspan=2)
label_result_incorrect_words.grid(row=2, column=0, pady=20, columnspan=2)
label_typed_words.grid(row=3, column=0)
label_result_correct_words.grid(row=3, column=1)
text_typed_words.grid(row=4, column=0, padx=(50, 0))
text_correct_words.grid(row=4, column=1)
scrollbar_result.grid(row=4, column=2, sticky=N + S, padx=(0, 50))

button_okay.grid(row=8, column=0, columnspan=2, pady=50)

root.bind("<Control-q>", sys.exit)
mainframe.bind("<Return>", begin_test)

entry_typed_text.bind("<space>", evaluate)
entry_typed_text.bind("<Escape>", stop_test)

result.bind("<Return>", lambda event: [result.withdraw(), mainframe.focus()])
result.protocol("WM_DELETE_WINDOW", lambda: [result.withdraw(), mainframe.focus()])

result.withdraw()
mainframe.focus()
root.eval("tk::PlaceWindow . center")
root.mainloop()
