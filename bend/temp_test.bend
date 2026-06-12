def add_range(start, end) -> u24:
  if start > end:
    return 0
  else:
    mid = (start + end) / 2
    left = add_range(start, mid)
    right = add_range(mid + 1, end)
    return left + right

def main() -> u24:
  return add_range(0, 10)
