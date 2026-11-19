
# Transportation Fare Comparison and Cost Optimization
# Using Dijkstra's Algorithm

# Transportation network
# Each location is connected to another location
# The number represents the transportation fare (PHP)

routes = {
    "Home": {
        "Terminal": 15,
        "Market": 20
    },
    "Terminal": {
        "Home": 15,
        "University": 25,
        "Mall": 10
    },
    "Market": {
        "Home": 20,
        "Mall": 12
    },
    "Mall": {
        "Terminal": 10,
        "Market": 12,
        "University": 18
    },
    "University": {
        "Terminal": 25,
        "Mall": 18
    }
}


# Dijkstra's Algorithm
def dijkstra(routes, start, destination):

    # Set initial distances to infinity
    distances = {}

    for location in routes:
        distances[location] = float("inf")

    distances[start] = 0

    # Store the previous location
    previous = {}

    # Store visited locations
    visited = []

    while len(visited) < len(routes):

        # Find the unvisited location with the lowest cost
        current = None

        for location in routes:
            if location not in visited:
                if current is None or distances[location] < distances[current]:
                    current = location

        # Stop if no reachable location remains
        if current is None or distances[current] == float("inf"):
            break

        # Stop if destination is reached
        if current == destination:
            break

        visited.append(current)

        # Check connected locations
        for neighbor, fare in routes[current].items():

            new_cost = distances[current] + fare

            # Update if a cheaper route is found
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current

    # Check if destination is reachable
    if distances[destination] == float("inf"):
        return None, float("inf")

    # Reconstruct the cheapest route
    path = []
    current = destination

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path, distances[destination]


# Main program
print("===== TRANSPORTATION COST OPTIMIZATION =====")

print("\nAvailable Locations:")

for location in routes:
    print("-", location)

start = input("\nEnter starting location: ")
destination = input("Enter destination: ")

# Validate locations
if start not in routes or destination not in routes:
    print("\nInvalid location!")

elif start == destination:
    print("\nYou are already at your destination!")
    print("Total fare: PHP 0.00")

else:
    # Find cheapest route
    path, total_fare = dijkstra(routes, start, destination)

    if path is None:
        print("\nNo available route found.")

    else:
        print("\n===== OPTIMIZATION RESULTS =====")

        print("Cheapest route:")

        for location in path:
            print(location, end="")

            if location != destination:
                print(" -> ", end="")

        print("\nTotal transportation fare: PHP",
              format(total_fare, ".2f"))
