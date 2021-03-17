import re



terminals = \
[
('WS', '\\s+',0),
('IF', '^(if)$', 2),
('ELSE', '^(else)$', 2),
('WHILE', '^(while)$', 2),
('VAR', '^[a-z]+$', 0),
('NUM', '^0|[1-9][0-9]*$', 0),
('ASGN', '^=$', 0),
('OP', '^(\+|-|\*|/)$', 0),
('LBR', '^\($', 0),
('RBR', '^\)$', 0),
('LSBR', '^{$', 0),
('RSBR', '^}$', 0),
('LGOP', '^(>|<)$', 0)
]



def lexer(str):
    lexemes = []
    while(len(str)>0):
        lex = next_lexeme(str)
        lexemes.append(lex[:2])
        str = str[lex[3]:]
    return lexemes
        

def next_lexeme(str):
    accum = ''
    accum += str[0]
    if len(terminals_match(accum)) > 0:
        while len(terminals_match(accum)) > 0 and len(accum) < len(str):
            accum += str[len(accum)]
        if len(accum)>1:
            accum = accum[:len(accum)-1]
        matches = terminals_match(accum)
        return max(matches, key=lambda x: x[2])
    else:
        raise Exception('unexpected symbol')



def terminals_match(accum):
    matches = []
    for t in terminals:
        m = re.fullmatch(t[1], accum)
        if m != None:
            matches.append((t[0], m.string, t[2], m.endpos))
    return matches


def get_lexemes(str):
    lexemes = []
    accum = ''
    best = ('', '', True)
    space = False

    for c in str:
        if c == ' ' or c == '\t' or c == '\n':
            space = True
            continue

        for cl in terminals:
            cls = cl[1]
            res = re.match(cls, c)
            if res != None:
                newbest = cl
                if best != newbest:
                    if best[2] == False and newbest[2] == False:
                        if space != True:
                            raise Exception("Incorrect lexeme "+c)
                    lexemes.append((best[0], accum))
                    best = newbest
                    accum = c
                    space = False
                    break
                else:
                    if space == True:
                        if len(accum) > 0:
                            lexemes.append((best[0], accum))
                            accum = c
                            space = False
                    else:
                        accum += c
                    break

    if len(accum)>0:
        lexemes.append((best[0], accum))
    res = []

    for i in lexemes:
        if i[0]=='VAR' and i[1].upper() in list(map(lambda y: y[0], terminals[0:3])):
            res.append((i[1].upper(), i[1]))
        else:
            res.append(i)
    return res[1:]

