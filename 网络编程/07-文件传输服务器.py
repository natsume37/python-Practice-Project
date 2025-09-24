# -*- coding: utf-8 -*-
import json
import socket
import os
import sys
import traceback

# 创建文件存储目录
if not os.path.exists('uploads'):
    os.makedirs('uploads')

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(('127.0.0.1', 8081))
sk.listen(5)
print("服务器已开启".center(50, '-'))


def recv_header_json(conn):
    """
    header_json解析函数
    :param conn:
    :return: header_json|None
    """
    header_h_bytes = conn.recv(4)
    header_h = int(header_h_bytes.decode('utf-8'))
    # 收取header_json
    header_json_bytes = conn.recv(header_h)
    if not header_json_bytes:
        conn.close()
        print("文件头问题、断开连接")
        return None
    header_json = json.loads(header_json_bytes.decode('utf-8'))
    return header_json


def recv_data(conn):
    """
    接收数据的协议实现
    协议格式: [4字节头部长度（二进制）] + [头部JSON] + [数据内容]
    """
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
            print("到这步")
            # 发送relady信息

            received = 0
            while received < data_size:
                chunk_size = min(1024, data_size - received)
                try:
                    chunk = sk.recv(chunk_size)
                    if not chunk:
                        print(f"数据接收中断，已接收: {received}/{data_size} 字节")
                        break
                    data_bytes += chunk
                    received += len(chunk)
                    print(f"接收数据块: {len(chunk)} 字节，总计: {received}/{data_size}")
                except socket.timeout:
                    print(f"接收数据超时，已接收: {received}/{data_size} 字节")
                    break
            print("recv结束")
        return header_dict, data_bytes

    except Exception as e:
        print(f"接收数据异常: {e}")
        traceback.print_exc()
        return None, None


def send_data(conn, header_json, data=None):
    """
    发送数据的协议实现
    """
    try:
        header_str = json.dumps(header_json)
        header_bytes = header_str.encode('utf-8')
        header_length = bytes(str(len(header_bytes)), 'utf-8').zfill(4)
        conn.send(header_length)
        conn.send(header_bytes)
        print(f"发送头部: {header_json}")
        if data is not None:
            if isinstance(data, str):
                data = data.encode('utf-8')
            header_json['size'] = len(data)  # 确保头部 size 与实际数据一致
            conn.send(data)
            print(f"发送数据: {len(data)} 字节")
        return True
    except Exception as e:
        print(f"发送数据失败: {e}")
        traceback.print_exc()
        return False


def recv_file(conn, header_json):
    """
    客户端获取文件命令
    :param conn:
    :param header_json:
        {
            "mode":'file',
            "user":"Martin",
            "file_name":"test",
            "file_type":".md",
            "action":"pull_file",
            "md5":"fasdfasdfsafsdfaddf"
            "file_size":123123
        }
    :return: bool
    """
    pass

def reply_msg(conn, header_json):
    data = header_json.get('msg', None)
    if not data:
        return None
    header = {
        "code": 200,
        "mode": 'msg',
        "msg": f"{data.upper()}",
    }
    send_data(conn, header)
    return True


def send_file():
    pass


def show_file():
    pass


def handle_client_request(conn, addr):
    try:
        while True:
            # 固定收取文件头
            header_json = recv_header_json(conn)
            if header_json is None:
                break
            # 正常消息回复大写
            if header_json['mode'] == 'msg':
                reply_msg(conn, header_json)
            else:
                continue
    except socket.timeout:
        print("客户端连接超时")
    except Exception as e:
        print(f"处理客户端请求时出错: {e}")
        traceback.print_exc()
    finally:
        conn.close()
        print("连接已关闭")


def main():
    while True:
        conn, addr = sk.accept()
        print(f"\n客户端连接来自: {addr}")
        handle_client_request(conn, addr)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务器关闭")
    finally:
        sk.close()
