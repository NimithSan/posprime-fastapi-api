from fastapi import APIRouter, Form, HTTPException,Depends
import requests
import json
import os
from routes.jwt_setup import current_user

router = APIRouter(tags=["QRCode"])

url = "https://api.qrcode-monkey.com/qr/custom"

# This end point is for verify hash password to let user generate qrcode for login new session
@router.post("/api/verify-hash")
def verifyPassword(plain_text:str = Form(...),current_user: dict | None = Depends(current_user)):
    
    pass




@router.post("/api/request_qrcode")
def requestQRCode(data: str = Form(...),current_user: dict | None = Depends(current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = {
        "data": data,
        "config": {
            "body": "dot",
            "eye": "frame14",
            "eyeBall": "ball16",
            "erf1": [],
            "erf2": ["fh"],
            "erf3": ["fv"],
            "brf1": [],
            "brf2": ["fh"],
            "brf3": ["fv"],
            "bodyColor": "#5C8B29",
            "bgColor": "#FFFFFF",
            "eye1Color": "#3F6B2B",
            "eye2Color": "#3F6B2B",
            "eye3Color": "#3F6B2B",
            "eyeBall1Color": "#60A541",
            "eyeBall2Color": "#60A541",
            "eyeBall3Color": "#60A541",
            "gradientColor1": "#5C8B29",
            "gradientColor2": "#25492F",
            "gradientType": "radial",
            "gradientOnEyes": False,
            "logo": ""
        },
        "size": 200,
        "download": True,
        "file": "png"
    }
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = json.loads(response.text)
        
        # Extract and return the imageUrl
        imageUrl = response_data.get("imageUrl")
        if imageUrl:
        
            return {"qrcode": "https:" + imageUrl}
        else:
            raise HTTPException(status_code=500, detail="Failed to generate QR code")
    else:
        # Raise an HTTPException with an appropriate error message
        raise HTTPException(status_code=response.status_code, detail="Failed to generate QR code")
