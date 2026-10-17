# 前後に顔があるか: 頭の正面と背面(左右反転)の「顔まわりの細部」の相関が高ければNG
import sys,numpy as np
from PIL import Image,ImageFilter
p=sys.argv[1]
def g(n):
    im=Image.open(f'{p}_{n}.png').convert('L').resize((100,140))
    a=np.asarray(im).astype(float)-np.asarray(im.filter(ImageFilter.GaussianBlur(4))).astype(float)
    a=a[75:115,25:75];return (a-a.mean())/(a.std()+1e-6)
f=g('headF');b=g('headB')[:,::-1]
c=float((f*b).mean());print('face_corr',round(c,3),'NG(両面顔の疑い)' if c>0.35 else 'OK')
