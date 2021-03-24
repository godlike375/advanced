import lexer as lex
import re


test = "a = 2 + g l=((l*2+1)+a) if (c>0){ if(a>2){a = a+1 if(a>2){a = a+1} if(a>2){a = a+1} k=k+1 c=c+2}k = k+1}else{k=k+1}"

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
    ('varasgn', 'VAR ASGN'),
    ('value', 'NUM|VAR'),
    ('log_exp', 'value LGOP value( LGOP value)*'),
    ('if_condition', 'LBR log_exp RBR'),
    ('math', '(LBR value( OP value)* RBR)|(value( OP value)*)'),
    ('math', 'LBR math( OP math)* RBR'),
    ('expr', 'varasgn math'),
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

def remove_whitespaces(helper):
    for j in range(len(helper)):
        h2 = helper[j]
        if len(h2) > 0 and h2[0] == ' ':
            helper[j] = h2[1:]
        if len(h2) > 0 and h2[len(h2) - 1] == ' ':
            helper[j] = h2[:len(h2) - 1]

def get_positions(m, helper):

    start, end = int(m.start()), int(m.end())
    new_helper = [helper[:start], helper[start:end], helper[end:]]

    remove_whitespaces(new_helper)

    fp_len = len(new_helper[0].split(' '))
    sp_len = len(new_helper[1].split(' '))

    return start, end, fp_len, sp_len



def abstraction_up(AST):
    changes = False
    for g in grammar:
        while True:
            helper = get_helper_AST(AST)
            matched = re.search(g[1], helper)
            # суть в том, чтобы замапить массив лексем в строку из типов лексем:
            # [Node('VAR','a'), Node('ASGN','=')] => 'VAR ASGN'
            # по этой строке пройтись регулярками, найти совпадение (то есть найти один нетерминал)
            # взять стартовый и конечный индекс совпадения и разрезать строку на 1-3 строки:
            # 'IF LBR NUM LGOP NUM RBR' => 'IF LBR', 'NUM LGOP NUM', 'RBR'
            # разделить строки через пробелы на массивы строк
            # 'IF LBR', 'NUM LGOP NUM', 'RBR' => ['IF', 'LBR'], (a) ['NUM', 'LGOP', 'NUM'] (b), ['RBR]
            # получшить индексы начала и конца (a, b) среднего массива
            # и таким образом получить аналогичные индексы для оригинального массива Nodes
            # далее в оригинальном массиве заменить по этим индексам несколько нод на новую
            # а ля [Node(IF, if), Node(LBR, '(') Node(log_exp, [Node('NUM', '1'), Node('OP', '*')....]),  Node('RBR', ')')  ]
            if matched != None:
                changes = True
                start, end, first_len, second_len = get_positions(matched, helper)
                NEW_AST = []
                if start != 0:
                    NEW_AST.extend(AST[:first_len])
                    NEW_AST.append(Node(g[0], AST[first_len:first_len + second_len]))
                    if end != len(helper):
                        NEW_AST.extend(AST[first_len + second_len:len(AST)])
                else:
                    NEW_AST.append(Node(g[0], AST[:second_len]))
                    if end != len(helper):
                        NEW_AST.extend(AST[second_len:len(AST)])

                AST = NEW_AST

            else:
                break
        print(helper)
    return changes, AST



def parse_AST(lexemes):
    lexemes = list(filter(lambda x: x[0]!='WS', lexemes))
    AST = to_nodes(lexemes)
    while True:
        changes, NEW_AST = abstraction_up(AST)
        AST = NEW_AST
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



print(parse_AST(tokens))


