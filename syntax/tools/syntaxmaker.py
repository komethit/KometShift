import json

def clearnyToList(line):
    line = line.replace('\\', ''); line = line.replace('b(?P', ''); line = line.replace(')b', '')
    line = line.replace('*', ''); line = line.replace('^', ''); line = line.replace('(', '')
    line = line.replace(')', ''); line = line.replace(']', ''); line = line.replace('[', '')
    line = line.replace('?', ''); line = line.replace('"', ''); line = line.replace(':', '')
    line = line.replace("'", '')
    line = line.replace('<TYPES>', ''); line = line.replace('<KEYWORD>', ''); line = line.replace('<INSTANCE>', '')
    line = line.replace('<BUILTIN>', ''); line = line.replace('P<EXCEPTION>', '')
    line = line.split('|')
    for ind in line:
        for ind2 in ind:
            if ind2 in ['.', '0', '#', '+', '-', '@']: 
                try:
                    line.remove(ind)
                except: pass
    return line

def func():
    while True:
        cmd = input('>>> ').split(' ')
        if cmd[0] == 'kom':
            if cmd[1] == 'new':
                with open('./syntax/tools/exemple.json', 'r') as file2:
                    stock = json.load(file2)
                    templateSyntaxPattern = {
                        f"{cmd[2]}": {
                            "regex": cmd[3],
                            "description": cmd[4]
                        }
                    }
                    stock.update(templateSyntaxPattern)
                    with open('./syntax/tools/exemple.json', 'w') as file:
                        json.dump(stock, file, indent=4)
            elif cmd[1] == 'list':
                with open('./syntax/tools/exemple.json', 'r') as file2:
                    stock = json.load(file2)
                    for index in stock:
                        print(index)
        elif cmd[0] == 'exit': break
