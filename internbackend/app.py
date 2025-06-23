from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                   "http://127.0.0.1:5500", 
        "http://localhost:52330",  # Add this
        "http://127.0.0.1:52330"],  # or ["http://localhost:5500"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LOGIC_APP_URL = "https://prod-18.centralindia.logic.azure.com:443/workflows/98eae4dd05214aae9aca1d3840a1de72/triggers/When_a_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=LVnn4NTbfBUuseOC_7ClZqL7qL4ZwHaq07DT-wZJFFc"

@app.get("/product/{product_id}")
def get_product(product_id: str):
    try:
        # Send POST request to Logic App
        response = requests.post(LOGIC_APP_URL)
        response.raise_for_status()
        data = response.json()

        # Adjust this if your Logic App returns a nested object
        products = data.get("ResultSets", {}).get("Table1", data)

        # Find the matching product
        product = next((item for item in products if item.get("ProductID") == product_id), None)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    except HTTPException as http_err:
        raise http_err  # preserve original 404
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # general server error

@app.get("/products")
def get_products():
    try:
        # Send POST request to Logic App
        response = requests.post(LOGIC_APP_URL)
        response.raise_for_status()
        data = response.json()

        # Adjust based on Logic App response format
        products = data.get("ResultSets", {}).get("Table1", data)

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




   