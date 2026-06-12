
# Algorithm to count solutions of 4/p = 1/x + 1/y + 1/z
# Ported from fp.c to Bend
# This implementation leverages Bend's parallelism by treating 
# the search for x and the check for divisors as parallelizable tasks.

def solve_for_x(p: i64, x: i64) -> i64:
  a = 4 * x - p
  
  # Pre-calculate constants for the divisor loop
  r0 = (a - (4 * (x % a) * (x % a)) % a) % a
  r1 = (a - (x % a)) % a
  dmin = 0
  if 2 * x > p:
    dmin = 2 * x * (2 * x - p)

  # In a fully optimized Bend version, we would map over a list of divisors.
  # Here we use a recursive function to simulate the loop over i from 1 to x.
  def count_divs(i: i64, c0: i64, c1: i64, n3: i64) -> (i64, i64, i64):
    if i > x:
      return (c0, c1, n3)
    
    if (x * x) % i == 0:
      nc0, nc1, nn3 = c0, c1, n3
      
      # Process d1 = i
      if i % a == r0 and i >= dmin:
        nc0 = c0 + 1
        if dmin > 0 and i == dmin: nn3 = n3 + 1
      if i <= x and i % a == r1 and p * i >= dmin:
        nc1 = c1 + 1
        if i == x: nn3 = nn3 + 1
        if dmin > 0 and p * i == dmin: nn3 = nn3 + 1
        
      # Process d2 = (x*x)//i (if distinct)
      d2 = (x * x) // i
      if d2 != i:
        if d2 % a == r0 and d2 >= dmin:
          nc0 = nc0 + 1
          if dmin > 0 and d2 == dmin: nn3 = nn3 + 1
        if d2 <= x and d2 % a == r1 and p * d2 >= dmin:
          nc1 = nc1 + 1
          if d2 == x: nn3 = nn3 + 1
          if dmin > 0 and p * d2 == dmin: nn3 = nn3 + 1
          
      return count_divs(i + 1, nc0, nc1, nn3)
    
    return count_divs(i + 1, c0, c1, n3)

  c0, c1, n3 = count_divs(1, 0, 0, 0)
  return 6 * (c0 + c1) - 3 * n3

def solve_for_p(p: i64) -> i64:
  # x range: (p/4, 3p/4]
  # We use a recursive sum to iterate through the range of x
  def sum_x(x: i64, acc: i64) -> i64:
    if x > (3 * p) // 4:
      return acc
    # The call to solve_for_x can be executed in parallel for different x
    return sum_x(x + 1, acc + solve_for_x(p, x))
    
  return sum_x(p // 4 + 1, 0)

def main() -> i64:
  # Test with p=97 (a prime 1 mod 24)
  return solve_for_p(97)
