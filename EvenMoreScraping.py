import time
import random
from tkinter import SE
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import undetected_chromedriver as uc
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from tkinter import filedialog, messagebox
import threading
import math


def get_videos():
    """
    Scrapes YouTube to find videos based on user input
    and find their corresponding data(title and view count)
    """
    try:
        title_and_views = []# a list containing the titles and views of each video

        search = entry.get()#get the users input

        search = search.split()

        search = "+".join(search) #replace spaces in the query with the plus sign (e.g, "expensive car": "expensive+car")
    
        url = f"https://www.youtube.com/results?search_query={search}"

        #options for the chrome webdriver
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        driver.execute_script("window.scrollBy(0, 50000);") # scroll down by fifty thousand pixels to load more videos

        titles = driver.find_elements(By.ID, "video-title")# find all of the video titles

        views = driver.find_elements(By.CLASS_NAME, "style-scope ytd-video-meta-block")# find all of the video views

        print(str(len(titles)) + "\n")# print the number of videos found

        i = 0

        for title in titles:
            title_and_views.append(title.text + ": "  + views[i].text + "\n")#append all of the titles and their corresponding view count to a list
            i+=1
    
        #show fifteen videos at a time in a message box
        chunk_size = 15
        for i in range(0, len(title_and_views), chunk_size):
            chunk = title_and_views[i:i+chunk_size]
        
            messagebox.showinfo("Results", "\n".join(chunk))
    except Exception as e:
        messagebox.showerror("Error", e)
        
    
    driver.quit()

#a function to start the main functions thread    
def start_thread():
    thread = threading.Thread(target=get_videos)
    thread.start()

window = ttk.Window(themename="journal")

window.geometry("800x400")

#ui setup
label = tk.Label(text="Type something", font="Ariel 24 bold")
entry = tk.Entry()
button = tk.Button(text="Search", command=start_thread)

#place the elements on the screen
label.pack()
entry.pack(pady=5)
button.pack(pady=10)

window.mainloop()