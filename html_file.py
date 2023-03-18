# Class for html file
from helper import get_config, internal_id_count

config = get_config()
OBJECT_PROPERTYS = ["Style", "Class", "Content", "Name", "Children", "__ID"]


class Style_attribut():
    def __init__(self):
        pass

    def __str__(self) -> str:
        s = "style='"
        propertys = vars(self)
        for key in propertys:
            if propertys[key] != None:
                s += key.replace("_", "-") + ":" + propertys[key] + ";"
        s += "'"
        return s
    
    def is_empty(self) -> bool:
        return len(vars(self)) == 0
    

class Class_attribut():
    def __init__(self):
        self.__classes:list[str] = []
    
    def __iadd__(self, other:str):
        if isinstance(other, str):
            self.__classes.append(other)
        else: print("you can not use a non string as a class")
        return self

    def __isub__(self, other:str):
        try:
            self.__classes.remove(other)
        except ValueError:
            print("this class is not added to this element")
        return self

    def __str__(self) -> str:
        s = "class='" + " ".join(self.__classes) + "'"
        return s
    
    def is_empty(self) -> bool:
        return len(self.__classes) == 0


class Children():
    def __init__(self):
        self.__contents:list[Tag] = []

    def __iadd__(self, other):
        if isinstance(other, Tag):
            self.__contents.append(other)
        else: 
            print("You cant use a non Tag as a Children")
        return self
    
    def __isub__(self, other):
        try:
            self.__contents.remove(other)
        except ValueError:
            print("this Tag is not a Child")
        return self

    def is_empty(self) -> bool:
        return len(self.__contents) == 0


class Tag():
    @internal_id_count
    def __init__(self, name:str, id:int):
        self.__ID = id
        self.Name = name
        self.Class = Class_attribut() # shit all uppercase
        self.Style = Style_attribut()
        self.Content = ""
        self.Children = Children()

    def __str__(self) -> str:
        s = "<" + self.Name
        if not self.Class.is_empty(): s += " " + str(self.Class) 
        if not self.Style.is_empty(): s += " " + str(self.Style)
        propertys = vars(self)
        for key in propertys:
            if key not in OBJECT_PROPERTYS and propertys[key] != None:
                s += " " + key + "=" + propertys[key]
        if self.Children.is_empty():
            s += ">" + self.Content
        else:
            s += ">" + str(self.Children)
        s += "</" + self.Name + ">"
        return s
    
    def __hash__(self) -> int:
        return self.__ID
    

    
class File():
    def __init__(self, name:str):
        self.Name = name
        if "lang" in config: self.Lang = config["lang"] 
        else: self.lang = "en"
        if "charset" in config: self.Charset = config["charset"] 
        else: self.lang = "UTF-8"


#f = File("test")
#s = Style_attribut()
#s.background_color = "white" # no Hyphen but underscore
#print(s)
#print(vars(f))
# c = Class_attribut()
# c += "hallo"
# c += "test"
# print(c)
# c -= "test"
# print(c)
t = Tag("a")
t.Style.color = "red"
t.Style.font_weight = "bold"
t.Class += "important"
t.Class += "test"
t.Content = Tag("p")
t.Content.Content = "halllo hier ist text"
t.href = "example.html"
print(t)
