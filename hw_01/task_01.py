# Задание 1.
# Условие:
# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе
# и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

def check_exec(cmd: str, text: str) -> bool:
    import subprocess

    result = subprocess.run(args=f'{cmd}', shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode == 0:
        out = result.stdout
        if text in out:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    print(check_exec('cat /etc/os-release', 'VERSION="22.04.3 LTS (Jammy Jellyfish)"'))
