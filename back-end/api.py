from fastapi import FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn
from PIL import Image
import torch.nn.functional as F 
import torch
from torchvision import transforms as T  
from torchvision.models import resnet50
from torch import nn 
import requests 
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI() 

origins = [
    "http://localhost",
    "http://localhost:3000",
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting CPU to make predictions
device = torch.device("cpu")

# load pretrained model
model = resnet50(pretrained=True) 
model.fc = nn.Linear(in_features=2048,out_features = 3, bias=True) 
model.load_state_dict(torch.load('./solar_resnet_50.pt',map_location=torch.device('cpu')))
model.to(device) 

# labels
class_map = ['Annular_solar_eclipse', 
    'Partial_solar_eclipse', 
    'Total_solar_eclipse']

# prediction function
def predict_img(image): 

    INPUT_DIM = 224 
    preprocess = T.Compose([
            T.Resize(INPUT_DIM ),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )]) 
    

    im = Image.open(image).convert('RGB')
    im_preprocessed = preprocess(im) 
    batch_img_tensor = torch.unsqueeze(im_preprocessed, 0)
    output = model(batch_img_tensor) 
    confidence = F.softmax(output, dim=1)[0] * 100 
    _, indices = torch.sort(output, descending=True) 
    return [(class_map[idx], confidence[idx].item()) for idx in indices[0][:1]]

# prediction function
def predict_img_url(url): 

    INPUT_DIM = 224 
    preprocess = T.Compose([
            T.Resize(INPUT_DIM ),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )]) 
    

    im = Image.open(requests.get(url, stream=True).raw).convert('RGB')
    im_preprocessed = preprocess(im) 
    batch_img_tensor = torch.unsqueeze(im_preprocessed, 0)
    output = model(batch_img_tensor) 
    confidence = F.softmax(output, dim=1)[0] * 100 
    _, indices = torch.sort(output, descending=True) 
    return [(class_map[idx], confidence[idx].item()) for idx in indices[0][:1]]


@app.get("/")
async def root():
    return {"message": "Solar Type prediction"} 

@app.post("/url/")
async def create_url( url : str):       
    # send file to prediction function 
    prediction = predict_img_url(url)
    print(prediction[0]) 
    predicted_eclipse = prediction[0][0] 
    confidence = prediction[0][1]
    return {
        "predicted_eclipse": predicted_eclipse, 
        "confidence": confidence
    }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):       
    print(file)
    # send file to prediction function 
    prediction = predict_img(file.file) 
    print(prediction[0]) 
    predicted_eclipse = prediction[0][0] 
    confidence = prediction[0][1]
    return {
<<<<<<< HEAD
        "predicted_eclipse      ": predicted_eclipse, 
=======
        "predicted_eclipse": predicted_eclipse, 
>>>>>>> e17edf2 (updated twilio service)
        "confidence": confidence
    }


@app.post("/twilio")
async def twilio(predicted_eclipse: str , confidence: str ,mobile : str): 
    print(predicted_eclipse , confidence, mobile) 
<<<<<<< HEAD
<<<<<<< HEAD
    account_sid = "AC206559fde6304309e3c82935789d051b"
    print(account_sid)
=======
>>>>>>> e17edf2 (updated twilio service)
=======
=======
    account_sid = "AC206559fde6304309e3c82935789d051b"
    print(account_sid)
>>>>>>> 87f89bf (integrated with frontend)
>>>>>>> ee990fd (updated api)

    ACCOUNT_SID = os.environ.get("ACCOUNT_SID")

    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
<<<<<<< HEAD
<<<<<<< HEAD
    body= "The Predicted art is from the culture of "+predicted_eclipse,
=======
    body= "The Predicted eclipse is"+predicted_eclipse,
>>>>>>> e17edf2 (updated twilio service)
=======
    body= "The Predicted eclipse is"+predicted_eclipse,
=======
    body= "The Predicted art is from the culture of "+predicted_eclipse,
>>>>>>> 87f89bf (integrated with frontend)
>>>>>>> ee990fd (updated api)
    from_= "+19403146763",
    to= '+91' +mobile
    )
    print(message.sid)
    return {"message": "Message sent successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)