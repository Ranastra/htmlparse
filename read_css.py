import htmlparse as hp

def get_css_file(path:str, name:str) -> hp.CSSFile:
    with open(f"{path}/{name}.css", "r") as file:
        s = "".join(line.strip() for line in file.readlines())
    return parse_css_file(s)

def parse_css_file(s:str) -> hp.CSSFile:
    s = "}" + "".join([line.strip() for line in s.split("\n")]) + "{"
    css = hp.CSSFile()
    rules = []
    last_index = 0
    for i in range(len(s)):
        if s[i] in ["}", "{"]:
            rules.append(s[last_index:i].strip())
            last_index = i
    rules = rules[1:]
    for i in range(len(rules) // 2):
        selector = rules[i*2][1:]
        properties = rules[i*2 +1][1:]
        property_dict = {}
        for prop in properties.split(";")[:-1]:
            prop = prop.split(":")
            property_dict[prop[0].strip()] = prop[1].strip()
        css.new_selector(selector).set_properties_dict(property_dict)
    return css

def parse_css_rule(s:str) -> hp.CSSRule:
    s = s.split(";")
    if s[-1] == "": s = s[:-1]
    rule = hp.CSSRule()
    rules = {}
    for r in s:
        r = r.split(":")
        rules[r[0].strip()] = r[1].strip()
    rule.set_properties_dict(rules)
    return rule


# rule = "background-color: red; color: blue;"
# r = parse_css_rule(rule).set_properties(font_family="Consolas")
# print(r)
# css = get_css_file("projects/test", "test")
# css.new_selector("#important").set_properties(font_family="'Consolas'")
# css.output("projects", "test2")
