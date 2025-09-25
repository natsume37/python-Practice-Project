# -*- coding: utf-8 -*-
"""
@File    : 07-文件传输客户端.py
@Author  : Martin
@Time    : 2025/9/23 15:39
@Desc    : TCP串行版本 - 修复版
"""

import hashlib
import json
import socket
import os
import time


def read_large_file(file_path, chunk_size=1024):
    """
    文件读取生成器
    """
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk


def file_to_md5(file_path):
    """
    计算文件的MD5值
    """
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


def send_header_json(sk, header):
    header_bytes = bytes(json.dumps(header), encoding='utf-8')
    header_bytes_l = len(header_bytes)
    header_l_bytes = bytes(str(header_bytes_l), "utf-8").zfill(4)
    # 发送数据头长度
    sk.send(header_l_bytes)
    # 发送header_json
    sk.send(bytes(json.dumps(header), encoding='utf-8'))
    return True


def send_msg(sk, msg):
    header = {
        "mode": 'msg',
        "user": "Martin",
        "msg": msg.strip()
    }
    if not send_header_json(sk, header):
        print("发送失败")
    print("请求发送成功")
    # 处理收请求
    header_json = recv_header_json(sk)
    if header_json.get("code", 0) == 200:
        print(header_json.get('msg'))


def send_file(sk, file_path):
    """
    上传文件到服务器
    """
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_header = {
        "mode": 'file',
        "user": "Martin",
        "file_name": os.path.splitext(file_name)[0],
        "file_type": os.path.splitext(file_name)[1],
        "action": "pull_file",
        "md5": file_to_md5(file_path),
        "file_size": file_size,
    }
    print(f"准备上传文件: {file_name}, 大小: {file_size} 字节")
    res = send_header_json(sk, file_header)
    if not res:
        print("文件发送失败")
        return False
    # 开始发送文件
    # 大文件判断

    for chunk in read_large_file(file_path):
        sk.send(chunk)
    print("文件已发送")
    # 处理服务器的反馈信息
    header_200 = recv_header_json(sk)
    if header_200.get("code", 0) != 200:
        msg = header_200.get("msg")
        print(msg)
        return False
    print("传送成功")
    return True


def receive_file_chunks(sk, file_size, chunk_size=1024):
    """
    服务器端接收文件数据的迭代器

    参数:
        conn: 连接对象，用于接收数据
        file_size: 预期的文件总大小
        chunk_size: 每次接收的数据块大小，默认1024字节

    返回:
        生成器，每次产生接收到的数据块
    """
    remaining = file_size
    while remaining > 0:
        # 计算本次应该接收的实际大小（不超过剩余大小和块大小）
        receive_size = min(chunk_size, remaining)
        # 接收数据
        chunk = sk.recv(receive_size)

        if not chunk:
            # 如果没有接收到数据，但还有剩余 bytes 未接收，说明连接可能中断
            raise ConnectionAbortedError("连接已中断，文件传输不完整")

        yield chunk
        remaining -= len(chunk)

    # 如果所有数据都已接收完毕
    if remaining == 0:
        return True
    else:
        raise RuntimeError(f"文件传输不完整，预期接收{file_size}字节，实际接收{file_size - remaining}字节")


def get_file(sk, file_name):
    """
    从服务器下载文件
    """
    file_name_all = os.path.basename(file_name)
    file_name = os.path.splitext(file_name_all)[0]
    file_type = os.path.splitext(file_name_all)[1]
    header = {
        "mode": 'file',
        "user": "Martin",
        "file_name": file_name,
        "file_type": file_type,
        "action": "get_file"
    }
    res = send_header_json(sk, header)
    header_json = recv_header_json(sk)
    if header_json.get("code", 0) != 200:
        msg = header_json.get("msg")
        print(msg)
        return False
    # 接收
    file_size = header_json.get("file_size")
    with open(file_name_all, "wb") as f:
        for i in receive_file_chunks(sk, file_size, chunk_size=1024):
            f.write(i)
    print(f"{file_name_all}文件下载成功")
    return True


def show_files(sk):
    """
    请求显示服务器文件列表
    """
    header = {
        "mode": "file",
        "action": "show_file"
    }
    # 发送头数据
    send_header_json(sk, header)
    header_200 = recv_header_json(sk)
    if header_200.get('code', 0) != 200:
        print("请求失败")
        return False
    file_list_json = header_200.get("file_list", {"r": "err"})['uploads']

    for i in file_list_json:
        print(i)
    return True


def recv_header_json(sk):
    """

    :param sk:
    :return:
    """
    header_h_bytes = sk.recv(4)
    header_h = int(header_h_bytes.decode('utf-8'))
    # 收取header_json
    header_json_bytes = sk.recv(header_h)
    if not header_json_bytes:
        sk.close()
        print("文件头问题、断开连接")
        return None
    header_json = json.loads(header_json_bytes.decode('utf-8'))
    return header_json


def help_menu():
    """
    显示帮助菜单
    """
    print('help界面'.center(50, '-'))
    menu = """1. show files                    # 查看服务器文件列表
2. get [file_name]              # 下载文件
3. pull [file_path]             # 上传文件
4. send [message]               # 发送消息
5. exit                         # 退出程序"""
    print(menu)


def main():
    """
    主函数
    """
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(60)
        sk.connect(('127.0.0.1', 8081))
        print("连接服务器成功！")
        while True:
            help_menu()
            user_input = input("请输入命令>>> ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit' or user_input == '5':
                print("退出程序")
                break
            parts = user_input.split(' ', 1)
            cmd = parts[0].lower()
            try:
                if cmd == '1' or cmd == 'show':
                    show_files(sk)
                elif cmd == '2' or cmd == 'get':
                    if len(parts) > 1:
                        get_file(sk, parts[1])
                    else:
                        print("请指定要下载的文件名，例如: get filename.txt")
                elif cmd == '3' or cmd == 'pull':
                    if len(parts) > 1:
                        send_file(sk, parts[1])
                    else:
                        print("请指定要上传的文件路径，例如: pull /path/to/file.txt")
                elif cmd == '4' or cmd == 'send':
                    if len(parts) > 1:
                        send_msg(sk, parts[1])
                    else:
                        print("请指定要发送的消息，例如: send Hello Server")
                else:
                    print("无效命令，请输入1-5或show/get/pull/send/exit")
            except Exception as e:
                print(f"执行命令时出错: {e}")
    except ConnectionRefusedError:
        print("无法连接到服务器，请确保服务器正在运行")
    except socket.timeout:
        print("连接超时")
    except Exception as e:
        print(f"程序出错: {e}")
    finally:
        try:
            sk.close()
        except:
            pass


if __name__ == '__main__':
    main()
