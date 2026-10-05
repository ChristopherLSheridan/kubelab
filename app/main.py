import os
import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Customer(BaseModel):
    name: str
    email: str

@app.get("/")
def root():
    return {"message": "Kubelab API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/environment")
def environment():
    return {"environment": os.getenv("APP_ENV", "unknown")}

@app.get("/customers")
def get_customers():
    conn = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers;")
    customers = cursor.fetchall()
    cursor.close()

    conn.close()

    customers_list = []
    
    for customer in customers:
        customers_list.append({
            "id": customer[0],
            "name": customer[1],
            "email": customer[2]
        })

    return customers_list

@app.post("/customers")
def create_customer(customer: Customer):
    conn = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()
    query = "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id;"
    data = (customer.name, customer.email)
    cursor.execute(query, data)
    customer_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "id": customer_id,
        "name": customer.name,
        "email": customer.email
    }
