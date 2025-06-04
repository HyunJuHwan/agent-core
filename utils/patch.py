from config import settings

def patch_output_urls(output: dict) -> dict:
    """로컬 경로 기반 파일들을 FastAPI 이미지 URL로 치환"""
    keys = ["image_url", "webtoon_url", "video_url"]
    valid_exts = (".png", ".jpg", ".jpeg", ".gif", ".mp4")

    for key in keys:
        if key in output and isinstance(output[key], str):
            path = output[key]
            if path.lower().endswith(valid_exts):
                parts = path.split("/")
                if len(parts) >= 2:
                    type_, filename = parts[-2], parts[-1]
                    output[key] = f"{settings.IMAGE_BASE_URL}/{type_}/{filename}"

    return output
