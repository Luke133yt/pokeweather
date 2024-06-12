import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *
import ttkbootstrap

last_searched_city = open('last.txt', 'r').read()

def change_theme(event):
    selected_theme = combobox.get()
    app.style.theme_use(selected_theme)

def get_weather(city):

    api_key = ""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found!")
        return None

    weather = res.json()
    icon_id = weather["weather"][0]["icon"]
    temperature_farheneit = round(weather["main"]["temp"])
    temperature_celsius = round((temperature_farheneit - 32)/1.8)
    description = weather["weather"][0]["description"]
    city = weather['name']
    country = weather["sys"]["country"]

    icon_path = f"assets/{icon_id}.png"
    return(icon_path, temperature_farheneit, temperature_celsius, description, city, country)

def search():

    city = city_prompt.get()
    weather = get_weather(city)
    if weather is None:
        return

    #unpack the return
    icon_path, temperature_farheneit, temperature_celsius, description, city, country = weather

    location_label.configure(text=f"{city}, {country}")

    image = Image.open(icon_path)

    #resize cause i don't want to resize by hand
    width, height = image.size
    new_width = width * 2
    new_height = height * 2

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    icon = ImageTk.PhotoImage(resized_image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature_celsius}°C / {temperature_farheneit}°F")
    description_label.configure(text=f"Description: {description.title()}")

    #if i search a new city i'll update the last result, so the next time that i'll open the app, it will rest the last city searched
    if last_searched_city != city:
        change_last_city(city)

#everytime i search for the weather of a new city i changed the last city seen, like a weather mobile app
def change_last_city(city):
    with open('last.txt', 'w') as file: file.write(city)

#app structure
app = ttkbootstrap.Window(themename="solar")    #if you want to change the default theme, change it with the theme name, you can find the name in the dropdown menu when you launch the software
app.title("PokèWeather")
app.geometry("800x800")

logo = Image.open("logo.png")

tk_logo = ImageTk.PhotoImage(logo)

label = tk.Label(app, image=tk_logo)
label.pack()

#icon section
#icon_image = Image.open("icon.ico")
#icon_image_tk = ImageTk.PhotoImage(icon_image)
#app.iconphoto(True, icon_image_tk)

#app it self
city_prompt = ttkbootstrap.Entry(app, font="Arial, 18")
city_prompt.pack(pady=10)
city_prompt.insert(0, last_searched_city)  # Insert default text

search_btn = ttkbootstrap.Button(app, text="Search", command=search, bootstyle="warning")
search_btn.pack(pady=10)

location_label = tk.Label(app, font = "Arial, 25")
location_label.pack(pady=20)

icon_label = tk.Label(app)
icon_label.pack()

temperature_label = tk.Label(app, font="Arial, 20")
temperature_label.pack()

description_label = tk.Label(app, font="Arial, 20")
description_label.pack()

#theme changer
theme = app.style.theme_names()
combobox = ttkbootstrap.Combobox(app, values=theme, state="readonly", font=("Arial", 14))
combobox.pack(side=BOTTOM, anchor=SE, padx=10, pady=10)
combobox.bind("<<ComboboxSelected>>", change_theme)

combobox.set(app.style.theme_use())

app.mainloop()

#TODO
#idk if is kinda cool, but i can make that there's the possibility to encaunter a shiny icon, but yeah is kinda useless i guess
#icon picture that doesm't work

#DONE:
#old location search as default
#theme chooser
#celsius farheneit
#pokèmon icon