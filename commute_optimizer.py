# 64 km Corridor Commute Fare Optimizer
# Built using main.py (Dijkstra's algorithm) as reference.
# Solves for the minimum total commute fare between any two valid points
# along the 64 km UPLB - LRT Buendia corridor without rounding fares.

from decimal import Decimal, InvalidOperation
import heapq
import math


CORRIDOR_MIN = Decimal("0")
CORRIDOR_MAX = Decimal("64")
ALABANG_KM = Decimal("47")
STUDENT_DISCOUNT_MULTIPLIER = Decimal("0.8")

MARKED_STATIONS = {
    Decimal("0"): "UPLB",
    Decimal("1"): "Olivarez",
    Decimal("13"): "Calamba",
    Decimal("18"): "Real",
    Decimal("47"): "Alabang",
    Decimal("62"): "Magallanes",
    Decimal("64"): "LRT Buendia",
}

# Integer kilometers along regular roads where boarding/alighting/transfers are allowed.
REGULAR_ROAD_INTEGERS = [
    Decimal(km) for km in list(range(0, 19)) + list(range(62, 65))
]

AVAILABLE_ROUTES = [
    {
        "mode": "Tricycle",
        "name": "UPLB to Olivarez",
        "fareType": "fixed",
        "fixedFare": Decimal("80"),
        "boardRanges": [(Decimal("0"), Decimal("1"))],
        "alightRanges": [(Decimal("0"), Decimal("1"))],
    },
    {
        "mode": "Tricycle",
        "name": "Calamba to Real",
        "fareType": "fixed",
        "fixedFare": Decimal("50"),
        "boardRanges": [(Decimal("13"), Decimal("18"))],
        "alightRanges": [(Decimal("13"), Decimal("18"))],
    },
    {
        "mode": "Jeepney",
        "name": "UPLB to Calamba",
        "fareType": "jeepney",
        "fixedFare": None,
        "boardRanges": [(Decimal("0"), Decimal("13"))],
        "alightRanges": [(Decimal("0"), Decimal("13"))],
    },
    {
        "mode": "Jeepney",
        "name": "Calamba to Real",
        "fareType": "jeepney",
        "fixedFare": None,
        "boardRanges": [(Decimal("13"), Decimal("18"))],
        "alightRanges": [(Decimal("13"), Decimal("18"))],
    },
    {
        "mode": "Bus",
        "name": "Olivarez to Alabang",
        "fareType": "bus",
        "fixedFare": None,
        # Regular road boarding KM 1..18; expressway KM 18..47; alight-only terminal at KM 47.
        "boardRanges": [(Decimal("1"), Decimal("18"))],
        "alightRanges": [(Decimal("1"), Decimal("18")), (ALABANG_KM, ALABANG_KM)],
    },
    {
        "mode": "Bus",
        "name": "Olivarez to LRT Buendia",
        "fareType": "bus",
        "fixedFare": None,
        # Regular road stops KM 1..18 and KM 62..64; expressway KM 18..62 (bypasses Alabang).
        "boardRanges": [(Decimal("1"), Decimal("18")), (Decimal("62"), Decimal("64"))],
        "alightRanges": [(Decimal("1"), Decimal("18")), (Decimal("62"), Decimal("64"))],
    },
]


def isRegularRoad(km):
    return (Decimal("0") <= km <= Decimal("18")) or (Decimal("62") <= km <= Decimal("64"))


def isInRanges(km, ranges):
    for low, high in ranges:
        if low <= km <= high:
            return True
    return False


def canBoardRoute(route, km):
    return isInRanges(km, route["boardRanges"])


def canAlightRoute(route, km):
    return isInRanges(km, route["alightRanges"])


def calculateJeepneyFare(distanceKm):
    billedKm = math.ceil(distanceKm)
    extraKm = max(0, billedKm - 4)
    return Decimal("14") + Decimal("2") * Decimal(extraKm)


def calculateBusFare(distanceKm):
    billedKm = math.ceil(distanceKm)
    extraKm = max(0, billedKm - 5)
    return Decimal("18") + Decimal("2.9") * Decimal(extraKm)


def calculateSegmentFare(route, distanceKm, isStudent=False):
    fareType = route["fareType"]
    if fareType == "fixed":
        return route["fixedFare"]
    if fareType == "jeepney":
        fare = calculateJeepneyFare(distanceKm)
        return fare * STUDENT_DISCOUNT_MULTIPLIER if isStudent else fare
    if fareType == "bus":
        fare = calculateBusFare(distanceKm)
        return fare * STUDENT_DISCOUNT_MULTIPLIER if isStudent else fare
    raise ValueError(f"Unknown fare type: {fareType}")


def checkEndpointValidity(startKm, endKm):
    if startKm == ALABANG_KM:
        return (
            "No valid route exists: Alabang (KM 47) is a terminal expressway exit. "
            "Passengers cannot board or continue onward from KM 47."
        )
    if not isRegularRoad(startKm):
        return (
            f"No valid route exists: start_km (KM {formatKm(startKm)}) falls on the "
            "expressway, where boarding is not allowed."
        )
    if not (isRegularRoad(endKm) or endKm == ALABANG_KM):
        return (
            f"No valid route exists: end_km (KM {formatKm(endKm)}) falls on the "
            "expressway, where alighting is not allowed."
        )
    return None


def buildCorridorGraph(startKm, endKm, isStudent=False):
    nodeSet = set(REGULAR_ROAD_INTEGERS)
    nodeSet.add(ALABANG_KM)
    if isRegularRoad(startKm):
        nodeSet.add(startKm)
    if isRegularRoad(endKm) or endKm == ALABANG_KM:
        nodeSet.add(endKm)

    nodes = sorted(nodeSet)
    graph = {node: [] for node in nodes}

    for route in AVAILABLE_ROUTES:
        boardingNodes = [km for km in nodes if canBoardRoute(route, km)]
        alightingNodes = [km for km in nodes if canAlightRoute(route, km)]

        for u in boardingNodes:
            for v in alightingNodes:
                if u < v:
                    fare = calculateSegmentFare(route, v - u, isStudent)
                    graph[u].append((v, fare, route))

    return graph


def findCheapestCommute(startKm, endKm, isStudent=False):
    endpointError = checkEndpointValidity(startKm, endKm)
    if endpointError is not None:
        return None, None, endpointError

    graph = buildCorridorGraph(startKm, endKm, isStudent)

    # Dijkstra's algorithm with exact Decimal costs.
    # Secondary tie-breaker: fewer rides when total fares are strictly identical.
    bestCost = {startKm: (Decimal("0"), 0)}
    previous = {}
    pq = [(Decimal("0"), 0, startKm)]

    while pq:
        currentFare, currentRides, u = heapq.heappop(pq)

        if (currentFare, currentRides) > bestCost.get(u, (Decimal("Infinity"), 0)):
            continue

        if u == endKm:
            break

        for v, edgeFare, route in graph[u]:
            newFare = currentFare + edgeFare
            newRides = currentRides + 1
            candidate = (newFare, newRides)

            if v not in bestCost or candidate < bestCost[v]:
                bestCost[v] = candidate
                previous[v] = (
                    u,
                    {
                        "mode": route["mode"],
                        "routeName": route["name"],
                        "startKm": u,
                        "endKm": v,
                        "fare": edgeFare,
                    },
                )
                heapq.heappush(pq, (newFare, newRides, v))

    if endKm not in bestCost:
        return (
            None,
            None,
            f"No valid route exists from KM {formatKm(startKm)} to KM {formatKm(endKm)}.",
        )

    segments = []
    curr = endKm
    while curr != startKm:
        prevKm, segment = previous[curr]
        segments.append(segment)
        curr = prevKm
    segments.reverse()

    return bestCost[endKm][0], segments, None


def formatKm(km):
    text = format(km, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def formatStop(km):
    label = f"KM {formatKm(km)}"
    station = MARKED_STATIONS.get(km)
    if station is not None:
        return f"{label} ({station})"
    return label


def formatPhp(amount):
    exact = format(amount, "f")
    if "." in exact:
        whole, frac = exact.split(".")
        fracTrimmed = frac.rstrip("0")
        if len(fracTrimmed) <= 2:
            return f"PHP {whole}.{fracTrimmed.ljust(2, '0')}"
        return f"PHP {whole}.{fracTrimmed}"
    return f"PHP {exact}.00"


def parseKmInput(prompt):
    raw = input(prompt).strip()
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(
            f"Invalid number: '{raw}'. Please enter a numeric value from 0 to 64."
        ) from exc

    if not value.is_finite():
        raise ValueError("Please enter a finite numeric value from 0 to 64.")
    if value < CORRIDOR_MIN or value > CORRIDOR_MAX:
        raise ValueError("Kilometer value must be between 0 and 64 (inclusive).")
    return value


def parseYesNoInput(prompt):
    raw = input(prompt).strip().lower()
    if raw in ("y", "yes"):
        return True
    if raw in ("n", "no"):
        return False
    raise ValueError(f"Invalid response: '{raw}'. Please enter 'y' or 'n'.")


def printHeader():
    print("===== 64 KM CORRIDOR COMMUTE FARE OPTIMIZER =====")
    print("\nMarked Stations:")
    for km, name in MARKED_STATIONS.items():
        print(f"  - KM {formatKm(km):>2}: {name}")


def main():
    printHeader()

    try:
        startKm = parseKmInput("\nEnter start_km (0 to 64): ")
        endKm = parseKmInput("Enter end_km (0 to 64): ")
        isStudent = parseYesNoInput("Are you a student? (y/n): ")
    except ValueError as err:
        print(f"\nInput error: {err}")
        return

    if startKm >= endKm:
        print("\nInput error: Travel is strictly one-way, so start_km must be less than end_km.")
        return

    totalFare, segments, errorMessage = findCheapestCommute(startKm, endKm, isStudent)

    if errorMessage is not None or totalFare is None or segments is None:
        print(f"\n{errorMessage}")
        return

    passengerLabel = "Student (20% discount on Jeepney & Bus)" if isStudent else "Regular"

    print("\n===== OPTIMIZATION RESULTS =====")
    print(f"Trip: {formatStop(startKm)} -> {formatStop(endKm)}")
    print(f"Passenger Type: {passengerLabel}")
    print(f"Minimum Total Fare: {formatPhp(totalFare)}")
    print(f"Total Rides: {len(segments)} (Transfers: {len(segments) - 1})")
    print("\nStep-by-Step Route:")

    for idx, seg in enumerate(segments, start=1):
        distance = seg["endKm"] - seg["startKm"]
        print(
            f"  {idx}. [{seg['mode']}] {seg['routeName']} | "
            f"{formatStop(seg['startKm'])} -> {formatStop(seg['endKm'])} "
            f"(Distance: {formatKm(distance)} km) | "
            f"Segment Fare: {formatPhp(seg['fare'])}"
        )


if __name__ == "__main__":
    main()
