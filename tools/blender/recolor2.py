from PIL import Image;import numpy as np,sys,json
K='/tmp/kk/KayKit-Character-Pack-Adventures-1.0/addons/kaykit_character_pack_adventures/Textures/'
S='/tmp/kk/KayKit-Character-Pack-Skeletons-1.0/addons/kaykit_character_pack_skeletons/Textures/'
TEX={'barb':K+'barbarian_texture.png','mage':K+'mage_texture.png','rogue':K+'rogue_texture.png','hood':K+'rogue_texture.png','skel':S+'skeleton_texture.png'}
MAP={'barb':{(6,0):'B',(7,0):'B',(5,0):'B',(0,1):'A',(1,1):'A',(2,1):'L',(7,1):'M',(3,2):'B',(1,0):'B',(3,0):'M',(7,2):'M',(4,0):'M'},
'mage':{(0,1):'A',(1,1):'A',(3,0):'M',(4,0):'M',(5,0):'C',(7,1):'B',(2,2):'C',(3,2):'B',(2,1):'C'},
'rogue':{(0,1):'A',(1,1):'A',(6,0):'B',(3,0):'M',(5,0):'B',(7,1):'B',(5,2):'B',(3,2):'B',(4,0):'M'},
'skel':{(3,0):'M',(4,0):'M',(1,1):'bone',(7,0):'B',(6,0):'B',(2,2):'A',(7,3):'C',(6,2):'B',(5,0):'B'}}
MAP['hood']=MAP['rogue']
def hx(s):s=s.lstrip('#');return np.array([int(s[i:i+2],16) for i in (0,2,4)],float)
def run(body,pal,out):
  a=np.array(Image.open(TEX[body]).convert('RGB')).astype(float)
  for (c,r),role in MAP[body].items():
    if role not in pal:continue
    cell=a[r*256:(r+1)*256,c*128:(c+1)*128];lum=cell@[.3,.59,.11];m=max(lum.mean(),1)
    t=hx(pal[role]);f=np.clip(lum/m,0.55,1.6)[...,None]
    a[r*256:(r+1)*256,c*128:(c+1)*128]=np.clip(t*f,0,255)
  Image.fromarray(a.astype(np.uint8)).save(out)
if __name__=='__main__':run(sys.argv[1],json.loads(sys.argv[2]),sys.argv[3])
