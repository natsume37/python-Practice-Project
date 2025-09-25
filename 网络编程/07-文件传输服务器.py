# -*- coding: utf-8 -*-
import hashlib
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


def send_header_json(conn, header):
    header_bytes = bytes(json.dumps(header), encoding='utf-8')
    header_bytes_l = len(header_bytes)
    header_l_bytes = bytes(str(header_bytes_l), "utf-8").zfill(4)
    # 发送数据头长度
    conn.send(header_l_bytes)
    # 发送header_json
    conn.send(bytes(json.dumps(header), encoding='utf-8'))
    return True


def receive_file_chunks(conn, file_size, chunk_size=1024):
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
        chunk = conn.recv(receive_size)

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


def file_to_md5(file_path):
    """
    计算文件的MD5值
    """
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


def recv_file(conn, header_json):
    """
    处理file-pull_file请求
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
    file_name = header_json['file_name'] + header_json['file_type']
    file_path = os.path.join("uploads", file_name)
    with open(file_path, 'wb') as f:
        for i in receive_file_chunks(conn, file_size=header_json['file_size']):
            f.write(i)
    # 文件看清校验
    file_md5 = header_json.get('md5')
    if file_md5 != file_to_md5(file_path):
        # 返回处理结果
        header_200 = {
            "code": 400,
            "file_name": header_json['file_name'],
            "file_type": header_json['file_type'],
            "action": "pull_file",
            "msg": "文件可能被篡改、上传失败"
        }
        send_header_json(conn, header_200)
        return False
    # 返回处理结果
    header_200 = {
        "code": 200,
        "file_name": header_json['file_name'],
        "file_type": header_json['file_type'],
        "action": "pull_file",
        "msg": "上传成功"
    }
    res = send_header_json(conn, header_200)
    if not res:
        return False
    return True


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
            elif header_json['mode'] == 'file':
                if header_json['action'] == 'pull_file':
                    recv_file(conn, header_json)
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
