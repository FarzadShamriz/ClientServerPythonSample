import socket
import traceback

customers = {}
with open("data.txt") as file_in:
    for line in file_in:
        splitetLine = line.split("|")
        if len(splitetLine) > 0:
            customerName = splitetLine[0].strip().replace(",","-")
            if not customerName:
                continue
            customerAge = ""
            customerAddress = ""
            customerPhone = ""
            if len(splitetLine) > 1:
                customerAge = splitetLine[1].strip().replace(",","-")
            if len(splitetLine) > 2:
                customerAddress = splitetLine[2].strip().replace(",","-")
            if len(splitetLine) > 3:
                customerPhone = splitetLine[3].strip().replace(",","-")
            customers[customerName.lower()] = {'name': customerName,
                                   'age':customerAge,
                                   'address':customerAddress,
                                   'phone': customerPhone}
        else:
            continue
try:
    while True:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.bind(('localhost', 9999))
        conn.listen(5)
        print("Server is listennig now")
        clientsocket, address = conn.accept()
        while True:
            userInput = ""
            userInput = clientsocket.recv(8000)
            userInput = userInput.decode("UTF-8")
            if not userInput:
                break
            elif ("MAINMENUREQ" in userInput):
                clientsocket.send(bytes("""        1: Find customer
        2: Add customer
        3: Delete customer
        4: Update customer age
        5: Update customer address
        6: Update customer phone
        7: Print report
        8: Exit
        ============================""", "UTF-8"))
                serverLog = "MAINMENUPRINT"
            elif ("ADDCUSTOMER" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                pipeSplitetUserInput = splitedUserInput[1].split("|")
                customerNameToAdd = pipeSplitetUserInput[0]
                customerAgeToAdd = pipeSplitetUserInput[1]
                customerAddressToAdd = pipeSplitetUserInput[2]
                customerPhoneToAdd = pipeSplitetUserInput[3]
                if (customerNameToAdd in customers.keys()):
                    clientsocket.send(bytes("There is a customer with the same name exist in list.", "UTF-8"))
                else:
                    customers[customerNameToAdd] = {'name': customerNameToAdd,
                                                    'age': customerAgeToAdd,
                                                    'address': customerAddressToAdd,
                                                    'phone': customerPhoneToAdd}
                    clientsocket.send(
                        bytes("Customer " + customerNameToAdd + " is successfully added to the list.", "UTF-8"))
                serverLog = "ADDCUSTOMER"
            elif ("DELETECUSTOMER" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                customerNameKeyToDelete = splitedUserInput[1]
                if not (customerNameKeyToDelete in customers.keys()):
                    clientsocket.send(bytes("Customer Not Found.", "UTF-8"))
                else:
                    del customers[customerNameKeyToDelete]
                    clientsocket.send(bytes("Customer " + customerNameKeyToDelete + " successfully deleted.", "UTF-8"))
                serverLog = "DELETECUSTOMER"
            elif ("UPDATEAGE" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                customerNameToUpdateAge = splitedUserInput[1]
                customerNewAgeToUpdate = splitedUserInput[2]
                if not (customerNameToUpdateAge in customers.keys()):
                    clientsocket.send(bytes("Customer Not Found.", "UTF-8"))
                else:
                    customers.get(customerNameToUpdateAge, "").update(age=customerNewAgeToUpdate)
                    clientsocket.send(
                        bytes(customerNameToUpdateAge + "'s age changed to " + customerNewAgeToUpdate, "UTF-8"))
                serverLog = "UPDATEAGE"
            elif ("UPDATEADDRESS" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                customerNameToUpdateAddress = splitedUserInput[1]
                customerNewAddressToUpdate = splitedUserInput[2]
                if not (customerNameToUpdateAddress in customers.keys()):
                    clientsocket.send(bytes("Customer Not Found.", "UTF-8"))
                else:
                    customers.get(customerNameToUpdateAddress, "").update(address=customerNewAddressToUpdate)
                    clientsocket.send(
                        bytes(customerNameToUpdateAddress + "'s address changed to " + customerNewAddressToUpdate, "UTF-8"))
                serverLog = "UPDATEADDRESS"
            elif ("UPDATEPHONE" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                customerNameToUpdatePhone = splitedUserInput[1]
                customerNewPhoneToUpdate = splitedUserInput[2]
                if not (customerNameToUpdatePhone in customers.keys()):
                    clientsocket.send(bytes("Customer Not Found.", "UTF-8"))
                else:
                    customers.get(customerNameToUpdatePhone, "").update(phone=customerNewPhoneToUpdate)
                    clientsocket.send(
                        bytes(customerNameToUpdatePhone + "'s phone number changed to " + customerNewPhoneToUpdate,
                              "UTF-8"))
                serverLog = "UPDATEPHONE"
            elif ("FINDCUSTOMER" in userInput):
                splitedUserInput = ""
                splitedUserInput = userInput.split(",")
                customerNameKey = splitedUserInput[1]
                if not (customerNameKey in customers.keys()):
                    clientsocket.send(bytes("Customer not found.", "UTF-8"))
                else:
                    resultCustomerFound = customers.get(customerNameKey, "Customer not found.")
                    userRetInfo = "name: " + resultCustomerFound['name'] + " Age: " + resultCustomerFound[
                        'age'] + " Address: " + resultCustomerFound['address'] + "Phone Number: " + resultCustomerFound['phone']
                    clientsocket.send(bytes(userRetInfo, "UTF-8"))
                serverLog = "FINDCUSTOMER"
            elif ("PRINTREPORT" in userInput):
                splitedUserInput = ""
                tableForPrintReport = " ------------------------------------------------------------------------------------------------- " + '\n'
                tableForPrintReport += "|        Name        | Age |                      Address                     |   Phone Number     |" + '\n'
                tableForPrintReport += " ------------------------------------------------------------------------------------------------- " + '\n'
                for customerItem in customers:
                    customerItemValue = customers.get(customerItem, "")
                    customerNameForTableReport = ("{:<20}".format(customerItemValue['name']))
                    customerAgeForTableReport = ("{:<5}".format(customerItemValue['age']))
                    customerAddressForTableReport = ("{:<50}".format(customerItemValue['address']))
                    customerPhoneForTableReport = ("{:<20}".format(customerItemValue['phone']))
                    tableForPrintReport += "|" + customerNameForTableReport + "|"
                    tableForPrintReport += customerAgeForTableReport + "|"
                    tableForPrintReport += customerAddressForTableReport + "|"
                    tableForPrintReport += customerPhoneForTableReport + "|" + '\n'
                tableForPrintReport += " ------------------------------------------------------------------------------------------------- "
                clientsocket.send(bytes(tableForPrintReport, "UTF-8"))
                serverLog = "PRINTREPORT"
            print(serverLog)
except:
    print("Server stopped!!! {}".format(traceback.format_exc()))
