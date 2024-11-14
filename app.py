from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from deepface import DeepFace
import shutil
import os
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Temporary folder to store uploaded files
UPLOAD_FOLDER = "./uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.post("/verify")
async def verify_faces(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
        file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

        # Save files temporarily
        with open(file1_path, "wb") as f:
            shutil.copyfileobj(file1.file, f)
        with open(file2_path, "wb") as f:
            shutil.copyfileobj(file2.file, f)

        # Verify files exist
        if not os.path.exists(file1_path) or not os.path.exists(file2_path):
            return JSONResponse({"error": "Uploaded files not found after saving."}, status_code=500)

        # DeepFace verification
        result = DeepFace.verify(file1_path, file2_path)

        # Cleanup
        os.remove(file1_path)
        os.remove(file2_path)

        return JSONResponse({
            "is_same_person": result["verified"],
            "similarity_score": 1 - result["distance"]
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
