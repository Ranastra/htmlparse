import copy
from helper import get_config, format_identifiers as fm_idf

config = get_config()
INDENT = int(config["indentation-per-level"])


class Project():
    def __init__(self, name:str):
        self.HTML = HTMLFile(name)
        self.CSS = CSSFile(name)
        self.name = name

class HTMLFile():
    def __init__(self, name:str):
        self.html = Tag("html")
        self.head = self.html.normal_tag_child("head")
        self.body = self.html.normal_tag_child("body")
        self.name = name

    def __str__(self):
        self.html.fix_indent(0)
        return str(self.html)
    
class CSSFile():
    def __init__(self, name:str):
        self.name = name
        self.rules = {"class":[], "id":[]}


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
            s += " " + " ".join(f"{fm_idf(key)}={str(self.propertys[key])}" for key in self.propertys)
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
            s += " " + " ".join(f"{fm_idf(key)}={str(self.propertys[key])}" for key in self.propertys)
        s += " />"
        return s

f = HTMLFile("test")
t = f.body.normal_tag_child("div").normal_tag_multi_child(["h3", "p", "p"]).duplicate()
for i in range(2):
    f.body[i][0].set_propertys(style="'background-color:red;'")

br = STag("br")
f.body.insert_at(1, br)
print(f)
