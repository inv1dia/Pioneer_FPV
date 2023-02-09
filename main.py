from pioneer_sdk import Camera, Pioneer
import pygame
import numpy as np
import pygame.pixelcopy

if __name__ == '__main__':
    pioneer = Pioneer()
    camera = Camera()
    pygame.init()
    display = pygame.display.set_mode((640, 480), 0)
    screen = pygame.surface.Surface((640, 480), 0, display)
    capture = True
    while capture:
        try:
            img = camera.get_cv_frame()
            img = np.swapaxes(img, 0, 1)
            surf = pygame.pixelcopy.make_surface(img)
            display.blit(surf, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    capture = False
        except ValueError:
            print(ValueError)
            pass
    pygame.quit()
    pioneer.close_connection()
    del pioneer
