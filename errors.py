import json
lenguage = "es"
messages_file = None

def load_messages(language):
    with open(f"locales/{language}.json", "r", encoding="utf-8") as messages_file:
        return json.load(messages_file)
    
messages_file = load_messages(lenguage)

class MoreThanOneKeyError(Exception):
    def __init__(self, message=messages_file["value_error_press_just_one_key_message"]):  
        super().__init__(message)

class NumberIsNotPositiveError(Exception):
    def __init__(self, message=messages_file["value_error_not_positive_number_message"]):
        super().__init__(message)

class OptionNotValidError(Exception):
    
    def __init__(self, options_tuple, message=messages_file["option_not_valid_message"]):
        message = message.format(options_tuple=options_tuple)
        super().__init__(message)