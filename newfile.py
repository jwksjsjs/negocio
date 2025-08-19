from erros import ErroWLAN
#teste
def soma():
    
    if 1+1 == 3:
        print(3)
        
    else:
        raise ErroWLAN()



try:
    soma()
    
    
except ErroWLAN as E:
    print(E.pin())
