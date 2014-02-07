n 0 1 0 0 = 1
n 1 0 1 0 = 1
n 2 0 0 1 = 1
n 0 r b w | r > 0 = n 1 (r-1) b w + n 2 (r-1) b w
n 1 r b w | b > 0 = n 0 r (b-1) w + n 2 r (b-1) w
n 2 r b w | w > 0 = n 0 r b (w-1) + n 1 r b (w-1)
n _ _ _ _ = 0

main = print (n 0 5 5 3 + n 1 5 5 3 + n 2 5 5 3)
