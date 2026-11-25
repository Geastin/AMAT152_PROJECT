# Results: Minimum Exact Commute Fair

## 1. Cost Optimization
The program was tested to find the optimal route by comparing the proposed optimal route to the alternative routes and the direct route. Here are the results:

### Start station UPLB to end station LRT Buendia

### a. Without Student Discount
| Optimization | Rides | Transfer | Mode | Distance to Switch | Routes | Total Fare | 
| --- | --- | --- | --- | --- | --- | --- |
| Optimal | 2 | 1 | Jeepney to Bus | 0 KM to 13 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 183.40 |
| Alternative | 2 | 1 | Jeepney to Bus | 0 KM to 12 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 184.30 |
| Alternative | 3 | 2 | Jeepney to Jeepney to Bus | 0 KM to 13 KM to 18 KM to 64 KM | UPLB to Calamba to Real to LRT Buendia | PHP 184.90 |
| Alternative | 2 | 1 |  to Jeepney to Bus | 0 KM to 11 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 185.20 |
| Worst | 3 | 2 | Jeepney to Jeepney to Bus | 0 KM to 13 KM to 17 KM to 64 KM | UPLB to Calamba to Real to LRT Buendia | PHP 185.90 |

### b. With Student Discount
| Optimization | Rides | Transfer | Mode | Distance to Switch | Routes | Total Fare | 
| --- | --- | --- | --- | --- | --- | --- |
| Optimal | 2 | 1 | Jeepney to Bus | 0 KM to 13 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 146.72 |
| Alternative | 2 | 1 | Jeepney to Bus | 0 KM to 12 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 147.44 |
| Alternative | 3 | 2 | Jeepney to Jeepney to Bus | 0 KM to 13 KM to 18 KM to 64 KM | UPLB to Calamba to Real to LRT Buendia | PHP 147.92 |
| Alternative | 2 | 1 |  to Jeepney to Bus | 0 KM to 11 KM to 64 KM | UPLB to Calamba to LRT Buendia | PHP 148.16 |
| Worst | 3 | 2 | Jeepney to Jeepney to Bus | 0 KM to 13 KM to 17 KM to 64 KM | UPLB to Calamba to Real to LRT Buendia | PHP 148.64 |

According to the results, the program was able to find out the most cost efficient traveling routes and the mode of transportation to be used. It was also able to calculate the fare with and without the student discount.

## 2. Transportation Vehicle
The program was analyzed to find out which mode of transportation it uses most in the algorithm. 

| Mode | Times used per Travel |
| --- | --- |
| Tricycle | 0 |
| Jeepney | 7 | 
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
1. The program only shoes one optimized results which makes comparing other possible routes found by the algorithm impossible.
2. The stations are limited to a 64 km distance which lessens the data results.
3. There are only 3 modes of transporation. Other modes of transportation may be added later.


