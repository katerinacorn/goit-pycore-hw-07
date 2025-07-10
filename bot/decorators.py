from .error_messages import ERROR_MESSAGES


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return ERROR_MESSAGES["KeyError"]
        except ValueError as e:
            return ERROR_MESSAGES["ValueError"](e)
        except IndexError:
            return ERROR_MESSAGES["IndexError"]
        except TypeError:
            return ERROR_MESSAGES["TypeError"]
        except Exception as e:
            return ERROR_MESSAGES["Unexpected"](e)

    return wrapper
