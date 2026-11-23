# 64 km Corridor Commute Fare Optimizer

A Python optimization model that computes the **minimum total commute fare** between any two valid points along the 64 km UPLB–LRT Buendia corridor. Built using [`main.py`](main.py) (Dijkstra's algorithm) as a reference, [`commute_optimizer.py`](commute_optimizer.py) models multi-modal routes, piecewise distance-based fares, fixed-rate segments, expressway boarding/alighting restrictions, and the Alabang terminal branch.

Convenience and comfort are not considered—the model strictly minimizes total peso cost without rounding fares.

---

## Corridor Specification

### Marked Stations (UPLB = KM 0)

| Station | Kilometer | Notes |
| --- | --- | --- |
| UPLB | KM 0 | Corridor origin |
| Olivarez | KM 1 | Regular road |
| Calamba | KM 13 | Regular road |
| Real | KM 18 | End of south regular-road segment |
| Alabang | KM 47 | Separate expressway exit (alight-only terminal branch) |
| Magallanes | KM 62 | Start of north regular-road segment |
| LRT Buendia | KM 64 | Corridor terminus |

### Available Routes

| Mode | Route | Coverage | Notes |
| --- | --- | --- | --- |
| Tricycle | UPLB to Olivarez | KM 0 – KM 1 | Fixed rate: **80 PHP** |
| Tricycle | Calamba to Real | KM 13 – KM 18 | Fixed rate: **50 PHP** |
| Jeepney | UPLB to Calamba | KM 0 – KM 13 | Passes through Olivarez |
| Jeepney | Calamba to Real | KM 13 – KM 18 | Regular road |
| Bus | Olivarez to Alabang | KM 1 – KM 47 | Passes through Calamba & Real; expressway KM 18–47; terminates at Alabang |
| Bus | Olivarez to LRT Buendia | KM 1 – KM 64 | Passes through Calamba, Real, & Magallanes; expressway KM 18–62 (bypasses Alabang) |

### Fare Rules

- **Jeepney**: `14 PHP` base fare for the first `4 km`, plus `2 PHP` per succeeding km (or fraction thereof).
- **Bus**: `18 PHP` minimum fare for the first `5 km`, plus `2.9 PHP` per succeeding km (or fraction thereof).
- **Tricycle**: Fixed rate (`80 PHP` for UPLB–Olivarez; `50 PHP` for Calamba–Real), even if boarding or alighting mid-segment.
- **Student Discount**: If the commuter is a student (`y`/`yes`), a **20% discount** is applied to **Jeepney** and **Bus** fares (exact `0.8` multiplier, no rounding). Tricycle fares remain at their fixed rate.
- **Distance & Exact Arithmetic**:
  - For jeepneys and buses, ride distance is rounded **up** using `math.ceil` before computing the fare (e.g., a `6.2 km` ride is billed as `7 km`).
  - Resulting peso fares are **never rounded** and are computed using Python's `decimal.Decimal` to avoid binary floating-point inaccuracies.

### Transfer, Expressway, and Branch Rules

1. **One-way travel**: Strictly `0 <= start_km < end_km <= 64` (decimals allowed).
2. **Regular-road stops**: Commuters may board, alight, or transfer at any integer kilometer along regular roads (`KM 0–18` and `KM 62–64`), as well as at their exact `start_km` and `end_km` if those fall on regular roads.
3. **Expressway restriction**: No boarding or alighting is allowed at intermediate expressway kilometers (`18 < km < 47` and `47 < km < 62`).
4. **Alabang branch rule**: Passengers can alight at Alabang (`KM 47`) via the *Olivarez to Alabang* bus, but cannot board or continue onward from `KM 47` toward Magallanes (`KM 62`) or LRT Buendia (`KM 64`).

---

## How the Model Works

Because jeepney and bus fares include a base fare for the first 4–5 km, the cost of a continuous ride is **non-additive** across individual kilometers. To model this exactly:

1. **Node Construction**: The graph contains all valid stop/transfer points:
   - Integer regular-road kilometers (`0..18` and `62..64`)
   - Alabang (`47`)
   - The exact user-supplied `start_km` and `end_km` (when valid)
2. **Direct Single-Ride Edges**: For every route and every valid pair of boarding and alighting nodes `(u, v)` with `u < v`, a directed edge `u -> v` is added with weight equal to the exact fare of riding that single route continuously from `u` to `v`.
3. **Shortest-Path Optimization**: Dijkstra's algorithm (`findCheapestCommute`) finds the globally cheapest sequence of rides/transfers from `start_km` to `end_km`. When two paths have strictly identical exact fares, fewer rides/transfers is used as a deterministic tie-breaker.

---

## Usage

### Requirements

- Python 3.8+ (uses standard library only: `decimal`, `heapq`, `math`)

### Running the Program

```bash
python commute_optimizer.py
```

Enter `start_km`, `end_km` (numbers from `0` to `64`, decimals allowed), and whether you are a student (`y`/`n`) when prompted.

---

## Example Runs

### Example 1: Full Corridor (`0` to `64`, Regular Passenger)

```text
Enter start_km (0 to 64): 0
Enter end_km (0 to 64): 64
Are you a student? (y/n): n

===== OPTIMIZATION RESULTS =====
Trip: KM 0 (UPLB) -> KM 64 (LRT Buendia)
Passenger Type: Regular
Minimum Total Fare: PHP 183.40
Total Rides: 2 (Transfers: 1)

Step-by-Step Route:
  1. [Jeepney] UPLB to Calamba | KM 0 (UPLB) -> KM 13 (Calamba) (Distance: 13 km) | Segment Fare: PHP 32.00
  2. [Bus] Olivarez to LRT Buendia | KM 13 (Calamba) -> KM 64 (LRT Buendia) (Distance: 51 km) | Segment Fare: PHP 151.40
```

### Example 2: Full Corridor (`0` to `64`, Student — 20% Discount)

```text
Enter start_km (0 to 64): 0
Enter end_km (0 to 64): 64
Are you a student? (y/n): y

===== OPTIMIZATION RESULTS =====
Trip: KM 0 (UPLB) -> KM 64 (LRT Buendia)
Passenger Type: Student (20% discount on Jeepney & Bus)
Minimum Total Fare: PHP 146.72
Total Rides: 2 (Transfers: 1)

Step-by-Step Route:
  1. [Jeepney] UPLB to Calamba | KM 0 (UPLB) -> KM 13 (Calamba) (Distance: 13 km) | Segment Fare: PHP 25.60
  2. [Bus] Olivarez to LRT Buendia | KM 13 (Calamba) -> KM 64 (LRT Buendia) (Distance: 51 km) | Segment Fare: PHP 121.12
```

### Example 2: Decimal Endpoints (`1.2` to `15.2`)

```text
Enter start_km (0 to 64): 1.2
Enter end_km (0 to 64): 15.2

===== OPTIMIZATION RESULTS =====
Trip: KM 1.2 -> KM 15.2
Minimum Total Fare: PHP 44.00
Total Rides: 2 (Transfers: 1)

Step-by-Step Route:
  1. [Jeepney] UPLB to Calamba | KM 1.2 -> KM 11 (Distance: 9.8 km) | Segment Fare: PHP 26.00
  2. [Bus] Olivarez to Alabang | KM 11 -> KM 15.2 (Distance: 4.2 km) | Segment Fare: PHP 18.00
```

### Example 3: Restricted / Unreachable Route (`47` to `64`)

```text
Enter start_km (0 to 64): 47
Enter end_km (0 to 64): 64

No valid route exists: Alabang (KM 47) is a terminal expressway exit. Passengers cannot board or continue onward from KM 47.
```

---

## Project Files

- [`commute_optimizer.py`](commute_optimizer.py) — Main 64 km corridor fare optimization model and CLI.
- [`main.py`](main.py) — Original reference implementation of Dijkstra's algorithm for transportation cost optimization.
- [`README.md`](README.md) — Program documentation and usage guide.
