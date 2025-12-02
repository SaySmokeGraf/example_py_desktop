"""Скрипт смены размера изображения для лого и значка загрузки."""

import os.path

from PIL import Image


# константы для смены размера лого
IMG_SIZES = (900, 506)
PATH_IMG_ORIG = 'res/preview_img_orig.jpg'
PATH_IMG_SIZED = 'res/preview_img_sized.png'

# константы для смены размера значка ожидания
LOADING_SIZES = (120, 120)
PATH_LOADING_ORIG = 'res/loading_orig.png'
PATH_LOADING_SIZED = 'res/loading_sized.png'


# функция для смены изображения
def resize(path_orig: str, path_sized: str, sizes: tuple[int, int]) -> None:
    """Смена размера изображения.

    :param path_orig: путь до изменяемой картинки
    :type path_orig: str
    :param path_sized: путь для сохранения измененной картинки
    :type path_sized: str
    :param sizes: размеры в формате (ширина, высота) в пикселях
    :type sizes: tuple[int, int]
    """
    if os.path.exists(path_orig):
        image = Image.open(path_orig)
        resized_image = image.resize(sizes)
        resized_image.save(path_sized)
        print(f'Resizing into {path_sized} completed!')
    else:
        print(f'ERROR: No such file: {path_orig}.')


# изменение размера
if __name__ == "__main__":
    print('Resizing...')
    resize(PATH_IMG_ORIG, PATH_IMG_SIZED, IMG_SIZES)
    resize(PATH_LOADING_ORIG, PATH_LOADING_SIZED, LOADING_SIZES)
    input('Press Enter to exit...')
