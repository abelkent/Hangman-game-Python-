# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:05:28 2022

@author: abelw
"""

import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk, Image


valid = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
            "R","S","T","U","V","W","X","Y","Z"," "]


#Purely textual implementation of the pen and paper "Hangman" game
class Hangman(): 
    
    def __init__(self):
        super().__init__()
        self.secret = list()
        self.known = list()
        self.guesses = list()
        self.count = int()
        self.count_limit = int(6)
        
        self.play_game()
        
    def get_secret(self):
        
        while True:
            invalid = 0
            proposed = str(input("Please enter your word: ")).upper()
            
            for character in proposed:
                if character not in valid:
                    invalid = invalid+1
            
            if invalid > 0:
                print("Please enter a valid word")
            else:
                break
        
        self.secret = list(proposed)
        self.known = list("_" * len(proposed))
        
    
    def make_guess(self):
        print("Errors remaining: "+str(self.count_limit - self.count))
        while True:
            guess = str(input("Please enter your guess: ")).upper()
            
            if (len(guess) != 1) or (guess not in valid):
                print("Please enter a valid guess")
            elif (guess in self.guesses):
                print("You have already guessed: "+guess)
            else:
                break
        
        
        if guess in self.secret:
            for index in range(len(self.secret)):
                if self.secret[index] == guess:
                    self.known[index] = guess
        else:
            self.count = self.count+1

        
        self.guesses.append(guess)
        

    def play_game(self):

        self.get_secret()
        
        print("\n"*50)
        
        solved = False
        while solved == False:

            print (" ".join(self.known))
            print("Guessed letters: "+", ".join(self.guesses))
            
            self.make_guess()
            
            if (self.known != self.secret) and (self.count == self.count_limit):
                print("DEFEAT")
                print("Answer: "+"".join(self.secret))
                break
            elif self.known == self.secret:
                print("VICTORY")
                print("".join(self.secret))
                break
                


class Hangman_GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #Attributes
        self.secret = list("DOG")
        self.known = list("_" * len(self.secret))
        self.known_string = " ".join(self.known) + "\n"
        self.guesses = list()
        self.remaining = int(6)
        self.icon = ImageTk.PhotoImage(Image.open("Assets/stage0.png"))
        self.stage = int(0)
        
        #Widgets / Tkinter attributes
        self.title("Hangman!")
        self.geometry("400x300")

        
        
        self.entry_header = tk.Label(self, text = "Enter your word below")
        self.word_entry = tk.Entry(self)
        self.entry_submit = tk.Button(self, text = "Submit", command = self.setup_play)
        
        self.entry_header.pack()
        self.word_entry.pack()
        self.entry_submit.pack()

        self.bind("<KeyPress-Return>", lambda event: self.setup_play())

        
        
    def setup_play(self):

        self.secret = list(self.word_entry.get().upper())
        self.known = list("_" * len(self.secret))
        self.known_string = " ".join(self.known) + "\n"
        
        if len(self.secret) >= 1:

            self.entry_header.destroy()
            self.word_entry.destroy()
            self.entry_submit.destroy()
    
            self.heading = tk.Label(self,text = "Hangman - Enter your guess below")
            self.box = tk.Entry(self)
            self.submit = tk.Button(self, text = "Submit", command = self.submit_guess)
            self.known_label = tk.Label(self, text = self.known_string)
            self.countdown = tk.Label(self, text = "Wrong guesses remaining: "+str(self.remaining))
            self.guesses_label = tk.Label(self, text = "Letters guessed: "+str(self.guesses).strip("[]"))
            self.panel = tk.Label(self, image = self.icon)
    
            #Packing
            self.heading.pack()
            self.box.pack()
            self.submit.pack()
            self.known_label.pack()
            self.countdown.pack()
            self.guesses_label.pack()
            self.panel.pack()
            
            self.bind("<KeyPress-Return>", lambda event: self.submit_guess())
        
        else:
            messagebox.showerror(title = "Alert", message = "Please enter a valid word")
        
    def get_secret(self, word):
        self.secret = list(word.upper())
        self.known = list("_" * len(word))
        self.known_string = " ".join(self.known)
        
        #print(self.known_string)
        

            

    
    def submit_guess(self):
        #print(self.known)
        guess = self.box.get().upper()
        self.box.delete(0)
        #print(guess)
        if (len(guess) != 1) or (guess not in valid):
            messagebox.showerror(title = "Alert", message = "Please enter a valid guess")
        elif (guess in self.guesses):
            messagebox.showerror(title="Alert", message = ("You have already guessed: "+guess))
        else:
            if guess in self.secret:
                for index in range(len(self.secret)):
                    if self.secret[index] == guess:
                        self.known[index] = guess
                        self.known_string = " ".join(self.known) + "\n"

            else:
                self.remaining = self.remaining-1
                self.countdown.configure(text="Wrong guesses remaining: "+str(self.remaining))
                self.stage = self.stage+1
                self.icon = ImageTk.PhotoImage(Image.open("Assets/stage"+str(self.stage)+".png"))
                self.panel.configure(image=self.icon)
            
            self.guesses.append(guess)
            self.guesses_label.configure(text="Letters guessed: "+str(self.guesses).strip("[]"))
            self.known_label.configure(text=self.known_string)
        
        if self.secret == self.known:
            messagebox.showinfo(title = "Victory!", message = "You have successfully guessed the word: " +"".join(self.secret))
            self.destroy()
        elif self.remaining == 0:
            messagebox.showinfo(title = "Defeat", message = "You did not manage to guess the word: "+"".join(self.secret))
            self.destroy()


        
#hangman = Hangman_GUI()
#hangman = Hangman()
hangman.get_secret("Dog")
hangman.mainloop()
