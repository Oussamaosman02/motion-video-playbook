import sys, numpy as np
from PIL import Image, ImageFilter
cut, out_th, out_sh = sys.argv[1:4]
im = Image.open(cut).convert("RGBA")
al = im.split()[3].filter(ImageFilter.GaussianBlur(2))
m = np.asarray(al).astype(np.float32)/255
L = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(30))).astype(np.float32)/255
core = np.asarray(al.filter(ImageFilter.GaussianBlur(70))).astype(np.float32)/255
h = np.clip(0.75*core + 0.25*L, 0, 1); h = np.clip((h-0.2)/0.75, 0, 1)
xs=[0,0.3,0.6,0.85,1]; cols=np.array([(150,10,30),(235,45,20),(255,110,20),(255,200,70),(255,248,215)],np.float32)
rgb=np.stack([np.interp(h,xs,cols[:,c]) for c in range(3)],-1)
Image.fromarray(np.dstack([rgb,m*255]).astype(np.uint8)).save(out_th)
Image.fromarray(np.dstack([np.full_like(rgb,20),m*255]).astype(np.uint8)).save(out_sh)
