from __future__ import annotations
import data


class Style:
    __used_props: set[str]

    def __init__(self, props: str = ""):
        self.__dict__["_Style__used_props"] = set()
        self.__read(props)

    def __setattr__(self, name: str, value):
        # check if the field that is tried to access is a css property
        name = name.replace("_", "-")
        if not isinstance(value, str):
            value = str(value)
        if name in data.properties:
            self.__used_props.add(name)
            self.__dict__[name] = value
        else:
            raise AttributeError(f"no css property {name} in existance")

    def display(self, separator="\n") -> str:
        # convert Style to str using separator between the rules
        properties = []
        for property in self.__used_props:
            properties.append(property + ":" + self.__dict__[property] + ";")
        return separator.join(properties)

    def __str__(self) -> str:
        return self.display()

    def empty(self) -> bool:
        return len(self.__used_props) == 0

    def __read(self, css: str) -> None:
        # parse rules from str to the current Style instance
        if not isinstance(css, str):
            raise TypeError("only str can be converted to a Style instance")
        for rule in css.split(";"):
            if not rule:
                continue
            rule = rule.split(":")
            self.__setattr__(rule[0].strip(), rule[1].strip())


