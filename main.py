# APA Citation Generator
# Copyright (c) 2023, Isrg
# All rights reserved.

import threading
import requests
import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def fetch_info(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')

        # get title
        if soup.title:
            title = soup.title.string.strip()
        else:
            title = ""

        # get published date
        published_date = ""
        for tag in soup.find_all(['time', 'span']):
            if tag.has_attr('datetime'):
                try:
                    date = datetime.fromisoformat(tag['datetime'])
                    if not published_date or date < published_date:
                        published_date = date
                except:
                    pass

        # get accessed date
        accessed_date = datetime.now()

        # create citation
        citation = ""
        if title:
            citation += f"{title}. "
        if published_date:
            citation += f"({published_date:%Y, %B %d}). "
        citation += f"Retrieved {accessed_date:%B %d, %Y}, from {url}"

        return citation

    except:
        return "An error occurred while fetching information from the URL."


def fetch_info_thread(url, output_box):
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)

    # validate the URL
    pattern = re.compile(r'^https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^/\s]+)*$')
    if not pattern.match(url):
        output_box.insert(tk.END, "Invalid URL")
        output_box.config(state=tk.DISABLED)
        return

    output_box.insert(tk.END, "Fetching information...\n")
    output_box.config(state=tk.DISABLED)

    # rest of the function remains the same


    def target():
        citation = fetch_info(url)

        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, citation)
        output_box.config(state=tk.DISABLED)

    thread = threading.Thread(target=target)
    thread.start()


def clear_output(output_box):
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.config(state=tk.DISABLED)


def main():
    # create GUI
    root = tk.Tk()
    root.title("APA Citation Generator")
    root.geometry("800x500")

    # create URL input
    url_label = tk.Label(root, text="Enter URL:")
    url_label.pack()
    url_entry = tk.Entry(root, width=100)
    url_entry.pack()

    # create output box
    output_label = tk.Label(root, text="APA Citation:")
    output_label.pack()
    output_box = ScrolledText(root, height=20)
    output_box.pack()

    # create buttons
    fetch_button = tk.Button(root, text="Fetch Information", command=lambda: fetch_info_thread(url_entry.get(), output_box))
    fetch_button.pack(side=tk.LEFT, padx=10)
    clear_button = tk.Button(root, text="Clear Output", command=lambda: clear_output(output_box))
    clear_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()


if __name__ == '__main__':
    main()
