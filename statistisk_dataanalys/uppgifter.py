import random

men_amount = 80
women_amount = 20
pick_amount = 3
sim_amount = 1000
sim_sim_amount = 5



for a in range(sim_sim_amount): 
    one_woman_picked = 0
    for i in range(sim_amount):
        women_picked = 0
        for j in range(pick_amount):
            pick = random.randint(0, 1)
            if pick == 1:
                women_picked += 1
        if women_picked == 1:
            one_woman_picked += 1

    print(f"One woman picked: {one_woman_picked/sim_amount}")
