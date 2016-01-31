# This is the main program. This can be changed quite a bit to
# customize it for your program... But remember what you do, so you
# can integrate with a new version of DSE when it comes out.

# Set up a default schedule.
init python:
    gold = 100
    fame = 10
    popularity = 10
    condition = 100
    
    qualPos = ParameterizedText(xpos=1.0,xanchor=1.0,ypos=1.0,yanchor=1.0)
    costPos = ParameterizedText(xpos=1.0,xanchor=1.0,ypos=1.0,yanchor=1.0)
    
    #qualPos = ParameterizedText(xalign = 0.5, yalign = 0.2)
    #costPos = ParameterizedText(xalign = 0.5, yalign = 0.3)
    
    quality_list = ["pathetic", "poor", "passable", "ok", "tasty", "delishius", "Better than the kings"]
    cost_list = ["free", "very cheap", "cheap", "average", "pricy", "exorbrunt", "Dragon Hoard"]
    
    food_quality = 300
    food_cost = 303
    
    drink_quality = 300
    drink_cost = 308
    
    bar_tended = False
    
    heroes_finished = []

    register_stat("Energy", "energy", 0, 100)
    register_stat("Influence", "inf", 10, 100)
    register_stat("Knowledge", "know", 10, 100)
    register_stat("Skill", "skill", 10, 100)
    
    unlocked_quests = [True, True]
    register_quest("Kill Rat", "Gotta start somewhere", 3, 1, 1, 1, 1, 100)
    register_quest("Clean Up Valley", "Keep it clean", 5, 1, 5, 1, 1, 100)
    
    
    register_hero("Bob", 1, 0, 1, 1, 1)
    
    # This is an example of an event that should only show up under special circumstances
    # dp_choice("Fly to the Moon", "fly", show="strength >= 100 and intelligence >= 100")

    dp_period("Daytime", "daytime_act")
    dp_choice("Cleanup", "clean_daytime")
    dp_choice("Promote Bar", "promote_daytime")
    dp_choice("Manage Stock", "manage_daytime")

    dp_period("Evening", "evening_act")
    dp_choice("Talk Customers", "talk_evening")
    dp_choice("Tend Bar", "tend_evening")
    dp_choice("Manage Stock", "manage_evening")
    
    inf = 20
    
    
    daytime_act = None
    evening_act = None
    ready = _return
    
    
# Declare characters used by this game.
define adv1 = Character('ADV 1', color="#c8ffc8")
define me = Character('Me', color="#c8c8ff")

    
# This is the entry point into the game.
label start:

    # Initialize the default values of some of the variables used in
    # the game.
    $ day = 0

    # Show a default background.
    scene black

    # The script here is run before any event.

    "For many years you were a adventurer."
    #"You traveled the lands, saved villagese, found treasure, and helped kingdoms."
    #"You also lost friends, been betrayed, and almost died more times than you could count."
    #"So you finally decided to retire andopen that bar you always wanted."
    
    #"One day a fresh face came in."
    
    #adv1 "Hey, you are that adventurer I have always heard about right?"
    #me "Maybe, what do you want"
    #adv1 "For you to guide me and help me grow into a great hero like you."
    #me "More text here"

    # We jump to day to start the first day.
    jump day
    

label base:
    menu:

        #"Check stats":
        #    jump statsview

        "Plan Day":
            jump planday
            
        "Send Adventurer on Quest":
            jump sendQuest
            
label statsview:
    call screen display_stats(True, True, True, True)
    
    jump base
    
label planday:
    call screen day_planner(["Daytime", "Evening"])
    
    if ready == False:
       jump base
       
    jump morning 
       
label sendQuest:
    call screen display_quests
    jump base
       
#--------------------------------------------------------------------------------------
            
# This is the label that is jumped to at the start of a day.
label day:
    python:
        day += 1

        renpy.say(None, "It's day %(day)d.")
        for h in heroes_finished:
            if h.trust > 10:
                renpy.say(None, "The hero %(h.name) comes in bright and early")
                renpy.say(None, "Thanks for all the help you have given me.")
                renpy.say(None, "%(h.name) hands you %(h.gold) gold")
                gold += h.gold
            elif h.trust < -10:
                renpy.say(None, "The hero %(h.name) seems to have left a note on your door")
                renpy.say(None, "Thanks for nothing.")
            else:
                renpy.say(None, "The hero %(h.name) comes in bright and early")
                renpy.say(None, "Thanks for all the help you have given me.")
                renpy.say(None, "%(h.name) hands you %i gold and gets a drink for the road" % h.gold / 2)
                gold += h.gold / 2
            heroes_finished.remove(h)
    
    jump base

    
    # We process each of the three periods of the day, in turn.
label morning:

    # Tell the user what period it is.
    centered "Daytime"

    # Set these variables to appropriate values, so they can be
    # picked up by the expression in the various events defined below. 
    $ period = "daytime"
    $ act = daytime_act
    
    # Execute the events for the morning.
    call events_run_period

    # That's it for the morning, so we fall through to the
    # evening.


label evening:
    
    # The evening is the same as the afternoon.
    if check_skip_period():
        jump night

    centered "Evening"

    $ period = "evening"
    $ act = evening_act
    
    call events_run_period


label night:

    # This is now the end of the day, and not a period in which
    # events can be run. We put some boilerplate end-of-day text
    # in here.

    centered "Night"

    "It's getting late, so I close up the bar for the night."
    
    "You tally up the profits for the day."
    
    python:
        if bar_tended:
            gold += popularity / 5
        else:
            gold += popularity / 10
        
        for h in heroes_list:
            if h.onQuest == False and h.gold > 1:
                gold += 1
                h.gold -= 1

    # We call events_end_day to let it know that the day is done.
    call events_end_day

    # And we jump back to day to start the next day. This goes
    # on forever, until an event ends the game.
    jump day
         

# This is a callback that is called by the day planner. 
label dp_callback:

    # Add in a line of dialogue asking the question that's on
    # everybody's mind.
    $ narrator("What should I do today?", interact=False)
    
    return

