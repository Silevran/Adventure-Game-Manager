# stats.rpy
# Keeps track of and displays the stats for the DSE.
#
# To change styles, add a style block for the element you want
# preceded by "dse_stats_" down below

init -100 python:
    selectedHero = None
    selectedQuest = None
    
    exp_to_level = [0,3,10,20,50,100]
    
    heroes_list = [ ]
    quests_list = [ ]

    class __Quest(object):

        def __init__(self, name, desc, days, diff, prog, reward, exp, max):
            self.name = name
            self.desc = desc
            self.days = days
            self.difficulty = diff
            self.progress = prog
            self.reward = reward
            self.exp = exp
            self.isFull = False
            self.maxHeros = max
            self.heroes = [ ]
            
    def __init_quests():
        for q in quests_list:
            setattr(store, q.name, "XXX")

    config.start_callbacks.append(__init_quests)
    
    def register_quest(name, desc, days, diff, prog, reward, exp, max):
        quests_list.append(__Quest(name, desc, days, diff, prog, reward, exp, max))
    

    class __Hero(object):

        def __init__(self, name, level, exp, power, skill, trust):
            self.name = name
            self.level = level
            self.exp = exp
            self.power = power
            self.skill = skill
            self.trust = trust
            self.gold = 0
            self.onQuest = False
            self.daysLeft = 0
            self.progress = 0
            
    def __init_heroes():
        for h in heroes_list:
            setattr(store, h.name, "xxx")

    config.start_callbacks.append(__init_heroes)
    
    def register_hero(name, level, exp, power, skill, trust):
        heroes_list.append(__Hero(name, level, exp, power, skill, trust))

screen display_quests(name=True, bar=True, value=True, max=True):
    frame:        
        yalign 0.0
        xalign 0.0

        grid 2 2:
            xfill True
            yfill True
            
            vbox:
                xalign 0.5
                label "Heroes" xalign 0.5

                for h in heroes_list:
                    if h != None:
                        if name:
                            if h.onQuest == True:
                                textbutton h.name
                            elif selectedHero == h:
                                textbutton h.name action SetVariable("selectedHero", None)
                            else:
                                textbutton h.name action SetVariable("selectedHero", h)
                    
            vbox:
                if selectedHero != None:
                    xalign 0.5
                    label selectedHero.name
                    label ("Level %i" % (selectedHero.level))
                    label ("Power %i" % (selectedHero.power))
                    label ("Skill %i" % (selectedHero.skill))
                    label ("Trust %i" % (selectedHero.trust))
                    label ("OnQuest %s" % ("True" if selectedHero.onQuest else "False"))
                            
            vbox:
                xalign 0.5
                label "Quests" xalign 0.5

                for q in quests_list:
                    if q != None:
                        if name:
                            if q.isFull == True:
                                textbutton q.name
                            elif selectedQuest == q:
                                textbutton q.name action SetVariable("selectedQuest", None)
                                $ inf += 1
                            else:
                                textbutton q.name action SetVariable("selectedQuest", q)
                
            vbox:
                xalign 0.5
                if selectedQuest != None:
                    label selectedQuest.name
                    label selectedQuest.desc
                    label ("Days %i" % (selectedQuest.days))
                    label ("Reward %i" % (selectedQuest.reward))
                    label ("Exp %i" % (selectedQuest.exp))
            
        hbox:
            xfill True
            yalign 1.0
            xalign 0.5
            textbutton "Return" xalign 0.25 action Return()
            
            if selectedHero != None and selectedQuest != None:
                textbutton "Send Hero"  xalign 0.75 action [SetField(selectedHero, "onQuest", True), AddToSet(selectedQuest.heroes, selectedHero), SetVariable("selectedQuest", None), SetVariable("selectedHero", None)]
            else:
                textbutton "Send Hero"  xalign 0.75

# Quests`
# name desc days difficulty progress reward exp isFull maxHeros heroes 

# Heroes
# name level exp power skill trust gold onQuest daysLeft progress 
                
label end_of_day_quests:
    python:
        for q in quests_list:
            for h in q.heroes:
                h.daysLeft -= 1
                if h.progress < 0:
                    if h.skill >= q.difficulty:
                        h.progress -= h.power
                    else:
                        h.progress -= h.power / 2
                        
                if h.progress <= 0:
                    h.exp += q.exp
                    h.gold += q.reward
                    h.onQuest = False
                    q.heroes.remove(h)
                    AddToSet(heroes_finished, h)
                elif h.daysLeft <= 0:
                    h.exp += (q.exp / 2)
        for h in heroes_list:
            if h.exp > __exp_to_level[h.level]:
                h.level += 1
                h.power += 1
                h.skill += 1
                    
                
    return