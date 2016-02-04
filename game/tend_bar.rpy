# stats.rpy
# Keeps track of and displays the stats for the DSE.
#
# To change styles, add a style block for the element you want
# preceded by "dse_stats_" down below

transform alpha_dissolve:
    alpha 0.0
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0
    # This is to fade the bar in and out, and is only required once in your script

screen countdown:
    timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01), false=[Hide('countdown'), Jump(timer_jump)])
    bar value time range timer_range xalign 0.5 yalign 0.9 xmaximum 300 at alpha_dissolve # This is the timer bar.

init -100 python:
    customer = ""
    
    end_day = False
    drink_choice = ""
    
    timer_range = 0
    timer_jump = 0
    
label tend_tables:
    $ time = 10
    $ timer_range = 10
    $ timer_jump = 'close_shop'
    show screen countdown
    jump tend_tables_person
    
label tend_tables_person:
    call find_customer
    
    me "Let me get you a drink [customer]"
    
    menu:
        "Serve Wine":
            $ drink_choice = "wine"
            me "Have some Wine"
            jump tend_result
        "Serve Ale":
            $ drink_choice = "ale"
            me "Have some Ale"
            jump tend_result
        "Serve Beer":
            $ drink_choice = "beer"
            me "Have some Beer"
            jump tend_result
        "Serve Hard Liquor":
            $ drink_choice = "liquor"
            me "Have some Liquor"
            jump tend_result

label close_shop:
    if customer == None:
        jump end_serving
    else:
        me "Guess you are the last customer for the day."
        
        $ end_day = True
        
        me "Let me get you a drink [customer]"
        
        menu:
            "Serve Wine":
                $ drink_choice = "wine"
                me "Have some Wine"
                jump tend_result
            "Serve Ale":
                $ drink_choice = "ale"
                me "Have some Ale"
                jump tend_result
            "Serve Beer":
                $ drink_choice = "beer"
                me "Have some Beer"
                jump tend_result
            "Serve Hard Liquor":
                $ drink_choice = "liquor"
                me "Have some Liquor"
                jump tend_result

label tend_result:
    "They finish their drink"
    
    if customer == "Mark":
        call customer_mark pass (drink=drink_choice)
    elif customer == "Mary":
        call customer_mary pass (drink=drink_choice)
    elif customer == "Steve":
        call customer_steve pass (drink=drink_choice)
    elif customer == "Sara":
        call customer_sara pass (drink=drink_choice)
        
    $ customer = None
    
    if end_day:
        jump end_serving
    
    jump tend_tables_person
    
label end_serving:
    "Done Serving"
    
    return