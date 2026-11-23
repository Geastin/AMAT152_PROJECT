# Statement of the Problem: Minimum Exact Commute Fare

## Problem
Commuters traveling one-way along the 64 km corridor from UPLB to LRT Buendia must choose among tricycles, jeepneys, and buses with different fare rules, discounts, and boarding/alighting restrictions. Because fares are not additive across individual kilometers, the cheapest itinerary may require multiple rides or transfers. Given a start point, destination, and student status, determine the exact minimum total fare and the optimal ride sequence without rounding peso values.

## 1. Scope
Compute the minimum exact total fare for a one-way commute along the 64 km corridor from UPLB to LRT Buendia using tricycles, jeepneys, and buses. Return the optimal ride sequence and total fare without rounding peso values. If multiple routes have equal minimum fare, choose the one with fewer rides.

## 2. Inputs and Validity
Inputs: start $s$, destination $t$, and student status.

Valid trip condition:

$$
0 \le s < t \le 64,\quad s \in R,\quad t \in R \cup A
$$

where

$$
R = [0,18] \cup [62,64], \qquad A = \{47\}
$$

Let $\delta = 0.8$ for students and $\delta = 1.0$ for regular passengers.

## 3. Graph Model
Construct directed graph $G=(V,E)$:

$$
V = \left(\mathbb{Z} \cap R\right) \cup \{47,s,t\}
$$

For each transit route/mode $r$, add directed edge $(u,v,r)$ whenever:

$$
u < v,\quad u \in B_r,\quad v \in L_r
$$

where $B_r$ and $L_r$ are the permitted boarding and alighting intervals for route $r$. Regular roads allow boarding/alighting, expressways do not, and Alabang is exit-only.

Edge weight:

$$
w(u,v,r)=F_{m(r)}(v-u)
$$

with billed distance:

$$
d_{\text{billed}}=\lceil v-u \rceil
$$

## 4. Fare Functions

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

## 5. Optimization Objective
For path $P=(e_1,\dots,e_k)$ from $s$ to $t$, minimize lexicographically:

$$
P^*=\arg\min_{P\in\mathcal{P}(s,t)}
\left(
\sum_{i=1}^{k} w(e_i),\;
k
\right)
$$

That is, minimize total fare first; if tied, minimize number of rides $k$.

## 6. Computation Procedure
1. Parse $s,t$, and discount status.
2. Build vertex set $V$ and all valid edges $E$ with exact weights.
3. Run Dijkstra’s algorithm using priority key $(\text{total fare},\text{ride count})$.
4. Use `decimal.Decimal` for all fare arithmetic; do not round intermediate or final peso values.
5. Reconstruct the optimal path.
6. Output exact total fare and ride/transfer sequence; apply fewer-rides tie-break.

## 7. Output
Return:

- Exact minimum total fare, unrounded.
- Sequence of rides and transfer points.
- Number of rides.

Tie-break rule: minimum fare, then minimum rides.