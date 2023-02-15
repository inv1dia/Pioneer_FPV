from pioneer_sdk import Camera, Pioneer
import pygame
import time

MIN_V = 1300
MAX_V = 1700


def _define_size(camera):
    while True:
        try:
            surf = pygame.surfarray.make_surface(camera.get_cv_frame())
            h, w = surf.get_size()
            if w > 0 and h > 0:
                print("Camera resolution:", w, h)
                return w, h
        except:
            pass


class Interface:
    def __init__(self):
        pygame.init()
        self.pioneer = Pioneer()
        self.camera = Camera()

        pygame.display.set_caption("Pioneer FPV")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.display = pygame.display.set_mode(_define_size(self.camera), 0)

        self._main()
        pygame.quit()
        time.sleep(1)
        self.pioneer.land()
        self.pioneer.close_connection()

    def _controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.ch_3 = MIN_V
        if keys[pygame.K_a]:
            self.ch_4 = MIN_V
        if keys[pygame.K_s]:
            self.ch_3 = MAX_V
        if keys[pygame.K_d]:
            self.ch_4 = MAX_V
        if keys[pygame.K_q]:
            self.ch_2 = 2000
        if keys[pygame.K_e]:
            self.ch_2 = 1000
        if keys[pygame.K_i]:
            self.ch_1 = 2000
        if keys[pygame.K_k]:
            self.ch_1 = 1000
        if keys[pygame.K_1]:
            self.pioneer.arm()
        if keys[pygame.K_2]:
            self.pioneer.disarm()
        if keys[pygame.K_3]:
            time.sleep(2)
            self.pioneer.arm()
            time.sleep(1)
            self.pioneer.takeoff()
            time.sleep(2)
        if keys[pygame.K_4]:
            time.sleep(2)
            self.pioneer.land()
            time.sleep(2)

    def _main(self):
        active = True
        while active:
            self.ch_1 = 1500
            self.ch_2 = 1500
            self.ch_3 = 1500
            self.ch_4 = 1500
            self.ch_5 = 2000
            try:
                img = self.camera.get_cv_frame()[:, :, ::-1]
                if img is not None:
                    img_surf = pygame.surfarray.make_surface(img)
                    img_surf = pygame.transform.rotate(img_surf, -90)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            active = False
                    self._controls()
                    self.display.blit(img_surf, (0, 0))
                    pygame.display.update()
            except:
                self.display.blit(pygame.image.load("images/fail.png"), (8, 8))
                pygame.display.update()
            self.pioneer.send_rc_channels(channel_1=self.ch_1, channel_2=self.ch_2, channel_3=self.ch_3,
                                          channel_4=self.ch_4, channel_5=self.ch_5)
            time.sleep(0.02)


if __name__ == '__main__':
    Interface()
