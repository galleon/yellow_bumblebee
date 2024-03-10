from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import os
import tempfile
from tennis_shot_identification_and_counts import run

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    """
    Process the uploaded video file.

    Parameters:
    - file: UploadFile object representing the uploaded video file.

    Returns:
    - If the video processing is successful, returns the processed video file as a FileResponse object.
    - If there is an error during video processing, returns a dictionary with an "error" key.

    """
    _, file_extension = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as temp_file:
        temp_file.write(await file.read())
        temp_file.seek(0)

        run(source=temp_file.name, device="0")

        try:
            output_video_path = Path(temp_file.name.split(".")[0] + "_wed.mp4")
            if output_video_path.exists() and output_video_path.is_file():
                return FileResponse(str(output_video_path), media_type="video/mp4", filename=output_video_path.name)
        finally:
            if output_video_path.exists():
                output_video_path.unlink()
    return {"error": "Failed to process the video"}

app = FastAPI()
