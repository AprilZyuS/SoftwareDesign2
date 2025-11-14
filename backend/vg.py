import time
from volcenginesdkarkruntime import Ark

class SingletonMeta(type):
    """A metaclass for creating singleton classes."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class VideoGenerator():
    def __init__(self, base_url, api_key):
        self.client = Ark(base_url=base_url, api_key=api_key)

    def D_vedio(self, text, first_imgurl, last_imgurl):
        print("----- create request -----")
        create_result = self.client.content_generation.tasks.create(
            model="doubao-seedance-1-0-pro-250528",
            content=[
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": first_imgurl}, "role": "first_frame"},
                {"type": "image_url", "image_url": {"url": last_imgurl}, "role": "last_frame"}
            ]
        )
        print(create_result)

        task_id = create_result.id
        POLL_INTERVAL = 10  # Polling interval in seconds
        flag = True
        while flag:
            print("----- get request -----")
            get_result = self.client.content_generation.tasks.get(task_id=task_id)
            print(get_result)
            if get_result.status == "succeeded":
                flag = False
                video_url = get_result.output[0].get("url", None)
                if video_url:
                     print(f"Generated video URL: {video_url}")
                     return video_url
                else:
                    print("Video URL not found.")
                    return None
            elif get_result.status == "failed":
                print(f"Task failed with error: {get_result.error}")
                return None
            else:
                print("Task is still running, waiting...")
                time.sleep(POLL_INTERVAL)
        print("----- delete request -----")
        # 删除任务
        try:
            self.client.content_generation.tasks.delete(task_id=task_id)
            print(f"任务 {task_id} 已删除。")
        except Exception as e:
            print(f"删除任务失败: {e}")

        return None