import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import inputN
import outputP
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.path = "/front_end/"
        path = self.path
        # file_path = "front_end/index.html"
        if path == "/":
            file_path = "front_end/index.html"
        else:
            file_path = path.lstrip("/")

        # if self.headers["other"] == "first":
        #     file_path = "first.json"

        # 获取文件的扩展名
        _, file_extension = os.path.splitext(file_path)

        print(_, file_extension)


        # 设置Content-Type
        content_type = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
        }.get(file_extension, "application/octet-stream")

        try:
            # 打开并读取文件内容
            if file_extension == ".png":
                with open(file_path, "rb") as file:
                    file_content = file.read()
            else :
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()

            # 发送响应状态码
            self.send_response(200)

            # 发送响应头
            self.send_header("Content-type", content_type)
            self.end_headers()
            # 发送文件内容
            
            if file_extension == ".png":
                self.wfile.write(file_content)
            else :
                self.wfile.write(file_content.encode("utf-8"))
        except FileNotFoundError:
            # 处理文件未找到的情况
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        print("PPOST")
        content_length = int(self.headers["Content-Length"])

        # 读取 POST 数据
        post_data = self.rfile.read(content_length)
        print("POST", post_data)

        try:
            # 解析 JSON 数据
            json_data = json.loads(post_data)
            print("json", json_data)
            if json_data['type'] == 0:
                res_str = "是N等价的"
                suc = inputN.inputN(3, json_data['p1'], json_data['p2'])
            else :
                res_str = "是P等价的"
                suc = outputP.outputP(3, json_data['p1'], json_data['p2'])
            print("suc:", suc)
            if not suc:
                res_str = "不" + res_str
            # 发送响应状态码
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # 返回处理结果
            # response = {"status": "success", "ok": suc}
            self.wfile.write(json.dumps(res_str).encode("utf-8"))
        except json.JSONDecodeError:
            # 处理 JSON 解码错误
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "message": "Invalid JSON"}
            self.wfile.write(json.dumps(response).encode("utf-8"))



server_address = ("", 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Starting server on port 8000...")

httpd.serve_forever()