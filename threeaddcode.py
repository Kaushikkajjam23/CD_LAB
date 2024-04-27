class Stack:    
    def __init__(self,max_lim):
        self.__lis_of_eles=[]
        self.__max_lim=max_lim
        self.__top=-1
    def get_stack_eles(self):
        return self.__lis_of_eles
    def is_full(self):
        if(self.__top==self.__max_lim-1):
            return True
        else:
            return False
    def is_empty(self):
        if(self.__top==-1):
            return True
        else:
            return False
    def push(self,E):
        if(self.is_full()):
            print("Stack is full")
            return 
        else:
            self.__top+=1
            self.__lis_of_eles.insert(self.__top,E)
            #print("Pushed ele: ",self.__lis_of_eles[self.__top])    
    def pop(self):
        if(self.is_empty()):
            print("Stack is empty")
            return
        else:
            del_ele=self.__lis_of_eles.pop(self.__top)
            #print("Deleted element: ",del_ele)            
            self.__top-=1
            return del_ele
    def fetch_top(self):
        return self.__top
    def display(self):
        i=self.__top
        for j in range(i,-1,-1):
            print(self.__lis_of_eles[j])
class Equation:
    # List of arithmetic operators according to precedence
    operators1 = ["*", "/"]
    operators2 = ["-", "+"]
    # Only alphabet operands:
    operands_lower_case = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    operands_upper_case = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    def __init__(self, given):
        self.__c = 0
        lis = given.split("=")  # lis[0]-location to store answer,lis[1]-location to store expression
        self.__res = lis[0] if len(lis) > 1 else "result"
        self.__expr = lis[1] if len(lis) > 1 else given
        self.__last_symbol = lis[1][-1]
    def get_c(self):
        return self.__c
    def get_result(self):
        return self.__res
    def get_expression(self):
        return self.__expr
    def get_last_symbol(self):
        return self.__last_symbol
    def is_operand(self, ele):
        return (ele in self.operands_lower_case) or (ele in self.operands_upper_case)
    def is_operator(self, op):
        return (op in self.operators1) or (op in self.operators2)
    def validate(self):
        f = self.__expr[0]
        n = len(self.__expr)
        if (
            (f not in self.operands_lower_case and f not in self.operands_upper_case)
            or (self.__last_symbol not in self.operands_lower_case
                and self.__last_symbol not in self.operands_upper_case)
        ):
            return False
        s = Stack(n)
        for ele in self.__expr:
            if s.is_empty():
                if self.is_operand(ele):
                    s.push(ele)
                    self.__c += 1
                else:
                    return False
            else:
                top_pos = s.fetch_top()
                stack_elements = s.get_stack_eles()
                if self.is_operand(stack_elements[top_pos]):
                    if self.is_operator(ele):
                        s.push(ele)
                    else:
                        return False
                elif self.is_operator(stack_elements[top_pos]):
                    if self.is_operand(ele):
                        s.push(ele)
                        self.__c += 1
                    else:
                        return False
                else:
                    return False
        return True
class ThreeAddressCodeGenerator(Equation):
    def __init__(self, eqn):
        super().__init__(eqn)
    def generate(self):
        if not super().validate():
            print("INVALID expression")
            return
        exp = super().get_expression()
        n = len(exp)
        sob = Stack(n)  # Stack for operands and temporary variables
        temp_var = 1  # Counter for temporary variables
        i = 0
        track = 0  # Track for handling high precedence operators
        while i < n:
            e = exp[i]
            if super().is_operator(e):
                if e not in super().operators1:
                    sob.push(e)
                    i += 1
                else:
                    track += 1
                    top_ele = sob.pop()
                    t = "t" + str(temp_var)
                    sob.push(t)
                    temp_var += 1
                    # Print three-address code based on track value
                    if track == 1:
                        print(f"{t} := {top_ele} {e} {exp[i+1]}")
                    else:
                        prev_val = sob.pop()
                        print(f"{t} := {prev_val} {e} {exp[i+1]}")
                        sob.push(prev_val)  # Push back the previous value
                    i += 2
            else:
                sob.push(e)
                i += 1
        track1 = 0
        tracker = sob.fetch_top()
        while tracker > -1:
            track1 += 1
            operand2 = sob.pop()
            operator = sob.pop()
            operand1 = sob.pop()
            t = "t" + str(temp_var)
            sob.push(t)
            temp_var += 1
            # Print three-address code based on track values
            if track == 0 and track1 == 1:
                prev_val = t
            if track >= 1:
                prev_val = operand2  # Use the latest operand for calculations
            if track1 > 1:
                print(f"{t} := {operand1} {operator} {prev_val}")
            else:
                print(f"{t} := {operand1} {operator} {operand2}")
            tracker -= 3
# User Input
expression = input("Enter an arithmetic expression (result_var = expression): ")
# Generate three-address code
tac_generator = ThreeAddressCodeGenerator(expression)
tac_generator.generate()