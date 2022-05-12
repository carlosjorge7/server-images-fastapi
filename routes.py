from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove # Get current working directory
from shutil import rmtree

router = APIRouter()

@router.get('/')
def main():
    return {'Hola': 'mundo'}

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    with open(getcwd() + '/' + file.filename, "wb") as my_file:
        content = await file.read()
        my_file.write(content)
        my_file.close()
    return "success"

@router.get('/file/{file_name}')
def get_file(file_name: str):
    return FileResponse(getcwd() + '/' + file_name)

@router.get('/download/{file_name}')
def download_file(file_name: str):
    return FileResponse(getcwd() + '/' + file_name, media_type='application/octet-stream', filename=file_name)

@router.delete('/delete/{file_name}')
def delete_file(file_name: str):
    try:
        remove(getcwd() + '/' + file_name)
        return JSONResponse(content={
            'removed': True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            'removed': False,
            'message': 'File not found'
        }, status_code=404)

@router.delete('/folder')
def delete_folder(folder_name: str = Form(...)):
    rmtree(getcwd() + folder_name)
    return JSONResponse(content={
        'removed': True
    }, status_code=200)
   


