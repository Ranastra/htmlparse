# htmlparse
Ever wanted to write HTML and CSS in a non HTML style and that in python? there you go!
Feel free to do whatever you want with this!

test.py produces some actual working ugly-looking HTML stuff :)
Nearly all methods return the object itself or a object of the same type to allow for method chaining. 
Tags are generally organized in a tree like structure: every tag has a reference to its child-tags and parent-tag
Child-tags can be accessed by indexing or iterating through the parent-tag. 
The methods that create only one new child-tag return the child tag, the others self.
The class Project sets up a template with a CCSFile and HTMLFile instance, creates a folder at specified path and links the stylesheet.  
The class STag is for self-closing tags.
for the html class attribut you have to use "klass" because "class" is reserved.

This are all methods / classes on the file:
```
class Project():
    def __init__(self, path:str, name:str):
@property    def HTML(self) -> "HTMLFile":
@property    def CSS(self) -> "CSSFile":
    def output(self) -> None:
    def __str__(self) -> str:

class HTMLFile():
    def __init__(self, path:str, name:str):
@property    def html(self) -> "Tag":
@property    def head(self) -> "Tag":
@property    def body(self) -> "Tag":
@property    def name(self) -> "str":
@name.setter    def name(self, new:str) -> None:
@property    def path(self) -> str:
@path.setter    def path(self, new:str) -> None:
    def __str__(self) -> str:
    def output(self) -> None:

class CSSRule():
    def __init__(self, type:int=INLINE_CSS):
    def set_properties(self, **properties:str) -> "CSSRule":
    def delet_properties(self, *properties:str) -> "CSSRule":
    def set_properties_dict(self, properties:dict[str, str]) -> "CSSRule":
    def delet_properties_list(self, properties:list[str]) -> "CSSRule":
    def clear(self) -> "CSSRule":
    def copy(self) -> "CSSRule":
    def switch_type(self, new_type:int) -> "CSSRule":
    def is_empty(self) -> bool:
    def __str__(self) -> str:

class CSSFile():
    def __init__(self, path:str, name:str):
@property    def name(self) -> str:
@name.setter    def name(self, new:str) -> None:
@property    def path(self) -> str:
@path.setter    def path(self, new:str) -> None:
    def new_selector(self, name:str) -> "CSSRule":
    def pop_selector(self, name:str) -> "CSSRule":
    def __getitem__(self, sel:str) -> CSSRule:
    def get_selector(self, sel:str) -> CSSRule:
    def __str__(self) -> str:
    def output(self) -> None:

class ClassContainer():
    def __init__(self):
    def add_classes_list(self, classes:list[str]) -> "ClassContainer":
    def remove_classes_list(self, classes:list[str]) -> "ClassContainer":
    def add_class(self, cls:str) -> "ClassContainer":
    def remove_class(self, cls:str) -> "ClassContainer":
    def clear(self) -> None:
    def is_empty(self) -> bool:
    def __str__(self) -> str:

class Tag():
    def __init__(self, name:str):
@property    def name(self) -> str:
@name.setter    def name(self, new:str) -> None:
@property    def klass(self) -> "ClassContainer":
@property    def style(self) -> "CSSRule":
@property    def parent(self) -> "Tag":
@property    def content(self) -> str:
@property    def indent_level(self) -> int:
    def set_indent_level(self, level:int=0) -> None:
    def set_content(self, text:str) -> "Tag":
    def set_parent(self, parent:"Tag") -> "Tag":
    def remove_child(self, child:Union["Tag", "STag"]) -> "Tag":
    def remove_child_multi(self, children:list[Union["Tag", "STag"]]) -> "Tag":
    def pop_at_multi(self, indexes:list[int]) -> list[Union["Tag", "STag"]]:
    def pop_at(self, index:int) -> Union["Tag", "STag"]:
    def set_properties(self, **properties:str) -> "Tag":
    def unset_properties(self, *properties:str) -> "Tag":
    def set_properties_dict(self, properties:dict[str, str]) -> "Tag":
    def unset_properties_list(self, properties:list[str]) -> "Tag":
    def insert_at(self, index:int, tag:Union["Tag",  "STag"]):
    def __getitem__(self, index:int) -> Union["Tag", "STag"]:
    def __iter__(self) -> Iterator[Union["Tag", "STag"]]:
    def single_tag_child(self, name:str) -> "STag":
    def normal_tag_child(self, name:str) -> "Tag":
    def single_tag_child_multi(self, names:list[str]) -> "Tag":
    def normal_tag_child_multi(self, names:list[str]) -> "Tag":
    def append_multi(self, children:list[Union["Tag", "STag"]]) -> "Tag":
    def append(self, child:Union["Tag", "STag"]) -> "Tag":
    def copy(self) -> "Tag":
    def deepcopy(self) -> "Tag":
    def duplicate(self) -> "Tag":
    def at_position(self, indexes:list[int]) -> Union["Tag", "STag"]:
    def get_position(self, prev:list[int]=[]) -> list[int]:
    def get_position_of_child(self, child:Union["Tag", "STag"]) -> int:
    def __eq__(self, other) -> bool:
    def clear_children(self) -> "Tag":
    def __str__(self) -> str:

class STag():
    def __init__(self, name:str):
@property    def name(self) -> str:
@name.setter    def name(self, new:str) -> None:
@property    def style(self) -> "CSSRule":
@property    def klass(self) -> "ClassContainer":
@property    def parent(self) -> "Tag":
@property    def indent_level(self) -> int:
    def set_indent_level(self, level:int=0) -> None:
    def set_properties(self, **properties:str) -> "STag":
    def set_properties_dict(self, properties:dict[str, str]) -> "STag":
    def set_parent(self, parent:"Tag") -> "STag":
    def get_parent(self) -> Tag:
    def unset_properties(self, *properties:str) -> "STag":
    def unset_properties_list(self, properties:list[str]) -> "STag":
    def __getitem__(self, _index:int) -> None:
    def __iter__(self) -> Iterator[Union["Tag", "STag"]]:
    def copy(self) -> "STag":
    def deepcopy(self) -> "STag":
    def duplicate(self) -> "STag":
    def at_position(self, _indexes:list[int]) -> None:
    def get_position(self, prev=[]) -> list[int]:
    def __eq__(self, other) -> bool:
    def __str__(self) -> str:
```

