import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("Mohenjo Daro Clock")
root.geometry("400x150")
root.configure(bg="black")

def update_time():
    string = strftime('%H:%M:%S %p\n%A, %b %d')
    label.config(text=string)
    label.after(1000, update_time)

label = tk.Label(root, font=('calibri', 24, 'bold'), background='black', foreground='cyan')
label.pack(anchor='center', expand=True)

update_time()
root.mainloop()
