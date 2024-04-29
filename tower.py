from pygame import*
from pymunk import *
from pymunk.pygame_util import* 
from pymunk import constraints
import math
from random import randint
positive_y_is_up=False
space=Space()
clock=time.Clock()
space.gravity=0,98
fps=144
init()
w,h=display.Info().current_w//2,display.Info().current_h//4*3
screen=display.set_mode((w,h))
draw_screen=DrawOptions(screen)

m=mixer.Sound('music/posta.mp3')
m.play(-1)

all_move=[]

platform_body=Body(body_type=Body.KINEMATIC)
platform=Segment(platform_body,(-w,h),(w,h),h//20)
platform.elasticity=0
platform.friction=1
space.add(platform,platform_body)

all_move.append(platform)

cran_bod=Body(body_type=Body.KINEMATIC)
cran=Segment(platform_body,(w//3,0),(w-w//3,0),h//20)
cran.body.position=w//2,-h//20
space.add(cran_bod,cran)


# cube_body=Body(10,10,Body.DYNAMIC)
# cube=Segment(cube_body,(0,0),(0,0),h/30)
# cube.body.position=w//2,-h//20
# space.add(cube,cube_body)

class Block(sprite.Sprite):
    def __init__(self,vovasize,m,vovaspace,pic):
        sprite.Sprite.__init__(self)
        self.pic=transform.scale(pic,vovasize)
        self.image=self.pic
        self.mybox=self.Block_body(vovasize,m,vovaspace)
        self.rect=self.image.get_rect(center=self.mybox.body.position)
        self.image.set_colorkey((0,0,0))
        
    def update(self):
        self.image=transform.rotate(self.pic,-math.degrees(self.mybox.body.angle))
        self.rect=self.image.get_rect(center=self.mybox.body.position)

    def Block_body(self,vovasize,m,vovaspace):
        inertia=moment_for_box(m,vovasize)
        box_body=Body(m,inertia,Body.DYNAMIC)
        box=Poly.create_box(box_body,vovasize)
        box.elasticity=0
        box.friction=10
        vovaspace.add(box_body,box)
        return box

m=space.gravity[1]*7
box_w=w//4
box_h=h//8

all_spites=sprite.Group()

block_pic_0=image.load("sprites/svin.png")
block_pic_1=image.load("sprites/svin.png")
fon_pic=image.load("sprites/gay_fon.jpg")
fon_pic=transform.scale(fon_pic,(w,h))

count_block=0
new_block=True
move=False
move_h=0
while True:
    screen.blit(fon_pic,(0,0))
    space.step(1/fps)
    clock.tick(fps)
    for ev in event.get():
        if ev.type==QUIT:
            import sys
            sys.exit()
        if ev.type==KEYDOWN:
            if ev.key==K_SPACE:
                if new_block:
                    if move_h<=0:
                        new_block=False
                        move=True
                        block_pos=randint(1,4)
                        
                        if count_block==0:
                            pic=block_pic_0
                        else:
                            pic=block_pic_1
                        count_block=+1

                        block=Block((box_w,box_h),m,space,pic)
                        all_spites.add(block)
                        all_move.append(block.mybox)
                        if block_pos==1:
                            block.mybox.body.position=(w//5,h//3)
                        elif block_pos==2:
                            block.mybox.body.position=(w-200,h//3)
                        elif block_pos==3:
                            block.mybox.body.position=(w//5,h//5)
                        else:
                            block.mybox.body.position=(w-200,h//5)
                        # box_join=constraints.PinJoint(block.mybox.body,cran.body)
                        box_join=constraints.DampedSpring(block.mybox.body,cran.body,(0,0),(0,0),rest_length=h//15,stiffness=700,damping=100)
                        space.add(box_join)
                else:
                    new_block=True
                    space.remove(box_join)
    if count_block>2 and len(space.shape_query(block.mybox))>0 and move:
        move=False
        move_h=box_h
    if move_h>0:
        move_h-=0.1
        for obj in all_move:
            obj.body.position=obj.body.position[0],obj.body.position[1]+0.1
    space.debug_draw(draw_screen)
    all_spites.update()
    all_spites.draw(screen)
    
    display.flip()
