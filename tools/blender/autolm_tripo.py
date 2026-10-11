import bpy,numpy as np,os
from collections import deque
D=r'C:\Users\LoZy\Downloads\\'
def load_V(fn):
    if 'TP_AN' not in bpy.data.scenes:bpy.data.scenes.new('TP_AN')
    sc=bpy.data.scenes['TP_AN'];bpy.context.window.scene=sc
    for o in list(sc.objects):bpy.data.objects.remove(o,do_unlink=True)
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=fn);new=[o for o in bpy.data.objects if o not in before]
    V=[]
    for M in [o for o in new if o.type=='MESH']:
        co=np.empty(len(M.data.vertices)*3,np.float32);M.data.vertices.foreach_get('co',co);co=co.reshape(-1,3)
        mw=np.array(M.matrix_world);V.append(co@mw[:3,:3].T+mw[:3,3])
    for o in new:bpy.data.objects.remove(o,do_unlink=True)
    return np.concatenate(V)
def runs(row):
    r=[];s=None
    for i,v in enumerate(row):
        if v and s is None:s=i
        if not v and s is not None:r.append((s,i-1));s=None
    if s is not None:r.append((s,len(row)-1))
    return r
def auto_lm(V,N=240):
    zmin=V[:,2].min();V=V.copy();V[:,2]-=zmin;H=V[:,2].max()
    cx=(V[:,0].min()+V[:,0].max())/2
    s=H/N;W=int((V[:,0].max()-V[:,0].min())/s)+4;x0=V[:,0].min()-2*s
    img=np.zeros((N+1,W),bool);ix=((V[:,0]-x0)/s).astype(int);iz=(V[:,2]/s).astype(int);img[np.clip(iz,0,N),np.clip(ix,0,W-1)]=True
    # dilate 1
    d=img.copy();d[1:]|=img[:-1];d[:-1]|=img[1:];d[:,1:]|=img[:,:-1];d[:,:-1]|=img[:,1:];img=d
    X=lambda i:x0+(i+.5)*s
    # torso center x: midpoint of the two leg runs at .2H (fallback median)
    m=(V[:,2]>.5*H)&(V[:,2]<.7*H);tc=float(np.median(V[m,0]))
    z=int(.2*N);rs=runs(img[z])
    if len(rs)>=2:
        rs=sorted(rs,key=lambda r:-(r[1]-r[0]))[:2];tc=float(np.mean([X((r[0]+r[1])/2) for r in rs]))
    tci=int((tc-x0)/s)
    # per row: central run (containing tci) and outer runs
    info={}
    for z in range(N+1):
        rs=runs(img[z]);c=[r for r in rs if r[0]<=tci<=r[1]]
        info[z]=(rs,c[0] if c else None)
    # legs: at z=.08H find 2 runs closest to center
    def legx(fz):
        z=int(fz*N);rs=info[z][0]
        rs=sorted(rs,key=lambda r:abs((r[0]+r[1])/2-tci))[:2]
        if len(rs)<2:return None
        return sorted([abs(X((r[0]+r[1])/2)-tc) for r in rs])
    ax=legx(.06) or [0.07*H,0.07*H];kx=legx(.25) or ax
    # crotch: lowest z where center pixel is filled
    crotch=None
    for z in range(int(.15*N),int(.7*N)):
        if img[z,tci]:crotch=z/N;break
    crotch=min(max(crotch or .42,.36),.5)
    # arms: rows between .3H and .72H where there are runs strictly outside the central run on each side
    sideL=[];sideR=[]
    for z in range(int(.2*N),int(.78*N)):
        rs,c=info[z]
        if not c:continue
        for r in rs:
            if r[0]>c[1]:sideL.append((z,r))
            if r[1]<c[0]:sideR.append((z,r))
    def armfit(side,sg):
        if len(side)<4:return None
        zs=np.array([z for z,_ in side],float);xs=np.array([abs(X((r[0]+r[1])/2)-tc) for _,r in side])
        A=np.polyfit(zs,xs,1);zlo=zs.min()
        return A,zlo/N
    aL=armfit(sideL,1);aR=armfit(sideR,-1)
    arms=[a for a in (aL,aR) if a]
    # body widths
    def halfw(fz):
        z=max(0,min(int(fz*N),N));c=info[z][1]
        return (X(c[1])-X(c[0]))/2 if c else .1*H
    neckz=None
    # neck: narrowest central width between .7H and .9H
    best=None
    for z in range(int(.68*N),int(.9*N)):
        c=info[z][1]
        if c:
            w=c[1]-c[0]
            if best is None or w<best[0]:best=(w,z)
    neckz=best[1]/N if best else .74
    shz=neckz-.06
    shx=halfw(shz-.03)*.72
    if arms:
        tipz=float(np.mean([a[1] for a in arms]))
        tipx=float(np.mean([np.polyval(a[0],a[1]*N) for a in arms]))
        shx2=float(np.mean([np.polyval(a[0],shz*N) for a in arms]))
        shx=min(shx,max(shx2,shx*.6))
    else:
        tipx=shx+.06*H;tipz=crotch
    hax=shx+(tipx-shx)*.85;haz=shz+(tipz-shz)*.85
    elx=shx+(tipx-shx)*.45;elz=shz+(tipz-shz)*.45
    hpz=crotch+.02;hpx=max(ax[0]*.9,.05*H)
    LM={'hips':(hpz+.02,0.0),'spine':hpz+(neckz-hpz)*.25,'chest':hpz+(neckz-hpz)*.5,'uchest':hpz+(neckz-hpz)*.75,'neck':neckz,'head':neckz+.05,'top':1.0,'head_r':max(halfw(neckz+.12),.08),
        'sh':(shx,0,shz),'el':(elx,0,elz),'ha':(hax,0,haz),'tip':(tipx,0,tipz),'hp':(hpx,0,hpz),'kn':(kx[0],0,(hpz+.06)/2+.03),'an':(ax[0],0,.08),'toe':(ax[0],-.08,.02)}
    # LM in units of H; scale to model units
    def sc_(v):
        if isinstance(v,tuple):return tuple(float(a)*H if i!=0 or True else a for i,a in enumerate(v))
        return float(v)*H
    out={}
    for k,v in LM.items():
        if k in('sh','el','ha','tip','hp','kn','an','toe'):out[k]=tuple(float(a) for a in (v[0],v[1]*H,v[2]*H)) if False else (float(v[0]),float(v[1]*H),float(v[2]*H))
        elif k=='hips':out[k]=(float(v[0]*H),0.0)
        elif k=='head_r':out[k]=float(v)
        else:out[k]=float(v*H)
    return out,{'tci':tci,'H':float(H),'tc':tc,'zmin':float(zmin),'arms':arms,'crotch':crotch,'neck':neckz},img
def overlay(img,LM,meta,fn):
    N=img.shape[0]-1;H=meta['H'];W=img.shape[1]
    rgb=np.stack([img*.4,img*.4,img*.4],-1).astype(np.float32)
    s=H/N;x0=0
    def put(x,z,col):
        # x relative to torso center
        i=int(meta['tci']+x/s);j=int(z/s)
        rgb[max(0,j-2):j+3,max(0,i-2):i+3]=col
    for k in('sh','el','ha','tip','hp','kn','an'):
        v=LM[k]
        for sg in(1,-1):put(sg*v[0],v[2],(1,0.2,0.2))
    for k in('spine','chest','uchest','neck','head','top'):put(0,LM[k],(0.2,1,0.2))
    put(0,LM['hips'][0],(0.2,0.6,1))
    im=bpy.data.images.new('ov',W,N+1);px=np.concatenate([rgb,np.ones((N+1,W,1),np.float32)],-1).ravel();im.pixels.foreach_set(px);im.filepath_raw=fn;im.file_format='PNG';im.save();bpy.data.images.remove(im)
