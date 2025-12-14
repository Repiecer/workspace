M=int(1e6+5)
MOD=int(1e9)                            #取余数的数
x_idx=[0] ; y_idx=[0] ; color=[0]
father=[0]*M; d=[0]*M

def init(lim:int):                      #加权并查集初始化模板init
    for i in range(1,lim+1):
        father[i]=i ; d[i]=0
def get_father(x:int):                  #并查集组合的合并，权重数组保存异或值
    if x==father[x]:return x
    f=get_father(father[x])
    d[x]^=d[father[x]]
    father[x]=f
    return f

def mul(a:int,b:int):                   #快速幂运算模板mul(x,y)-->pow(x,y)                  
    ans=1
    while b:
        if b&1:ans=(ans*a)%MOD
        a=(a*a)%MOD
        b>>=1
    return ans
def solve(op:int):
    init(n+m)
    father[n+1]=1
    global k
    for i in range(1,k+1):
        if x_idx[i]==1 and y_idx[i]==1:continue  #(1,1)点无需再次判断
        temp=((x_idx[i]%2==0) and (y_idx[i]%2==0))^color[i]^op
        a=get_father(x_idx[i]) ; b=get_father(y_idx[i]+n)
        res=d[x_idx[i]]^d[y_idx[i]+n]^temp
        if a==b and res:return 0
        father[a]=b
        d[a]^=res
    cnt=0
    for i in range(1,n+m+1):
        if father[i]==i:cnt+=1
    return mul(2,cnt-1)

if __name__=='__main__':
    n,m,k=map(int,input().split())
    flag=-1
    for i in range(k):
        idx,idy,col=map(int,input().split())
        x_idx.append(idx);y_idx.append(idy);color.append(col)
    for i in range(1,k+1):
        if (x_idx[i]==1) and (y_idx[i]==1):flag=color[i]
    if flag==0:
        print(solve(0))
    elif flag==1:
        print(solve(1))
    else:
        print((solve(0)+solve(1))%MOD)