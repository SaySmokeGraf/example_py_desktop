"""Скрипт смены размера изображения для лого."""

import os.path

from PIL import Image


# константы для смены размера из конфига
IMG_SIZES = (900, 506)
PATH_IMG_ORIG = 'res/preview_img_orig.jpg'
PATH_IMG_SIZED = 'res/preview_img_sized.png'


# создание картинки с измененным под ГПИ размером по необходимости
if __name__ == "__main__":
    print('Resizing...')
    if os.path.exists(PATH_IMG_ORIG):
        image = Image.open(PATH_IMG_ORIG)
        resized_image = image.resize(IMG_SIZES)
        resized_image.save(PATH_IMG_SIZED)
        print(f'Resizing into {PATH_IMG_SIZED} completed!')
    else:
        print(f'ERROR: No such file: {PATH_IMG_ORIG}.')
    input('Press Enter to exit...')
