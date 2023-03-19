import copy
from helper import get_config, format_identifiers as fm_idf
from os import mkdir

config = get_config()
INDENT = int(config["indentation-per-level"])


class Project():
    def __init__(self, path:str, name:str):
        try:
            mkdir(path)
        except: pass
        self.HTML = HTMLFile(path, name)
        self.CSS = CSSFile(path, name)
        self.name = name
        self.path = path
        self.HTML.head.single_tag_child("link").set_propertys(rel="'stylesheet'", href=f"'{self.name}.css'")

    def output(self):
        self.HTML.output()
        self.CSS.output()

    def __str__(self):
        return str(self.HTML) + "\n\n" + str(self.CSS)


class HTMLFile():
    def __init__(self, path:str, name:str):
        self.html = Tag("html")
        self.head = self.html.normal_tag_child("head")
        self.body = self.html.normal_tag_child("body")
        self.name = name
        self.path = path

    def __str__(self):
        self.html.fix_indent(0)
        return "<!DOCTYPE html>\n" + str(self.html)
    
    def output(self):
        with open(f"{self.path}/{self.name}.html", "w") as f:
            f.write(str(self))
    

class CSSFile():
    def __init__(self, path:str, name:str):
        self.name = name
        self.path = path
        self.__rules = {}

    def new_selector(self, name:str):
        self.__rules[name] = {}

    def delet_selector(self, name:str):
        self.__rules.pop(name, None)

    def modify_selector(self, s_name, **rules):
        self.__rules[s_name].update(rules)

    def remove_rules(self, s_name, *rules):
        for r in rules: self.__rules[s_name].pop(r, None)

    def __str__(self):
        s = "\n"
        for sel in self.__rules:
            s += fm_idf(sel) + " {\n"
            for key in self.__rules[sel]:
                s += " "*INDENT + f"{fm_idf(key)}: {self.__rules[sel][key]};\n"
            s += "}\n\n"
        return s
    
    def output(self):
        with open(f"{self.path}/{self.name}.css", "w") as f:
            f.write(str(self))


class Tag():

    def __init__(self, name:str):
        self.name = name
        self.propertys = {}
        self.children = []
        self.content = ""
        self.parent = None
        self.indent_level = 0

    def fix_indent(self, level=0):
        self.indent_level = level
        for c in self: c.fix_indent(level +1)

    def set_content(self, text:str):
        self.content = text
        return self
    
    def set_parent(self, parent):
        self.parent.children.remove(self)
        self.parent = parent
        return self

    def set_propertys(self, **propertys):
        self.propertys.update(propertys)
        return self
    
    def unset_propertys(self, *propertys:str):
        for property in propertys:
            self.propertys.pop(property, None)
        return self
    
    def insert_at(self, index:int, tag):
        self.children.insert(index, tag)
    
    def __getitem__(self, index:int):
        return self.children[index]
    
    def __iter__(self):
        return iter(self.children)
    
    def single_tag_child(self, name:str):
        c = STag(name)
        c.parent = self
        self.children.append(c)
        return c
    
    def normal_tag_child(self, name:str):
        c = Tag(name)
        c.parent = self
        self.children.append(c)
        return c
    
    def single_tag_multi_child(self, names:list[str]):
        for name in names: self.single_tag_child(name)
        return self
    
    def normal_tag_multi_child(self, names:list[str]):
        for name in names: self.normal_tag_child(name)
        return self
    
    def s_child_p(self, name:str):
        c = Tag(name)
        c.parent = self
        self.children.append(c)
        return self
    
    def append(self, children):
        for c in children:
            c.parent = self 
            self.children.append(c)
        return self
    
    def copy(self):
        t = Tag(self.name)
        t.propertys = copy.deepcopy(self.propertys)
        t.parent = self.parent
        t.content = copy.copy(self.content)
        return t
    
    def deepcopy(self):
        t = self.copy()
        t.children = [c.deepcopy() for c in self]
        for c in t: c.parent = t
        return t
    
    def duplicate(self):
        t = self.deepcopy()
        t.parent = self.parent
        self.parent.append([t])
        return t
    
    def at_position(self, indexes:list[int]):
        if len(self.children) == 0:
            return None
        else:
            if len(indexes) == 1:
                return self[indexes[0]]
            else:
                return self[indexes[0]].at_position(indexes[1:])
            
    def get_position(self, prev=[]):
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.children.index(self)] + prev)

    def __eq__(self, other) -> bool:
        if isinstance(other, Tag): return id(self) == id(other)
        else: return False
            
    def clear_children(self):
        self.children = []
        return self
    
    def __str__(self):
        s = " "*INDENT*self.indent_level + f"<{self.name}"
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
        self.name = name
        self.propertys = {}
        self.parent = None
        self.indent_level = 0

    def fix_indent(self, level=0):
        self.indent_level = level

    def set_propertys(self, **propertys):
        self.propertys.update(propertys)
        return self
    
    def set_parent(self, parent):
        self.parent.children.remove(self)
        self.parent = parent
        return self

    def unset_propertys(self, *propertys:str):
        for property in propertys:
            self.propertys.pop(property, None)
        return self
    
    def __getitem__(self, _index:int):
        return None
    
    def __iter__(self):
        return iter([])
    
    def copy(self):
        t = STag(self.name)
        t.propertys = copy.deepcopy(self.propertys)
        t.parent = self.parent
        return t
    
    def deepcopy(self):
        return self.copy()
    
    def duplicate(self):
        t = self.copy()
        t.parent = self.parent
        self.parent.append([t])
        return t
    
    def at_position(self, indexes:list[int]):
        return None
            
    def get_position(self, prev=[]):
        if self.parent == None: return prev
        else:
            return self.parent.get_position([self.parent.children.index(self)] + prev)

    def __eq__(self, other) -> bool:
        if isinstance(other, STag): return id(self) == id(other)
        else: return False
    
    def __str__(self):
        s = " "*INDENT*self.indent_level + f"<{self.name}"
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
    child.set_content("some text" + str(i)).set_propertys(Class="'child_tag'")
p.CSS.new_selector("#parent-tag")
p.CSS.new_selector(".child-tag")
p.CSS.modify_selector(".child-tag", background_color="black")
p.CSS.modify_selector("#parent-tag", font_weight="bold", color="red")
p.output()