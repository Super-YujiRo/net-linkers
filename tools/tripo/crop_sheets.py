from PIL import Image, ImageDraw
import numpy as np, sys
U='/root/.claude/uploads/ae98a61e-3799-512a-a9f6-469101aeb247/'
M={'volt':'f483a9d3','mist':'eb5359ca','crow':'2cf0296a','canary':'452a813b','dam':'a14cf3d3','crane':'070d2980','jammer':'ee52ce71','neon':'cd0b4a76','liner':'5eb67467','wave':'3df291e5','hanabi':'4dcf6573','bamboo':'7f49ca84','shade':'25937445'}
def nobg(im):
    a=np.array(im.convert('RGB')).astype(int);h,w,_=a.shape
    white=(a.min(2)>232)&((a.max(2)-a.min(2))<20)
    # flood from border
    from collections import deque
    m=np.zeros((h,w),bool);q=deque()
    for x in range(w):
        for y in (0,h-1):
            if white[y,x] and not m[y,x]:m[y,x]=1;q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if white[y,x] and not m[y,x]:m[y,x]=1;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and white[ny,nx] and not m[ny,nx]:m[ny,nx]=1;q.append((ny,nx))
    rgba=np.dstack([a,np.where(m,0,255)]).astype(np.uint8)
    return Image.fromarray(rgba,'RGBA')
out={}
for k,f in M.items():
    im=Image.open(U+f+'-image.png').convert('RGB')
    # front full-body: leftmost column x<(first figure gap)
    a=np.array(im).astype(int);nonw=(a.min(2)<225)
    sub=nonw[0:640,0:360];cols=np.where(sub.sum(0)>3)[0];rows=np.where(sub.sum(1)>3)[0]
    x0,x1,y0,y1=cols.min(),cols.max(),rows.min(),rows.max()
    full=im.crop((x0,y0,x1+1,y1+1));nobg(full).save(f'front_{k}.png')
    out[k]=(x0,y0,x1,y1)
print(out)
