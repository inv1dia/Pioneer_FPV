from pioneer_sdk import Camera, Pioneer
import pygame
import io
import cv2
import numpy as np

if __name__ == '__main__':
    pioneer = Pioneer()
    camera = Camera()
    pygame.init()
    FPS = 60
    clock = pygame.time.Clock()

    img = camera.get_cv_frame()[:, :, ::-1]
    img = np.rot90(img)
    surf = pygame.surfarray.make_surface(img)
    w, h = surf.get_size()
    h += 150  # for interface.py
    display = pygame.display.set_mode((w, h), 0)
    screen = pygame.surface.Surface((w, h), 0, display)
    pygame.display.set_caption("ESP Camera Stream")

    capture = True
    while capture:
        try:
            img = camera.get_cv_frame()
            if img is not None:
                img = img[:, :, ::-1]
                img = np.rot90(img)
                surf = pygame.surfarray.make_surface(img)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        capture = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    print("left")
                if keys[pygame.K_d]:
                    print("right")
                if keys[pygame.K_w]:
                    print("up")
                if keys[pygame.K_s]:
                    print("down")
                if keys[pygame.K_q]:
                    print("turn left")
                if keys[pygame.K_e]:
                    print("turn rigth")
                if keys[pygame.K_i]:
                    print("upp")
                if keys[pygame.K_k]:
                    print("downn")

                if keys[pygame.K_1]:
                    print("1")
                if keys[pygame.K_2]:
                    print("2")
                if keys[pygame.K_3]:
                    print("3")
                if keys[pygame.K_4]:
                    print("4")
                display.blit(surf, (0, 0))
                pygame.display.update()
            clock.tick(FPS)

        except ValueError:
            print(ValueError)
            pass
    pygame.quit()
    pioneer.close_connection()
    del pioneer
