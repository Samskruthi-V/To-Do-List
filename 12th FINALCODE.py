from collections import OrderedDict
import datetime
import os
import threading
import winsound
from datetime import timedelta
from peewee import *
import matplotlib.pyplot as plt
from tkinter import *
import random
import time
from time import strftime 
from tkinter import messagebox
import speech_recognition as sr
import csv
import webbrowser
print("DIFFICULT ROADS OFTEN LEAD TO BEAUTIFUL DESTINATIONS")
print()
time.sleep(1)
print("WELCOME TO STUDENTIO")
time.sleep(1)
print()
print("EXPLORE ALL THE FEATURES TO DE-STRESS YOUR DAY")
time.sleep(1)
s='y'
def welcome():
    while s=='y':
        print("TASKS AVAILABLE")
        time.sleep(0.5)
        print("1.TIMEAHOLIC-DAY PLANNER")
        time.sleep(0.5)
        print("2.BOUNCERY-BALL GAME ")
        time.sleep(0.5)
        print("3.HELPEX-SELF HELP")
        time.sleep(0.5)
        print("4.DONE DEAL-QUIT")
        time.sleep(0.5)
        print()
        m=int(input("KINDLY CHOOSE THE TASK YOU DESIRE:"))
        print()
        if m==1:
            
            db = SqliteDatabase('to_do_list.db')

            def alarm(): 
                print("FINISH THE TASK SOON!!!")
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
                for i in range(4):
                    frequency =2000  # Set Frequency To 2000 Hertz
                    duration =500  # Set Duration To 1000 ms == 1 second
                    winsound.Beep(frequency, duration)
                    

            class ToDo(Model):
                """Model for creating to-do items. 'done' indicates that it's been completed,
                'protected' makes it immune to cleanup"""
                task = CharField(max_length=255)
                timestamp = DateTimeField(default=datetime.datetime.now)
                done = BooleanField(default=False)
                protected = BooleanField(default=False)

                class Meta:
                    database = db


            def clear():
                """Clear the display"""
                os.system('cls' if os.name == 'nt' else 'clear')


            def initialize():
                """Connect to database, build tables if they don't exist"""
                db.connect()
                db.create_tables([ToDo], safe=True)


            def view_entries(index, entries, single_entry):
                """"View to-do list"""
                clear()

                index = index % len(entries)  # determines which entry is selected for modification
                if single_entry:  # to see only 1 entry
                    entries = [entries[index]]
                    index = 0
                else:
                    print('\nMY TO-DO LIST')
                    print('=' * 40)
                prev_timestamp = None

                for ind, entry in enumerate(entries):
                    timestamp = entry.timestamp.strftime('%d/%B/%Y')

                    if timestamp != prev_timestamp:  # same timestamps get printed only once
                        print('\n')
                        print(timestamp)
                        print('=' * len(timestamp))
                        prev_timestamp = timestamp

                    if ind == index:  # placing the selection tick
                        tick = '> '
                    else:
                        tick = '  '

                    tasktimestamp = entry.timestamp.strftime('%H:%M:%S %p')
                    print('{}{}     {}'.format(tick, entry.task, tasktimestamp), end='')
                    if entry.done:
                        print('\t(DONE)', end='')
                    if entry.protected:
                        print('\t <P>', end='')
                    print('')

                return entries  # so that we can modify the given entry if needed


            def add_entry(index, entries):
                """Add a new task"""
                n="y"
                while n.lower().strip()=="y":
                      new_task = input('\nTo do: ')
                      if input('Protect [y/n]? ').lower().strip() == 'y':
                           protect = True
                      else:
                            protect = False
                      print("By when do you want to complete task?")
                      print("Enter the time you want to finish the task in __ mins from now")
                      a=float(input())
                      newtimestamp=datetime.datetime.now()+timedelta(seconds=a*60)  
                      ToDo.create(task=new_task,timestamp=newtimestamp,
                                 protected=protect)
                      s=float(input("Alert in(min):"))
                      
                      
                      timer = threading.Timer(s*60.0, alarm) 
                      timer.start()

                      n=input("Do you want to enter a new task[y/n]")


            def modify_entry(index, entries):
                """Modify selected entry"""
                entry = view_entries(index, entries, True)[0]
                print('\n\n')

                for key, value in sub_menu.items():
                    print('{}) {}'.format(key, sub_menu[key].__doc__))
                print('q) Back to Main')
                next_action = input('Action: ')

                if next_action.lower().strip() in sub_menu:
                    sub_menu[next_action](entry)
                else:
                    return


            def cleanup_entries(index, entries):
                """Cleanup: delete completed, non-protected entries older than a week"""
                if (input('Have you checked that you protected the important stuff? [y/n]').lower().strip() == 'y'):
                    now = datetime.datetime.now()
                    for entry in entries:
                        if (now - entry.timestamp > datetime.timedelta(7, 0, 0) or entry.done and not entry.protected):
                            entry.delete_instance()

            def graph(index, entries):
                "Plot the graph"
                x=[]
                y=[]
                for ind,entry in enumerate(entries):
                    timestamp = entry.timestamp.strftime('%d/%B/%Y')
                    #print('{}   {} {}'.format(ind,entry.done,timestamp),end=' ')
                    x.append(timestamp)
                x=list(set(x))
                x.sort(key= lambda date: datetime.datetime.strptime(date, '%d/%B/%Y'))
                y=[0 for i in range(len(x))]
                for ind,entry in enumerate(entries):
                    timestamp=entry.timestamp.strftime('%d/%B/%Y')
                    if entry.done==True:
                        y[x.index(timestamp)]+=1
                plt.xlabel("Date")
                plt.ylabel("Tasks that are completed")
                plt.bar(x,y)
                plt.show()

                





            def modify_task(entry):
                """Change name of the task"""
                new_task = input('> ')
                entry.task = new_task
                entry.save()


            def delete_entry(entry):
                """Erase entry"""
                if (input('Are you sure [y/n]? ').lower().strip() == 'y'):
                    entry.delete_instance()


            def toggle_done(entry):
                """Toggle 'DONE'"""
                entry.done = not entry.done
                entry.save()


            def toggle_protection(entry):
                """Toggle 'Protected'"""
                entry.protected = not entry.protected
                entry.save()


            def menu_loop():
                choice = None
                index = 0  # shows which entry is selected
                entries =ToDo.select().order_by(ToDo.timestamp.asc())
                print(entries)
                
                while choice != 'q':
                    if len(entries) != 0:
                        view_entries(index, entries, False)

                        print('\n' + '=' * 40 + '\n')
                        print(' Type p/n to go to Previous/Next Task \n')
                    for key, value in main_menu.items():
                        print('{}) {}'.format(key, value.__doc__))
                    print('q) Quit')

                    choice = input('\nAction: ')
                    if choice in main_menu:
                        try:
                            main_menu[choice](index, entries)
                        except ZeroDivisionError:
                            continue
                        entries = ToDo.select().order_by(ToDo.timestamp.asc())  # update entries after operations

                    elif choice == 'n':
                        index += 1
                    elif choice == 'p':
                        index -= 1
                if choice=='q':
                    global s
                    print("Do you want to go back to the main page")
                    s=input("y/n")
                    print()
                    if s=="n":
                        exit()

            main_menu = OrderedDict([
                ('a', add_entry),
                ('m', modify_entry),
                ('c', cleanup_entries),
                ('g',graph)
            ])

            sub_menu = OrderedDict([
                ('c', modify_task),
                ('d', toggle_done),
                ('p', toggle_protection),
                ('e', delete_entry)
            ])

            if __name__ == '__main__':
                initialize()
                menu_loop()
                db.close()

        if m==2:
            class Ball:
                def __init__(self, canvas, paddle, color):
                        self.canvas = canvas
                        self.paddle = paddle
                        self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
                        #self.canvas.move(self.id, 245, 100)
                        self.canvas.move(self.id, random.randint(50, 400), random.randint(10, 350))
                        starts = [-3, -2, -1, 1, 2, 3]
                        random.shuffle(starts)
                        #self.x = 0
                        self.x = starts[0]
                        self.y = -3
                        self.canvas_height = self.canvas.winfo_height()
                        self.canvas_width = self.canvas.winfo_width()
                        self.hit_bottom = False

                def hit_paddle(self, pos):
                        paddle_pos = self.canvas.coords(self.paddle.id)
                        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                                        return True
                        return False

                def draw(self):
                        self.canvas.move(self.id, self.x, self.y)
                        pos = self.canvas.coords(self.id)
                        if pos[1] <= 0:
                                self.y = 3
                        if pos[3] >= self.canvas_height:
                                self.hit_bottom = True
                        if self.hit_paddle(pos) == True:
                                self.y = -3
                        if pos[0] <= 0:
                                self.x = 3
                        if pos[2] >= self.canvas_width:
                                self.x = -3
                def reset(self):
                        if (self.hit_bottom == True):
                                self.canvas.move(self.id, 0, -400)
                                self.hit_bottom = False

            class Paddle:
                    def __init__(self, canvas, color):
                            self.canvas = canvas
                            self.id = canvas.create_rectangle(0, 0, 170, 10, fill=color)
                            self.canvas.move(self.id, 300, 400)
                            self.x = 0
                            self.canvas_width = self.canvas.winfo_width()
                            self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
                            self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
                    def draw(self):
                            self.canvas.move(self.id, self.x, 0)
                            self.x = 0
                            pos = self.canvas.coords(self.id)
                            if pos[0] <= 0:
                                    self.x = 0
                            elif pos[2] >= self.canvas_width:
                                    self.x = 0
                    def turn_left(self, evt):
                            self.x = -12
                    def turn_right(self, evt):
                            self.x = 12

            class Score(object):
                    """docstring for ClassName"""
                    def __init__(self, canvas, color):
                            self.canvas = canvas
                            self.id1 = canvas.create_text(100, 30, text='Max : ', font=('Courier', 10))
                            self.id2 = canvas.create_text(100, 50, text='Current : ', font=('Courier', 10))
                            self.datetimeFormat = '%H:%M:%S %p'
                            self.starttime = strftime('%H:%M:%S %p')
                            self.current = 0
                            self.max = 0
                    def updateMax(self):
                            self.max = self.current
                            string = "Max : " + str(self.max)
                            self.canvas.itemconfig(self.id1, text = string)
                    def updateCurrent(self):
                            diff = datetime.datetime.strptime(strftime('%H:%M:%S %p'), self.datetimeFormat)\
                                    - datetime.datetime.strptime(self.starttime, self.datetimeFormat)
                            self.current = diff
                            string = "Current : " + str(self.current)
                            self.canvas.itemconfig(self.id2, text=string)
                    def resetStart(self):
                            self.starttime = strftime('%H:%M:%S %p') 



            tk = Tk()
            tk.title("Game")
            tk.resizable(0, 0)
            tk.wm_attributes("-topmost", 1)
            canvas = Canvas(tk, width=600, height=500, bd=0, highlightthickness=0)
            global running
            running=True
            canvas.pack()
            tk.update()

            bg = PhotoImage(file="background.gif")
            w = bg.width()
            h = bg.height()
            for x in range(0, 6):
                    for y in range(0, 5):
                            canvas.create_image(x * w, y * h,image=bg, anchor='nw')

            paddle = Paddle(canvas, 'blue')
            ball1 = Ball(canvas, paddle, 'yellow')
            #ball2 = Ball(canvas, paddle, 'green')
            score = Score(canvas, 'black')

            def on_closing():
                result=messagebox.askyesno("Do you want to go back to the main page y/n")
                
                if result==True:
                        tk.destroy()
                        running=False   #To turn off the while loop
                        welcome()
                          
                        
                else:
                        tk.destroy()
                        exit(1)
                        
            tk.protocol("WM_DELETE_WINDOW", on_closing)
            def restart():
                    if ball1.hit_bottom == True:
                            ball1.reset()
            #		ball2.reset()
                            score.resetStart()
                            score.updateMax()
                    
            
            btn = Button(tk, text="Restart", command=restart)
            btn.pack()
            
            while running:
                
                    if ball1.hit_bottom  == False:
            #		if ball2.hit_bottom  == False:
                                    ball1.draw()
            #			ball2.draw()
                                    paddle.draw()
                                    score.updateCurrent()
                    tk.update_idletasks()
                    tk.update()
                    time.sleep(0.03)
           
        if m==3:
            def main(l):
                happy = 0
                sad = 0
                irritated = 0
                depressed = 0
                anxious = 0
                broken = 0
                jealous = 0
                demotivated = 0
                stressed = 0
                unknown=0
                # loop 1
                for i in l:
                    if i == "sad" or i == "lonely" or i == "upset" or i=="bad":
                        sad += 1
                    elif i == "happy" or i == "good":
                        happy += 1
                    elif i == "irritated" or i == "frustrated" or i == 'angry' or i=='mad':
                        irritated += 1
                    elif i == "depressed" or i == "low" or i == "hurting":
                        depressed += 1
                    elif i == "anxious" or i == "uneasy":
                        anxious += 1
                    elif i == "broken" or i == "damaged":
                        broken += 1
                    elif i == "jealous":
                        jealous += 1
                    elif i == "demotivated" or i == "lazy":
                        demotivated += 1
                    elif i == "stressed":
                        stressed += 1
                    else:
                        unknown+=1
                        

                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                x = ['happy', 'sad', 'irritated', 'depressed', 'anxious', 'broken', 'jealous', 'demotivated','stressed']
                y = [happy, sad, irritated, depressed, anxious, broken, jealous, demotivated, stressed]
                ax.bar(x, y)
                plt.xticks(rotation=90)
                plt.show()

                time.sleep(3)

                d = {'happy': happy, 'sad': sad, 'irritated': irritated, 'depressed': depressed, 'anxious': anxious,
                     'broken': broken, 'jealous': jealous, 'demotivated': demotivated, 'stressed': stressed,'unknown':unknown}
                values = d.values()
                l = list(values)
                l.sort(reverse=True)
                max = l[0]
                a = []
                for i in d:
                    if d.get(i) == max:
                        a.append(i)
                print("Hope the following video helps you out")
                print()
                
                for k in a:
                    if k == 'happy':
                        print("I am very glad to hear that, I hope your day continues to be amazing.")
                        print("Take care and be well")
                        print()
                    elif k == 'sad':
                        webbrowser.open_new_tab(url='https://youtu.be/5Vzkbz-P29A')
                    elif k == 'irritated':
                        webbrowser.open_new_tab(url='https://youtu.be/ns2ZYdBMx4w')
                    elif k == 'depressed':
                        webbrowser.open_new_tab(url='https://youtu.be/vB9M0f9FDiE')
                    elif k == 'anxious':
                        webbrowser.open_new_tab(url='https://youtu.be/r9bltqeHtak')
                    elif k == 'broken':
                        webbrowser.open_new_tab(url='https://youtu.be/2ou_zUINQ9k')
                    elif k == 'jealous':
                        webbrowser.open_new_tab(url='https://youtu.be/FL2cE6WGzIc')
                    elif k == 'demotivated':
                        webbrowser.open_new_tab(url='https://youtu.be/t6Kw3n9CNrc')
                    elif k == 'stressed':
                        webbrowser.open_new_tab(url='https://open.spotify.com/user/sah8opgy08gnfvchjkkko2ody/playlist/76WNsLuUpwQY5vxv2YrUfS?si=vD74V8yiQlawHXt_wA6Hnw')
                    elif k == 'unknown':
                        webbrowser.open_new_tab(url='https://www.youtube.com/watch?v=4yLZeOBGhPc')
            print("LIFE IS TOO SHORT TO HIDE YOUR FEELINGS.")
            print("DON'T BE AFRAID TO SAY WHAT YOU FEEL")
            print()
            time.sleep(2)
            print("Welcome to the section of Journaling and Self help")
            print()
            print("Would you like to use AUDIO or TEXT for input?")
            print()
            a=input("Please enter your choice:")  
            a=a.lower()
            if a=='audio':
                r=sr.Recognizer()
                with sr.Microphone() as source:
                    print("Speak now")
                    audio=r.listen(source)
                try:
                    text=r.recognize_google(audio)
                    fw=open("Result.txt",'w')
                    print(format(text),file=fw)
                    fw.close()
                except:
                    print("sorry could not recognise your voice")
                
                try:
                    l = []
                    with open('Result.txt','r') as fo:
                        csv_reader=csv.reader(fo,delimiter=' ')
                        for i in csv_reader:
                            l=i
                    main(l)
                    with open('Result.txt','r') as f:
                        os.remove(f)
                except:
                    print("Failed to read")
                    print()

            elif a=='text':
                r = input("What has been on your mind lately:  ")
                l = r.split()
                main(l)
            else:
                print('Invalid input')
        if m==4:
            running=False
            exit()
welcome()

                    
