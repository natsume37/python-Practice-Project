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
        f.seek(0, 2)  # 将指针移到最后
        size = f.tell()  # 获取当前指针的位置
        one_tenth = size // 10
        for i in range(10):
            f.seek(i * one_tenth, 0)
            res = f.read(100)
            m.update(res)
        return m.hexdigest()


def send_data(sk, header_json, data=None):
    """
    发送数据的协议实现
    协议格式: [4字节头部长度] + [头部JSON] + [数据内容]

    :param sk: socket对象
    :param header_json: 头部信息字典
    :param data: 要发送的数据，可以是str或bytes
    :return: 是否发送成功
    """
    try:
        # 序列化头部
        header_str = json.dumps(header_json)
        header_bytes = header_str.encode('utf-8')

        # 发送头部长度（固定4字节，右补0）
        header_length = str(len(header_bytes)).zfill(4).encode('utf-8')
        sk.send(header_length)

        # 发送头部数据
        sk.send(header_bytes)

        # 发送数据内容（如果有）
        if data is not None:
            if isinstance(data, str):
                data = data.encode('utf-8')
            sk.send(data)

        return True

    except Exception as e:
        print(f"发送数据失败: {e}")
        return False


def recv_data(sk, timeout=10):
    """
    接收数据的协议实现
    协议格式: [4字节头部长度] + [头部JSON] + [数据内容]

    :param sk: socket对象
    :param timeout: 超时时间（秒）
    :return: (header_dict, data_bytes) 或 (None, None) 如果失败
    """
    sk.settimeout(timeout)

    try:
        # 1. 接收头部长度（4字节）
        header_length_bytes = sk.recv(4)
        if not header_length_bytes:
            return None, None

        header_length = int(header_length_bytes.decode('utf-8').strip())

        # 2. 接收头部JSON数据
        header_bytes = b''
        while len(header_bytes) < header_length:
            chunk = sk.recv(header_length - len(header_bytes))
            if not chunk:
                return None, None
            header_bytes += chunk

        header_dict = json.loads(header_bytes.decode('utf-8'))

        # 3. 接收数据内容
        data_size = header_dict.get('size', 0)
        data_type = header_dict.get('type', 'msg')

        data_bytes = b''
        if data_size > 0:
            # 接收指定大小的数据
            while len(data_bytes) < data_size:
                chunk_size = min(1024, data_size - len(data_bytes))
                chunk = sk.recv(chunk_size)
                if not chunk:
                    break
                data_bytes += chunk

        return header_dict, data_bytes

    except socket.timeout:
        print("接收数据超时")
        return None, None
    except Exception as e:
        print(f"接收数据失败: {e}")
        return None, None


def send_msg(sk, msg):
    """
    发送消息到服务器
    """
    header_json = {
        "type": "msg",
        "size": len(msg.encode('utf-8')),
        "action": "message"
    }

    if send_data(sk, header_json, msg):
        # 等待服务器响应
        response_header, response_data = recv_data(sk)
        if response_header and response_data:
            response_text = response_data.decode('utf-8')
            print(f"服务器响应: {response_text}")
            return True
    return False


def send_file(sk, file_path):
    """
    上传文件到服务器
    """
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # 准备文件头信息
    file_header = {
        "type": "file",
        "file_name": os.path.splitext(file_name)[0],
        "file_format": os.path.splitext(file_name)[1],
        "MD5": file_to_md5(file_path),
        "size": file_size,
        "action": "upload"
    }

    print(f"准备上传文件: {file_name}, 大小: {file_size} bytes")

    # 先发送文件头信息
    if not send_data(sk, file_header):
        print("发送文件头失败")
        return False

    # 等待服务器确认
    response_header, response_data = recv_data(sk)
    if not response_header or response_header.get('status') != 'ready':
        print("服务器未准备好接收文件")
        return False

    # 发送文件内容
    try:
        total_sent = 0
        for chunk in read_large_file(file_path):
            sk.send(chunk)
            total_sent += len(chunk)
            progress = total_sent / file_size * 100
            print(f"\r上传进度: {total_sent}/{file_size} bytes ({progress:.1f}%)", end='')

        print("\n文件内容发送完成")

        # 等待最终确认
        final_header, final_data = recv_data(sk)
        if final_data:
            final_text = final_data.decode('utf-8')
            print(f"服务器确认: {final_text}")

        return True

    except Exception as e:
        print(f"文件发送失败: {e}")
        return False


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
        # 接收文件头信息
        file_header, file_data = recv_data(sk)
        if file_header and file_header.get('type') == 'file':
            file_size = file_header.get('size', 0)
            file_name = file_header.get('file_name', 'download') + file_header.get('file_format', '')

            print(f"开始下载文件: {file_name}, 大小: {file_size} bytes")

            # 如果文件头中已经包含部分数据，先保存
            received_size = len(file_data)
            with open(file_name, 'wb') as f:
                if file_data:
                    f.write(file_data)

                # 继续接收剩余数据
                while received_size < file_size:
                    chunk_size = min(1024, file_size - received_size)
                    chunk = sk.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_size += len(chunk)
                    progress = received_size / file_size * 100
                    print(f"\r下载进度: {received_size}/{file_size} bytes ({progress:.1f}%)", end='')

            print(f"\n文件下载完成: {file_name}")
            return True
        else:
            # 接收错误消息
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
        "size": 0,  # 没有数据体
        "action": "list_files"
    }

    if send_data(sk, header_json):  # 只发送头部，没有数据体
        response_header, response_data = recv_data(sk)
        if response_data:
            file_list = response_data.decode('utf-8')
            print("服务器文件列表:")
            print(file_list)
            return True
    return False


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
        # 创建TCP socket
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(10)  # 设置超时时间

        # 连接服务器
        sk.connect(('127.0.0.1', 8081))
        print("连接服务器成功！")

        while True:
            help_menu()
            user_input = input("请输入命令>>> ").strip()

            if not user_input:
                continue

            # 退出命令
            if user_input.lower() == 'exit' or user_input == '5':
                print("退出程序")
                break

            # 分割命令和参数
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
        # 关闭连接
        try:
            sk.close()
        except:
            pass


if __name__ == '__main__':
    main()