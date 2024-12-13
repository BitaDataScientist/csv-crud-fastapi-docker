from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os

app = FastAPI()

class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str

CSV_FILE = 'data.csv'

def read_csv():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'nome', 'cognome', 'codice_fiscale']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.post("/items/")
def create_item(item: Item):
    data = read_csv()
    item_dict = item.dict()
    data.append(item_dict)
    write_csv(data)
    return item_dict

@app.get("/items/")
def get_items():
    return read_csv()

@app.get("/items/{id}")
def get_item(id: int):
    data = read_csv()
    for item in data:
        if item['id'] == str(id):
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{id}")
def update_item(id: int, updated_item: Item):
    data = read_csv()
    for i, item in enumerate(data):
        if item['id'] == str(id):
            data[i] = updated_item.dict()
            write_csv(data)
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{id}")
def delete_item(id: int):
    data = read_csv()
    for i, item in enumerate(data):
        if item['id'] == str(id):
            del data[i]
            write_csv(data)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/count/total")
def get_count():
    data = read_csv()
    return {"count": len(data)}


