
MAX_PASSENGERS = 100
MAX_TRAINS = 50
MAX_TICKETS = 200

passengers = []
trains = []
tickets = []


def find_passenger(passenger_id):
    for i, passenger in enumerate(passengers):
        if passenger["id"] == passenger_id:
            return i
    return -1


def find_train(train_number):
    for i, train in enumerate(trains):
        if train["number"] == train_number:
            return i
    return -1


def find_ticket(ticket_id):
    for i, ticket in enumerate(tickets):
        if ticket["id"] == ticket_id and ticket["booked"]:
            return i
    return -1


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def register_passenger():
    if len(passengers) >= MAX_PASSENGERS:
        print("Passenger limit reached.")
        return

    passenger_id = get_int("Enter passenger ID: ")

    if find_passenger(passenger_id) != -1:
        print("Passenger ID already exists.")
        return

    name = input("Enter passenger name: ").strip()
    age = get_int("Enter age: ")
    gender = input("Enter gender: ").strip()

    if not name or age <= 0 or not gender:
        print("Invalid passenger details.")
        return

    passengers.append({
        "id": passenger_id,
        "name": name,
        "age": age,
        "gender": gender
    })

    print("Passenger registered successfully.")


def add_train():
    if len(trains) >= MAX_TRAINS:
        print("Train limit reached.")
        return

    number = get_int("Enter train number: ")

    if find_train(number) != -1:
        print("Train number already exists.")
        return

    name = input("Enter train name: ").strip()
    source = input("Enter source station: ").strip()
    destination = input("Enter destination station: ").strip()
    distance = get_float("Enter distance in km: ")
    rate = get_float("Enter fare rate per km: ")
    total_seats = get_int("Enter total seats: ")

    if (not name or not source or not destination
            or distance <= 0 or rate < 0 or total_seats <= 0):
        print("Invalid train details.")
        return

    trains.append({
        "number": number,
        "name": name,
        "source": source,
        "destination": destination,
        "distance": distance,
        "rate": rate,
        "total_seats": total_seats,
        "available_seats": total_seats
    })

    print("Train added successfully.")


def display_trains():
    if not trains:
        print("No train details available.")
        return

    print("\n--- TRAIN DETAILS ---")

    for train in trains:
        print(f"\nTrain Number: {train['number']}")
        print(f"Train Name: {train['name']}")
        print(f"Route: {train['source']} to {train['destination']}")
        print(f"Distance: {train['distance']:.2f} km")
        print(f"Available Seats: {train['available_seats']}")


def book_ticket():
    if len(tickets) >= MAX_TICKETS:
        print("Ticket limit reached.")
        return

    passenger_id = get_int("Enter passenger ID: ")
    p = find_passenger(passenger_id)

    if p == -1:
        print("Passenger not found. Register first.")
        return

    train_number = get_int("Enter train number: ")
    t = find_train(train_number)

    if t == -1:
        print("Train not found.")
        return

    train = trains[t]

    if train["available_seats"] <= 0:
        print("No seats available.")
        return

    ticket_id = len(tickets) + 1
    fare = train["distance"] * train["rate"]

    tickets.append({
        "id": ticket_id,
        "passenger_id": passenger_id,
        "train_number": train_number,
        "fare": fare,
        "booked": True
    })

    train["available_seats"] -= 1

    print("\nTicket booked successfully.")
    print(f"Ticket ID: {ticket_id}")
    print(f"Passenger: {passengers[p]['name']}")
    print(f"Train: {train['name']}")
    print(f"Fare: Rs. {fare:.2f}")


def cancel_ticket():
    ticket_id = get_int("Enter ticket ID to cancel: ")
    t = find_ticket(ticket_id)

    if t == -1:
        print("Active ticket not found.")
        return

    tickets[t]["booked"] = False

    train_index = find_train(tickets[t]["train_number"])

    if train_index != -1:
        train = trains[train_index]
        if train["available_seats"] < train["total_seats"]:
            train["available_seats"] += 1

    print("Ticket cancelled successfully.")


def calculate_fare():
    train_number = get_int("Enter train number: ")
    t = find_train(train_number)

    if t == -1:
        print("Train not found.")
        return

    train = trains[t]
    fare = train["distance"] * train["rate"]

    print(f"Train: {train['name']}")
    print(f"Distance: {train['distance']:.2f} km")
    print(f"Rate per km: Rs. {train['rate']:.2f}")
    print(f"Estimated fare: Rs. {fare:.2f}")


def display_passenger_list():
    train_number = get_int("Enter train number: ")
    t = find_train(train_number)

    if t == -1:
        print("Train not found.")
        return

    print(f"\nPassenger list for {trains[t]['name']}")
    print("Ticket ID | Passenger ID | Name | Fare")

    found = False

    for ticket in tickets:
        if (ticket["train_number"] == train_number
                and ticket["booked"]):
            p = find_passenger(ticket["passenger_id"])

            if p != -1:
                passenger = passengers[p]
                print(
                    f"{ticket['id']:9} | "
                    f"{passenger['id']:12} | "
                    f"{passenger['name']} | "
                    f"Rs. {ticket['fare']:.2f}"
                )
                found = True

    if not found:
        print("No active bookings for this train.")


def main():
    while True:
        print("\n===== RAILWAY RESERVATION SYSTEM =====")
        print("1. Passenger Registration")
        print("2. Add Train Details")
        print("3. Display Train Details")
        print("4. Book Ticket")
        print("5. Cancel Ticket")
        print("6. Calculate Ticket Fare")
        print("7. Display Passenger List")
        print("8. Exit")

        choice = get_int("Enter your choice: ")

        if choice == 1:
            register_passenger()
        elif choice == 2:
            add_train()
        elif choice == 3:
            display_trains()
        elif choice == 4:
            book_ticket()
        elif choice == 5:
            cancel_ticket()
        elif choice == 6:
            calculate_fare()
        elif choice == 7:
            display_passenger_list()
        elif choice == 8:
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
