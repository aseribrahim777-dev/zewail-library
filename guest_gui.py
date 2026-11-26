import csv
from tkinter import *
from tkinter import ttk

def guestGUI(parentWindow):

    # Library Functions and Logic
    # def fillLibrary(filter_text=None):


    # PREPARING
    # CLEANS BUY LIST WHEN GUESTGUI OPENS
    with open('buylist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Category', 'Price'])  # keep headers only


    parentWindow.destroy()
    guestgui = Tk()
    guestgui.geometry('1200x600')
    guestgui.title('Guest')

    notebook1 = ttk.Notebook(guestgui)  # Widget that manages a collection of windows and displays

    # Frame = a rectangular container to group and hold widgets together
    tab_1 = Frame(notebook1)  # welcome
    tab_2 = Frame(notebook1)  # library
    tab_3 = Frame(notebook1)  # store - filter - add to buy list
    tab_4 = Frame(notebook1)  # buylist - checkout
    tab_5 = Frame(notebook1)  # rating
    tab_6 = Frame(notebook1)  # report
    notebook1.pack(expand=True, fill='both')

    # --- Tab 1 WELCOME TAB
    notebook1.add(tab_1, text='Welcome')
    label1 = Label(tab_1, text='Hi! Welcome to Zewail Library!', font=('Arial', 20))
    label1.pack()

    ##############################

    # --- Tab 2 VIEW LIBRARY
    notebook1.add(tab_2, text='Library')
    label1 = Label(tab_2, text='Library', padx=10, pady=10)
    label1.pack()

    # Tab 2 - tree view function block
    def treeview(tab, csvfile):
        libraryTable = ttk.Treeview(tab, columns=('1', '2', '3', '4', '5',), show='headings')
        libraryTable.heading('1', text='Title')
        libraryTable.heading('2', text='Category')
        libraryTable.heading('3', text='Price')
        libraryTable.heading('4', text='Quantity')
        libraryTable.heading('5', text='Rating')
        libraryTable.pack()

        # Tab 2 - insert the data to tree view
        library = []
        with open(csvfile, 'r') as file:
            data = csv.reader(file)
            next(data)  # skips the first row cause its labels
            for row in data:
                library.append(row)
                libraryTable.insert(parent='', index=END, values=row)
        return libraryTable, library

    # Create Treeview for Tab 2
    libraryTable, library = treeview(tab_2, 'library.csv')

    ##############################

    # --- Tab 3 ----
    notebook1.add(tab_3, text='Store')

    # Tab 3 - filtering categories
    # calls tree view function block
    label1 = Label(tab_3, text='Book List')
    label1.pack(padx=10, pady=10)
    libraryTableFilter, libraryFilter = treeview(tab_3, 'library.csv')

    # combobox for filtering
    categories = ['All', 'Programming', 'Technology', 'Fiction', 'Kids', 'Science', 'History', 'Cooking']
    category_var = StringVar()
    category_var.set('All')

    # to seperate by text
    labelseperator = Label(tab_3, text='Filter')
    labelseperator.pack(padx=10, pady=10)

    category_menu = ttk.Combobox(tab_3, textvariable=category_var, values=categories)
    category_menu.pack()

    # Filter function uses the already existing Treeview & data
    def filterCategory(event=None):
        selected = category_var.get()
        # clear current rows
        for row in libraryTableFilter.get_children():
            libraryTableFilter.delete(row)
        # insert rows that match
        for row in libraryFilter:
            cat = row[1]
            if selected == 'All' or cat == selected:
                libraryTableFilter.insert('', END, values=row)

    # Bind combobox
    category_menu.bind('<<ComboboxSelected>>', filterCategory)

    # --- Tab 3 [] add to buy list ----

    def addSelectedToBuylist():

        selected_items = libraryTableFilter.selection()
        if not selected_items:
            return  # nothing selected

        quantity_str = quantity_entry.get()
        if not quantity_str.isdigit() or int(quantity_str) <= 0:
            quantity_str = 1  # fallback to 1 if invalid input

        with open('buylist.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for item in selected_items:
                row = libraryTableFilter.item(item)['values']  # Get the actual data from the selected row in the Treeview
                # fetches current stock
                available_quantity = int(row[3])
                # checks current stock if the number is stupid
                if int(quantity_str) > available_quantity:
                    quantity_str = str(available_quantity)
                # internally 'values' is the list of columns for that row
                writer.writerow([row[0], row[1], row[2], quantity_str])
                # Writes that list of values as a new row into the CSV file buylist.csv
                libraryTableBuylist.insert('', END, values=[row[0], row[1], row[2], quantity_str]) # UPDATES the buy list

    labelq = Label(tab_3, text='Quantity')
    labelq.pack()
    quantity_entry = Entry(tab_3)
    quantity_entry.pack(padx=10, pady=5)
    quantity_entry.insert(0, "1")  # default quantity = 1

    add_button = Button(tab_3, text="Add Selected to Buylist", command=addSelectedToBuylist)
    add_button.pack(padx=10, pady=10)

    ###########################

    # --- Tab 4 [] Buy List ----
    notebook1.add(tab_4, text='Buylist')
    Label(tab_4, text='BuyList').pack(padx=10, pady=10)

    # Treeview for Buylist
    libraryTableBuylist, libraryBuylist = treeview(tab_4, 'buylist.csv')

    # Entry fields for user info
    Label(tab_4, text='First Name').pack(padx=10, pady=2)
    first_name_entry = Entry(tab_4)
    first_name_entry.pack(padx=10, pady=2)

    Label(tab_4, text='Last Name').pack(padx=10, pady=2)
    last_name_entry = Entry(tab_4)
    last_name_entry.pack(padx=10, pady=2)

    Label(tab_4, text='Address').pack(padx=10, pady=2)
    address_entry = Entry(tab_4, width=50)
    address_entry.pack(padx=10, pady=2)

    Label(tab_4, text='Phone Number').pack(padx=10, pady=2)
    phone_entry = Entry(tab_4)
    phone_entry.pack(padx=10, pady=2)

    # --- Promo Code Entry
    Label(tab_4, text='Promo Code').pack(padx=10, pady=2)
    promo_code_entry = Entry(tab_4)
    promo_code_entry.pack(padx=10, pady=2)

    TAX_RATE = 0.14  # 14% tax example

    def submitBuylist():
        first = first_name_entry.get().strip()
        last = last_name_entry.get().strip()
        address = address_entry.get().strip()
        phone = phone_entry.get().strip()

        if not (first and last and address and phone):
            return  # stop if any info missing

        # Prepare order list and calculate subtotal
        order_rows = []
        subtotal = 0
        for item in libraryTableBuylist.get_children():
            row = libraryTableBuylist.item(item)['values']
            title, category, price, quantity = row[0], row[1], float(row[2]), int(row[3])
            total_price = price * quantity
            subtotal += total_price
            order_rows.append([title, category, price, quantity, total_price])

        tax = subtotal * TAX_RATE
        total_before_discount = subtotal + tax

        # --- Promo code application
        entered_code = promo_code_entry.get().strip()
        discount_percent = 0
        try:
            with open('promos.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    code, percent = row
                    if code == entered_code:
                        discount_percent = float(percent)
                        break
        except FileNotFoundError:
            pass  # no promo file, ignore

        discount_amount = total_before_discount * (discount_percent / 100)
        total_after_discount = total_before_discount - discount_amount

        # Save order including discount
        with open('orders.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for row in order_rows:
                writer.writerow(row + [first, last, address, phone, discount_percent, total_after_discount])

        # Clear buylist tree
        for item in libraryTableBuylist.get_children():
            libraryTableBuylist.delete(item)

        # Reset entry fields
        first_name_entry.delete(0, END)
        last_name_entry.delete(0, END)
        address_entry.delete(0, END)
        phone_entry.delete(0, END)
        promo_code_entry.delete(0, END)

        # Display receipt
        receipt_window = Toplevel()
        receipt_window.title("Receipt")
        receipt_text = f"Receipt for {first} {last}\nAddress: {address}\nPhone: {phone}\n\n"
        receipt_text += "Items:\n"
        for row in order_rows:
            receipt_text += f"{row[0]} | {row[1]} | ${row[2]:.2f} x {row[3]} = ${row[4]:.2f}\n"

        receipt_text += f"\nSubtotal: ${subtotal:.2f}\nTax (14%): ${tax:.2f}\nDiscount: {discount_percent}% (-${discount_amount:.2f})\nTotal: ${total_after_discount:.2f}\nThank you for using our service!"
        Label(receipt_window, text=receipt_text, justify=LEFT, padx=10, pady=10).pack()

    submit_button = Button(tab_4, text="Submit Order", command=submitBuylist)
    submit_button.pack(pady=10)

    ######################################

    # --- Tab 5 Rate a book
    notebook1.add(tab_5, text='Rate Book')

    Label(tab_5, text='Select a book to rate [1-5]').pack(padx=10, pady=10)

    libraryTableRate, libraryRate = treeview(tab_5, 'library.csv')
    rating_entry = Entry(tab_5)
    rating_entry.pack()

    def submitRating():
        selected = libraryTableRate.selection()
        if not selected:
            return # no book is selected

        user_rating = rating_entry.get()
        if not user_rating.isdigit() or not 1 <= int(user_rating) <= 5:
            return
        # FETCH SELECTED BOOK TITLE
        item = selected[0]
        values = libraryTableRate.item(item)['values']
        selected_title = values[0]

        updated_rows = []

        with open('library.csv', 'r')as file:
            data = csv.reader(file)
            header = next(data)
            updated_rows.append(header)

            for row in data:
                title = row[0]
                ratings = row[4]
                if title == selected_title:
                    if ratings:
                        ratings = ratings + '|' + user_rating
                    else:
                        ratings = user_rating
                    row[4] = ratings
                updated_rows.append(row)

        with open('library.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        for row in libraryTableRate.get_children():
            libraryTableRate.delete(row)

        with open('library.csv', 'r') as file:
            data = csv.reader(file)
            next(data)  # skip headers
            for row in data:
                libraryTableRate.insert('', END, values=row)

        rating_entry.delete(0, END)

    Button(tab_5, text="Submit Rating", command=submitRating).pack(pady=10)

    # --- Tab 6 Report a problem
    notebook1.add(tab_6, text='Report Problem')

    Label(tab_6, text="Describe the problem:").pack(padx=10, pady=10)

    report_text = Text(tab_6, width=60, height=10)
    report_text.pack(padx=10, pady=10)

    def submitReport():
        report = report_text.get("1.0", END).strip()
        if not report:
            return  # empty report, ignore

        # create file if it doesn't exist, append otherwise
        with open('reports.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([report])

        report_text.delete("1.0", END)

    Button(tab_6, text="Submit Report", command=submitReport).pack(pady=10)

    guestgui.mainloop()
