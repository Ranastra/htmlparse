import copy
from os import mkdir
from typing import Iterator, Union


def get_config() -> dict[str, str]:
    with open("config.cfg", "r") as file:
        cfg = {}
        for line in file.readlines():
            if line:
                if line[0] == "#": continue
                else:
                    line = line.strip().split(" = ")
                    cfg[line[0]] = line[1]
        file.close()
    return cfg
    
def fm_idf(s:str) -> str:
    return s.replace("_", "-").lower()

def deformat(s:str) -> str:
    return s.replace("-", "_")


config:dict[str, str] = get_config()
INDENT:str = int(config["indentation-per-level"]) * " "
INLINE_CSS:int = 0
EXTERNAL_CSS:int = 1


class Project():
    def __init__(self, path:str, name:str):
        try:
            mkdir(path)
        except: pass
        self.__name = name
        self.__path = path
        self.__HTML:HTMLFile = HTMLFile()
        self.__CSS:CSSFile = CSSFile()
        self.__HTML.head.single_tag_child("link").set_properties(rel="'stylesheet'", href=f"'{name}.css'")
        self.__HTML.html.set_properties(lang=f"'{config['lang']}'")

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, new:str) -> None:
        self.__name = new

    @property
    def path(self) -> str:
        return self.__path
    
    @path.setter
    def path(self, new:str) -> None:
        self.__path = new

    @property
    def HTML(self) -> "HTMLFile":
        return self.__HTML
    
    @HTML.setter
    def HTML(self, new:"HTMLFile") -> None:
        if isinstance(new, HTMLFile): self.__HTML = new
    
    @property
    def CSS(self) -> "CSSFile":
        return self.__CSS
    
    @CSS.setter
    def CSS(self, new:"CSSFile") -> None:
        if isinstance(new, CSSFile): self.__CSS = new

    def output(self) -> None:
        self.HTML.output(self.path, self.name)
        self.CSS.output(self.path, self.name)

    def __str__(self) -> str:
        return str(self.HTML) + "\n\n" + str(self.CSS)


class HTMLFile():
    def __init__(self):
        self.__html:Tag = Tag("html")
        self.__head:Tag = self.__html.normal_tag_child("head")
        self.__body:Tag = self.__html.normal_tag_child("body")

    @property
    def html(self) -> "Tag":
        return self.__html
    
    @property
    def head(self) -> "Tag":
        return self.__head
    
    @property
    def body(self) -> "Tag":
        return self.__body

    def __str__(self) -> str:
        self.html.set_indent_level(0)
        return "<!DOCTYPE html>\n" + str(self.html)
    
    def output(self, path:str, name:str) -> None:
        with open(f"{path}/{name}.html", "w") as f:
            f.write(str(self))
    

class CSSRule():
    def __init__(self, type:int=INLINE_CSS):
        self.__type:int = type 
        self.__properties:dict[str, str] = {}

    def set_properties(self, **properties:str) -> "CSSRule":
        return self.set_properties_dict(properties)

    def delet_properties(self, *properties:str) -> "CSSRule":
        return self.delet_properties_list(properties)
    
    def set_properties_dict(self, properties:dict[str, str]) -> "CSSRule":
        for (pr, value) in properties.items():
            if value == None:
                self.delet_properties(pr)
            else:
                self.__properties[deformat(pr)] = value
        return self
    
    def delet_properties_list(self, properties:list[str]) -> "CSSRule":
        for pr in properties: self.__properties.pop(deformat(pr), None)
        return self
    
    def clear(self) -> "CSSRule":
        self.__properties = {}
        return self
    
    def copy(self) -> "CSSRule":
        rule = CSSRule(self.__type)
        rule.set_properties_dict(self.__properties)
        return rule

    def switch_type(self, new_type:int) -> "CSSRule":
        self.__type = new_type
        return self
    
    def is_empty(self) -> bool:
        return len(self.__properties) == 0
    
    def __str__(self) -> str:
        if self.__type == INLINE_CSS:
            s = "'" + "".join([f"{key}:{value};" for (key, value) in self.__properties.items()]) + "'"
        elif self.__type == EXTERNAL_CSS:
            s = " {\n"
            for (key, value) in self.__properties.items():
                s += f"{INDENT}{fm_idf(key)}: {value};\n"
            s += "}"
        return s


class CSSFile():
    def __init__(self):
        self.__rules:dict[str, CSSRule] = {}

    def new_selector(self, name:str) -> "CSSRule":
        self.__rules[deformat(name)] = CSSRule(1)
        return self[name]

    def pop_selector(self, name:str) -> "CSSRule":
        return self.__rules.pop(name, None)

    def __getitem__(self, sel:str) -> CSSRule:
        return self.__rules[deformat(sel)]
    
    def get_selector(self, sel:str) -> CSSRule:
        return self[sel]

    def __str__(self) -> str:
        s = "\n"
        for (sel, value) in self.__rules.items():
            s += fm_idf(sel) + str(value) + "\n\n"
        return s
    
    def output(self, path:str, name:str) -> None:
        with open(f"{path}/{name}.css", "w") as f:
            f.write(str(self))


class ClassContainer():
    def __init__(self):
        self.__classes:list[str] = []

    def add_classes_list(self, classes:list[str]) -> "ClassContainer":
        for cls in classes: self.__classes.append(deformat(cls))
        return self
    
    def remove_classes_list(self, classes:list[str]) -> "ClassContainer":
        for cls in classes:
            cls = deformat(cls)
            if cls in self.__classes: self.__classes.remove(cls)
        return self
    
    def add_class(self, cls:str) -> "ClassContainer":
        self.__classes.append(deformat(cls))
        return self
    
    def remove_class(self, cls:str) -> "ClassContainer":
        if deformat(cls) in self.__classes: self.__classes.remove(deformat(cls))
        return self
    
    def clear(self) -> None:
        self.__classes = []
    
    def is_empty(self) -> bool:
        return len(self.__classes) == 0
    
    def __str__(self) -> str:
        s = "'" + " ".join(fm_idf(cls) for cls in self.__classes) + "'"
        return s


class Tag():

    def __init__(self, name:str):
        self.__name:str = name
        self.__properties:dict[str, str] = {}
        self.__children:list[Tag | STag] = []
        self.__content:str = ""
        self.__parent:Tag = None
        self.__indent_level:int = 0
        self.__style:CSSRule = CSSRule(0)
        self.__klass:ClassContainer = ClassContainer()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new:str) -> None:
        self.__name = new

    @property
    def klass(self) -> "ClassContainer":
        return self.__klass
    
    @property
    def style(self) -> "CSSRule":
        return self.__style
    
    @property
    def parent(self) -> "Tag":
        return self.__parent
    
    @property
    def content(self) -> str:
        return self.__content
    
    @property
    def indent_level(self) -> int:
        return self.__indent_level

    def set_indent_level(self, level:int=0) -> None:
        self.__indent_level = level
        for c in self: c.set_indent_level(level +1)

    def set_content(self, text:str) -> "Tag":
        self.__content = text
        return self
    
    def set_parent(self, parent:"Tag") -> "Tag":
        if self.parent != None:
            self.parent.remove_child(self)
        self.__parent = parent
        return self
    
    def remove_child(self, child:Union["Tag", "STag"]) -> "Tag":
        if child in self.__children:
            self.__children.remove(child)
        return self
    
    def remove_child_multi(self, children:list[Union["Tag", "STag"]]) -> "Tag":
        for child in children:
            if child in self.__children:
                self.__children.remove(child)
        return self
    
    def pop_at_multi(self, indexes:list[int]) -> list[Union["Tag", "STag"]]:
        return [self.__children.pop(index) for index in indexes]

    def pop_at(self, index:int) -> Union["Tag", "STag"]:
        return self.__children.pop(index)

    def set_properties(self, **properties:str) -> "Tag":
        return self.set_properties_dict(properties)
    
    def unset_properties(self, *properties:str) -> "Tag":
        return self.unset_properties_list(properties)
    
    def set_properties_dict(self, properties:dict[str, str]) -> "Tag":
        self.__properties.update(properties)
        return self
    
    def unset_properties_list(self, properties:list[str]) -> "Tag":
        for property in properties:
            self.__properties.pop(property, None)
        return self
    
    def insert_at(self, index:int, tag:Union["Tag",  "STag"]):
        self.__children.insert(index, tag)
    
    def __getitem__(self, index:int) -> Union["Tag", "STag"]:
        return self.__children[index]
    
    def __iter__(self) -> Iterator[Union["Tag", "STag"]]:
        return iter(self.__children)
    
    def single_tag_child(self, name:str) -> "STag":
        c = STag(name)
        self.append(c)
        return c
    
    def normal_tag_child(self, name:str) -> "Tag":
        c = Tag(name)
        self.append(c)
        return c
    
    def single_tag_child_multi(self, names:list[str]) -> "Tag":
        for name in names: self.single_tag_child(name)
        return self
    
    def normal_tag_child_multi(self, names:list[str]) -> "Tag":
        for name in names: self.normal_tag_child(name)
        return self
    
    def append_multi(self, children:list[Union["Tag", "STag"]]) -> "Tag":
        for c in children:
            c.set_parent(self) 
            self.__children.append(c)
        return self
    
    def append(self, child:Union["Tag", "STag"]) -> "Tag":
        child.set_parent(self)
        self.__children.append(child)
        return self
    
    def copy(self) -> "Tag":
        t = Tag(self.name)
        t.set_properties_dict(copy.deepcopy(self.__properties))
        t.set_parent(self.parent)
        t.set_content(copy.copy(self.content))
        t.klass.add_classes_list(self.klass._ClassContainer__classes)
        return t
    
    def deepcopy(self) -> "Tag":
        t = self.copy()
        t.append_multi(c.deepcopy() for c in self)
        for c in t: c.set_parent(t)
        return t
    
    def duplicate(self) -> "Tag":
        t = self.deepcopy()
        self.parent.append(t)
        return t
    
    def at_position(self, indexes:list[int]) -> Union["Tag", "STag"]:
        if len(self.__children) == 0:
            return None
        else:
            if len(indexes) == 1:
                return self[indexes[0]]
            else:
                return self[indexes[0]].at_position(indexes[1:])
            
    def get_position(self, prev:list[int]=[]) -> list[int]:
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.get_position_of_child(self)] + prev)
        
    def get_position_of_child(self, child:Union["Tag", "STag"]) -> int:
        return self.__children.index(child)

    def __eq__(self, other) -> bool:
        if isinstance(other, Tag): return id(self) == id(other)
        else: return False
            
    def clear_children(self) -> "Tag":
        self.__children = []
        return self
    
    def __str__(self) -> str:
        s = INDENT*self.indent_level + f"<{self.name}"
        if not self.style.is_empty():
            s += f" {str(self.style)}"
        if not self.klass.is_empty():
            s += f" class={str(self.klass)}"
        if len(self.__properties):
            s += " " + " ".join(f"{fm_idf(key)}={str(value)}" for (key, value) in self.__properties.items())
        s += ">"
        if self.content:
            s += self.content
        elif len(self.__children):
            s += "\n" + "\n".join(str(c) for c in self) + "\n" + INDENT*self.indent_level 
        s += f"</{self.name}>"
        return s


class STag():
    def __init__(self, name:str):
        self.__name:str = name
        self.__properties:dict[str, str] = {}
        self.__parent:Tag = None
        self.__indent_level:int = 0
        self.__style:CSSRule = CSSRule(0)
        self.__klass:ClassContainer = ClassContainer()

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, new:str) -> None:
        self.__name = new

    @property
    def style(self) -> "CSSRule":
        return self.__style
    
    @property
    def klass(self) -> "ClassContainer":
        return self.__klass
    
    @property
    def parent(self) -> "Tag":
        return self.__parent
    
    @property
    def indent_level(self) -> int:
        return self.__indent_level

    def set_indent_level(self, level:int=0) -> None:
        self.__indent_level = level

    def set_properties(self, **properties:str) -> "STag":
        return self.set_properties_dict(properties)
    
    def set_properties_dict(self, properties:dict[str, str]) -> "STag":
        self.__properties.update(properties)
        return self
    
    def set_parent(self, parent:"Tag") -> "STag":
        if self.parent != None:
            self.parent.remove_child(self)
        self.__parent = parent
        return self

    def get_parent(self) -> Tag:
        return self.__parent

    def unset_properties(self, *properties:str) -> "STag":
        return self.unset_properties_list(properties)
    
    def unset_properties_list(self, properties:list[str]) -> "STag":
        for property in properties:
            self.__properties.pop(property, None)
        return self
    
    def __getitem__(self, _index:int) -> None:
        return None
    
    def __iter__(self) -> Iterator[Union["Tag", "STag"]]:
        return iter([])
    
    def copy(self) -> "STag":
        t = STag(self.name)
        t.set_properties_dict(copy.deepcopy(self.__properties))
        t.set_parent(self.get_parent())
        return t
    
    def deepcopy(self) -> "STag":
        return self.copy()
    
    def duplicate(self) -> "STag":
        t = self.copy()
        t.set_parent(self.parent)
        self.parent.append(t)
        return t
    
    def at_position(self, _indexes:list[int]) -> None:
        return None
            
    def get_position(self, prev=[]) -> list[int]:
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.get_position_of_child(self)] + prev)

    def __eq__(self, other) -> bool:
        if isinstance(other, STag): return id(self) == id(other)
        else: return False
    
    def __str__(self) -> str:
        s = INDENT*self.indent_level + f"<{self.name}"
        if not self.style.is_empty():
            s += f" style={str(self.style)}"
        if not self.klass.is_empty():
            s += f" class={str(self.klass)}"
        if len(self.__properties):
            s += " " + " ".join(f"{fm_idf(key)}={str(value)}" for (key, value) in self.__properties.items())
        s += " />"
        return s

