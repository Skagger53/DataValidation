import datetime

class DataValidation:
    # Validates user input against any criteria for numbers.
    # Set relevant parameters to False when calling this method to disallow those inputs (e.g., if you do NOT want to allow negative numbers, set negative_num = False). By default all rational numbers are allowed (all parameters are set to True).
    # Allows user to go back (returns "back").
    # Returns False is failed. Returns the user's input as string if succeeds.
    def validate_user_input_num(self, user_input, float_num = True, negative_num = True, zero_num = True, positive_num = True):
        self.check_types_to_raise_exc((user_input, float_num, negative_num, zero_num, positive_num), ((str, int, float), bool, bool, bool, bool), ("user_input", "float_num", "negative_num", "zero_num", "positive_num"))

        # Checking if all criteria are set to False (nothing would pass this check)
        if negative_num == False and zero_num == False and positive_num == False:
            input("\nAll real numbers are excluded by this criteria.\n(Press Enter.)\n\n")
            return False

        # Invalid entry messages to user
        invalid_num = "\nYour input must be a number.\n\n(Press Enter.)\n"
        invalid_float_num = "\nYour input may not be a float. (Your input must be an integer).\n\n(Press Enter.)\n"
        invalid_negative_num = "\nYour input may not be negative.\n\n(Press Enter.)\n"
        invalid_zero_num = "\nYour input may not be zero.\n\n(Press Enter.)\n"
        invalid_positive_num = "\nYour input may not be positive.\n\n(Press Enter.)\n"

        user_input = user_input.strip().lower()
        orig_user_input = user_input

        if user_input == "": return False

        if user_input == "back": return "back"

        # Checking that user's input is a number
        try: user_input = float(user_input)
        except ValueError:
            input(invalid_num)
            return False

        if float_num == False:
            if user_input != int(user_input):
                input(invalid_float_num)
                return False

        if negative_num == False:
            if user_input < 0:
                input(invalid_negative_num)
                return False

        if zero_num == False:
            if user_input == 0:
                input(invalid_zero_num)
                return False

        if positive_num == False:
            if user_input > 0:
                input(invalid_positive_num)
                return False

        return orig_user_input

    # Validates user input based on custom tuple in "acceptable" argument.
    # This does not loop; this should be called within a loop obtaining user's input.
    # user_input is not case-sensitive. Elements in acceptable list/tuple are case-sensitive. (Ideally elements in acceptable should each be all lower case or all upper case.)
    # Allows user to go back (returns "back").
    # Returns False for a failed check. Returns "back" if user wants to go back. Returns stripped user's input if succeeded.
    def validate_user_input_custom(self, user_input, acceptable):
        self.check_types_to_raise_exc((user_input, acceptable), (str, (list, tuple), str), ("user_input", "acceptable"))

        user_input = user_input.strip()
        user_input_l = user_input.lower()

        if user_input == "": return False

        if user_input_l == "back": return "back"

        if user_input in acceptable or user_input.capitalize() in acceptable or user_input_l in acceptable: return user_input

        return False

    # Validates user input as a date.
    # This does not loop; this should be called within a loop obtaining user's input.
    # NOT case-sensitive. Commas do not matter.
    # Allows user to go back (returns "back").
    # Returns False for a failed check. Returns "back" if user wants to go back. Returns datetime object if succeeded.
    def validate_User_input_date(self, user_input):
        if isinstance(user_input, str) == False: raise InvalidTypePassed(user_input, type(user_input), str)

        if user_input == "": return False

        user_input = user_input.strip().lower().replace(",", "").replace("-", "/").replace(".", "/")

        if user_input == "back": return "back"

        # Tuples to be cycled through for checks
        # no_year_input_test is testing when the user enters a month and day and the year will then be assumed to be the current year.
        no_year_input_test = (
            ("/" + str(datetime.datetime.now().year), "%m/%d/%Y"),
            (" " + str(datetime.datetime.now().year), "%B %d %Y"),
            (" " + str(datetime.datetime.now().year), "%b %d %Y")
        )

        # input_test is testing when the user enters a date including the year
        input_test = ("%m/%d/%Y", "%m/%d/%y", "%b %d %Y", "%b %d %y", "%B %d %Y", "%B %d %y")

        # Checks for instances when the user did not provide a year
        for check in no_year_input_test:
            try: time_obj = datetime.datetime.strptime(user_input + check[0], check[1])
            except: pass
            else: return time_obj

        # Checks for instances when the user provided the full date
        for check in input_test:
            try: time_obj = datetime.datetime.strptime(user_input, check)
            except: pass
            else: return time_obj

        return False

    # Checks numerous variables to ensure they are the correct type. Raises exception if type is incorrect.
    # All arguments MUST be lists/tuples, even if they have only one element. (Note that if checking just one element, just doing the check directly, without check_to_raise_exc(), and then directly callin InvalidTypePassed(), is better.)
    # vars_to_check is a list/tuple of all variables to validate type
    # types_to_compare is a list/tuple of all types (must use type here, not string)
    # vars_as_strings is a list/tuple of strings of all variables being evaluated. This list visually is identical to vars_to_check except each element is a string (is in quotation marks).
    def check_types_to_raise_exc(self, vars_to_check, types_to_compare, vars_as_strings):
        # Before validating the data types provided, method first validates that the lists/tuples are the same length and that they are in fact lists or tuples.
        # Checks that the list lengths match (the lists will be zipped)
        if len(vars_to_check) != len(types_to_compare) or \
                len(types_to_compare) != len(vars_as_strings): raise InvalidListLength((vars_to_check, types_to_compare, vars_as_strings))

        # Checks that the arguments are lists or tuples
        validate_vars = zip((vars_to_check, types_to_compare, vars_as_strings), ("vars_to_check", "types_to_compare", "vars_as_strings"))
        for tup in validate_vars:
            if isinstance(tup[0], (list, tuple)) == False: raise InvalidTypePassed(tup[1], type(vars_to_check), (list, tuple))

        # Checks that the variables (vars_to_check) match the types provided (types_to_compare). Failure raises an Exception and informs the user of the problematic variable.
        list_to_check = zip(vars_to_check, types_to_compare, vars_as_strings)
        for checks in list_to_check:
            if isinstance(checks[0], checks[1]) == False: raise InvalidTypePassed(checks[2], type(checks[0]), checks[1])

# ----------------------------EXCEPTIONS CLASSES----------------------------
# This exception is available for any method to check a variable type. An invalid type will raise this error.
# To check multiple variables at once, use WedriverMain() method check_types_to_raise_exc(). That method loops and checks each variable with the below class.
# relevant_variable is a string that can be printed to the user to identify which variable is invalid
# type_passed is the actual type of the variable (valid or invalid). Use type() around the variable i question for this.
# type_needed is the type itself that the code requires (e.g., just type "str" or "float" but without quotation marks)
class InvalidTypePassed(Exception):
    def __init__(self, relevant_variable, type_passed, type_needed):
        message = f"Argument {relevant_variable} must be {type_needed}. Received {type_passed}."
        super().__init__(message)