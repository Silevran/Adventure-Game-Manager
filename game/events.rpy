# This file contains the events that will be part of the game. It's
# expected that the user will add and remove events as appropriate
# for this game.


# Some characters that are used in events in the game.
init:
    $ t = Character('Teacher')
    $ gg = Character('Glasses Girl', color=(192, 255, 192, 255))
    $ sg = Character('Sporty Girl', color=(255, 255, 192, 255))
    $ bg = Character('Both Girls')
    $ narrator = Character(' ')
    

init:
    # First up, we define some simple events for the various actions, that
    # are run only if no higher-priority event is about to occur.
    
    $ event("cleanM", "act == 'clean_daytime'", event.only(), priority=200)
    $ event("promoteM", "act == 'promote_daytime'", event.only(), priority=200)
    $ event("manageM", "act == 'manage_daytime'", event.only(), priority=200)
    
    $ event("talkE", "act == 'talk_evening'", event.only(), priority=200)
    $ event("tendE", "act == 'tend_evening'", event.only(), priority=200)
    $ event("manageE", "act == 'manage_evening'", event.only(), priority=200)


    # This is an introduction event, that runs once when we first go
    # to class. 
    #$ event("introduction", "act == 'class'", event.once(), event.only())

    # These are the events with glasses girl.
    #
    # The glasses girl is studying in the library, but we do not
    # talk to her.
    #$ event("gg_studying",
    #        # This takes place when the action is 'study'.
    #        "act == 'study'",
    #        # This will only take place if no higher-priority
    #        # event will occur.
    #        event.solo(),
    #        # This takes place at least one day after seeing the
    #        # introduction event.
    #        event.depends("introduction"),
    #        # This takes priority over the study event.
    #        priority=190)

    # She asks to borrow our pen. 
    #$ event("borrow_pen",
    #        # This takes place when we go to study, and we have an int
    #        # >= 50. 
    #        "act == 'study' and intelligence >= 50",
    #        # It runs only once.
    #        event.once(),
    #        # It requires the introduction event to have run at least
    #        # one day before.
    #        event.depends("introduction"))

    # After the pen, she smiles when she sees us.
    #$ event("gg_smiling", "act == 'study'",
    #        event.solo(), event.depends("borrow_pen"),
    #        priority = 180)
    
    # Here are Sporty Girl's events that happen during the exercise act.
    #$ event("catchme", "act == 'exercise'",
    #        event.depends('introduction'), event.once())

    # Ending with both girls only happens if we have seen both of their final events
    # This needs to be higher-priority than either girl's ending.    
    #$ event('both_confess', 'act == "class"',
    #        event.depends("dontsee"), event.depends("cookies"),
    #        event.once(), priority = 50)
     
label cleanM:

    "You spend some time cleaning up"
    
    menu:
        "Get new supplies and fix things up. (-5 gold)" if gold >= 5:
            $ gold -= 5
            $ condition += 10
        
        "Work with what you have.":
            $ condition += 3

    return

label promoteM:

    "You head out to drum up some interest in the bar."
    
    menu:
        "Pay someone to promote the tavern with you (-5 gold)." if gold >= 5:
            $ gold -= 5
            $ populatirt += 10
        "Walk around and try and talk to people":
            $ populatiry += 3
    
    return

label manageM:

    "You look over the supplies you have."
    
    menu:
        "Adjust the menu?":
            $ index = int(food_quality / 100)
            $ quality = quality_list[index]
            show qualPos "You current food quality is %(quality)"
            menu:
                "Raise food prices but keep quality level?":
                    "something"
                "Lower food quality to save money?":
                    "something"
        "Adjust the drinks?":
            "something"
        "Look through old adventuring equipment for something of value?":
            "something"
    
    return
    
label talkE:

    "You spend the evening talking to the customers."

    $ fame += 2
    
    return
    
label tendE:

    "You spend the evening serving drinks."

    $ bar_tended = True
    
    return
    
label manageE:

    "You look over the supplies you have."
    
    return

