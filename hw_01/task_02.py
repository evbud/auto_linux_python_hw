# Задание 2. (повышенной сложности)
# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

def check_exec(cmd: str, text: str, rmv_punctuation: bool = False) -> bool:
    import subprocess
    from string import punctuation

    result = subprocess.run(args=f'{cmd}', shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode == 0:
        out = result.stdout
        if rmv_punctuation:
            for sym in punctuation:
                out = out.replace(sym, ' ')
            new_list = out.split()
            if text in new_list:
                return True
            else:
                return False

        else:
            if text in out:
                return True
            else:
                return False
    else:
        return False


if __name__ == '__main__':
    print(check_exec('cat /etc/os-release', 'VERSION="22.04.3 LTS (Jammy Jellyfish)"'))
    print(check_exec('cat /etc/os-release', 'VERSION', True))
