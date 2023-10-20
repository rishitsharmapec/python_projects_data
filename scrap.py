import pandas as pd
import requests
from bs4 import BeautifulSoup
import tkinter as tk
def scrap():
    searchraw=num1_entry.get()
    search=searchraw.replace(" ","+")
    filenameraw=num2_entry.get()
    filename=filenameraw.replace(" ","_")
    name = []
    price = []
    description = []
    rating = []
    for j in range(1, 26):

        url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={j}"

        r = requests.get(url)
        htmlcontent = r.content
        soup = BeautifulSoup(r.content, 'html.parser')
        section = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        s = section.find_all("div", class_="_4rR01T")
        for n in s:
            uplistname = (n.text)
            name.append(uplistname)
        s1 = section.find_all("div", class_="_30jeq3 _1_WHN1")
        for p in s1:
            uplistprice = (p.text)
            price.append(uplistprice)
        s2 = section.find_all("ul", class_="_1xgFaf")
        for d in s2:
            uplistdescription = d.text
            description.append(uplistdescription)

    df = pd.DataFrame({"Product Name": name, "Price": price, "Description": description})
    result_label = tk.Label(root, text="Check Your Python CSV Folder in D drive")
    result_label.grid(row=3, column=0, columnspan=2)

    return df.to_csv(f"D:\python csv\{filename}.csv")



root = tk.Tk()
root.title("excel")


# create the widgets
num1_label = tk.Label(root, text="What do you want to buy:")
num1_entry = tk.Entry(root)
num2_label = tk.Label(root, text="File name")
num2_entry = tk.Entry(root)
add_button = tk.Button(root, text="Download",command=scrap)


# layout the widgets
num1_label.grid(row=0, column=0, sticky="e")
num1_entry.grid(row=0, column=1)
num2_label.grid(row=1, column=0, sticky="e")
num2_entry.grid(row=1, column=1)
add_button.grid(row=2, column=0, columnspan=2, pady=10)


# run the main loop
root.mainloop()
