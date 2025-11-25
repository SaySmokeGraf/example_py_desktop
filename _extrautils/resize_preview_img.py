"""Скрипт смены размера изображения для лого."""

import os.path

from PIL import Image


# константы для смены размера из конфига
IMG_SIZES = (900, 506)
PATH_IMG_ORIG = 'res/preview_img_orig.jpg'
PATH_IMG_SIZED = 'res/preview_img_sized.png'


# создание картинки с измененным под ГПИ размером по необходимости
if __name__ == "__main__":
    print('Меняем размер изображения...')
    if os.path.exists(PATH_IMG_ORIG):
        image = Image.open(PATH_IMG_ORIG)
        resized_image = image.resize(IMG_SIZES)
        resized_image.save(PATH_IMG_SIZED)
        print('Новый файл создан. Размер изменен!')
    else:
        print(f'Отсутствует файл: {PATH_IMG_ORIG}. Процесс не завершен!')
    input('Введите Enter, чтобы выйти.')
