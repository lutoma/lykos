from src import defaultsettings
import botconfig

class SettingsDict(dict):
    def __getitem__(self, item):
        return super().__getitem__(item.upper())

    def __setitem__(self, item, value):
        super().__setitem__(item.upper(), value)

    def __delitem__(self, item):
        super().__delitem__(item.upper())

    def __contains__(self, item):
        return super().__contains__(item.upper())

class SettingsAPI:
    def __init__(self):
        object.__setattr__(self, "_settings", SettingsDict())
        object.__setattr__(self, "_non_settings", [])

    def __getattribute__(self, item):
        if not hasattr(defaultsettings, item.upper()):
            raise AttributeError
        if item in object.__getattribute__(self, "_settings"):
            return object.__getattribute__(self, "_settings")[item]
        return getattr(botconfig, item.upper(), getattr(defaultsettings, item.upper()))

    def __getattr__(self, item):
        if hasattr(defaultsettings, item):
            return getattr(defaultsettings, item)
        if item == "clear":
            return object.__getattribute__(self, "clear")
        raise AttributeError("no such setting or function: " + item)

    def __setattr__(self, item, value):
        if not hasattr(defaultsettings, item.upper()):
            setattr(defaultsettings, item.upper(), value)
            object.__getattribute__(self, "_non_settings").append(item.upper())
        elif item.upper() in object.__getattribute__(self, "_non_settings"):
            setattr(defaultsettings, item.upper(), value)
        else:
            object.__getattribute__(self, "_settings")[item] = value

    def __delattr__(self, item):
        if item.upper() in object.__getattribute__(self, "_non_settings"):
            delattr(defaultsettings, item.upper())
            del object.__getattribute__(self, "_non_settings")[item]
        if item in object.__getattribute__(self, "_settings"):
            del object.__getattribute__(self, "_settings")[item]

    def __getitem__(self, item):
        return object.__getattribute__(self, "_settings").__getitem__(item)

    def __setitem__(self, item, value):
        object.__getattribute__(self, "_settings").__setitem__(item, value)

    def __delitem__(self, item):
        object.__getattribute__(self, "_settings").__delitem__(item)

    def __contains__(self, item):
        return item.upper() in object.__getattribute__(self, "_settings")

    def __len__(self):
        return object.__getattribute__(self, "_settings").__len__()

    def clear(self):
        object.__getattribute__(self, "_settings").clear()
