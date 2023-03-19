from htmlparse import Project
    
p = Project(path="projects/test", name="test")
p.HTML.body.normal_tag_child("div").set_properties(Class="'important'", id="'parent_tag'").normal_tag_child_multi(["p", "p"])
for (i, child) in enumerate(p.HTML.body[0]):
    child.set_content("some text" + str(i)).klass.add_class("child-tag")
p.CSS.new_selector("#parent-tag").set_properties(font_weight="bold", color="red")
p.CSS.new_selector(".child-tag").set_properties(background_color="black")
p.output()
