import turtle
import pandas as pd
import tkinter as tk
from tkinter import messagebox

from pandas.io.stata import stata_epoch

data = pd.read_csv("50_states.csv")
all_states = data['state'].tolist()

screen = turtle.Screen()
correct_guesses = 0
total_states = len(data)
screen.title("U.S States Game.")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

guessed_city = []
user_guess  = None

root = tk.Tk()
root.withdraw()



def display_state_on_map(state_name):
    state_data = data[data["state"].str.lower() == user_guess.lower()]
    if not state_data.empty:
        state_x, state_y = state_data.iloc[0]['x'], state_data.iloc[0]['y']
        marker = turtle.Turtle()
        marker.hideturtle()
        marker.penup()
        marker.goto(state_x, state_y)
        marker.write(user_guess, align="center", font=("Arial", 10, "normal"))
        return True
    return False

def check_user_guess():
    global user_guess, correct_guesses

    if user_guess is None:
        return

    if user_guess.lower() in data['state'].str.lower().values:
        if display_state_on_map(user_guess):
            guessed_city.append(user_guess)
            correct_guesses += 1
            screen.title(f"Guess a State {correct_guesses}/{total_states}")

            if correct_guesses == total_states:
                messagebox.showinfo("Congratulations!", "you have guessed all states correctly")
                turtle.bye()

            user_guess = None
            ask_for_guess()
    else:
        messagebox.showinfo("Game over!", "Incorrect guess. Try again!")
        save_remaining_file()
        turtle.bye()


def save_remaining_file():
    remaining_states = [state for state in all_states if state not in guessed_city]
    if remaining_states:
        remaining_df = pd.DataFrame(remaining_states, columns=["state"])
        remaining_df.to_csv("states_you_need_to_learn.csv", index= False)
        messagebox.showinfo("States Saved", "The remaining states have been saved to 'states_you_need_to_learn.csv'.")

def ask_for_guess():
    global user_guess
    user_guess = screen.textinput(title=f"Guess a state: {correct_guesses} / {total_states}",
                                      prompt="What's another state name?")

    if user_guess:
        if user_guess.lower() == "exit":
            save_remaining_file()
            turtle.bye()
        else:
            check_user_guess()
    else:
        turtle.bye()

ask_for_guess()
screen.mainloop()





# def check_guess(state, x, y):
#     global correct_guesses
#     state_data = data[data['state'].str.lower() == state.lower()]
#     if not state_data.empty:
#         state_x, state_y = state_data.iloc[0]['x'], state_data.iloc[0]['y']
#
#         if abs(x - state_x) < 20 and abs(y - state_y) < 20:
#             marker = turtle.Turtle()
#             marker.hideturtle()
#             marker.penup()
#             marker.goto(state_x, state_y)
#             marker.write(state, align="center", font=("Arial", 10 , "normal"))
#             guessed_city.append(state)
#             correct_guesses += 1
#         else:
#             screen.bye()
#             print("game over")
#     else:
#         print("Incorrect state name.")
#
#
#
# def ask_for_guess():
#     while correct_guesses < total_states:
#         user_guess = screen.textinput(title=f"Guess a city {correct_guesses} / {total_states}", prompt="What's another state name?")
#         if user_guess is None:
#             break
#
#         x, y = screen.numinput("click the map", "Click on the guessed state's location", minval=1000, maxval=1000) , \
#                 screen.numinput("click the map", "Click on the guessed state's location", minval=1000, maxval=1000)
#
#         if "x" is not None and "y" is not None:
#             if check_guess(user_guess, x, y):
#                 if correct_guesses == total_states:
#                     messagebox.showinfo("Congratulations!", "You guessed all states correctly!")
#                     break
#                 else:
#                     messagebox.showinfo("Game over", "Incorrect guess. Try again!")
#                     break
#
#
#
# ask_for_guess()

screen.exitonclick()