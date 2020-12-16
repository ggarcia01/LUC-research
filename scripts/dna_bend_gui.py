'''
garcia,gil
created: 12/15/2020
updated: 12/16/2020

purpose: GUI for DNA bend program found in dna_bending.py

'''

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import csv
from tkinter.filedialog import asksaveasfile
from dna_bending import dna_bend



root = tk.Tk()
root.title('DNA Bending')


root.geometry('900x900')
root.pack_propagate(False)
root.resizable(1,1)


#frame for tree view
frame1 = tk.LabelFrame(root,text='Data')
frame1.place(height = 500, width= 900,relx=0)

#frame for open file dialog

file_frame = tk.LabelFrame(root,text ='Open File')
file_frame.place(height = 200,width =600,rely =0.65,relx = 0)


#buttons
button1 = tk.Button(file_frame,text = 'Save Data',command = lambda: save_data())
button1.place(rely = 0.7, relx = 0.65)


button2 = tk.Button(file_frame,text='Run',command = lambda: excecute())
button2.place(rely = 0.3,relx=0.65)


#labels
bend_label = ttk.Label(file_frame,text = 'Current Bend: None')
bend_label.place(rely=0,relx=0)


phi_label = tk.Label(file_frame,text = 'Phi value (deg):')
phi_label.place(rely=0.2,relx=0)


beta_label = tk.Label(file_frame,text = 'Beta value (deg):')
beta_label.place(rely = 0.2,relx = 0.3)


save_data_label = tk.Label(file_frame,text ='File name to save data as:')
save_data_label.place(rely = 0.6,relx = 0.3)

#entry boxes
phi_entry = tk.Entry(master = file_frame)
phi_entry.place(rely=0.35,relx=0)


beta_entry = tk.Entry(file_frame)
beta_entry.place(rely = 0.35,relx = 0.3)

save_data_entry = tk.Entry(file_frame)
save_data_entry.place(rely = 0.75,relx=0.3)





#treeview widget

tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1,relwidth=1)

tree_scroll_y = tk.Scrollbar(frame1, orient = 'vertical',command = tv1.yview)
tree_scroll_x = tk.Scrollbar(frame1,orient = 'horizontal',command = tv1.xview)
tv1.configure(xscrollcommand = tree_scroll_x.set,yscrollcommand = tree_scroll_y.set)
tree_scroll_x.pack(side = 'bottom',fill = 'x')
tree_scroll_y.pack(side = 'right',fill='y')



def file_dialog():
    filename = filedialog.askopenfilename(initialdir ='/',
        title='Select a file',
        filetypes=(('xlsx files','*.xlsx'),('All Files','*.*')))
    label_file['text'] = filename
    return None

def save_data():
    file_name = save_data_entry.get()
    result = messagebox.askquestion('Save As',"Do you want to save the data as " + file_name+'.csv?')
    if result == 'yes':
        phi = phi_entry.get()
        beta = beta_entry.get()
        df = dna_bend(float(phi),float(beta))
        df.to_csv(file_name+'.csv',index = False)
        return None
    else:
        pass


def excecute():
    try:
        phi = phi_entry.get()
        beta = beta_entry.get()
        df = dna_bend(float(phi),float(beta))
    except ValueError:
        tk.messagebox.showerror("Information", "The values you have entered are invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    bend_label['text'] = 'Current Bend: Phi = {phi} deg, Beta = {beta} deg'.format(phi = phi,beta = beta)
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None



def clear_data():
    tv1.delete(*tv1.get_children())







root.mainloop()
