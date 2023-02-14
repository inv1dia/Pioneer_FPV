from pioneer_sdk import Camera, Pioneer
import pygame
import numpy as np

key_w = pygame.image.load("images/w.png")
key_a = pygame.image.load("images/a.png")
key_s = pygame.image.load("images/s.png")
key_d = pygame.image.load("images/d.png")
key_q = pygame.image.load("images/q.png")
key_e = pygame.image.load("images/e.png")
key_i = pygame.image.load("images/i.png")
key_k = pygame.image.load("images/k.png")
key_1 = pygame.image.load("images/1.png")
key_2 = pygame.image.load("images/2.png")
key_3 = pygame.image.load("images/3.png")
key_4 = pygame.image.load("images/4.png")

FPS = 60


def _define_size(camera):
    while True:
        try:
            img = camera.get_cv_frame()[:, :, ::-1]
            img = np.rot90(img)
            surf = pygame.surfarray.make_surface(img)
            w, h = surf.get_size()
            if w > 0 and h > 0:
                print("Camera resolution:", w, h)
                return w, h+150
        except:
            pass


def _render_icons(display, height):
    display.fill((165, 165, 165))
    key_w.set_alpha(165)
    display.blit(key_w, (48, height-76))
    key_a.set_alpha(165)
    display.blit(key_a, (15, height-43))
    key_s.set_alpha(165)
    display.blit(key_s, (48, height-43))
    key_d.set_alpha(165)
    display.blit(key_d, (81, height-43))
    key_q.set_alpha(165)
    display.blit(key_q, (15, height-76))
    key_e.set_alpha(165)
    display.blit(key_e, (81, height-76))
    key_1.set_alpha(165)
    display.blit(key_1, (15, height-123))
    key_2.set_alpha(165)
    display.blit(key_2, (48, height-123))
    key_3.set_alpha(165)
    display.blit(key_3, (81, height-123))
    key_4.set_alpha(165)
    display.blit(key_4, (114, height-123))
    key_i.set_alpha(165)
    display.blit(key_i, (128, height-90))
    key_k.set_alpha(165)
    display.blit(key_k, (128, height-57))
    return display


def _controls(display, height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        print(height)
        display.blit(key_w, (48, height-76))
    if keys[pygame.K_a]:
        display.blit(key_a, (15, height-43))
    if keys[pygame.K_s]:
        display.blit(key_s, (48, height-43))
    if keys[pygame.K_d]:
        display.blit(key_d, (81, height-43))
    if keys[pygame.K_q]:
        display.blit(key_q, (15, height-76))
    if keys[pygame.K_e]:
        display.blit(key_e, (81, height-76))
    if keys[pygame.K_i]:
        display.blit(key_i, (90, height-60))
    if keys[pygame.K_k]:
        display.blit(key_k, (90, height-35))
    if keys[pygame.K_1]:
        display.blit(key_1, (15, height - 123))
    if keys[pygame.K_2]:
        display.blit(key_2, (48, height-123))
    # display.blit()


class Interface:
    def __init__(self):
        pygame.init()
        self.pioneer = Pioneer()
        self.camera = Camera()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("FPV")
        # pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.width, self.height = _define_size(self.camera)
        self.display = pygame.display.set_mode((self.width, self.height), 0)
        self.screen = pygame.surface.Surface((self.width, self.height), 0, self.display)

        self.background = pygame.surface.Surface((self.width, self.height), 0, self.display)
        _render_icons(self.background, self.height)
        pygame.display.update()

        self._main()
        pygame.quit()
        self.pioneer.close_connection()
        del self.pioneer

    def _main(self):
        active = True
        while active:
            try:
                img = self.camera.get_cv_frame()

                if img is not None:
                    img = img[:, :, ::-1]
                    img = np.rot90(img)
                    surf = pygame.surfarray.make_surface(img)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            active = False
                    self.display.blit(self.background, (0, 0))
                    _controls(self.display, self.height)
                    self.display.blit(surf, (0, 0))
                    pygame.display.update()
                self.clock.tick(FPS)

            except ValueError:
                print(ValueError)
                pass


if __name__ == '__main__':
    Interface()
