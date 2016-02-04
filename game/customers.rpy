# stats.rpy
# Keeps track of and displays the stats for the DSE.
#
# To change styles, add a style block for the element you want
# preceded by "dse_stats_" down below


label find_customer():
    python:
        randomChoice = renpy.random.randint(0, 3)
        if randomChoice == 0:
            customer = "Mark"
        elif randomChoice == 1:
            customer = "Mary"
        elif randomChoice == 2:
            customer = "Steve"
        elif randomChoice == 3:
            customer = "Sara"
    
    return 


label customer_mark(drink="none"):
    if drink == "wine":
        "I guess this will do"
        $ gold += 2
    elif drink == "ale":
        "Ah a fine drink"
        $ gold += 5
    elif drink == "beer":
        "Why would I want this swell"
        $ gold += 0
    elif drink == "liquor":
        "Ah, it burns"
        $ gold += 0
    elif drink == "none":
        "Something wierd happened"
        
    return
        
label customer_mary(drink="none"):
    if drink == "wine":
        "IThank you"
        $ gold += 5
    elif drink == "ale":
        "No thanks"
        $ gold += 0
    elif drink == "beer":
        "No"
        $ gold += 0
    elif drink == "liquor":
        "Ah, it burns"
        $ gold += 0
            
    return
        
label customer_steve(drink="none"):
    if drink == "wine":
        "Too fancy"
        $ gold += 0
    elif drink == "ale":
        "It will do for now"
        $ gold += 2
    elif drink == "beer":
        "A good pint indeed"
        $ gold += 3
    elif drink == "liquor":
        "Ah, it burns"
        $ gold += 0
        
    return
        
label customer_sara(drink="none"):
    if drink == "wine":
        "I would never drink this"
        $ gold += 0
    elif drink == "ale":
        "I would never drink this"
        $ gold += 0
    elif drink == "beer":
        "I would never drink this"
        $ gold += 0
    elif drink == "liquor":
        "Wonderful"
        $ gold += 7
        
    return
    
    