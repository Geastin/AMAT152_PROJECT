# Results: Minimum Exact Commute Fair

## 1. Cost Optimization
The program was tested to run all possible starting stations to their maximum distance from the starting station, which is the LRT Buendia. Here are the results:

### a. Without Student Discount
| Starting Station | Mode | Routes | Total Kilometers | Fare | Total Rides | Student |
| --- | --- | --- | --- | --- | --- | --- |
| UPLB | Jeepney & Bus | UPLB to Calamba, Olivarez to LRT Buendia | KM 64 | PHP 183.40 | 2 | No |
| Olivarez | Jeepney & Bus | UPLB to Calamba, Olivarez to LRT Buendia | KM 63 | PHP 181.40 | 2 | No |
| Calamba | Bus | Olivarez to LRT Buendia | KM 51 | PHP 151.40 | 1 | No |
| Real | Bus | Olivarez to LRT Buendia | KM 46 | PHP 136.90 | 1 | No |
| Alabang | N/A | N/A | N/A | N/A | N/A | N/A |
| Magallanes | Bus | Olivarez to LRT Buendia | KM 2 | PHP 18.0 | 1 | No |

### b. With Student Discount
| Starting Station | Mode | Routes | Total Kilometers | Fare | Total Rides | Student |
| --- | --- | --- | --- | --- | --- | --- |
| UPLB | Jeepney & Bus | UPLB to Calamba, Olivarez to LRT Buendia | KM 64 | PHP 146.72 | 2 | Yes |
| Olivarez | Jeepney & Bus | UPLB to Calamba, Olivarez to LRT Buendia | KM 63 | PHP 145.12 | 2 | Yes |
| Calamba | Bus | Olivarez to LRT Buendia | KM 51 | PHP 121.12 | 1 | Yes |
| Real | Bus | Olivarez to LRT Buendia | KM 46 | PHP 109.52| 1 | Yes |
| Alabang | N/A | N/A | N/A | N/A | N/A | N/A |
| Magallanes | Bus | Olivarez to LRT Buendia | KM 2 | PHP 14.40 | 1 | Yes |

According to the results, the program was able to find out the most cost efficient traveling routes and the mode of transportation to be used. It was also able to calculate the fare with and without the student discount.

## 2. Transportation Vehicle
The program was analyzed to find out which mode of transportation it uses most in the algorithm. 

| Mode | Times used per Travel |
| --- | --- |
| Tricycle | 0 |
| Jeepney | 2 | 
| Bus | 5 | 

After reviewing the results, the bus was the most used mode of transportation used by the algorithm.

## 3. Fixed Fare Rate
The program was able to implement the fare constraints for all the transportation modes. 

### Fare Functions
**Tricycle** — fixed rate, no discount:

$$
F_{\text{tri}}(d)=
\begin{cases}
80, & [0,1]\text{ UPLB--Olivarez}\\
50, & [13,18]\text{ Calamba--Real}
\end{cases}
$$

**Jeepney** — base ₱14 for first 4 km, +₱2/km thereafter:


$$
F_{\text{jeep}}(d)=\delta\left(14+2\max(0,\lceil d\rceil-4)\right)
$$

**Bus** — base ₱18 for first 5 km, +₱2.90/km thereafter:

$$
F_{\text{bus}}(d)=\delta\left(18+2.9\max(0,\lceil d\rceil-5)\right)
$$

### Test Results
| Mode | Route | Kilometers | Base Fare per KM | Increased rate per KM | Additional Fare |
| --- | --- | --- | --- | --- | --- |
| Tricycle | UPLB to Olivarez | KM 1 | PHP 80 | Fixed | N/A |
| Jeepney | UPLB to Calamba | KM 13 | PHP 14 per 4 KM | PHP 2 per 1 KM | PHP 18 |
| Bus | Olivarez to LRT Buendia | KM 44 | PHP 18 per 5 KM | PHP 2.9 per 1 KM | PHP 113.1 |

The table above shows the constraints on the fares are calculated properly as the fares increases per additional kilometer based on the mode of transportation.

## 4. Limitations
a. The program only shoes one optimized results which makes comparing other possible routes found by the algorithm impossible.
b. The stations are limited to a 64 km distance which lessens the data results
c. There are only 3 modes of transporation. Other modes of transportation may be added later.


