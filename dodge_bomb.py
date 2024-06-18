import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1500, 800
DELTA = { # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #縦方向判定
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    font = pg.font.Font(None, 80)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_flip_img = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):#衝突判定
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0])
        txt = font.render(str(tmr/50), True, (255, 255, 255))
        screen.blit(txt, [300, 200])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        
        if sum_mv==[-5,0]:
            kk_img = pg.transform.rotozoom(kk_img,0,1)
        elif sum_mv==[-5,-5]:
            kk_img = pg.transform.rotozoom(kk_img,-45,1)
        elif sum_mv==[-5, +5]:
            kk_img = pg.transform.rotozoom(kk_img,45,1)
        elif sum_mv==[+5, 0]:
            kk_img = kk_flip_img
        elif sum_mv==[+5, -5]:
            kk_img = pg.transform.rotozoom(kk_flip_img,45,1)
        elif sum_mv==[0, -5]:
            kk_img = pg.transform.rotozoom(kk_flip_img,90,1)
        elif sum_mv==[+5, +5]:
            kk_img = pg.transform.rotozoom(kk_flip_img,-45,1)
        elif sum_mv==[0, +5]:
            kk_img = pg.transform.rotozoom(kk_flip_img,-90,1)

        kk_rct.move_ip(sum_mv)


        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみでたら
            vx *= -1
        if not tate: #縦方向にはみでたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
