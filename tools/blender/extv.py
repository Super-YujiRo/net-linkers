import json,struct,base64,numpy as np
from scipy.spatial.transform import Rotation as Rr
CT={5126:np.float32,5123:np.uint16,5125:np.uint32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
out={}
for k in ['bitton','phantom']:
  f='/mnt/user-data/uploads/Downloads/nl_kk/vir_%s.glb'%k
  d=open(f,'rb').read();l=struct.unpack('<I',d[12:16])[0];j=json.loads(d[20:20+l]);b0=20+l+8
  def acc(i):
    a=j['accessors'][i];bv=j['bufferViews'][a['bufferView']];n=NC[a['type']];dt=CT[a['componentType']]
    o=b0+bv.get('byteOffset',0)+a.get('byteOffset',0);arr=np.frombuffer(d,dt,a['count']*n,o);return arr.reshape(-1,n) if n>1 else arr
  par={c:i for i,n in enumerate(j['nodes']) for c in n.get('children',[])}
  G={};parts=[]
  for i,n in enumerate(j['nodes']):
    if n['name'].startswith('p_'):G[n['name'][2:]]=[round(x,4) for x in n.get('translation',[0,0,0])]
  for i,n in enumerate(j['nodes']):
    if 'mesh' not in n:continue
    g=j['nodes'][par[i]]['name'][2:] if i in par else None
    R=Rr.from_quat(n.get('rotation',[0,0,0,1])).as_matrix();S=np.array(n.get('scale',[1,1,1]));T=np.array(n.get('translation',[0,0,0]))
    for p in j['meshes'][n['mesh']]['primitives']:
      m=j['materials'][p['material']];pb=m.get('pbrMetallicRoughness',{});col=pb.get('baseColorFactor',[1,1,1,1]);em=m.get('emissiveFactor',[0,0,0]);glow=sum(em)>.01
      c=em if glow else col[:3]
      pos=acc(p['attributes']['POSITION']).astype(np.float64)*S@R.T+T
      nor=acc(p['attributes']['NORMAL']).astype(np.float64)/S@R.T;nor/=np.linalg.norm(nor,axis=1,keepdims=True)+1e-9
      idx=acc(p['indices']).astype(np.uint16)
      mn=pos.min(0);sc=np.maximum(pos.max(0)-mn,1e-6);q=np.round((pos-mn)/sc*65535).astype(np.uint16);qn=np.round(nor*127).astype(np.int8)
      parts.append({'g':g,'c':'#%02x%02x%02x'%tuple(int(min(1,x**(1/2.2))*255) for x in c),'gl':int(glow),'mn':[round(float(x),5) for x in mn],'sc':[round(float(x),5) for x in sc],
        'p':base64.b64encode(q.tobytes()).decode(),'n':base64.b64encode(qn.tobytes()).decode(),'i':base64.b64encode(idx.tobytes()).decode()})
  out[k]={'G':G,'parts':parts};print(k,G,len(parts))
json.dump(out,open('/tmp/claude-0/boss/vir.json','w'),separators=(',',':'))
import os;print(os.path.getsize('/tmp/claude-0/boss/vir.json')//1024)
