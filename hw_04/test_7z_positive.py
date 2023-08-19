import yaml

from pp.conftest import save_log
from sshcheckers import ssh_checkout, ssh_getout, upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step0(start_time):
    # test0
    res = []
    upload_files(data['host'], data['user'], "11", "{}/p7zip-full.deb".format(data['local_path']),
                 "{}/p7zip-full.deb".format(data['remote_path']))
    res.append(ssh_checkout(data['host'], data['user'], "11", "echo '11' | sudo -S dpkg -i "
                                                              "{}/p7zip-full.deb".format(data['remote_path']),
                            "Настраивается пакет"))
    res.append(ssh_checkout(data['host'], data['user'], "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    save_log(start_time, data['stat_file'])
    assert all(res), "Test0 Fail"


def test_step1(start_time, make_folders, clear_folders, make_files):
    # test1
    res1 = ssh_checkout(data['host'], data['user'], "11",
                        "cd {}; 7z a -t{} {}/arx1".format(data['folder_in'], data['archive_type'],
                                                          data['folder_out']), "Everything is Ok")
    res2 = ssh_checkout(data['host'], data['user'], "11",
                        "ls {}".format(data['folder_out']), "arx1.{}".format(data['archive_type']))
    save_log(start_time, data['stat_file'])
    assert res1 and res2, "Test1 Fail"


def test_step2(start_time, clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "cd {}; 7z a -t{} {}/arx1".format(data['folder_in'], data['archive_type'],
                                                              data['folder_out']), "Everything is Ok"))
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "cd {}; 7z e arx1.{} -o{} -y".format(data['folder_out'], data['archive_type'],
                                                                 data['folder_ext']), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data['host'], data['user'], "11", "ls {}".format(data['folder_ext']), item))
    save_log(start_time, data['stat_file'])
    assert all(res), "test2 FAIL"


def test_step3():
    # test3
    assert ssh_checkout(data['host'], data['user'], "11",
                        "cd {}; 7z t {}/arx1.{}".format(data['folder_in'], data['folder_out'],
                                                        data['archive_type']),
                        "Everything is Ok"), "Test3 Fail"


def test_step4():
    # test4
    assert ssh_checkout(data['host'], data['user'], "11",
                        "cd {}; 7z u {}/arx1.{}".format(data['folder_in'], data['folder_out'],
                                                        data['archive_type']),
                        "Everything is Ok"), "Test4 Fail"


def test_step5(start_time, clear_folders, make_files):
    # test5
    res = []
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "cd {}; 7z a -t{} {}/arx1".format(data['folder_in'], data['archive_type'],
                                                              data['folder_out']), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data['host'], data['user'], "11",
                                "cd {}; 7z l arx1.{}".format(data['folder_out'], data['archive_type']), item))
    save_log(start_time, data['stat_file'])
    assert all(res), "test5 FAIL"


def test_step6(start_time, clear_folders, make_files, make_subfolder):
    # test6
    res = []
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "cd {}; 7z a -t{} {}/arx1".format(data['folder_in'], data['archive_type'],
                                                              data['folder_out']), "Everything is Ok"))
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "cd {}; 7z x arx1.{} -o{} -y".format(data['folder_out'], data['archive_type'],
                                                                 data['folder_ext2']), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data['host'], data['user'], "11", "ls {}".format(data['folder_ext2']), item))
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "ls {}".format(data['folder_ext2']), make_subfolder[0]))
    res.append(ssh_checkout(data['host'], data['user'], "11",
                            "ls {}/{}".format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
    save_log(start_time, data['stat_file'])
    assert all(res), "test6 FAIL"


def test_step7():
    # test7
    assert ssh_checkout(data['host'], data['user'], "11",
                        "7z d {}/arx1.{}".format(data['folder_out'], data['archive_type']),
                        "Everything is Ok"), "Test7 Fail"


def test_step8(start_time, clear_folders, make_files):
    # test8
    res = []
    for item in make_files:
        res.append(ssh_checkout(data['host'], data['user'], "11",
                                "cd {}; 7z h {}".format(data['folder_in'], item), "Everything is Ok"))
        hash_ = ssh_getout(data['host'], data['user'], "11",
                           "cd {}; crc32 {}".format(data['folder_in'], item)).upper()
        res.append(ssh_checkout(data['host'], data['user'], "11",
                                "cd {}; 7z h {}".format(data['folder_in'], item), hash_))
    save_log(start_time, data['stat_file'])
    assert all(res), "test8 FAIL"
