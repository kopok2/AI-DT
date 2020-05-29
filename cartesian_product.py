for a in range(2):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                for e in range(4):
                    czy_prac = 0
                    if a:
                        czy_prac = 1
                    if not c:
                        czy_prac = 0
                    if not e:
                        if b < 2:
                            czy_prac = 0
                    if not d and not a:
                        czy_prac = 0
                    if d == 2 and e > 1:
                        czy_prac = 1
                    print(a, b, c, d, e, czy_prac, sep=',')