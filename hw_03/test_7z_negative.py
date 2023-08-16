import yaml
from checker import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(clear_folders, make_folders, make_files, make_badarx):
    # test1
    assert checkout_negative("cd {}; 7z e badarx.{} -o{} -y".format(data['folder_badarx'], data['archive_type'],
                                                                    data['folder_ext']), "ERROR"), "Test1 neg Fail"


def test_step2(clear_folders, make_folders, make_files, make_badarx):
    # test2
    assert checkout_negative("cd {}; 7z t badarx.{}".format(data['folder_badarx'], data['archive_type']),
                             "ERROR"), "Test2 neg Fail"


def test_step3(clear_folders, make_folders, make_files):
    # test3
    assert checkout_negative("cd {}; 7z a -t{} {}/arx".format(data['folder_in'], data['badarx_type'],
                                                              data['folder_badarx']), "Unsupported archive type")
