<MenuScreen>:
    BoxLayout:
        padding: dp(10)
        spacing: dp(10)
        orientation: 'vertical'

        Label:
            text: 'Crypto App Main Menu'
            bold: True
        Button:
            text: 'Select Coin'
            on_press:
                root.manager.current = 'SelectCoinScreen'
                root.manager.transition.direction = 'left'
        Button:
            text: 'View History'
            on_press:
                root.manager.current = 'ViewHistoryScreen'
                root.manager.transition.direction = 'left'

<SelectCoinScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)


        Label:
            text: 'Select Coin'
            bold: True
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            size_hint_y: None
            height: dp(30)

        TextInput:
            size_hint_y: None
            spacing: dp(10)
            padding: [dp(10), 0]
            id: search_input
            hint_text: 'Search...'
            multiline: False
            on_text: root.search_coins()

        Label:
            id: select_coin_message
            text: 'Loading Data...'
            font_size: '14sp'
            size_hint_y: None
            halign: 'center'

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(10)
            padding: [dp(10), 0]

            Label:
                text: '[u]Coin Name [i](Symbol)[/i][/u]'
                markup: True
            Label:
                text: '[u]Current Price[/u]'
                markup: True
            Label:
                text: '[u]24h percent change[/u]'
                markup: True
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            BoxLayout:
                id: coin_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
        Button:
            text: 'Back to Main Menu'
            size_hint_y: None
            height: dp(40)
            on_press:
                root.manager.current = 'MenuScreen'
                root.manager.transition.direction = 'right'
                # clear textbox
                root.ids.search_input.text = ''


<ViewHistoryScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        ScrollView:
            do_scroll_y: True
            do_scroll_x: False

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(10)

                Label:
                    text: 'View History'
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

                TextInput:
                    id: coin_symbol_input
                    hint_text: 'Coin Symbol'
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: start_date_input
                    hint_text: 'Start Date'
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                TextInput:
                    id: end_date_input
                    hint_text: 'End Date'
                    multiline: False
                    size_hint_y: None
                    height: dp(40)

                Button:
                    text: 'Submit'
                    on_press: root.submit_history()
                    size_hint_y: None
                    height: dp(40)



                Label:
                    id: history_message
                    text: ''
                    font_size: '14sp'
                    color: (1, 0, 0, 1)
                    size_hint_y: None
                    height: dp(20)
                    halign: 'center'
                    text_size: self.size

                Image:
                    id: line_chart
                    source: ''
                    size_hint_y: None
                    height: dp(300)
                    allow_stretch: True
                    keep_ratio: True

        Button:
            text: 'Back to Select Coin'
            on_press:
                root.manager.current = 'SelectCoinScreen'
                root.manager.transition.direction = 'right'
            size_hint_y: None
            height: dp(40)
            disabled: not root.came_from_select_coin
            opacity: 1 if root.came_from_select_coin else 0

        Button:
            text: 'Back to Main Menu'
            on_press:
                root.manager.current = 'MenuScreen'
                root.manager.transition.direction = 'right'
            size_hint_y: None
            height: dp(40)




<Screen>:
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<Label>:
    color: (0, 0, 0, 1)
<Button>:
    color: (1, 1, 1, 1)
    background_color: (0, 0, 1, 1)
    bold: True