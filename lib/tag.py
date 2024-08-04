from __future__ import annotations
import data
import style

type ChildNodes = list[TextNode | Tag]


class SelfclosingError(Exception):
    pass


class Root:
    # will include the DOCTYPE and html tag stuff
    pass


indentation = "  "  # 2 spaces


class TextNode:
    parent: Tag | Root | None
    text: str
    __self_closing = True

    def __init__(self, text: str = "", parent: Tag | Root | None = None):
        self.parent = parent
        self.text = text

    def display(self, indent_level: int = 0) -> str:
        if isinstance(indent_level, int) and indent_level >= 0:
            return indentation * indent_level + self.text
        else:
            raise ValueError("indentlevel must be a positive integer")


class Tag:
    __self_closing: bool
    __attributes: list[str]

    def __init__(self, tag_name: str):
        if not isinstance(tag_name, str):
            raise TypeError("Tag name must be of type string")
        if tag_name not in data.all.keys():
            raise ValueError(f"Tag name {tag_name} is not recognized")

        self.__dict__["tag_name"] = tag_name
        self.__dict__["_Tag__self_closing"] = data.all[tag_name]["self_closing"]
        self.__dict__["_Tag__attributes"] = data.all[tag_name]["attributes"]
        self.style = style.Style()
        self.__dict__["children"] = []
        self.__dict__["parent"] = None

    def __setattr__(self, name: str, value: str | style.Style | ChildNodes | Tag):
        if (
            name == "parent"
            or name == "style"
            or name == "children"
            or name == "tag_name"
        ):
            # use custom setter
            object.__setattr__(self, name, value)
        else:
            # lookup in attributes list for tags
            if not isinstance(value, str):
                raise TypeError("values of tag attributes must be of type string")
            else:
                if name not in self.__attributes and name != "id" and name != "class":
                    raise AttributeError(
                        f"attribute {name} not recognized for tag of type {self.tag_name}"
                    )
                else:
                    self.__dict__[name] = value

    def __add__(self, other: Tag | TextNode | str) -> Tag:
        if isinstance(other, str):
            other = TextNode(other)
        if isinstance(other, Tag) or isinstance(other, TextNode):
            if not self.__self_closing:
                other.parent = self
                self.__dict__["children"].append(other)
            else:
                raise SelfclosingError(
                    f"tag {self.tag_name} is self closing. you cant assign any child tags or child text nodes"
                )
        else:
            raise ValueError("child nodes must be of type str or Tag")
        return self

    @property
    def parent(self) -> Tag | Root | None:
        return self.__dict__["parent"]

    @parent.setter
    def parent(self, parent: Tag | Root | None):
        if (
            not isinstance(parent, Tag)
            and not isinstance(parent, Root)
            and not parent == None
        ):
            raise TypeError("parent tag must be of type Tag or Root")
        self.__dict__["parent"] = parent

    @property
    def style(self) -> style.Style:
        return self.__dict__["style"]

    @style.setter
    def style(self, css: style.Style):
        if not isinstance(css, style.Style):
            raise TypeError("cannot assign non style type to style attribute")
        else:
            self.__dict__["style"] = css

    @property
    def children(self) -> ChildNodes:
        return self.__dict__["children"]

    @children.setter
    def children(self, children):
        if type(children) != ChildNodes:
            raise ValueError(f"cannot assign non ChildNodes type to tag.children")
        else:
            for child in self.children:
                child.parent = None
            self.__dict__["children"] = []
            for child in children:
                self += child

    @property
    def tag_name(self) -> str:
        return self.__dict__["tag_name"]

    @tag_name.setter
    def tag_name(self, _):
        raise AttributeError("cant change the name of the tag right now")

    def display(self, indent_level: int = 0) -> str:
        if isinstance(indent_level, int) and indent_level >= 0:
            s = indentation * indent_level + "<" + self.tag_name
            if not self.style.empty:
                s += ' style="' + self.style.display() + '"'
            for attr in self.__attributes:
                if attr in self.__dict__.keys():
                    s += " " + attr + '="' + self.__dict__[attr] + '"'
            if self.__self_closing:
                s += " />"
            else:
                s += ">\n"
                for child in self.children:
                    s += child.display(indent_level=indent_level + 1) + "\n"
                s += indentation * indent_level + "</" + self.tag_name + ">"
            return s
        else:
            raise ValueError("indentlevel must be a positive integer")

    def __str__(self) -> str:
        return self.display()

    @staticmethod
    def read(html: str) -> Tag | TextNode:
        if not isinstance(html, str):
            raise TypeError("only str can be converted to Tag")
        stack = []  # YAASSS!!, Love stacks :)
        parent_tag = Tag("div")
        stack.append(parent_tag)
        while True:
            if not len(html):
                break
            if html[0] == "<":
                tag_name_end = min(html.find(" "), html.find(">"))
                tag_name = html[1:tag_name_end]
                tag_end = html.find(">")
                if tag_name[0] == "/":
                    stack.pop()
                else:
                    new_node = Tag(tag_name)
                    attributes = html[tag_name_end:tag_end].strip()
                    for attr in attributes.split(" "):
                        if not attr:
                            continue
                        attr = attr.split("=")
                        new_node.__setattr__(attr[0], attr[1].strip('"'))
                    stack[-1] += new_node
                    if not new_node.__self_closing:
                        stack.append(new_node)
                html = html[tag_end + 1 :]
                pass
            else:
                tag_opener = html.find("<")
                if tag_opener == -1:
                    tag_opener = len(html)
                new_node = TextNode(html[:tag_opener])
                html = html[tag_opener:]
                stack[-1] += new_node
        spawn_tag = parent_tag.children[0]
        spawn_tag.parent = None
        return spawn_tag
