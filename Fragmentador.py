def fragmenter(file):
    ans=[]
    size=int(len(file)/6)
    residuo=len(file)%6
    inc=0
    ant=0
    for i in range(6):
        ant=inc
        if(residuo!=0):
            inc+=1
            residuo-=1
        ans.append(file[size*i+ant:size*(i+1)+inc])       
    return ans
file=[1,2,3,4,5,6,7,8,9,10,11]
ans=fragmenter(file)
for a in ans:
    print(a)
