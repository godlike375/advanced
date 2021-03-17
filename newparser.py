import lexer as lex
import re


test = "a = 2 + g l=(1+(l*2+1)+a) if (c>0){ if(a>2){a = a+1 if(a>2){a = a+1} if(a>2){a = a+1} k=k+1 c=c+2}k = k+1}else{k=k+1}"

print(test)
print(lex.lexer(test))


#получить строку из типов лексем
def get_helper_AST(AST):
    return ' '.join(list(map((lambda x: x.name), AST)))
#преобразовать массив лексем в массив Node
def to_nodes(lexemes):
    return list(map(lambda x: Node(x[0], x[1]), lexemes))



grammar = \
[
    (' ', ' WS '),
    ('expr', 'VAR ASGN (LBR (NUM|VAR)( OP (NUM|VAR))* RBR)|((NUM|VAR)( OP (NUM|VAR))*)'),
    ('value', 'NUM|VAR'),
    ('math', '(LBR value( OP value)* RBR)|(value( OP value)*)'),
    ('math', 'LBR math( OP math)* RBR'),
    ('expr', 'value ASGN math'),
    ('log_exp', 'value LGOP value( LGOP value)*'),
    ('if_condition', 'LBR log_exp RBR'),
    ('body', 'LSBR(( expr)*( if_exp)*)* RSBR'),
    ('if_head', 'IF if_condition'),
    ('if_exp', 'if_head body( ELSE body)?')
]

tokens = lex.lexer(test)

class Node:
    def __init__(self, name, token):
        self.token = token
        self.name = name

    def __repr__(self):
            return "({a}, {b})".format(a=self.name, b=self.token)

def replace(lexemes):
    lexemes = list(filter(lambda x: x[0]!='WS', lexemes))
    AST = to_nodes(lexemes)
    while True:
        changes = False
        for g in grammar:
            while True:
                helper = get_helper_AST(AST)
                m = re.search(g[1], helper)
                if m != None:
                    changes = True
                    start, end = int(m.start()), int(m.end())
                    helper2 = [helper[:start], helper[start:end], helper[end:]]
                    NEW_AST = []
                    for j in range(len(helper2)):
                        h2 = helper2[j]
                        if len(h2)>0 and h2[0]==' ':
                            helper2[j] = h2[1:]
                        if len(h2)>0 and h2[len(h2)-1]==' ':
                            helper2[j] = h2[:len(h2)-1]

                    fp_len = len(helper2[0].split(' '))
                    sp_len = len(helper2[1].split(' '))
                    if start != 0:
                        NEW_AST.extend(AST[:fp_len])
                        NEW_AST.append(Node(g[0], AST[fp_len:fp_len + sp_len]))
                        if end != len(helper):
                            NEW_AST.extend(AST[fp_len + sp_len:len(AST)])
                    else:
                        sp_len = len(helper2[1].split(' '))
                        NEW_AST.append(Node(g[0], AST[:sp_len]))
                        if end != len(helper):
                            NEW_AST.extend(AST[sp_len:len(AST)])

                    AST = NEW_AST

                else:
                    break
            print(helper)
        if changes == False:
            break

    print_AST(AST, -1, '')
    return AST

def print_AST(AST, lvl, name):
    print('\n' + '\t' * lvl, end='')
    print(name)
    for i in AST:
        if type(i.token) == list and len(i.token)>1:
            #print('\n' + '\t' * lvl, end='')
            print_AST(i.token, lvl+1, i.name)
        else:
            print('\n' + '\t' * (lvl+1), end='')
            print(i)


def evaluate(lexemes):
    pass



print(replace(tokens))


