from html_file import Project, CSSRule, Tag


p = Project("projects/test", "test")
div = Tag("div")
p.HTML.body.Children += div
div.Class += "important"
div.Children += Tag("p")
div.Children += Tag("p")
for (i, child) in enumerate(div.Children):
    child.Content = "some text" + str(i)
    child.Class += "child_tag"
div.id = "'parent-tag'"
rule = CSSRule()
rule2 = CSSRule()
p.CSS.Class.child_tag = rule
p.CSS.ID.parent_tag = rule2
rule.background_color = "black"
rule2.font_weight = "bold"
rule2.color = "red"
p.output()
