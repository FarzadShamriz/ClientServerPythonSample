#!/usr/bin/python3

import socket
import sys

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('localhost', 9999))
    conn.sendall(("MAINMENUREQ").encode("UTF-8"))
    mainMenu = conn.recv(1024).decode("UTF-8")
    while True:
        # while True:
        inputMenuValue = getMenuInput(mainMenu)
        if (int(inputMenuValue) == 1):
            customerNameForRet = getCustomerNameToFind()
            conn.sendall(("FINDCUSTOMER,"+customerNameForRet.lower()).encode("UTF-8"))
            responseServerDB = conn.recv(1024).decode("UTF-8")
            print(customerNameForRet+"""'s detail: """)
            print("     "+responseServerDB)
            print("-----------------------------------")
        elif (int(inputMenuValue) == 2):
            customerDetailToAdd = getCustomerDetailToAdd()
            if not (customerDetailToAdd == ""):
                conn.sendall(("ADDCUSTOMER,"+customerDetailToAdd).encode("UTF-8"))
                responseServerDB = conn.recv(1024).decode("UTF-8")
                print(responseServerDB)
                print("-----------------------------------")
        elif (int(inputMenuValue) == 3):
            customerNametoDelete = getCustomerNameToDelete()
            conn.sendall(("DELETECUSTOMER," + customerNametoDelete.lower()).encode("UTF-8"))
            responseServerDB = conn.recv(1024).decode("UTF-8")
            print(responseServerDB)
        elif (int(inputMenuValue) == 4):
            customerNameForUpdate = getCustomerNameForUpdate()
            if not (customerNameForUpdate.replace(" ","") == ""):
                customerAgeToUpdate = input("Enter new age for update:")
                conn.sendall(("UPDATEAGE,"+customerNameForUpdate+","+customerAgeToUpdate.replace(" ","")).encode("UTF-8"))
                responseServerDB = conn.recv(8000).decode("UTF-8")
                print(responseServerDB)
        elif (int(inputMenuValue) == 5):
            customerNameForUpdate = getCustomerNameForUpdate()
            if not (customerNameForUpdate.replace(" ", "") == ""):
                customerAddressToUpdate = input("Enter new address for update:")
                conn.sendall(("UPDATEADDRESS," + customerNameForUpdate + "," + customerAddressToUpdate.replace(" ", "")).encode("UTF-8"))
                responseServerDB = conn.recv(8000).decode("UTF-8")
                print(responseServerDB)
        elif (int(inputMenuValue) == 6):
            customerNameForUpdate = getCustomerNameForUpdate()
            if not (customerNameForUpdate.replace(" ", "") == ""):
                customerAddressToUpdate = input("Enter new phone number for update:")
                conn.sendall(("UPDATEPHONE," + customerNameForUpdate + "," + customerAddressToUpdate.strip()).encode("UTF-8"))
                responseServerDB = conn.recv(8000).decode("UTF-8")
                print(responseServerDB)
        elif (int(inputMenuValue) == 7):
            conn.sendall(("PRINTREPORT").encode("UTF-8"))
            responseServerDB = conn.recv(8000).decode("UTF-8")
            print(responseServerDB)
        elif (int(inputMenuValue) == 8):
            conn.close()
            print("Good bye")
            sys.exit()

def getCustomerNameToFind():
    while True:
        customerNameToFind = input("Enter Customer Name to find: ")
        if not (customerNameToFind.replace(" ","") == ""):
            return customerNameToFind.lower().replace(",","-")

def getCustomerNameForUpdate():
    while True:
        customerNameToFind = input("Enter Customer Name to find "+'\n'+"or enter blank to go to main menu: ")
        if not (customerNameToFind.replace(" ","") == ""):
            return (customerNameToFind.lower().replace(",","-"))
    return ""

def tryParseInt(numberForParse):
    try:
        (int(numberForParse))
        return True
    except:
        return False

def getCustomerNameToDelete():
    while True:
        customerNameToDelete = input("Enter Customer Name to find: ")
        if not (customerNameToDelete.replace(" ","") == ""):
            return customerNameToDelete.lower().replace(",","-")

def getCustomerDetailToAdd():
    print("""Here we need the customer info to add.
    Name of customer is required.
    To Go back to the menu put 0 (Zero number) for customer name""")
    customerNameToAdd = ""
    while True:
        customerNameToAdd = input("Customer Name: ")
        if not (customerNameToAdd.replace(" ","") == ""):
            break
        else:
            print("Customer name cannot be blank.")
    if not (customerNameToAdd == "0"):
        customerAgeToAdd = input("Customer Age: ")
        customerAddressToAdd = input("Customer Address: ")
        customerPhoneToAdd = input("Customer Phone:")
        customerConcatinatedDetailsToAdd = customerNameToAdd.lower().replace(",","-")+"|"+customerAgeToAdd.replace(",","-")+"|"+customerAddressToAdd.replace(",","-")+"|"+customerPhoneToAdd.replace(",","-")
        return customerConcatinatedDetailsToAdd
    else:
        return ""


def getMenuInput(mainMenu):
    while True:
        print(mainMenu)
        selectValueItem = input("Select: ")
        if not ((tryParseInt(selectValueItem))):
            print("""Your should select a number,
    do not enter alphabets""")
        elif ((int(selectValueItem) < 1) or (int(selectValueItem) > 8)):
            print("Invalid input, enter your select item in range (1-8).")
        else:
            return selectValueItem


main()