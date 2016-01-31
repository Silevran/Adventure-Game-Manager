#press F12

init -1600 python:

    def _dynamic_watch():
        if not config.developer:
            return
        renpy.show_screen("_dynamic_watcher", _layer="debug")
        renpy.restart_interaction()

    def _watching_exp(expression):
        return DynamicDisplayable(_dynamic_text, expression=expression)
    def _dynamic_text(st, at, expression):
        try:
            # remove text tags
            return Text(unicode(renpy.python.py_eval(expression)).replace('{', '{{'), substitute=False), .1
        except:
            return Text("Exception"), .1

    if persistent._watch_list is None:
        persistent._watch_list = []


screen _dynamic_watcher:
    zorder 2000

    frame:
        xalign 1.0
        background "#0002"
        xmaximum config.watcher_width
        ymaximum config.watcher_height
        has vbox
        viewport:
            scrollbars "both"
            mousewheel True
            vbox:
                spacing 5
                for i in persistent._watch_list:
                    hbox:
                        textbutton _("x") action [Function(persistent._watch_list.remove, i), Show("_dynamic_watcher", _layer="debug")]:
                            background None
                            xpadding 0
                            ypadding 0
                            xmargin  10
                            ymargin  0
                            yalign .5
                        text "[i!q]" yalign .5
                    hbox:
                        text "    -> " yalign .5
                        text _watching_exp(i) yalign .5
        hbox:
            xalign 1.
            textbutton _("add")   action Function(renpy.call_in_new_context, "_watch_list_add")
            textbutton _("close") action [Function(renpy.hide_screen, "_dynamic_watcher", layer="debug"), renpy.restart_interaction]

screen _watch_list_add:
    modal True
    zorder 2500
    key "game_menu" action Return(u"")

    frame:
        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _("Enter adding expression"):
            xalign 0.5

        hbox:
            xalign 0.5
            input

label _watch_list_add:
    python:
        v = renpy.call_screen('_watch_list_add', _layer="debug")
        if v:
            persistent._watch_list.append(v)
        # persistent._watch_list.append(renpy.call_screen('_watch_list_add', _layer="debug"))
    return

init -1099 python:

    # overwrite keymap
    km = renpy.Keymap(
        rollback = renpy.rollback,
        screenshot = _screenshot,
        toggle_fullscreen = renpy.toggle_fullscreen,
        toggle_skip = _keymap_toggle_skipping,
        fast_skip = _fast_skip,
        game_menu = _invoke_game_menu,
        hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
        launch_editor = _launch_editor,
        reload_game = _reload_game,
        developer = _developer,
        quit = renpy.quit_event,
        iconify = renpy.iconify,
        help = _help,
        choose_renderer = renpy.curried_call_in_new_context("_choose_renderer"),
        console = _console.enter,
        profile_once = _profile_once,
        self_voicing = Preference("self voicing", "toggle"),
        )

    config.underlay = [ km ]

    del km

init 1000 python:
    config.locked = False
    config.layers.append('debug')
    config.top_layers.append('debug')

    config.keymap["variable_viewer"] = 'K_F12'
    config.watcher_width = 600
    config.watcher_height = 300


    config.locked = True
