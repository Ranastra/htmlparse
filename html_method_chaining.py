import copy
from helper import get_config, format_identifiers as fm_idf, deformat
from os import mkdir
from typing import Type

config = get_config()
INDENT = int(config["indentation-per-level"])


class Project():
    def __init__(self, path:str, name:str):
        try:
            mkdir(path)
        except: pass
        self.HTML:HTMLFile = HTMLFile(path, name)
        self.CSS:CSSFile = CSSFile(path, name)
        self.name:str = name
        self.path:str = path
        self.HTML.head.single_tag_child("link").set_propertys(rel="'stylesheet'", href=f"'{self.name}.css'") # link stylesheet
        self.HTML.html.set_propertys(lang=f"'{config['lang']}'")

    def output(self) -> None:
        self.HTML.output()
        self.CSS.output()

    def __str__(self) -> str:
        return str(self.HTML) + "\n\n" + str(self.CSS)


class HTMLFile():
    def __init__(self, path:str, name:str):
        self.html:Tag = Tag("html")
        self.head:Tag = self.html.normal_tag_child("head")
        self.body:Tag = self.html.normal_tag_child("body")
        self.name:str = name
        self.path:str = path

    def __str__(self) -> str:
        self.html.fix_indent(0)
        return "<!DOCTYPE html>\n" + str(self.html)
    
    def output(self) -> None:
        with open(f"{self.path}/{self.name}.html", "w") as f:
            f.write(str(self))
    

class CSSRule():
    def __init__(self, type:int=0):
        self.__type:int = type  # 0 = inline, 1 = external
        self.__propertys:dict[str, str] = {}

    def set_propertys(self, **propertys:str) -> Type["CSSRule"]:
        self.__propertys.update(propertys)
        return self

    def delet_propertys(self, *propertys:str) -> Type["CSSRule"]:
        for pr in propertys: self.__propertys.pop(deformat(pr), None)
        return self
    
    def set_propertys_dict(self, propertys:dict[str, str]) -> Type["CSSRule"]:
        self.__propertys.update(propertys)
        return self
    
    def clear(self) -> Type["CSSRule"]:
        self.__propertys = {}
        return self
    
    def copy(self) -> Type["CSSRule"]:
        rule = CSSRule(self.__type)
        rule.set_propertys_dict(self.__propertys)
        return rule

    def switch_type(self) -> Type["CSSRule"]:
        self.__type = (self.__type+1)%2
        return self
    
    def is_empty(self) -> bool:
        return len(self.__propertys) == 0
    
    def __str__(self) -> str:
        if self.__type == 0:
            s = "'" + ";".join([f"{key}:{self.__propertys[key]}" for key in self.__propertys]) + ";'"
        else:
            s = " {\n"
            for key in self.__propertys:
                s += f"{INDENT*' '}{fm_idf(key)}: {self.__propertys[key]};\n"
            s += "}"
        return s


class CSSFile():
    def __init__(self, path:str, name:str):
        self.name:str = name
        self.path:str = path
        self.__rules:dict[str, CSSRule] = {}

    def new_selector(self, name:str) -> CSSRule:
        self.__rules[deformat(name)] = CSSRule(1)
        return self[name]

    def pop_selector(self, name:str) -> CSSRule:
        return self.__rules.pop(name, None)

    def __getitem__(self, sel:str) -> CSSRule:
        return self.__rules[deformat(sel)]
    
    def get_rule(self, sel:str) -> CSSRule:
        return self[sel]

    def __str__(self) -> str:
        s = "\n"
        for sel in self.__rules:
            s += fm_idf(sel) + str(self.__rules[sel]) + "\n\n"
        return s
    
    def output(self) -> None:
        with open(f"{self.path}/{self.name}.css", "w") as f:
            f.write(str(self))


class ClassContainer():
    def __init__(self):
        self.__classes:list[str] = []

    def add_classes(self, *classes:str) -> Type["ClassContainer"]:
        for cls in classes: self.__classes.append(deformat(cls))
        return self
    
    def remove_classes(self, *classes:str) -> Type["ClassContainer"]:
        for cls in classes:
            cls = deformat(cls)
            if cls in self.__classes: self.__classes.remove(cls)
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
        self.name:str = name
        self.propertys:dict[str, str] = {}
        self.children:list[Tag or STag] = []
        self.content:str = ""
        self.parent:Tag = None
        self.indent_level:int = 0
        self.style:CSSRule = CSSRule(0)
        self.klass:ClassContainer = ClassContainer()

    def fix_indent(self, level:int=0) -> None:
        self.indent_level = level
        for c in self: c.fix_indent(level +1)

    def set_content(self, text:str) -> Type["Tag"]:
        self.content = text
        return self
    
    def set_parent(self, parent:Type["Tag"]) -> Type["Tag"]:
        self.parent.children.remove(self)
        self.parent = parent
        return self

    def set_propertys(self, **propertys:str) -> Type["Tag"]:
        self.propertys.update(propertys)
        return self
    
    def unset_propertys(self, *propertys:str) -> Type["Tag"]:
        for property in propertys:
            self.propertys.pop(property, None)
        return self
    
    def insert_at(self, index:int, tag:Type["Tag" or "STag"]):
        self.children.insert(index, tag)
    
    def __getitem__(self, index:int) -> Type["Tag" or "STag"]:
        return self.children[index]
    
    def __iter__(self):
        return iter(self.children)
    
    def single_tag_child(self, name:str) -> Type["STag"]:
        c = STag(name)
        c.parent = self
        self.children.append(c)
        return c
    
    def normal_tag_child(self, name:str) -> Type["Tag"]:
        c = Tag(name)
        c.parent = self
        self.children.append(c)
        return c
    
    def single_tag_multi_child(self, names:list[str]) -> Type["Tag"]:
        for name in names: self.single_tag_child(name)
        return self
    
    def normal_tag_multi_child(self, names:list[str]) -> Type["Tag"]:
        for name in names: self.normal_tag_child(name)
        return self
    
    def append(self, children:list[Type["Tag" or "STag"]]) -> Type["Tag"]:
        for c in children:
            c.parent = self 
            self.children.append(c)
        return self
    
    def copy(self) -> Type["Tag"]:
        t = Tag(self.name)
        t.propertys = copy.deepcopy(self.propertys)
        t.parent = self.parent
        t.content = copy.copy(self.content)
        return t
    
    def deepcopy(self) -> Type["Tag"]:
        t = self.copy()
        t.children = [c.deepcopy() for c in self]
        for c in t: c.parent = t
        return t
    
    def duplicate(self) -> Type["Tag"]:
        t = self.deepcopy()
        t.parent = self.parent
        self.parent.append([t])
        return t
    
    def at_position(self, indexes:list[int]) -> Type["Tag" or "STag"]:
        if len(self.children) == 0:
            return None
        else:
            if len(indexes) == 1:
                return self[indexes[0]]
            else:
                return self[indexes[0]].at_position(indexes[1:])
            
    def get_position(self, prev:list[int]=[]) -> list[int]:
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.children.index(self)] + prev)

    def __eq__(self, other) -> bool:
        if isinstance(other, Tag): return id(self) == id(other)
        else: return False
            
    def clear_children(self) -> Type["Tag"]:
        self.children = []
        return self
    
    def __str__(self) -> str:
        s = " "*INDENT*self.indent_level + f"<{self.name}"
        if not self.style.is_empty():
            s += f" {str(self.style)}"
        if not self.klass.is_empty():
            s += f" class={str(self.klass)}"
        if len(self.propertys):
            s += " " + " ".join(f"{fm_idf(key)}={fm_idf(str(self.propertys[key]))}" for key in self.propertys)
        s += ">"
        if self.content:
            s += self.content
        elif len(self.children):
            s += "\n" + "\n".join(str(c) for c in self) + "\n" + " "*INDENT*self.indent_level 
        s += f"</{self.name}>"
        return s


class STag():
    def __init__(self, name:str):
        self.name:str = name
        self.propertys:dict[str, str] = {}
        self.parent:Tag = None
        self.indent_level:int = 0
        self.style:CSSRule = CSSRule(0)
        self.klass:ClassContainer = ClassContainer()

    def fix_indent(self, level:int=0) -> None:
        self.indent_level = level

    def set_propertys(self, **propertys:str) -> Type["STag"]:
        self.propertys.update(propertys)
        return self
    
    def set_parent(self, parent:Tag) -> Type["STag"]:
        self.parent.children.remove(self)
        self.parent = parent
        return self

    def unset_propertys(self, *propertys:str) -> Type["STag"]:
        for property in propertys:
            self.propertys.pop(property, None)
        return self
    
    def __getitem__(self, _index:int) -> None:
        return None
    
    def __iter__(self):
        return iter([])
    
    def copy(self) -> Type["STag"]:
        t = STag(self.name)
        t.propertys = copy.deepcopy(self.propertys)
        t.parent = self.parent
        return t
    
    def deepcopy(self) -> Type["STag"]:
        return self.copy()
    
    def duplicate(self) -> Type["STag"]:
        t = self.copy()
        t.parent = self.parent
        self.parent.append([t])
        return t
    
    def at_position(self, indexes:list[int]) -> None:
        return None
            
    def get_position(self, prev=[]) -> list[int]:
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.children.index(self)] + prev)

    def __eq__(self, other) -> bool:
        if isinstance(other, STag): return id(self) == id(other)
        else: return False
    
    def __str__(self) -> str:
        s = " "*INDENT*self.indent_level + f"<{self.name}"
        if not self.style.is_empty():
            s += f" style={str(self.style)}"
        if not self.klass.is_empty():
            s += f" class={str(self.klass)}"
        if len(self.propertys):
            s += " " + " ".join(f"{fm_idf(key)}={fm_idf(str(self.propertys[key]))}" for key in self.propertys)
        s += " />"
        return s


# f = HTMLFile("test")
# t = f.body.normal_tag_child("div").normal_tag_multi_child(["h3", "p", "p"]).duplicate()
# for i in range(2):
#     f.body[i][0].set_propertys(style="'background-color:red;'")

# br = STag("br")
# f.body.insert_at(1, br)
# css = CSSFile("test")
# css.new_selector("#test")
# css.modify_selector("#test", background_color="red", color="white", font_weight="bold")
# print(f)
# print(css)
p = Project("projects/test2", "test")
p.HTML.body.normal_tag_child("div").set_propertys(Class="'important'", id="'parent_tag'").normal_tag_multi_child(["p", "p"])
for (i, child) in enumerate(p.HTML.body[0]):
    child.set_content("some text" + str(i)).klass.add_classes("child-tag")
p.CSS.new_selector("#parent-tag").set_propertys(font_weight="bold", color="red")
p.CSS.new_selector(".child-tag").set_propertys(background_color="black")
p.output()