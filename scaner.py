import os
import pickle
import sys
import time
import socket


def scan(path):
    """
    Рекурсивно сканирует папку, путь к которой указан, считает размер файлов. Дабавляет в словарь с путем к
    файлу и его размером
    :param path: путь до файла
    :return: словарь формата {путь файла: размер файла в байтах}
    """
    files_pack = {}
    for current_dir in os.walk(path):
        path_to_file, dirs, files_in_dir = current_dir
        for file in files_in_dir:
            full_path = "{}/{}".format(path_to_file, file)
            files_pack.update({full_path: os.path.getsize(full_path)})
    return files_pack


def show_different(new_pack, pack):
    """
    Создает 3 словаря: новые, удаленные и измененные файлы
    :param new_pack: новый словарь с содержанием дирректории
    :param pack: старый словарь с содержанием дирректории
    :return: кортеж из словаря с новым содержанием дирректории и лист с тремя словарями
    данных: новые файлы, удаленные и измененные
    """
    new_pack_set = set(new_pack)
    pack_set = set(pack)
    new = {k: new_pack.get(k) for k in new_pack_set - pack_set}
    deleted = {k: pack.get(k) for k in pack_set - new_pack_set}
    changed = {k: new_pack.get(k) for k in new_pack_set & pack_set if new_pack.get(k) != pack.get(k)}
    return new_pack, [new, deleted, changed]


if __name__ == '__main__':

    my_path = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    files = {}
    while True:
        files, msg = show_different(scan(my_path), files)  # обновивили словарь файлов и получили сообщение для отправки
        data = pickle.dumps(msg)  # упаковали сообщение
        sock.sendall(data)  # отправили сообщение
        result = sock.recv(1024)
        time.sleep(2)
    # sock.close()
