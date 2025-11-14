# Timesfaner
import os
# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions
import requests
import os
import time
from volcenginesdkarkruntime import Ark


# base64
import base64


# url --> image
def download_image_by_url(download_url, save_path="downloaded_image.jpg"):
    """
    通过直接的下载URL下载图片
    :param download_url: 图片的下载URL（点击可自动下载的链接）
    :param save_path: 图片保存路径（含文件名，默认当前目录下的 downloaded_image.jpg）
    """
    # 模拟浏览器请求头，避免被服务器拒绝（部分网站会拦截爬虫请求）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:

        # 发送GET请求获取图片数据（stream=True 适合大文件，避免占用过多内存）
        response = requests.get(
            download_url,
            headers=headers,
            timeout=15,  # 超时时间15秒，防止无限等待
            stream=True
        )
        # 若请求失败（如404、500），直接抛出异常

        response.raise_for_status()

        # 确保保存目录存在（若save_path包含子目录，如 "images/pic.jpg"）
        save_dir = os.path.dirname(save_path)
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

        # 写入图片文件（二进制模式 "wb"）
        with open(save_path, "wb") as f:
            # 分块写入，适合大图片
            for chunk in response.iter_content(chunk_size=1024 * 8):  # 8KB/块
                if chunk:
                    f.write(chunk)

        print(f"图片下载成功！保存路径：{save_path}")

    except requests.exceptions.RequestException as e:
        # 捕获所有请求相关异常（网络错误、超时、HTTP错误等）
        print(f"图片下载失败！原因：{str(e)}")


class handleCenter:
    def __init__(self):
        pass

    def image_to_base64(image_path):
        """
        将本地图片文件转换为Base64编码字符串

        参数:
            image_path (str): 图片文件的本地路径

        返回:
            str: 包含图片格式前缀的Base64编码字符串，如 'data:image/jpeg;base64,xxxx...'

        异常:
            FileNotFoundError: 图片文件不存在时抛出
            IOError: 读取文件时发生错误时抛出
        """
        # 映射常见图片扩展名到MIME类型
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml'
        }

        # 获取文件扩展名
        import os
        ext = os.path.splitext(image_path)[1].lower()

        # 检查是否支持的格式
        if ext not in mime_types:
            raise ValueError(f"不支持的图片格式: {ext}，支持的格式有: {list(mime_types.keys())}")

        # 读取图片并转换为Base64
        try:
            with open(image_path, 'rb') as f:
                # 读取二进制数据
                image_data = f.read()
                # 转换为Base64编码
                base64_str = base64.b64encode(image_data).decode('utf-8')
                # 添加数据URL前缀
                return f"data:{mime_types[ext]};base64,{base64_str}"
        except FileNotFoundError:
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        except Exception as e:
            raise IOError(f"读取图片失败: {str(e)}")

    # 使用示例
    if __name__ == "__maiadadan__":
        try:
            # 替换为你的图片路径
            img_path = "test_image.jpg"
            base64_code = image_to_base64(img_path)
            print("图片转换为Base64成功，前100个字符:")
            print(base64_code[:100])  # 只打印前100个字符，避免输出过长
        except Exception as e:
            print(f"转换失败: {e}")

    # 将结果元组保存    todo
    def save_image_from_url(urls: tuple, save_directory=f"/temp/I"):
        for i, url in enumerate(urls):
            save_path = os.path.join(save_directory, f"generated_image_{i + 1}.jpg")
            download_image_by_url(url, save_path)

    # 文字生成图片
    def generateImageT2I(self, Tprompt: str):
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
            api_key="1b73476f-bf56-47f6-9d2d-06ef03976a61",
        )

        imagesResponse = client.images.generate(
            model="doubao-seedream-3-0-t2i-250415",
            prompt=Tprompt,
        )
        # 返回图片URL元组

        tup1 = tuple(image.url for image in imagesResponse.data)
        return tup1

    # 通过文字与图片生成图片元组
    def generateT_I2I(self, prompt: str, images: list):
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key="1b73476f-bf56-47f6-9d2d-06ef03976a61",
        )

        base64_images = [self.image_to_base64(img_path) for img_path in images]

        imagesResponse = client.images.generate(
            # Replace with Model ID.
            model="doubao-seedream-4-0-250828",
            prompt=prompt,
            image=base64_images,
            size="2K",
            sequential_image_generation="auto",
            sequential_image_generation_options=SequentialImageGenerationOptions(max_images=3),
            response_format="url",
            watermark=True
        )
        tup1 = tuple(image.url for image in imagesResponse.data)
        return tup1
