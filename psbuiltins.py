from colorsys import hls_to_rgb
from colors import *
from elements import StrConstant, DictConstant, CodeArray
#Name: Jonathan Banos
#Got help from Kace C and Emma M
#For Hw 5 got help from Conner D and Ryan R
class Stacks:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if(len(self.dictstack) > 0):
            return self.dictstack.pop()

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,dictionary):
        if isinstance(dictionary, tuple):
            self.dictstack.append((dictionary))
        else:
            self.opPush(dictionary)
            print("Error")
    #apply, if, ifelse, for needs changes as well
    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):
        if len(self.dictstack) > 0:
            dicts = self.dictPop()
            dicts[1][name] = value
            self.dictPush(dicts)
        else:
            newDictionay = {}
            newDictionay[name] = value
            self.dictPush((0,newDictionay))

        #NEED TO CHANGE THIS


    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        #needs to find a way to handle static and dynamic
        #This is static look up
        def helpers(name, ind, dictStack):
            if name in dictStack[ind][1]:
                yer = dictStack[ind][1][name]
                return dictStack[ind][1][name]
            elif ind == 0:
                return None
            else:
                helpers(name, dictStack[ind][0], dictStack)

        if self.scope == "static":
            newN = "/" + name
            index = len(self.dictstack)-1
            temp = helpers(newN, index,self.dictstack)
            return temp
            
        else:
            newN = "/" + name
            opt = 0
            for k,v in reversed(self.dictstack):
               if newN in v.keys():
                    opt = opt + 1  
                    return v[newN]
            if opt == 0:
                return None
            

    
        
    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 - op2)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 % op2)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mod expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of the StrConstant objects;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, StrConstant) and isinstance(op2, StrConstant):
              if(op1.value == op2.value):
                self.opPush(True)
              else:
              #  print("Error: == - one of the operands is not a number value")
                self.opPush(False)
            elif isinstance(op1, DictConstant) and isinstance(op2, DictConstant):
                if (op1 == op2):
                    self.opPush(True)
                else:
                  #  print("Error: == - one of the operands is not a number value")
                    self.opPush(False)
            elif isinstance(op1, int) and isinstance(op2, int):
                if (op1 == op2):
                    self.opPush(True)
                else:
                   # print("Error: == - one of the operands is not a number value")
                    self.opPush(False)

        else:
            print("Error: eq expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if (op1 < op2):
                self.opPush(True)
            else:
                self.opPush(False)
        #print("Error: lt - one of the operands is not a number value")    
                            
        else:
            print("Error: lt expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if (op1 > op2):
                self.opPush(True)
            else:
                self.opPush(False)
                            
        else:
            print("Error: gt expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print("===**opstack**===")
        
        # print("=================")
        
        #print(OKGREEN+"**opstack**")
        for item in reversed(self.opstack):
            print(item)
        print("=================")
        print("===**dictstack**===")
        #print(RED+"**dictstack**")
        count = len(self.dictstack)-1
        for k,v in reversed(self.dictstack):
            m = count
            print("---{}----{}---".format(count,k))
            for item in v:

                print("{}  {}".format(item,v[item]))
            
        print("-----------------------"+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        #this pops from the top of the of the stack
        #test this
        op = self.opPop()
        self.opPush(op)
        self.opPush(op)
        

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    #need help
    def copy(self):
        #need help
        op = self.opPop()
        if not isinstance(op,int):
            self.opPush(op)
            print("ERROR COPY VALUE IS NOT AN INTEGER")
            return
        
        if op > len(self.opstack):
            print("ERROR: Don't have enough items in your stack for the copy function!")
        vals = []
        while op > 0:
            vals.append(self.opPop())
            op-=1
        for i in reversed(vals):
            self.opPush(i)
        for i in reversed(vals):
            self.opPush(i)
        
    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        print(len(self.opstack))
        self.opstack.clear()
        print(len(self.opstack))
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        #This is the top of the stack
        top = self.opPop()
        #this is the second from the top
        second = self.opPop()
        self.opPush(top)
        self.opPush(second)
        

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        size = self.opPop()
        newstr = '('
        for i in range(size):
            newstr += "\x00"
        newstr += ')'
        self.opPush(StrConstant(newstr))
        
    
    """Creates a new empty dictionary  pushes it on the opstack """
    #test this
    def psDict(self):
        size = self.opPop()

        newDict = DictConstant({})
        self.opPush(newDict)
        

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictConstant and StrConstant values.
    """
    #not sure
    def length(self):
        vals = self.opPop()

        if isinstance(vals, DictConstant):
            self.opPush(len(vals.value))
        elif isinstance(vals, StrConstant):
            pushing = len(vals.value) -2
            self.opPush(pushing)
        else:
            print("ERROR: Element was not a dictionary type or string type")



    """ Pops either:
         -  "A (zero-based) index and an StrConstant value" from opstack OR 
         -  "A `name` (i.e., a key) and DictConstant value" from opstack.  
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictConstant, gets the value for the given `name` from DictConstant's dictionary value and pushes it onto the opstack
    """
    def get(self):
        index = self.opPop()
        getfrom = self.opPop()
        if isinstance(getfrom, StrConstant):
            py = getfrom.value
            val = ord(py[index +1])
            self.opPush(val)
        elif isinstance(getfrom, DictConstant):
            self.opPush(getfrom.value[index])
        else:
            print("ERROR: The argument was not of string or dictionary type!")
   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StrConstant value from  opstack", OR
    - "An `item`, a `name`, and a DictConstant value from  opstack". 
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an DictConstant, adds (or updates) "name:item" in DictConstant's dictionary `value`.
    """
    def put(self):
        val = self.opPop()
        index = self.opPop()

        putinto = self.opPop()
        if isinstance(putinto, StrConstant):
            fin = putinto.value
            fin = fin.replace('(', '')
            fin = fin.replace(')','')
            num = chr(val)
           # num = ord(num)
            putinto.value = '(' +"".join(fin[:index]+ num+ fin[1+index:]) + ')'
        if isinstance(putinto, DictConstant):
            putinto.value[index] = val
      #  self.opPush(putinto)    
        

    """
    getinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a `count`, a (zero-based) `index`, and an StrConstant value from  opstack, and 
    extracts a substring of length count from the `value` of StrConstant starting from `index`,
    pushes the substring back to opstack as a StrConstant value. 
    """ 
    def getinterval(self):
        count = self.opPop()
        index = self.opPop()
        val = self.opPop()
        
        if not isinstance(val, StrConstant):
            print("ERROR: Element is not a string constant value!")
            return
        val = val.value
        val = val.replace('(', '')
        val = val.replace(')','')
        temp = val[index:index+count]
        temp = '(' + temp + ')'
        self.opPush(StrConstant(temp))

    """
    putinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a StrConstant value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StrConstant's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        substr = self.opPop()
        index = self.opPop()
        val = self.opPop()
        if not (isinstance(val, StrConstant)):
            print("ERROR: This element is not of strcontant type!")
            return
        subs = substr.value
        subs = subs.replace('(', '')
        subs = subs.replace(')', '')
        val.value = (val.value[:index +1] + subs+val.value[index +len(subs)+1:])
        #substr.value = 
       # print("hello")
      #  one = 2
        #self.opPush(StrConstant(val.value[:index] + substr.value+val.value[index +len(substr.value):]))

    """
    search is a string only operator, i.e., works only with StrConstant values. 
    Pops two StrConstant values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StrConstant values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        searchfor = self.opPop()
        val = self.opPop()
        
        if isinstance(val, StrConstant):
            #transform the paren to no paren 
            #add the value           
           # one = "hello"

            val = val.value
            searching  = searchfor.value
            searching = searching.replace('(','')
            searching = searching.replace(')','')
            val = val.replace('(', '')
            val = val.replace(')', '')
            if searching in val:
                first, *rest = val.split(searching)
                val = searching.join(rest)
                val = '(' + val + ')'
                first = '(' + first + ')'

                self.opPush(StrConstant(val))
                self.opPush(searchfor)
                self.opPush(StrConstant(first))
                self.opPush(True)
            else:
                val = '(' + val + ')'
                self.opPush(StrConstant(val))
                self.opPush(False)
        else:
            print("ERROR: Element is not of type strconstant")
    
        

    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictConstant value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        #check this
        val = self.opPop()
        if isinstance(val, DictConstant):
           # if val.value:
            self.dictPush(val.value)
        else:
            self.opPush(val)
            print("ERROR: This is not a DictConstant value!")


    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        if len(self.dictstack) > 0:
            self.dictPop()
        else:
            print("error")

        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        val = self.opPop()
        nam = self.opPop()
        self.define(nam,val)
        

    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a Block and a boolean value, if the value is True, executes the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        if len(self.opPop) > 1:
            block = self.opPop()
            bool_val = self.opPop()
            if bool_val is True and isinstance(bool_val, bool) and isinstance(block, CodeArray):
                self.dictPush((len(self.dictstack)-1),{})
                block.apply(self)
                self.dictPop()
        

    """ ifelse operator
        Pops two Blocks and a boolean value, if the value is True, executes the bottom Block otherwise executes the top Block.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        if len(self.opstack) > 2:
            block1 = self.opPop()
            block2 = self.opPop()
            bool_val = self.opPop()
            if bool_val is True and isinstance(bool_val, bool):
                self.dictPush((len(self.dictstack)-1),{}) 
                block2.apply(self)
                self.dictPop()


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a Block, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the Block. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
        block = self.opPop()
        end = self.opPop()
        inc = self.opPop()
        begin = self.opPop()
        vars = 0
        if inc < 0:
            vars = end-1
        else:
            vars = end+1


        for i in range(begin,vars, inc):
            self.opPush(i)
            block.apply(self)

        

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

