Перед началом работы необходимо установить требуемые модули согласно **requirements.txt**. В случае возникновения ошибки автоматической настройки среды разработки имеет смысл установить самые актуальные версии модулей под вашу версию интерпретатора Python (т.е. если она не соответствует 3.11). Если pip не смог установить Pygame, попробуйте написать "pip install pygame --pre" в терминале.

* **interface.py** - основной файл для запуска приложения. Подключается к дрону через Wi-Fi (соединение на ПК должно быть установлено заранее). Открывает окно с видеопотоком из камеры, подключенной к ESP32, и минималистичным интерфейсом, который состоит из подсвечивающихся клавиш и информации об управлении дроном. При закрытии окна Pygame садит дрон (если он ещё не сел) и завершает скрипт.

* **no_interface.py** - то же, что и interface.py, но без дополнительных элементов интерфейса.
##

Before working make sure to install all the modules listed in **requirements.txt**. If an error occures during the automatic IDE configuration, it may make sense to install latest versions of modules aviable on your Python interpretator (3.11 was used in that project). If pip fails to install Pygame, try running "pip install pygame --pre" in terminal.

* **interface.py** - main file to run the app. Connects to the drone using Wi-Fi (connection on PC should be estabilished presumably). Opens a windows with a stream from camera connected to ESP32 and a minimalistic interface that consists of highlightable keyaboard buttons and a controls information label. Upon closing Pygame window, lands the drone if it's midflight and finishes the script.

* **no_interface.py** - the same as interface.py, but without additional interface features.
