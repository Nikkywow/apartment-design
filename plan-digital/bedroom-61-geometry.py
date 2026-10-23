"""Deterministic geometry reference, metres. Standard library only."""
from pathlib import Path
import math, struct, zlib, json
ROOT=Path(__file__).resolve().parent
W,H=1536,1024
pixels=bytearray(bytes((242,235,222))*W*H)
def polygon(points,color):
    if len(points)<3:return
    ymin=max(0,math.floor(min(p[1] for p in points)))
    ymax=min(H-1,math.ceil(max(p[1] for p in points)))
    for yy in range(ymin,ymax+1):
        y=yy+.5; xs=[]
        for a,b in zip(points,points[1:]+points[:1]):
            if (a[1]<=y<b[1]) or (b[1]<=y<a[1]):
                xs.append(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
        xs.sort()
        for l,r in zip(xs[::2],xs[1::2]):
            x0=max(0,math.ceil(l));x1=min(W,math.ceil(r))
            if x1>x0:pixels[(yy*W+x0)*3:(yy*W+x1)*3]=bytes(color)*(x1-x0)
camera=(3.40,1.78,1.60)
# Looking toward plan-left: screen-right is plan-top. No horizontal mirroring.
def project(points):
    pts=[(camera[1]-y,z-camera[2],camera[0]-x) for x,y,z in points]
    out=[]
    for a,b in zip(pts,pts[1:]+pts[:1]):
        ina=a[2]>=.12;inb=b[2]>=.12
        if ina:out.append(a)
        if ina!=inb:
            t=(.12-a[2])/(b[2]-a[2]);out.append(tuple(a[i]+t*(b[i]-a[i]) for i in range(3)))
    return [(W/2+800*u/d,400-800*v/d) for u,v,d in out]
def face(points,color):polygon(project(points),color)
cream=(229,218,198);olive=(83,91,64);floor=(92,62,43)
# Background of adjacent dressing space, visible only through the existing opening.
face([(-1.685,-1.89,0),(1,-1.89,0),(1,-1.89,3.2),(-1.685,-1.89,3.2)],(196,182,159))
face([(-1.685,-1.89,0),(-1.685,0,0),(-1.685,0,3.2),(-1.685,-1.89,3.2)],(207,194,170))
face([(-1.085,-1.7,0),(-1.085,-.1,0),(-1.085,-.1,2.9),(-1.085,-1.7,2.9)],(132,100,69))
face([(-1.685,-1.89,0),(3.3,-1.89,0),(3.3,3.56,0),(-1.685,3.56,0)],floor)
face([(0,0,3.2),(3.3,0,3.2),(3.3,3.56,3.2),(0,3.56,3.2)],(243,234,218))
# West/front wall fully restored after removing the 0.60 m deep wardrobe.
face([(0,0,0),(0,3.56,0),(0,3.56,3.2),(0,0,3.2)],cream)
face([(0,0,0),(0,3.56,0),(0,3.56,1.0),(0,0,1.0)],olive)
# North/right wall: opening starts at west corner, x=0..1.00. Solid wall x=1.00..3.69.
face([(1,0,0),(3.3,0,0),(3.3,0,3.2),(1,0,3.2)],cream)
face([(1,0,0),(3.3,0,0),(3.3,0,1),(1,0,1)],olive)
face([(0,0,2.45),(1,0,2.45),(1,0,3.2),(0,0,3.2)],cream)
face([(1,-.125,0),(1,0,0),(1,0,2.45),(1,-.125,2.45)],(203,190,169))
# South/left facade and existing opening, with a neutral curtain plane.
face([(0,3.56,0),(3.3,3.56,0),(3.3,3.56,3.2),(0,3.56,3.2)],cream)
face([(.71,3.54,.03),(2.96,3.54,.03),(2.96,3.54,2.95),(.71,3.54,2.95)],(250,245,228))
def box(x0,x1,y0,y1,z0,z1,c):
    face([(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)],tuple(max(0,v-12) for v in c))
    face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],tuple(max(0,v-20) for v in c))
    face([(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],c)
    face([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],c)
    face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],tuple(min(255,v+10) for v in c))
# Modest 1.40 x 0.38 m walnut console, not a large chest of drawers.
box(.02,.40,1.08,2.48,.66,.78,(129,86,53))
for y in [1.13,2.39]:box(.29,.34,y,y+.05,0,.66,(111,73,44))
box(.06,.37,1.53,2.03,0,.44,(187,168,133))
# Oval brass mirror above console, reflecting a neutral tone in the massing reference.
oval=[(.025,1.78+.36*math.cos(t*math.pi/40),1.55+.5*math.sin(t*math.pi/40)) for t in range(80)]
face(oval,(170,142,85))
oval=[(.03,1.78+.34*math.cos(t*math.pi/40),1.55+.48*math.sin(t*math.pi/40)) for t in range(80)]
face(oval,(196,202,186))
# Bed footprint kept from approved concept, foreground only.
box(1.54,3.3,.83,2.73,.18,.55,(91,98,66))
box(1.55,3.3,.85,2.71,.55,.70,(225,214,189))
def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
raw=b''.join(b'\x00'+pixels[y*W*3:(y+1)*W*3] for y in range(H))
data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
(ROOT/'bedroom-61-camera-reference.png').write_bytes(data)
model={'room_m':[3.69,3.56,3.2],'coordinates':'x plan-left to right; y plan-top to bottom','north_opening_x_m':[0,1.0],'north_solid_wall_x_m':[1.0,3.69],'opening_height_m':2.45,'opening_height_status':'illustrative, not measured','opening_width_status':'approximately 1.00 architectural gap read from source photo; prior 0.89 clear door width retained as uncertain','correction':'supersedes the unverified x=.93..1.82 doorway in bedroom-style-55-reference.svg','source':'updated-plan-right-detail.png','wardrobe':'removed from bedroom; adjoining R03 used as dressing space per user request','console_m':[1.4,.38,.78],'foot_clearance_m':1.14,'camera_m':camera,'construction_status':'concept geometry; not a demolition or construction instruction'}
(ROOT/'bedroom-61-geometry.json').write_text(json.dumps(model,ensure_ascii=False,indent=2))
print(ROOT/'bedroom-61-camera-reference.png')
