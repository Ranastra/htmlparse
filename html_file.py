from helper import get_config, internal_id_count

config = get_config()
OBJECT_PROPERTYS = ["Style", "Class", "Content", "Name", "Children", "_Tag__ID", "_Tag__Indentation_level"]


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
    
    def __eq__(self, other:str) -> bool:
        return other in self.__classes


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
    
    def __iter__(self):
        return iter(self.__contents)
    
    def __getitem__(self, index):
        return self.__contents[index]
    
    def __str__(self):
        return "\n" + "\n".join([str(tag) for tag in self]) + "\n"
    
    def filter_by(self, **kwargs):
        pass


class Tag():
    @internal_id_count
    def __init__(self, name:str, id:int):
        self.__Indentation_level = 0
        self.__ID = id
        self.Name = name
        self.Class = Class_attribut() # shit all uppercase
        self.Style = Style_attribut()
        self.Content = ""
        self.Children = Children()

    def __str__(self) -> str:
        s = (" " * self.__Indentation_level * int(config["indentation-per-level"])) + "<" + self.Name
        if not self.Class.is_empty(): s += " " + str(self.Class) 
        if not self.Style.is_empty(): s += " " + str(self.Style)
        propertys = vars(self)
        for key in propertys:
            if key not in OBJECT_PROPERTYS and propertys[key] != None:
                s += " " + key + "=" + propertys[key]
        s += ">" + self.Content
        if not self.Children.is_empty():
            s += str(self.Children) + (" " * self.__Indentation_level * int(config["indentation-per-level"])) 
        s += "</" + self.Name + ">"
        return s
    
    def __hash__(self) -> int:
        return self.__ID
    
    def __set_indentation(self, level):
        self.__Indentation_level = level
        for child in self.Children:
            child.__set_indentation(level+1)

    
class File():
    def __init__(self, name:str):
        self.Name = name
        if "lang" in config: self.Lang = config["lang"] 
        else: self.lang = "en"
        if "charset" in config: self.Charset = config["charset"] 
        else: self.lang = "UTF-8"
        self.body = Tag("body")

    def __str__(self):
        s = "<!DOCTYPE html>\n<html lang=" + self.Lang + ">\n"
        self.body._Tag__set_indentation(0)
        s += "<head><meta charset='" + self.Charset + "'></head>\n"
        s += str(self.body) + "\n</html>"
        return s
    

    def output(self):
        with open("html/" + self.Name + ".html", "w") as file:
            file.write(str(self))


class CSSFile():
    def __init__(self):



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
f = File("test_html")
t = Tag("div")
f.body.Children += t
t.Style.color = "red"
t.Style.font_weight = "bold"
t.Class += "important"
t.Children += Tag("p")
t.Children += Tag("p")
for (i, child) in enumerate(t.Children):
    child.Content = "some text" + str(i)
    child.Class += "child-tag"
t.id = "'parent-tag'"
f.output()
