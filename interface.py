from pioneer_sdk import Camera, Pioneer
import pygame
import numpy as np
import time

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

BACKGROUND_COLOR = (82, 82, 82)
INFO_COLOR = (31, 31, 31)
STATS_COLOR = (0, 0, 0)
MIN_V = 1300  # минимальное значение сигнала, который передается по каналам
MAX_V = 1700  # максимальное значение сигнала, который передается по каналам


def _define_size(camera):
    """
    Ожидать пока ESP32 передаст хотя бы 1 целый кадр, после чего вернуть его размеры для создания окна. Расчет идет на
    то, что разрешение используемых камер может отличаться, и интерфейс гибко подстраивается под любое
    :param camera: созданный заранее экземпляр класса Camera
    :return: ширина и высота с запасом для отображения элементов интерфейса
    """
    while True:
        try:
            surf = pygame.surfarray.make_surface(camera.get_cv_frame())
            h, w = surf.get_size()
            if w > 0 and h > 0:
                print("Camera resolution:", w, h)
                return w, h+138
        except:
            pass


def _interface(surf, height, font):
    """
    Единожды сгенерировать фон и интерфейс, включающий информацию по управлению и "погасшие" клавиши
    :param surf: рабочая поверхность, на которой будет генерироваться интерфейс
    :param height: высота рабочей поверхности
    :param font: объявленный заранее шрифт и размер надписей модулем pygame.font
    """
    surf.fill(BACKGROUND_COLOR)  # залить фон серым цветом

    # Создать надписи встроенным методом Pygame, используя сглаживание и темно-серый цвет
    info = font.render("W, A, S, D - horizontal flight controls", True, INFO_COLOR)
    surf.blit(info, (181, height-118))  # задать положение надписи
    info = font.render("Q, E - yaw controls", True, INFO_COLOR)
    surf.blit(info, (181, height-91))
    info = font.render("I, K - height controls", True, INFO_COLOR)
    surf.blit(info, (181, height-64))
    info = font.render("1 - arm, 2 - disarm, 3 - takeoff, 4 - land", True, INFO_COLOR)
    surf.blit(info, (181, height-37))

    key_w.set_alpha(165)  # задать прозрачность клавиши
    surf.blit(key_w, (48, height-76))  # задать положение клавиши
    key_a.set_alpha(165)
    surf.blit(key_a, (15, height-43))
    key_s.set_alpha(165)
    surf.blit(key_s, (48, height-43))
    key_d.set_alpha(165)
    surf.blit(key_d, (81, height-43))
    key_q.set_alpha(165)
    surf.blit(key_q, (15, height-76))
    key_e.set_alpha(165)
    surf.blit(key_e, (81, height-76))
    key_i.set_alpha(165)
    surf.blit(key_i, (128, height-76))
    key_k.set_alpha(165)
    surf.blit(key_k, (128, height-43))
    key_1.set_alpha(165)
    surf.blit(key_1, (15, height-123))
    key_2.set_alpha(165)
    surf.blit(key_2, (48, height-123))
    key_3.set_alpha(165)
    surf.blit(key_3, (81, height-123))
    key_4.set_alpha(165)
    surf.blit(key_4, (114, height-123))


class Interface:
    def __init__(self):
        pygame.init()
        self.pioneer = Pioneer()  # экземпляр класса Pioneer
        self.camera = Camera()  # экземпляр класса Camera

        pygame.display.set_caption("Pioneer FPV")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.width, self.height = _define_size(self.camera)
        self.font = pygame.font.SysFont("sans-serif", 22)  # задать шрифт и размер для надписей интерфейса
        # Создать окно и рабочую поверхность в этом окне для отображения интерфейса, видеопотока и данных с датчиков
        self.display = pygame.display.set_mode((self.width, self.height), 0)
        self.background = pygame.surface.Surface((self.width, self.height), 0, self.display)
        _interface(self.background, self.height, self.font)

        # Задать изначальные данные с датчиков, которые впоследствии заменятся актуальными
        self.battery_status = "..."
        self._x = "0.0"
        self._y = "0.0"
        self._z = "0.0"

        self._main()
        pygame.quit()
        time.sleep(1)
        self.pioneer.land()
        self.pioneer.close_connection()

    def _controls(self):
        """
        Функция управления Пионером (Мини). Каждый раз при вызове проверить какие клавиши нажаты и обработать каждое
        из нажатий: послать квадрокоптеру команды по каналам связи или непосредственно через методы pioneer_sdk
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # если нажата W
            self.display.blit(key_w, (48, self.height - 76))  # "подсветить" клавишу W в интерфейсе
            self.ch_3 = MIN_V  # передать по третьему каналу 1300
        if keys[pygame.K_a]:
            self.display.blit(key_a, (15, self.height - 43))
            self.ch_4 = MIN_V
        if keys[pygame.K_s]:
            self.display.blit(key_s, (48, self.height - 43))
            self.ch_3 = MAX_V
        if keys[pygame.K_d]:
            self.display.blit(key_d, (81, self.height - 43))
            self.ch_4 = MAX_V
        if keys[pygame.K_q]:
            self.display.blit(key_q, (15, self.height - 76))
            self.ch_2 = 2000
        if keys[pygame.K_e]:
            self.display.blit(key_e, (81, self.height - 76))
            self.ch_2 = 1000
        if keys[pygame.K_i]:
            self.display.blit(key_i, (128, self.height - 76))
            self.ch_1 = 2000
        if keys[pygame.K_k]:
            self.display.blit(key_k, (128, self.height - 43))
            self.ch_1 = 1000
        if keys[pygame.K_1]:
            self.display.blit(key_1, (15, self.height - 123))
            self.pioneer.arm()
        if keys[pygame.K_2]:
            self.display.blit(key_2, (48, self.height - 123))
            self.pioneer.disarm()
        if keys[pygame.K_3]:
            self.display.blit(key_3, (81, self.height - 123))
            time.sleep(2)
            self.pioneer.arm()
            time.sleep(1)
            self.pioneer.takeoff()
            time.sleep(2)
        if keys[pygame.K_4]:
            self.display.blit(key_4, (114, self.height - 123))
            time.sleep(2)
            self.pioneer.land()
            time.sleep(2)

    def _stats(self):
        """
        Отобразить актуальные данные с датчиков. В зависимости от вольтажа АКБ отобразить вольтаж определенным
        цветом (выше 8,1 - зеленый, выше 7,5 - желтый, иначе красный). Вывести систему координат, которую генерирует
        модуль оптического потока. Вывести состояние автопилота
        """
        value = float(np.float32(self.pioneer.get_battery_status()).item())  # перевод в стандартный python float
        if value > 0:
            voltage = round(value, 2)  # отображаемое значение округлить до 2 знаков после запятой
            if voltage > 8.1:
                color = (0, 255, 0)
            elif voltage > 7.5:
                color = (255, 255, 0)
            else:
                color = (255, 0, 0)
            self.battery_status = self.font.render(str(voltage), True, color)
        self.display.blit(self.battery_status, (self.width - 33, 5))  # отобразить в правом верхнем углу

        xyz = self.pioneer.get_optical_data()  # получить словарь значений с датчика
        if xyz is not None:
            self._x = self.font.render("x: " + str(xyz['integrated_x']), True, (0, 0, 0))
            self._y = self.font.render("y: " + str(xyz['integrated_y']), True, (0, 0, 0))
            self._z = self.font.render("z: " + str(round(xyz['distance'], 3)), True, (0, 0, 0))
        self.display.blit(self._x, (5, 5))  # отобразить в левом верхнем углу
        self.display.blit(self._y, (55, 5))
        self.display.blit(self._z, (107, 5))

        # Получить состояние автопилота (IDLE, MANUAL_ROLL и т.д.) и представить в виде надписи метода Pygame
        autopilot = self.font.render(str(self.pioneer.get_autopilot_state()), True, (0, 0, 0))
        self.display.blit(autopilot, (170, 5))  # отобразить рядом с координатами

    def _main(self):
        active = True
        while active:
            self.ch_1 = 1500  # установить нейтральный сигнал для канала 1
            self.ch_2 = 1500
            self.ch_3 = 1500
            self.ch_4 = 1500
            self.ch_5 = 2000
            try:
                # Получить кадр из видеопотока и перевести его из BGR режима в RGB
                img = self.camera.get_cv_frame()[:, :, ::-1]
                if img is not None:
                    img_surf = pygame.surfarray.make_surface(img)  # создать отдельной поверхности
                    img_surf = pygame.transform.rotate(img_surf, 270)  # перевернуть изображения на 270 градусов
                    img_surf = pygame.transform.flip(img_surf, True, False)  # отобразить кадр не зеркально
                    for event in pygame.event.get():
                        # Если окно Pygame закрыть, то приложение завершит работу и квадрокоптер сядет
                        if event.type == pygame.QUIT:
                            active = False
                    self.display.blit(self.background, (0, 0))  # восстановить фон
                    self.display.blit(img_surf, (0, 0))  # отобразить текущий кадр
                    self._controls()
                    self._stats()
                    pygame.display.update()  # отобразить все display.blit изменения в окне
            except:
                # Если соединение по какой-либо причине не работает, ждать его восстановления и выводить предупреждающую
                # иконку до тех пока, пока не переподключение не произойдет
                self.display.blit(pygame.image.load("images/fail.png"), (8, 30))
                pygame.display.update()
            self.pioneer.send_rc_channels(channel_1=self.ch_1, channel_2=self.ch_2, channel_3=self.ch_3,
                                          channel_4=self.ch_4, channel_5=self.ch_5)  # отправка команд по каналам связи


if __name__ == '__main__':
    Interface()
