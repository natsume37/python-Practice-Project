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


def send_data(sk, header, data=None):
    """
    发送数据的协议实现
    协议格式: [4字节头部长度（二进制）] + [头部JSON] + [数据内容]
    """
    try:
        header_json = json.dumps(header)
        header_bytes = header_json.encode('utf-8')
        header_length = bytes(str(len(header_bytes)), 'utf-8').zfill(4)
        sk.send(header_length)
        sk.send(header_bytes)
        print(f"发送头部: {header_json}")
        if data:
            print('data', data)
            if isinstance(data, str):
                data = data.encode('utf-8')
            sk.send(data)
            print(f"发送数据: {len(data)} 字节")
        return True
    except Exception as e:
        print(f"发送数据失败: {e}")
        return False


def recv_data(sk, timeout=60):
    """
    接收数据的协议实现
    """
    sk.settimeout(timeout)
    try:
        print("开始接收头部长度")
        header_length_bytes = sk.recv(4)
        if not header_length_bytes or len(header_length_bytes) < 4:
            print("接收头部长度失败或不足 4 字节")
            return None, None
        header_length = int(header_length_bytes.decode('utf-8'))
        print(f"头部长度: {header_length}")
        header_bytes = b''
        while len(header_bytes) < header_length:
            chunk = sk.recv(header_length - len(header_bytes))
            if not chunk:
                print("接收头部数据中断")
                return None, None
            header_bytes += chunk
        try:
            header_dict = json.loads(header_bytes.decode('utf-8'))
            print(f"接收到头部: {header_dict}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            return None, None
        data_size = header_dict.get('size', 0)
        print(f"预期数据大小: {data_size}")
        data_bytes = b''
        if data_size > 0:
            received = 0
            while received < data_size:
                chunk_size = min(1024, data_size - received)
                chunk = sk.recv(chunk_size)
                if not chunk:
                    print(f"数据接收中断，已接收: {received}/{data_size} 字节")
                    break
                data_bytes += chunk
                received += len(chunk)
                print(f"接收数据块: {len(chunk)} 字节，总计: {received}/{data_size}")
        return header_dict, data_bytes
    except socket.timeout:
        print("接收数据超时")
        return None, None
    except Exception as e:
        print(f"接收数据失败: {e}")
        return None, None


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


def get_file(sk, file_name):
    """
    从服务器下载文件
    """
    header_json = {
        "type": "msg",
        "size": len(file_name.encode('utf-8')),
        "action": "download"
    }
    if send_data(sk, header_json, file_name):
        file_header, file_data = recv_data(sk)
        if file_header and file_header.get('type') == 'file':
            file_size = file_header.get('size', 0)
            file_name = file_header.get('file_name', 'download') + file_header.get('file_format', '')
            print(f"开始下载文件: {file_name}, 大小: {file_size} 字节")
            received_size = len(file_data)
            with open(file_name, 'wb') as f:
                if file_data:
                    f.write(file_data)
                while received_size < file_size:
                    chunk_size = min(1024, file_size - received_size)
                    chunk = sk.recv(chunk_size)
                    if not chunk:
                        print(f"文件数据接收中断，已接收: {received_size}/{file_size} 字节")
                        break
                    f.write(chunk)
                    received_size += len(chunk)
                    progress = received_size / file_size * 100
                    print(f"\r下载进度: {received_size}/{file_size} 字节 ({progress:.1f}%)", end='')
            print(f"\n文件下载完成: {file_name}")
            return True
        else:
            if file_data:
                error_text = file_data.decode('utf-8')
                print(f"下载失败: {error_text}")
    return False


def show_files(sk):
    """
    请求显示服务器文件列表
    """
    header_json = {
        "type": "msg",
        "size": 0,
        "action": "list_files"
    }
    if send_data(sk, header_json):
        response_header, response_data = recv_data(sk)
        if response_data:
            file_list = response_data.decode('utf-8')
            print("服务器文件列表:")
            print(file_list)
            return True
    return False


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
