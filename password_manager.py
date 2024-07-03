import json
from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Courier"
FONT_SIZE = 12


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_char = [choice(symbols) for _ in range(randint(2, 4))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letter + password_char + password_number

    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    email = user_entry.get()
    password = pass_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }

    if website != "" and email != "" and password != "":
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating new data with new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            web_entry.delete(0, END)
            user_entry.delete(0, END)
            pass_entry.delete(0, END)
            web_entry.focus()
    else:
        messagebox.showwarning(title="Empty fields", message="Please fill all the fields!!!")


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    site = web_entry.get()
    if site == "":
        messagebox.showwarning(title="Warning", message="Enter website name!!!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No Data File Found!!!")
        else:
            if site in data:
                email = data[site]["email"]
                password = data[site]["password"]
                pyperclip.copy(email)
                messagebox.showinfo(title=site, message=f"Email: {email}\nPassword: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showerror(title="Error", message=f"No details  for this {site} exists!!!")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(False, False)

canvas = Canvas(height=200, width=200, highlightthickness=0)
passman_img = PhotoImage(file="images/logo.png")
canvas.create_image(100, 100, image=passman_img)
canvas.grid(row=0, column=1)

# Labels
web_label = Label(text="Website", font=(FONT_NAME, FONT_SIZE, "bold"), justify="center")
web_label.grid(row=1, column=0)
user_label = Label(text="Email/Username", font=(FONT_NAME, FONT_SIZE, "bold"), justify="center")
user_label.grid(row=2, column=0)
pass_label = Label(text="Password", font=(FONT_NAME, FONT_SIZE, "bold"), justify="center")
pass_label.grid(row=3, column=0)

# Entries
web_entry = Entry(width=21, border=1, font=(FONT_NAME, FONT_SIZE, "italic"), justify="left")
web_entry.focus()
web_entry.grid(row=1, column=1, padx=5, pady=5)
user_entry = Entry(width=35, border=1, font=(FONT_NAME, FONT_SIZE, "italic"), justify="left")
user_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
pass_entry = Entry(width=21, border=1, font=(FONT_NAME, FONT_SIZE, "italic"), justify="left")
pass_entry.grid(row=3, column=1, padx=7, pady=5)

# Buttons
search_btn = Button(text="Search", bg="white", border=0, width=14, command=search)
search_btn.grid(row=1, column=2, padx=18, pady=5)
gen_btn = Button(text="Generate Password", bg="white", border=0, width=14, command=password_generator)
gen_btn.grid(row=3, column=2, padx=18, pady=5)
add_btn = Button(text="Add", width=20, border=0, bg="white", command=save)
add_btn.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

window.mainloop()
