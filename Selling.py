import customtkinter as ctk 
import tkinter as tk
from tkinter  import messagebox as msg
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import MySQLdb as mdb

DBNAME="sql8655292"
DBHOST="sql8.freemysqlhosting.net"
DBPASS="DHPiKHZmdY"
DBUSER="sql8655292"


root =ctk.CTk()
root.geometry('331x700')
root .title("Selling")
my_image = None

label =ctk.CTkLabel(root, text=" Add Product to your Store  ", font =ctk.CTkFont(size=22, weight="bold"))
label.pack(padx=10,pady=(40,20))

item_info=ctk.CTkLabel(root, text="Please fill the required information :")
item_info.pack( padx=2, pady=10)


#imaaage  uplaod


def open():
    global my_image
    root.filename= filedialog.askopenfilename(initialdir="/Gallery" ,title="Select A File", filetypes=(("All files", "*"),("all files","*")))
    my_label=Label(root,text=root.filename)
    my_image=ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label=Label(image=my_image).place(x=340,y=270)

 
my_btn= Button(root,text="Choose Photo", command= open) .place(x=340,y=358)


#item name and its entry
# 
#
item_name_label = ctk.CTkLabel(root, text="Item Name",font =ctk.CTkFont(size=12,weight="bold"))
item_name_label.place(x=50,y=150)
#Entrys
productName = ctk.CTkEntry(root)
productName.place(x=50,y=177)


# Curanccy
Currency_label = ctk.CTkLabel(root, text="Currency",font =ctk.CTkFont(size=12,weight="bold"))
Curanccy = ctk.CTkComboBox(root, values=["", "SAR", "USD", "EUR"])
Currency_label.place(x=193,y=266)
Curanccy.place(x=193,y=290)


#price
price1= ctk.CTkLabel(root, text="Price",font =ctk.CTkFont(size=12,weight="bold"))
price1.place(x=50,y=266)
Price = ctk.CTkEntry(root)
Price.place(x=50,y=290)


#Category
Category_label = ctk.CTkLabel(root, text="Category",font =ctk.CTkFont(size=12,weight="bold"))
Category = ctk.CTkComboBox(root, values=["", "paper", "clothes", "Glass","Metal","Bottle","Textile"])
Category_label.place(x=50,y=209)
Category.place(x=50,y=232)


#Quantity 
Quantity_label = ctk.CTkLabel(root, text="Quantity",font =ctk.CTkFont(size=12,weight="bold"))
Quantity = ctk.CTkComboBox(root, values=["", "1", "2", "3","4","5","6"])
Quantity_label.place(x=50,y=318)
Quantity.place(x=50,y=347)



#decrpition textbox
label3 =ctk.CTkLabel(root, text=" Description: ",font =ctk.CTkFont(size=12,weight="bold"))
label3.place(x=50,y=375)
Description =ctk.CTkTextbox(root,height=130,width=197)
Description.place(x=50,y=400)

# checking step if the field empty or not
def validate_and_save_info():
    
    validation_conditions = [
        (productName.get(), "Product Name is required."),
        (Price.get(), "Price is required."),
        (Curanccy.get(), "Currency is required."),
        (Quantity.get(), "Quantity is required.")
    ]

    for value, error_message in validation_conditions:
        if not value:
            msg.showerror("Error", error_message)
            return

    # If all fields are filled, proceed to save the data
    save_info(productName.get(), Description.get("1.0", "end-1c"), Price.get(), Curanccy.get(), Quantity.get(), Category.get(), my_image)




# buttons
b1 = ctk.CTkButton(root, text="Add to the store", width=200, command=validate_and_save_info)
b1.place(x=120, y=558)
button2 = ctk.CTkButton(root, text="Cancel", width=90, command=root.destroy)  # Added command to close the application
button2.place(x=23, y=558)


def save_info(productName, Description, Price, Curanccy, Quantity,Category, my_image):
    db= mdb.connect(DBHOST,DBUSER,DBPASS,DBNAME)
    cur =db.cursor()
    print("connected") 


    check_query = "SELECT productName FROM Product WHERE productName = %s"
    cur.execute(check_query, (productName,))
    existing_product = cur.fetchone()
    if existing_product:
        msg.showinfo("Product Already Exists", f"The product '{productName}' already exists in the database.")
    
    else:
        insert = "INSERT INTO Product (productName, Description, Price, Curanccy,Quantity, Category, Image) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        values = (productName, Description, Price, Curanccy,Quantity ,Category, my_image)

        try:
            cur.execute(insert,values)
            db.commit()
        except Exception as e:
            print("was a error "+str(e))
        
    db.close()
    msg.showinfo("Data saved sucessefully" , "Data Saved")
root.mainloop()