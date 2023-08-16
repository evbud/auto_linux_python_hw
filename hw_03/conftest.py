import random
import string
import pytest
import yaml
from datetime import datetime

from checker import checkout_positive, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    return checkout_positive("mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'],
                                                        data['folder_ext'], data['folder_badarx']), "")


@pytest.fixture()
def clear_folders():
    return checkout_positive("rm -rf {}/* {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'],
                                                                      data['folder_ext'], data['folder_ext2'],
                                                                      data['folder_badarx']), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data['count_file']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data['folder_in'],
                                                                                       filename, data['size_file']),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data['folder_in'],
                                                                                      subfoldername, testfilename,
                                                                                      data['size_file']), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_badarx():
    checkout_positive("cd {}; 7z a {}/badarx.7z".format(data['folder_in'], data['folder_badarx']),
                      "Everything is Ok")
    checkout_positive("truncate -s 1 {}/badarx.7z".format(data['folder_badarx']), "Everything is Ok")
    yield "badarx"
    checkout_positive("rm -f {}/badarx.7z".format(data['folder_badarx']), "")


@pytest.fixture(autouse=True)
def make_stat():
    if not checkout_positive("ls {}".format(data['project_dir']), "{}".format(data['stat_file'])):
        checkout_positive("cd {}; > {}; ls".format(data['project_dir'], data['stat_file']),
                          "{}".format(data['stat_file']))
    avg_load = getout("cat /proc/loadavg")
    checkout_positive("cd {}; echo '{} Количество файлов: {}, размер: {}, статистика загрузки: {}' >> {}".
                      format(data['project_dir'], datetime.now(), data['count_file'], data['size_file'],
                             avg_load, data['stat_file']), "")
