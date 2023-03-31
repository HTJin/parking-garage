from datetime import timedelta, date, datetime
from time import sleep

class Garage():
    RATE = 3.50
    def __init__(self, name, tickets_available):
        self.garage_name = name
        self.tickets_available = tickets_available
        self.current_customers = [] # [{'licenseplate'}]
    
    def takeTicket(self):
        print()
        going = True
        while going:
            vehicle = input("License plate number? ").lower().strip()
            if len(self.current_customers) > 0:
                for customer in self.current_customers:
                    if customer.plate == vehicle:
                        print("This vehicle is already registered with a ticket. Input license plate number again.")
                    else:
                        going = False
            else:
                going = False
        customer = Customer(vehicle)
        self.current_customers.append(customer)
        self.tickets_available -= 1
        print(f"Your ticket has been created with your license plate, {vehicle}")

    def payForParking(self):
        print("\nPAYMENT MENU >")
        going = True
        while going:
            print()
            search_plate = input("What's your license plate number? ").lower().strip()
            for customer in self.current_customers:
                if customer.plate == search_plate:
                    print(f"We found your vehicle with the license plate {search_plate}")
                    elapsed_time = customer.calculate_time()
                    cost_per_time = self.RATE * elapsed_time
                    print(f"\nYou will be charged ${cost_per_time:.2f} for your stay of {elapsed_time:.2f} hours!")
                    while True:
                        pay = input("Are you ready to check out? [y/n] ").lower().strip()
                        if pay == 'y':
                            customer.paid = True
                            self.current_customers.remove(customer)
                            self.tickets_available += 1
                            print("Thanks, have a nice day!")
                            going = False
                            break
                        elif pay == 'n':
                            print("You've decided to pay for the ticket later. Bye")
                            going = False
                            break
                        else:
                            print("Invalid response, try again.")
                    break
            else:
                print("You entered the wrong license plate number, try again!")
    
    def __repr__(self):
        return f"Hello, welcome to {self.garage_name}! We have {self.tickets_available} spaces available!\nWe charge ${self.RATE:.2f} per hour."
    
    def leaveGarage(self):
        for customer in self.current_customers:
            if customer.paid:
                self.current_customers.remove(customer)
                self.tickets_available += 1
                print("Thanks, have a nice day!")
            else:
                print("Looks like you have not paid for your ticket yet.")
                self.payForParking()

    def run(self):
        print(self.__repr__())
        going = True
        while going:
            print(f"\n[-- You have reached {self.garage_name}'s Parking Kiosk --]")
            print("MAIN MENU >\n")
            response = input("Take a ticket or leave? [take, pay, leave] ").lower()
            if response == 'take':
                if self.tickets_available > 0:
                    self.takeTicket()
                else:
                    print("Sorry there are no more spaces available, try coming back later!")
            elif response == 'pay':
                if len(self.current_customers) > 0:
                    self.payForParking()
                    for customer in self.current_customers:
                        if customer.paid:
                            going = False
                else:
                    print("There's no car in the garage, please go take a ticket!")
            elif response == 'leave':
                if len(self.current_customers) <= 0:
                    print("No one's been here, you just chose to leave. Goodbye.")
                    going = False
                else:
                    self.leaveGarage()
                    for customer in self.current_customers:
                        if customer.paid:
                            print("Alright, you're leaving us. Bye.")
                            going = False
            else:
                print("Invalid input. Please try again.")            
    
class Customer():
    def __init__(self, plate):
        self.plate = plate
        self.start_time = datetime.now()
        self.end_time = float('inf')
        self.paid = False

    def calculate_time(self):
        self.end_time = datetime.now()
        return (self.end_time - self.start_time).total_seconds()

our_garage = Garage('GARAGELAND', 2)
our_garage.run()
# randomguy = Customer('28382891')
# print(randomguy.start_time)
# sleep(5)
# print(randomguy.calculate_time())