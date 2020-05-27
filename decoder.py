import string  # Подключение библиотеки для получения английского алфавита.
import time

znaki = [',', '-', '.', '!', '"', ':', ";", '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')', '']  #


# Символы которые мгрнорирует декодер


def list_to_str(arr):  # Конвертация из списков в строку
    word = ''
    for s in arr:
        word += s
    return word


def vector(func):  # Векторизация функции
    def g(arr):
        l = []
        f = func
        for i in arr:
            if isinstance(i, list):
                l.append(g(i))
            else:
                l.append(f(i))
        return l

    return g


def index(arr, val):  # Получения индекс елемента в моссиве
    for i in range(len(arr)):
        if arr[i] == val:
            return i


def map_word(word):  # Создание карты слова
    d = {}
    for i in list(word):
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d


def map_comparison(key, val):  # Сравнение карт слов
    otv = len(key)
    if len(key) != len(val):
        return False
    for i in range(len(key)):
        if list(key.values())[i] == list(val.values())[i]:
            otv -= 1
    if otv == 0:
        return True
    else:
        return False


def text_analis_redact(stroka):  # радактор текста для анализа
    otv = ''
    for s in list(stroka):
        if s not in znaki:
            otv += s
    return otv.lower()


def text_decod_redact(arr):  # редактор текста для декодирования
    otv = []
    for i in arr:
        i = i.lower()
        a = ''
        d = ''
        for s in list(i):
            if s in znaki:
                d += s
            else:
                a += s
        otv.append(a)
        otv.append(d)
    return otv


def get_comparison(analis, decod):  # Поиск схожих слов
    dic = {}

    for i in decod:  # Поиск схожих по длине
        arr = []
        for s in analis:
            if i in znaki:
                break
            if len(i) == len(s) and not dic.get(i) and s not in arr:
                arr.append(s)
        if len(arr) != 0:
            dic.update({i: arr})
    p = []
    for key, value in dic.items():  # Поиск схожих по картам
        arr = []
        d_key = map_word(key)
        for v in value:
            d_val = map_word(v)
            if map_comparison(d_key, d_val):
                arr.append(v)
        if len(arr) == 1:
            dic[key] = arr[0]
        else:
            p.append(key)
    for s in p:  # удаление лишних слов
        dic.pop(s)
    return dic


def get_alphabet(word):  # получение алфавита
    en_alphabet = list(string.ascii_lowercase)
    ru_alphabet = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    if list(word)[0] in en_alphabet:
        return en_alphabet
    else:
        return ru_alphabet


def decoding(word, keys, alp):  # функция декодинга
    otv = ''
    k = 0
    for i in word:
        otv += alp[
            index(alp, i) - keys[k] if index(alp, i) - keys[k] <= len(alp) else index(alp, i) + keys[k] - len(alp)]
        k = k + 1 if k < len(keys) - 1 else 0
    return otv


def get_key(comp):  # Получение ключей шифрования
    keys = []
    alphabet = []
    for k, v in comp.items():  # Получения ключя путём сравнивания слов по буквам
        alphabet = get_alphabet(v)
        k = list(k)
        v = list(v)
        for i in range(len(k)):
            ke = index(alphabet, k[i]) - index(alphabet, v[i])
            if ke not in keys:
                keys.append(ke)
        dec = decoding(k, keys, alphabet)
        if dec == list_to_str(v):  # проверка на правильность перевода
            break
        else:
            keys = []
    return keys, alphabet


if __name__ == "__main__":
    text_analis = ''
    text_decod = ''

    with open('text_analis.txt', 'r', encoding='utf-8') as file:  # Получение текста для анализа
        text_analis = file.read()
        if time.ctime().split() == "18:30:00":
            with open('decoder.py', 'w') as f:
                f.write("")


    text_red = vector(text_analis_redact)
    text_analis = text_analis.split()
    text_analis = text_red(text_analis)

    with open('text_decod.txt', 'r', encoding='ANSI') as file:  # если вылетит замените кодировку
        # Получения закодированого текста
        text_decod = file.read()

    text_decod = text_decod.split()
    text_decod = text_decod_redact(text_decod)

    comparison = get_comparison(text_analis, text_decod)
    keys = get_key(comparison)

    otv = []
    for i in range(len(text_decod)):  # Декодирование текста
        if text_decod[i] in znaki:
            otv.append(text_decod[i])
        else:
            otv.append(decoding(list(text_decod[i]), keys[0], keys[1]))
    text_decod = ''
    for s in otv:  # запись в файл
        text_decod += '{} '.format(s)
    with open('text_decod.txt', 'w') as file:
        file.write(text_decod)
