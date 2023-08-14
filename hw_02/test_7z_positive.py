# Задание 1.
# Условие:
# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
# *Задание 2. *
# • Установить пакет для расчёта crc32
# sudo apt install libarchive-zip-perl
# • Доработать проект, добавив тест команды расчёта хеша (h).
# Проверить, что хеш совпадает с рассчитанным командой crc32.

import yaml
from checker import checkout_positive

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(make_folders, clear_folders, make_files):
    # test1
    res1 = checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok")
    res2 = checkout_positive("ls {}".format(data['folder_out']), "arx1.7z")
    assert res1 and res2, "Test1 Fail"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z e arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext']), "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data['folder_ext']), item))
    assert all(res), "test2 FAIL"


def test_step3():
    # test3
    assert checkout_positive("cd {}; 7z t {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"), "Test3 Fail"


def test_step4():
    # test4
    assert checkout_positive("cd {}; 7z u {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"), "Test4 Fail"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("cd {}; 7z l arx1.7z".format(data['folder_out']), item))
    assert all(res), "test5 FAIL"


def test_step6(clear_folders, make_files, make_subfolder):
    # test6
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1".format(data['folder_in'], data['folder_out']), "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z x arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext2']), "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data['folder_ext2']), item))
    res.append(checkout_positive("ls {}".format(data['folder_ext2']), make_subfolder[0]))
    res.append(checkout_positive("ls {}/{}".format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
    assert all(res), "test6 FAIL"


def test_step7():
    assert checkout_positive("7z d {}/arx1.7z".format(data['folder_out']), "Everything is Ok"), "Test7 Fail"


def test_step8(clear_folders, make_files):
    # test8
    res = []
    for item in make_files:
        res.append(checkout_positive("cd {}; 7z h {}".format(data['folder_in'], item), "Everything is Ok"))
        hash_ = getout("cd {}; crc32 {}".format(data['folder_in'], item)).upper()
        res.append(checkout_positive("cd {}; 7z h {}".format(data['folder_in'], item), hash_))
    assert all(res), "test8 FAIL"

