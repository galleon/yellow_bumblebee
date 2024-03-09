from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
import cv2
from PIL import Image
import io
import tempfile
import os
from pathlib import Path


from tennis_shot_identification_and_counts import run

app = FastAPI()

@app.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(await file.read())
        temp_file.seek(0)

        run(source="temp_file.name", device="0")

        # Test if the video file exists and can be read
        try:
            output_video_path = Path(temp_file.name.split(".")[0] + "_wed.mp4")
            if output_video_path.exists() and output_video_path.is_file():
                return FileResponse(str(output_video_path), media_type="video/mp4", filename=output_video_path.name)
        finally:
            if output_video_path.exists():
                output_video_path.unlink()

    # If the process fails, return an error response
    return {"error": "Failed to process the video"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
