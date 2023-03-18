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
    

def internal_id_count(func):
    internal_id = 0
    def wrapper(*args):
        nonlocal internal_id
        internal_id += 1
        return func(*args, id=internal_id)
    return wrapper