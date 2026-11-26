from tkinter import *
from tkinter import ttk
import csv
from tkinter import messagebox
from passwords_and_checking import changePassword

def adminGUI():
    admingui = Tk()
    admingui.geometry('800x600')
    admingui.title('Admin Mode')

    notebook = ttk.Notebook(admingui)
    notebook.pack(expand=True, fill='both')

    # --- TAB FRAMES
    tab1 = Frame(notebook)  # library view
    tab2 = Frame(notebook)  # adjust and make changes to books
    tab3 = Frame(notebook)  # add books
    tab4 = Frame(notebook)  # create promo codes
    tab5 = Frame(notebook)  # profits from guest purchases
    tab6 = Frame(notebook)  # user reports
    tab7 = Frame(notebook)  # change password

    notebook.add(tab1, text='Library View')
    notebook.add(tab2, text='Adjust Book')
    notebook.add(tab3, text='Add Book')
    notebook.add(tab4, text='Promo Codes')
    notebook.add(tab5, text='Profits')
    notebook.add(tab6, text='User Reports')
    notebook.add(tab7, text='Change Password')

    # --- SIMPLE TREEVIEW FUNCTION
    def treeview(tab, csvfile):
        libraryTable = ttk.Treeview(tab, columns=('1', '2', '3', '4', '5',), show='headings')
        libraryTable.heading('1', text='Title')
        libraryTable.heading('2', text='Category')
        libraryTable.heading('3', text='Price')
        libraryTable.heading('4', text='Quantity')
        libraryTable.heading('5', text='Rating')
        libraryTable.pack()

        # load data
        data_list = []
        try:
            with open(csvfile, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for row in reader:
                    libraryTable.insert('', END, values=row)
                    data_list.append(row)
        except FileNotFoundError:
            messagebox.showwarning("Warning", f"{csvfile} not found!")
        return libraryTable, data_list

    # --- Tab 1 [] Library View
    Label(tab1, text="Library").pack(pady=10)
    libraryTree, libraryData = treeview(tab1, 'library.csv')

    # --- Tab 2 [] Adjust Book
    Label(tab2, text="Select a book to adjust").pack(pady=10)
    adjustTree, adjustData = treeview(tab2, 'library.csv')

    adjust_entries = {}
    for field in ('Title','Category','Price','Quantity','Rating'):
        Label(tab2, text=field).pack()
        adjust_entries[field] = Entry(tab2)
        adjust_entries[field].pack()

    def loadSelectedBook():
        sel = adjustTree.selection()
        if not sel:
            return
        vals = adjustTree.item(sel[0])['values']
        for i, field in enumerate(('Title','Category','Price','Quantity','Rating')):
            adjust_entries[field].delete(0, END)
            adjust_entries[field].insert(0, vals[i])

    Button(tab2, text="Load Selected", command=loadSelectedBook).pack(pady=5)

    def saveAdjustment():
        sel = adjustTree.selection()
        if not sel:
            return
        updated_rows = []
        with open('library.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            updated_rows.append(header)
            for row in reader:
                if row[0] == adjustTree.item(sel[0])['values'][0]:
                    row = [adjust_entries[field].get() for field in ('Title','Category','Price','Quantity','Rating')]
                updated_rows.append(row)
        with open('library.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
        messagebox.showinfo("Saved","Book updated!")
        # refresh tree
        for item in adjustTree.get_children():
            adjustTree.delete(item)
        for row in updated_rows[1:]:
            adjustTree.insert('', END, values=row)

    Button(tab2, text="Save Adjustment", command=saveAdjustment).pack(pady=5)

    # --- Tab 3 [] Add Book
    Label(tab3, text="Add New Book").pack(pady=10)
    add_entries = {}
    for field in ('Title','Category','Price','Quantity','Rating'):
        Label(tab3, text=field).pack()
        add_entries[field] = Entry(tab3)
        add_entries[field].pack(pady=2)

    def addBook():
        new_row = [add_entries[field].get() for field in ('Title','Category','Price','Quantity','Rating')]
        with open('library.csv','a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        messagebox.showinfo("Added","Book added!")
        for e in add_entries.values():
            e.delete(0, END)

    Button(tab3, text="Add Book", command=addBook).pack(pady=5)

    # --- Tab 4 [] Promo Codes
    Label(tab4, text="Create Promo Code").pack(pady=10)
    promo_entry = Entry(tab4)
    promo_entry.pack()
    discount_entry = Entry(tab4)
    discount_entry.pack()
    Label(tab4, text="Enter discount %").pack()

    def addPromo():
        with open('promos.csv','a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([promo_entry.get(), discount_entry.get()])
        messagebox.showinfo("Added","Promo added!")
        promo_entry.delete(0,END)
        discount_entry.delete(0,END)

    Button(tab4, text="Add Promo", command=addPromo).pack(pady=5)

    # --- Tab 5 [] Profits
    Label(tab5, text="Profits from Orders").pack(pady=10)

    profitsTree = ttk.Treeview(tab5, columns=(
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), show='headings')
    profitsTree.heading('1', text='Title')
    profitsTree.heading('2', text='Category')
    profitsTree.heading('3', text='Price')
    profitsTree.heading('4', text='Quantity')
    profitsTree.heading('5', text='Customer First')
    profitsTree.heading('6', text='Customer Last')
    profitsTree.heading('7', text='Address')
    profitsTree.heading('8', text='Phone')
    profitsTree.heading('9', text='Discount %')
    profitsTree.heading('10', text='Total Paid')
    profitsTree.pack()

    # --- TAG: Load orders manually and map columns correctly
    try:
        with open('orders.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # skip incomplete rows
                if len(row) < 11:
                    continue

                # map CSV -> Treeview exactly like receipt
                title = row[0]
                category = row[1]
                price = float(row[2])
                quantity = int(row[3])
                first = row[5]
                last = row[6]
                address = row[7]
                phone = row[8]
                discount = float(row[9])
                total_paid = float(row[10])

                profitsTree.insert('', END, values=[
                    title,
                    category,
                    f"{price:.2f}",
                    quantity,
                    first,
                    last,
                    address,
                    phone,
                    f"{discount:.2f}",
                    f"{total_paid:.2f}"
                ])
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No orders yet.")

    # --- Tab 6 [] User Reports
    Label(tab6, text="User Reports").pack(pady=10)
    reportsTree, reportsData = treeview(tab6, 'reports.csv')

    # --- Tab 7 [] Change Password
    Label(tab7, text="Admin Security").pack(pady=20)
    Button(tab7, text="Change Admin Password", command=changePassword).pack(pady=10)

    admingui.mainloop()
