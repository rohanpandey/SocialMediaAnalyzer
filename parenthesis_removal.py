from collections import Counter
import operator
def parenthesis_removing(s):
    result=""
    curr=False
    for i in range(0,len(s)):
        if(not curr):
            if(s[i]=='('):
                curr=True
            else:
                result+=s[i]
        else:
            if(s[i]==')'):
                curr=False
    return result
def double_space_remover(s):
    result=s[0]
    for i in range(1,len(s)):
        if(s[i-1]==' ' and s[i]==' '):
            continue
        else:
            result+=s[i]
    return result
check="This is      (an exampl e   f)   string.(Parentheses   removed) No pa  rentheses at all"
a=[1,1,1,2,2,2,2,2,3,3,3,4,4,44,4,4,44,4,4,5,5,5,5,5,5,5,5,5]
d=Counter(a)
newA = sorted(d, key=d.get, reverse=True)[:5]
print(d)
print(newA)