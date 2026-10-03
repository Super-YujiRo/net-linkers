import json,struct,base64,numpy as np,glob,os
from scipy.spatial.transform import Rotation as Rr
CT={5126:np.float32,5123:np.uint16,5125:np.uint32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def trs(n):
  if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
  M=np.eye(4);M[:3,:3]=Rr.from_quat(n.get('rotation',[0,0,0,1])).as_matrix()*np.array(n.get('scale',[1,1,1]));M[:3,3]=n.get('translation',[0,0,0]);return M
out={}
for f in sorted(glob.glob('/mnt/user-data/uploads/Downloads/nl_kk/pv2_*.glb')):
  k=os.path.basename(f)[4:-4]
  d=open(f,'rb').read();l=struct.unpack('<I',d[12:16])[0];j=json.loads(d[20:20+l]);b0=20+l+8
  def acc(i):
    a=j['accessors'][i];bv=j['bufferViews'][a['bufferView']];n=NC[a['type']];dt=CT[a['componentType']]
    o=b0+bv.get('byteOffset',0)+a.get('byteOffset',0);arr=np.frombuffer(d,dt,a['count']*n,o);return arr.reshape(-1,n) if n>1 else arr
  par={c:i for i,n in enumerate(j['nodes']) for c in n.get('children',[])}
  def world(i):
    M=trs(j['nodes'][i])
    while i in par:i=par[i];M=trs(j['nodes'][i])@M
    return M
  parts=[]
  for i,n in enumerate(j['nodes']):
    if not n['name'].startswith('NX') or 'mesh' not in n:continue
    bone=j['nodes'][par[i]]['name']
    W=world(i)
    for p in j['meshes'][n['mesh']]['primitives']:
      m=j['materials'][p['material']];pb=m.get('pbrMetallicRoughness',{});col=pb.get('baseColorFactor',[1,1,1,1]);em=m.get('emissiveFactor',[0,0,0]);glow=sum(em)>.01
      c=em if glow else col[:3]
      pos=acc(p['attributes']['POSITION']).astype(np.float32);nor=acc(p['attributes']['NORMAL']).astype(np.float32);idx=acc(p['indices'])
      mn=pos.min(0);sc=np.maximum(pos.max(0)-mn,1e-6);q=np.round((pos-mn)/sc*65535).astype(np.uint16);qn=np.round(np.clip(nor,-1,1)*127).astype(np.int8)
      ix=idx.astype(np.uint16 if len(pos)<65536 else np.uint32)
      parts.append({'b':bone,'w':[round(float(x),5) for x in W.T.flatten()],'c':'#%02x%02x%02x'%tuple(int(min(1,x**(1/2.2))*255) for x in c),'g':int(glow),'mn':[round(float(x),5) for x in mn],'sc':[round(float(x),5) for x in sc],
       'p':base64.b64encode(q.tobytes()).decode(),'n':base64.b64encode(qn.tobytes()).decode(),'i':base64.b64encode(ix.tobytes()).decode(),'i32':int(ix.dtype==np.uint32)})
  out[k]=parts;print(k,len(parts),set(x['b'] for x in parts))
json.dump(out,open('/tmp/claude-0/boss/parts3.json','w'),separators=(',',':'))
print(os.path.getsize('/tmp/claude-0/boss/parts3.json')//1024)
