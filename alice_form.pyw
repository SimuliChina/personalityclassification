import sys

from tkinter.ttk import Label
from tkinter.ttk import Style
from tkinter.ttk import Button
from tkinter.ttk import Entry
from tkinter.ttk import Radiobutton

from tkinter import Tk
from tkinter import Frame
from tkinter import StringVar
from tkinter import X, E, W, N, S
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import BOTH
from tkinter import Radiobutton
from personality import main
import numpy as np
import csv

# from tkinter import Button
# from tkinter import Entry

BG_COLOR = '#A1DBCD'
BG_COLOR = '#F0F0F0'


class Dialog(Frame):
    def __init__(self, questions):
        self.questions = questions
        self.cbox_labels = [1, 2, 3, 4, 5]

    def show(self):
        self.init_window()
        self.create_widgets()
        self.center_window(800, 600)
        self.pack(fill=BOTH, expand=True)
        self.parent.mainloop()

    def init_window(self):
        self.parent = Tk()
        self.style = Style()
        self.style.theme_use('default')
        self.style.configure('BW.TLabel', background='#F0F0F0')
        self.cbox_vars = [StringVar() for x in self.questions]
        for checkbox in self.cbox_vars:
            checkbox.set(self.cbox_labels[0])
        Frame.__init__(self, self.parent)
        self.parent.configure()
        self.parent.title('Personality Analysis')
        self.parent.bind('<Escape>', lambda event: sys.exit())

    # Centers the window in the screen
    def center_window(self, width=300, height=300):
        self.parent.update_idletasks()
        win_width = self.parent.winfo_screenwidth()
        win_height = self.parent.winfo_screenheight()
        x = win_width / 2 - width / 2
        y = win_height / 2 - height / 2
        self.parent.geometry('%dx%d+%d+%d' % ((width, height, x, y)))

    def create_widgets(self):

        #Entry Boxes for age and gender

        frame1 = Frame(self)
        frame1.pack(fill=X)


        lbl_age = Label(frame1, text='Age', width=4, background='#F0F0F0')
        lbl_age.pack(side=LEFT, padx=5, pady=5)

        self.entry_age = Entry(frame1)
        self.entry_age.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl_gender = Label(frame2, text='Gender', width=6, background='#F0F0F0')
        lbl_gender.pack(side=LEFT, padx=5, pady=5)

        self.entry_gender = Entry(frame2)
        self.entry_gender.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        self.frame4 = Frame(frame3, height=100)
        self.frame4.grid()

        Label(self.frame4, text='strongly disagree', background='#F0F0F0', width=15).grid(row=1, column=2)
        Label(self.frame4, text='disagree', background='#F0F0F0', width=7).grid(row=1, column=3)
        Label(self.frame4, text='agree', background='#F0F0F0', width=6).grid(row=1, column=4)
        Label(self.frame4, text='strongly agree', background='#F0F0F0', width=15).grid(row=1, column=5)
        #Label(self.frame4, text='no answer', background='#F0F0F0', width=8).grid(row=1, column=6)

        self.create_questions(self.questions)

        frame5 = Frame(self)
        frame5.pack(fill=X)

        b = Button(frame5, text='Analyse', command=self.get_input)
        b.pack()

        frame6 = Frame(self)
        self.frame6 = Frame(frame6, height=20)
        self.output = Label(
            frame5,
            text='PERSONALITY IS:',
            font=('Arial', 10, 'bold'),
            padding=5,
            justify=RIGHT,
            background='red'
        )
        self.output.pack(side='bottom')



    def create_questions(self, questions):

        for index, question in enumerate(questions):
            row_pos = index + 2
            Label(
                self.frame4,
                text='{}.'.format(row_pos - 1),
                font=('Arial', 10, 'bold'),
                padding=5,
                justify=RIGHT,
                background='#F0F0F0'
            ).grid(row=row_pos, column=0)

            Label(
                self.frame4,
                font=('Arial', 11, 'normal'),
                text=question,
                justify=LEFT,
                background='#F0F0F0'
            ).grid(row=row_pos, column=1, sticky=W)

            cbox_var = self.cbox_vars[index]
            Radiobutton(self.frame4, variable=cbox_var, value=self.cbox_labels[0],
                        width=6).grid(row=row_pos, column=2)
            Radiobutton(self.frame4, variable=cbox_var, value=self.cbox_labels[1],
                        width=6).grid(row=row_pos, column=3)
            Radiobutton(self.frame4, variable=cbox_var, value=self.cbox_labels[2],
                        width=6).grid(row=row_pos, column=4)
            Radiobutton(self.frame4, variable=cbox_var, value=self.cbox_labels[3],
                        width=6).grid(row=row_pos, column=5)
            #Radiobutton(self.frame4, variable=cbox_var, value=self.cbox_labels[4],
             #           width=6).grid(row=row_pos, column=6)

    def get_input(self):

        input_array=[]
        '''
        Returns the values set in the entry boxes and radio boxes
        '''
        self.entries = {
            'age': self.entry_age.get(),
            'gender': self.entry_gender.get()
        }
        for i, x in enumerate(self.cbox_vars):
            input_array.append(int(x.get()))
        input_array.append(int(self.entry_gender.get()))
        input_array.append(int(self.entry_age.get()))
        result = main()

        def get_result(result):
            result = np.array(result)
            result = float(result)

            if 0.5 <= result <= 1.4:
                return "Extrovert"
            elif 1.5 <= result <= 2.4:
                return "Neurotic"
            elif 2.5 <= result <= 3.4:
                return "Agreeable"
            elif 3.5 <= result <= 4.4:
                return "Conscious"
            else:
                return "Open"


        self.output['text'] = 'Your personality: {}'.format(get_result(result))
        print(result)

        with open('prediction.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','gender','age'])
            filewriter.writerow(input_array)


    def input(self):
        return self.entries


questions = [
    'I feel that I am a person of worth, at least on an equal plane with others.',
    'I feel that I have a number of good qualities.',
    'All in all, I am inclined to feel that I am a failure.',
    'I am able to do things as well as most other people.',
    'I feel I do not have much to be proud of.',
    'I take a positive attitude toward myself.',
    'On the whole, I am satisfied with myself.',
    'I wish I could have more respect for myself.',
    'I certainly feel useless at times.',
    'At times I think I am no good at all.'
]

if __name__ == '__main__':
    dialog = Dialog(questions)
    dialog.show()
