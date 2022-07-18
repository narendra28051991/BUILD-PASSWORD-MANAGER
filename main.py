from tkinter import *
from tkinter import messagebox
from random import randint, choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random_password = "".join(password_list)
    password_entry.insert(0, random_password)
    pyperclip.copy(random_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="OOPS!!", message="Please do not leave any fields empty..")

    else:
        is_ok = messagebox.askokcancel(title="Website", message=f"These are the details entered\nwebsite: {website}\n"
                                                                f"email: {email}\npassword: {password}\nIs it OK !!")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    load_data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                load_data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(load_data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


def website_info():
    website_name = website_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            load_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website_name in load_data:
            website_details = load_data[website_name]
            messagebox.showinfo(title=website_name,
                                message=f"These are the website: {website_name} details\n"
                                f"email: {website_details['email']}\n"
                                f"password: {website_details['password']}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_name} exists")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=50)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "Ex: narendra@gmail.com")
password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

search_website = Button(text="Search", width=14, command=website_info)
search_website.grid(row=1, column=2)
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(row=3, column=2)
add_login = Button(text="Add", width=42, command=save)
add_login.grid(row=4, column=1, columnspan=2)

window.mainloop()