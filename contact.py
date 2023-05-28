# -*- coding: utf-8 -*-
import base64
import json
import socket
import ssl


def request(socket, request):
    socket.send((request + '\n').encode())
    data = ""
    try:
        while True:

            recv_data = socket.recv(65535)  # надо в цикле
            data += recv_data.decode("cp1251")
    except OSError:
        return data


def prepare_message(dict_data: dict):
    message = dict_data["method"] + " " + dict_data["url"] + f" HTTP/{dict_data['version_http']}\n"
    for header, value in dict_data["headers"].items():
        message += f"{header}: {value}\n"
    message += "\n"

    if dict_data["body"] is not None:
        message += dict_data["body"]
        # message += "\n" не надо
    return message


def put_file(path, file):
    message = prepare_message(
        {
            "method": "PUT",
            "url": "{}".format(path),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode(), "Content-Length": len(file)},
            "body": file
        }
    )
    print(request(client, message), '\n')


def move_file(path_from, path_to):
    message = prepare_message(
        {
            "method": "MOVE",
            "url": "{}".format(path_from),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode(),
                        "Destination": path_to},
            "body": None
        }
    )
    print(request(client, message), '\n')


def delete(path):
    message = prepare_message(
        {
            "method": "DELETE",
            "url": "{}".format(path),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode()},
            "body": None
        }
    )
    print(request(client, message), '\n')


def copy(file, destination):
    message = prepare_message(
        {
            "method": "COPY",
            "url": "{}".format(file),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode(),
                        "Destination": destination},
            "body": None
        }
    )
    print(request(client, message), '\n')


def make_dir(path):
    message = prepare_message(
        {
            "method": "MKCOL",
            "url": "{}".format(path),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode()},
            "body": None
        }
    )
    print(request(client, message), '\n')


def get_file(file):
    message = prepare_message(
        {
            "method": "GET",
            "url": "{}".format(file),
            "version_http": "1.1",
            "headers": {"HOST": HOST_ADDR, "Accept": "*/*",
                        "Authorization": "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode()},
            "body": None
        }
    )
    print(request(client, message), '\n')

# HOST_ADDR = 'somkural.ru'
HOST_ADDR = 'webdav.yandex.ru'
# PORT = 80
PORT = 443 # тут так надо
with open("config.json", "r", encoding="UTF-8") as config_file:
    config = json.load(config_file)
    login = config["login"]
    print(login)
    password = config["password"]
    print(password)

# 443 - порт HTTPs
ssl_contex = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_contex.check_hostname = False
ssl_contex.verify_mode = ssl.CERT_NONE

with socket.create_connection((HOST_ADDR, PORT)) as sock:
    with ssl_contex.wrap_socket(sock, server_hostname=HOST_ADDR) as client:
        client.settimeout(2)
        # в HTTP/1.1 первым говорит клиент
        # message = prepare_message(
        #     {
        #         "method": "GET",
        #         "url": "/",
        #         "version_http": "1.1",
        #         "headers": {"Host": HOST_ADDR},
        #         "body": None
        #     }
        # )
        print("Напишите \"exit\" для выхода.\n"
              "help для помощи")
        input1 = input()
        input_array = input1.split()
        while input_array[0] != 'exit':
            if input_array[0] == "help":
                print("Есть команды:"
                      "\"mkdir path\" - создаёт директорию по пути path, при условии что по этому пути нет файла.\n"
                      "\"get /file.txt\" - получает содержание файла\n"
                      "\"put /asds/ins1.txt file\" - вносит на яндекс диск файл, file - местоположение файла на компе который надо залить\n"
                      "\"copy /asdss/ins1.txt /asds/ins1.txt\" - копирует из одного местоположения в другое\n"
                      "\"delete /a/xfiles\" - удаляет файл по пути\n"
                      "\"move /asdss/ins1.txt /asds/ins1.txt\" - перенос файла\n"
                      "Напишите \"exit\" для выхода.\n")
            elif input_array[0] == "mkdir":
                # make_dir("/a/xfiles/")
                make_dir(input_array[1])
            elif input_array[0] == "get":
                # get_file("/file.txt")
                get_file(input_array[1])
            elif input_array[0] == "put":
                # put_file("/asds/ins1.txt", f.read())
                f = open(input_array[2], 'r')
                put_file(input_array[1], f.read())
                f.close()
            elif input_array[0] == "copy":
                # copy("/a/ins1.txt", "/asdss/ins1.txt")
                copy(input_array[1], input_array[2])
            elif input_array[0] == "delete":
                # delete("/a/xfiles")
                print(input_array[1])
                delete(input_array[1])
            elif input_array[0] == "move":
                #move_file("/asdss/ins1.txt", "/asds/ins1.txt")
                move_file(input_array[1], input_array[2])
            input1 = input()
            input_array = input1.split()

# /folder/subfolder/file.html ННАУЧИТЬСЯ СМОТРЕТЬ ЧТО ЕСТЬ НА ДИСКЕ

##TODO
##Обработка ошибок Сети
##request переписать в цикле
## headers могут быть многострочными
"""
Content-Type: text/html;
    charset=windows-1251
"""
