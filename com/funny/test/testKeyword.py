from sqlalchemy.util._collections import OrderedSet

def methodA(a, b, *args, **kwargs):
    
    print(a)
    print(b)
    print("--- args ---")
    print(args)
    print("--- kwargs ---")
    print(kwargs)

if __name__ == '__main__':
    methodA(1, 5, 3, 6, 9, name='rocky', age=18)    
    
    

ds = OrderedSet([1, 5, 2, 5, 5, 3, 3])



    
