conversation = """
    QLineEdit {
            background-color: white;
            color: black;
            font-size: 25px;
            padding: 10px;
            border: 2px solid gray;
            border-radius: 5px;
        }
    """

language_box = """
    QComboBox {
        background-color: white;
        color: black;
        padding: 5px;
        border: 1px solid gray;
        border-radius: 3px;
        min-width: 6em;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
    }
    QComboBox QAbstractItemView {
        background-color: white;
        border: 1px solid gray;
        selection-background-color: lightgray;
    }
    """

text_edit = """
    QTextEdit {
        background-color: white;
        background-image: url(/test.jpg);
        color: black;
        font-size: 16px;
        padding: 10px;
        border: 1px solid gray;
        border-radius: 3px;
    }
    """

background_input = """
    QLineEdit {
            background-color: white;
            color: black;
            font-size: 25px;
            padding: 10px;
            border: 2px solid gray;
            border-radius: 5px;
        }
    """

speak_button = """
QPushButton { 
    background-color: grey; 
    border-radius: 20px; 
    padding: 10px; color:white; 
    font-size:20px;
} 
QPushButton:hover { 
    background-color: red; 
} 
QPushButton:pressed { 
    background-color: green; 
}
"""
