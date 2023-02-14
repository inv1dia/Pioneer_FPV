from pioneer_sdk import Camera, Pioneer
import pygame
import io
import cv2
import numpy as np

if __name__ == '__main__':
    # pioneer = Pioneer()
    # camera = Camera()
    pygame.init()
    FPS = 60

    # img = camera.get_cv_frame()[:, :, ::-1]
    img = np.zeros((640, 480))
    img = np.rot90(img)
    surf = pygame.surfarray.make_surface(img)
    display = pygame.display.set_mode(surf.get_size(), 0)
    screen = pygame.surface.Surface(surf.get_size(), 0, display)
    display = pygame.display.set_mode((640, 480+100), 0)
    # screen = pygame.surface.Surface((640, 480+100), 0, display)
    pygame.display.set_caption("ESP Camera Stream")

    capture = True
    while capture:
        try:
            # img = camera.get_cv_frame()
            if img is not None:
                # img = img[:, :, ::-1]
                img = np.rot90(img)
                surf = pygame.surfarray.make_surface(img)
                display.blit(surf, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        capture = False
        except ValueError:
            print(ValueError)
            pass
    pygame.quit()
    # pioneer.close_connection()
    # del pioneer
