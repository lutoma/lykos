from src import defaultsettings
import botconfig

class SettingsDict(dict):
    def __getitem__(self, item):
        return super().__getitem__(item.upper())

    def __missing__(self, item):
        return None

    def __setitem__(self, item, value):
        super().__setitem__(item.upper(), value)

    def __delitem__(self, item):
        super().__delitem__(item.upper())

    def __contains__(self, item):
        return super().__contains__(item.upper())

class SettingsAPI:
    def __init__(self):
        super().__setattr__("_settings", SettingsDict())
        super().__setattr__("_non_settings", SettingsDict())

    def __getattribute__(self, item):
        if not hasattr(defaultsettings, item.upper()) and item not in super().__getattribute__("_non_settings"):
            raise AttributeError
        if item in super().__getattribute__("_non_settings"):
            return super().__getattribute__("_non_settings")[item]
        if item in super().__getattribute__("_settings"):
            return super().__getattribute__("_settings")[item]
        return getattr(botconfig, item.upper(), getattr(defaultsettings, item.upper()))

    def __getattr__(self, item):
        from src import functions
        if hasattr(functions, item):
            return getattr(functions, item)
        if item == "clear":
            return super().__getattribute__("clear")
        raise AttributeError("no such function or variable: " + item)

    def __setattr__(self, item, value):
        if not hasattr(defaultsettings, item.upper()):
            super().__getattribute__("_non_settings")[item] = value
        else:
            super().__getattribute__("_settings")[item] = value

    def __delattr__(self, item):
        if item.upper() in super().__getattribute__("_non_settings"):
            del super().__getattribute__("_non_settings")[item]
        if item in super().__getattribute__("_settings"):
            del super().__getattribute__("_settings")[item]

    def __getitem__(self, item):
        return super().__getattribute__("_settings").__getitem__(item)

    def __setitem__(self, item, value):
        super().__getattribute__("_settings").__setitem__(item, value)

    def __delitem__(self, item):
        super().__getattribute__("_settings").__delitem__(item)

    def __contains__(self, item):
        return item.upper() in super().__getattribute__("_settings")

    def __len__(self):
        return super().__getattribute__("_settings").__len__()

    def clear(self):
        super().__getattribute__("_settings").clear()
