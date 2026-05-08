###### MATTIA SIMONUTTI SM3201292  #####

class EmptyStackException(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])


class Expression:

    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def from_program(cls, text, dispatch):  
        
        # otteniamo una lista con gli elementi della stringa text, passata in input, separati
        expr = text.split()                                    
        stack = Stack()                                        
        
        # iteriamo sugli argomenti della lista ottenuta
        for arg in expr:   
            # se l'elemento non è nel dizionario delle azioni (dispatch) valutiamo il caso sia una costante o una variabile  e facciamo push sullo stack                                  
            if( arg not in dispatch):                          
                try:                                           
                    value = float(arg)                              
                    stack.push(Constant(value))
                except ValueError:
                    stack.push(Variable(arg))
              
             # se è presente in dispatch, ne ricaviamo l'arità, facciamo tanti pop dallo stack tanta quanta è l'arità (otteniamo i parametri)
             # facciamo push del risultato della funzione coi parametri ottenuti   
            else:
                arity = dispatch[arg].arity
                param =[stack.pop() for i in range(arity)]
                stack.push(dispatch[arg](param))
                
        return stack.pop()       
                
    def evaluate(self, env):
        raise NotImplementedError()


class MissingVariableException(Exception):
    pass


class Variable(Expression):

    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        if(self.name in env):
            return env[self.name]
        else:
            print(f"manca variabile {self.name}")
            raise MissingVariableException

    def __str__(self):
        return self.name


class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)
    


class Operation(Expression):

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        values = []   
           
        # la lista values viene riempita con le valutazioni degli argomenti passati in input
        # e poi applichiamo loro l'operazione indicata
        
        for arg in self.args:                           
            values.append(arg.evaluate(env))
        return self.op(*values)
            
    def op(self, *args):
        raise NotImplementedError()

    def __str__(self):
        res = f'({self.name}'
        for arg in self.args:
            res += f' {arg}'
        res += f')'
        return res


###############  operazioni matematiche  ###############


class BinaryOp(Operation):             
    arity = 2


class UnaryOp(Operation):
    arity = 1


class Addition(BinaryOp):
    name = "+"
    
    def op(self, x, y):
        return x+y


class Subtraction(BinaryOp):
    name = "-"

    def op(self, x, y):
        return x-y

class Division(BinaryOp):
    name = "/"
    
    def op(self, x ,y):
        if y == 0:
            raise ValueError("Divisione per zero")
        return x/y


class Multiplication(BinaryOp):
    name  = "*"

    def op(self, x, y):
        return x*y

class Power(BinaryOp):
    name  = "**"
    
    def op(self, x, y):
        return x**y


class Modulus(BinaryOp):
    name = "%"
    
    def op(self, x ,y):
        return x%y


class Reciprocal(UnaryOp):
    name = "1/"
    
    def op(self,x):
        if x == 0:
            raise ValueError("Divisione per zero")
        return 1/x


class AbsoluteValue(UnaryOp):
    name = "abs"
    
    def op(self, x):
        return abs(x)
   
   
 ################## operazioni di confronto ####################
 
class Greater(BinaryOp):           
    name = ">"
    
    def op(self, x, y):
        return x>y
    
class Greater_Eq(BinaryOp):
    name = ">="
    
    def op(self, x, y):
        return x>=y

class Equal(BinaryOp):
    name = "=="
    
    def op(self, x, y):
        return x==y
    
class Less(BinaryOp):
    name = "<"
    
    def op(self, x, y):
        return x<y
    
class Less_Eq(BinaryOp):
    name = "<="
    
    def op(self, x, y):
        return x<=y
    
class Not_Eq(BinaryOp):
    name = "!="
    
    def op(self, x, y):
        return x!=y

##########################

class Alloc(UnaryOp):
    
    name = 'alloc'
    
    # Alloca una singola variabile e le assegna il valore 0 come default
    # in input viene passato il nome della variabile da allocare
    
    def __init__(self, args):
        self.args = args
    
    def evaluate(self, env):
        env[f'{self.args[0]}'] = 0
        
        
    

class Valloc(BinaryOp):
    
    name = 'valloc'
    
    # Alloca un array di dimensione n con valori di default 0
    # in input vengono passati il nome dell'array e la sua dimensione
    
    def __init__(self, args):
        self.args = args
        self.n = args[1]
        self.var = args[0]
        
    def evaluate(self, env):
        
        dim = self.n.evaluate(env)
        
        if not dim.is_integer() or dim<0:
            raise ValueError ("Dimensione deve essere un intero non negativo")
        
        # list comprehension per riempire l'array di zeri
        env[f'{self.var}'] = [0 for _ in range(int(dim))] 
        
        
class Setq(BinaryOp):
    
    name = 'setq'
    
    def __init__(self, args):
        self.args = args
        self.expr = args[1]
        self.x = args[0]
        
    # Dati in input un'espressione e una variabile, viene assegnata la valutazione dell'espressione alla variabile e viene poi ritornata
        
    def evaluate(self, env):                                                  
        if f'{self.x}' in env:                                                
            env[f'{self.x}'] = self.expr.evaluate(env)
            return env[f'{self.x}']
        else:
            raise MissingVariableException
        


class Setv(Operation):
    
    name = 'setv'
    arity = 3
    
    def __init__(self, args):
        self.args = args
        self.expr = args[2]                                                 
        self.n = args[1]                                                    
        self.x = args[0]
        
    # dati in input un'espressione, una variabile e un indice n, viene assegnata in posizione x[n] 
    # la valutazione dell'espressione (x rappresenta un array)
        
    def evaluate(self, env):      
        
        if f'{self.x}' not in env:
            raise MissingVariableException
        
        if not isinstance(env[f'{self.x}'], list):
            raise ValueError(f"Variabile {self.x} non è un array")
        
        if not self.n.evaluate(env).is_integer():
            raise ValueError ("Indice deve essere un intero")
        
        if self.n.evaluate(env) > len(env[f'{self.x}']):
            raise IndexError ("Indice troppo elevato")   

        env[f'{self.x}'][int(self.n.evaluate(env))] = self.expr.evaluate(env)
        return env[f'{self.x}'][int(self.n.evaluate(env))]
        


class Prog(Operation):
    
    # in base all'arità valutiamo le precedenti 2/3/4 espressioni, passate come argomento
    # e ritorniamo il valore della prima
    
    def __init__(self, args):
        self.args = args
        
    def evaluate(self, env):
                                                                       
        for expr in self.args:                                        
            res = expr.evaluate(env)
        return res
    
class Prog2(Prog):
    name = "prog2"
    arity = 2

class Prog3(Prog):
    name = "prog3"
    arity = 3
    
class Prog4(Prog):
    name = "prog4"
    arity = 4


##### condizionali #####

class Cond_if(Operation):
    
    name = "if"
    arity = 3
    
    # in input vengono passati una condizione, un ramo dell'if per la condizione soddisfatta
    # e uno per la condizione non soddisfatta, a seconda che la condizione sia vera o falsa  
    # valutiamo uno dei due rami dell'if
    
    def __init__(self, args):                                           
        self.args = args                                                
        self.if_no = args[2]
        self.if_yes = args[1]
        self.cond = args[0]
        
    def evaluate(self, env):
        if self.cond.evaluate(env):
            return self.if_yes.evaluate(env)
        
        return self.if_no.evaluate(env)
        


class While(BinaryOp):
    
    name = "while"
    
    # classe While, data una condizione e una espressione, 
    # valutiamo ripetutamente l'espressione fino a che non è più soddisfatta la condizione
    
    def __init__(self, args):
        self.args = args
        self.expr = args[1]                                            
        self.cond = args[0]
        
     
    def evaluate(self, env):
        if not isinstance(self.cond, Expression):
            raise TypeError("Cond deve essere un'istanza di Expression")

        while self.cond.evaluate(env):
            self.expr.evaluate(env) 
        return 
            

class For(Operation):
    
    name = "for"
    arity = 4
    
    # passati in input una variabile i, una costante start, una costante end e l'espressione da valutare
    # viene inserito nell'ambiente la variabile i associandole inizialmente il valore di start e ciclando fintantochè il valore di i
    # risulta essere inferiore a quello di end valutiamo l'espressione e incrementiamo di 1 il valore di i
    
    def __init__(self, args):                                           
        self.args = args                                                
        self.expr = args[3]                                             
        self.end = args[2]
        self.start = args[1]
        self.i = args[0]
        
    
    def evaluate(self, env):

        if not self.start.evaluate(env).is_integer():
            raise ValueError("Start deve essere un intero")
        
        if not self.end.evaluate(env).is_integer():
            raise ValueError("End deve essere un intero")
        
        
        start = self.start.evaluate(env)
        end = self.end.evaluate(env)
        env[f'{self.i}'] = start
        
        while(self.i.evaluate(env)<end):
            self.expr.evaluate(env)
            env[f'{self.i}']+= 1
            
        
class Defsub(BinaryOp):
    
    name = "defsub"
    
    # classe Defsub, usata per definire una subroutine, in input vengono passati una espressione e una variabile, 
    # inseriamo la variabile nell'ambiente associandole l'espressione in modo tale da utilizzarla (valutarla)
    # quando chiamata dalla classe Call
    
    def __init__(self, args):                                           
        self.args = args                                                
        self.expr = args[1]                                            
        self.f = args[0]
        
    def evaluate(self, env):
        env[f'{self.f}'] = self.expr

class Call(UnaryOp):
    
    name = "call"
    
    # classe Call, usata per valutare l'espressione associata a f dalla classe defsub,
    # sostituisce all'espressione il valore
    
    def __init__(self, args):                                          
        self.args = args
        self.f = args[0]
        
    def evaluate(self, env):
        env[f"{self.f}"].evaluate(env)
        
        
class Print(UnaryOp):
    name = "print"
    
    # Valuta un'espressione, stampa il risultato e lo ritorna
    # in input passiamo un'espressione

    def __init__(self, args):
        self.args = args
        self.expr = args[0]

    def evaluate(self, env):
        res = self.expr.evaluate(env)
        print(f"Risultato/i: {res}")
        return res     
        
class Nop(Operation):
    name = "nop"
    arity = 0
    
    # non esegue nessuna operazione

    def __init__(self, args):
        self.args = args
        pass

    def evaluate(self, env):
        pass
    


d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
     "/": Division, "1/": Reciprocal, "abs": AbsoluteValue,"%": Modulus}

d.update({"alloc": Alloc,"valloc": Valloc,"setq": Setq, "setv": Setv, "prog" : Prog, "prog2":Prog2,
          "prog3":Prog3, "prog4":Prog4
})

d.update({
    ">": Greater, ">=": Greater_Eq, "=" : Equal , "!=": Not_Eq,
    "<": Less, "<=": Less_Eq
})

d.update({
    "if": Cond_if, "while": While, "for": For, "defsub": Defsub, "call": Call,
    "print": Print, "nop": Nop
})

es = 'x 1 + x setq x 10 > while x alloc prog2'
e = Expression.from_program(es, d)
print(e)
env1 = {}
print(e.evaluate(env1))

