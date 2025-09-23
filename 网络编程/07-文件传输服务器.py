# -*- coding: utf-8 -*-
import json
import socket
import os
import traceback

# 创建文件存储目录
if not os.path.exists('uploads'):
    os.makedirs('uploads')

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(('127.0.0.1', 8081))
sk.listen(5)
print("服务器已开启".center(50, '-'))


def recv_data(sk):
    """
    接收数据的协议实现
    协议格式: [4字节头部长度] + [头部JSON] + [数据内容]
    """
    try:
        # 1. 接收头部长度（4字节）
        header_length_bytes = sk.recv(4)
        if not header_length_bytes or len(header_length_bytes) < 4:
            return None, None

        try:
            header_length = int(header_length_bytes.decode('utf-8').strip())
        except ValueError:
            return None, None

        # 2. 接收头部JSON数据
        header_bytes = b''
        while len(header_bytes) < header_length:
            chunk = sk.recv(header_length - len(header_bytes))
            if not chunk:
                return None, None
            header_bytes += chunk

        try:
            header_dict = json.loads(header_bytes.decode('utf-8'))
        except json.JSONDecodeError:
            return None, None

        # 3. 接收数据内容
        data_size = header_dict.get('size', 0)
        data_bytes = b''
        if data_size > 0:
            received = 0
            while received < data_size:
                chunk_size = min(1024, data_size - received)
                chunk = sk.recv(chunk_size)
                if not chunk:
                    break
                data_bytes += chunk
                received += len(chunk)

        return header_dict, data_bytes

    except Exception:
        traceback.print_exc()
        return None, None


def send_data(sk, header_json, data=None):
    """
    发送数据的协议实现
    """
    try:
        header_str = json.dumps(header_json)
        header_bytes = header_str.encode('utf-8')

        # 固定4字节头部长度
        header_length = str(len(header_bytes)).zfill(4).encode('utf-8')
        sk.send(header_length)
        sk.send(header_bytes)

        if data is not None:
            if isinstance(data, str):
                data = data.encode('utf-8')
            sk.send(data)

        return True
    except Exception:
        traceback.print_exc()
        return False


def handle_client_request(conn, addr):
    """
    处理客户端请求（长连接版本）
    """
    print(f"开始处理客户端 {addr} 的请求")

    try:
        while True:
            header_dict, data_bytes = recv_data(conn)
            if header_dict is None:
                print("客户端断开连接")
                break

            data_type = header_dict.get('type', 'msg')
            action = header_dict.get('action', '')

            if data_type == 'msg':
                if action == 'list_files':
                    files = [f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]
                    file_list = "\n".join(files) if files else "服务器上没有文件"

                    response_header = {
                        "type": "msg",
                        "size": len(file_list.encode('utf-8')),
                        "status": "success"
                    }
                    send_data(conn, response_header, file_list)

                elif action == 'message':
                    data = data_bytes.decode('utf-8') if data_bytes else ""
                    print(f"收到客户端消息: {data}")

                    response_text = f"服务器已收到: {data.upper()}"
                    response_header = {
                        "type": "msg",
                        "size": len(response_text.encode('utf-8')),
                        "status": "success"
                    }
                    send_data(conn, response_header, response_text)

                elif action == 'download':
                    file_name = data_bytes.decode('utf-8') if data_bytes else ""
                    file_path = os.path.join('uploads', file_name)

                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        response_header = {
                            "type": "file",
                            "file_name": os.path.splitext(file_name)[0],
                            "file_format": os.path.splitext(file_name)[1],
                            "size": file_size,
                            "status": "ready"
                        }
                        send_data(conn, response_header)

                        with open(file_path, 'rb') as f:
                            while chunk := f.read(1024):
                                conn.send(chunk)
                        print(f"文件 {file_name} 发送完成")
                    else:
                        send_data(conn, {
                            "type": "msg",
                            "size": 30,
                            "status": "error"
                        }, f"文件 {file_name} 不存在")

                else:
                    send_data(conn, {
                        "type": "msg",
                        "size": 20,
                        "status": "error"
                    }, "未知动作类型")

            elif data_type == 'file':
                file_name = header_dict.get('file_name', 'unknown')
                file_format = header_dict.get('file_format', '')
                file_size = header_dict.get('size', 0)

                full_filename = f"{file_name}{file_format}"
                file_path = os.path.join('uploads', full_filename)

                send_data(conn, {
                    "type": "msg",
                    "size": 20,
                    "status": "ready"
                }, "ready")

                received_size = len(data_bytes)
                if data_bytes:
                    with open(file_path, 'wb') as f:
                        f.write(data_bytes)

                while received_size < file_size:
                    chunk_size = min(1024, file_size - received_size)
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    with open(file_path, 'ab') as f:
                        f.write(chunk)
                    received_size += len(chunk)

                actual_size = os.path.getsize(file_path)
                if actual_size == file_size:
                    send_data(conn, {
                        "type": "msg",
                        "size": 50,
                        "status": "success"
                    }, f"文件 {full_filename} 上传成功")
                else:
                    send_data(conn, {
                        "type": "msg",
                        "size": 50,
                        "status": "error"
                    }, f"文件大小不匹配: 期望{file_size}, 实际{actual_size}")

            else:
                print(f"未知的数据类型: {data_type}")

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
