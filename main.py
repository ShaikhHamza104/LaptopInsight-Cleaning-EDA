from fastapi import FastAPI
import pandas as pd 

def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')

app = FastAPI()

@app.get('/')
async def root():
    return {'massage':'successful'}

df = load_data()

 
@app.get('/laptops')
def laptop():
    return {'laptops':
            df['model_name'].unique().tolist()} 

@app.get('/processor')
def processor():
    return {
        'processors': df['processor_name'].unique().tolist()
    }

@app.get('/brand')
def brand():
    return {'brand':df['brand'].unique().tolist()}

@app.get('/gaming_laptops')
def gaming():
  return {'gaming_laptop':df[df['is_gaming_laptop']]['model_name'].unique().tolist()}


@app.get('/regular_laptops')
def regular():
  return {'gaming_laptop':df[~df['is_gaming_laptop']]['model_name'].unique().tolist()}

