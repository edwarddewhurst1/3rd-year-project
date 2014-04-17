import pprint

def getPairs(string):

    pairs = []
    
    OPENB = "("
    CLOSEB = ")"
    
    startIndex = None
    
    stack = []
    
    pop = stack.pop
    push = stack.append
    
    counter = 0
    
    for index, char in enumerate(string):
        if char == OPENB:
            counter += 1
            if counter <= 2:
                push(index+1)
        elif char == CLOSEB:
            counter -= 1
            if counter < 2:
                tmp = pop()
                pairs.append((tmp, index))

    return pairs
    
def innerExtract(string):

    p = getPairs(string)
    p = sorted(p)
    
    tmp = []
    
    for pair in p:
        a, b = pair
        tmp.append(string[a:b])
        
    return tmp   

def extract(stringList, depth=0):

    if depth == 2:
        return [innerExtract(x) for x in stringList]
    OPEN_BRACKET = "("
    CLOSE_BRACKET = ")"
    
    new = []
    
    for string in stringList:
        if OPEN_BRACKET in string:
            counter = 0
            for index, char in enumerate(string):
                if char == OPEN_BRACKET:
                    counter += 1
                    if counter == 1:
                        start = index+1
                elif char == CLOSE_BRACKET:
                    counter -= 1
                    if counter == 0:
                        new.append(string[start:index].strip())
                        start = None

    if new:
        return extract(new, depth+1)
    else:
        return stringList
def main():

    ldoceString = None
    
    with open("ldoce", "r") as f:
        ldoceString = f.read()
    
    #ldoceString = "( (A) (8 aaa) ) ( (B) (8 bbb) ) )"
    #print "Expecting:\n[['A', '8 aaa'], ['B', '8 bbb']]"
    a = extract(["(" + ldoceString + ")"])
    pprint.pprint(a)

main()

