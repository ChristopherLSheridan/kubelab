import os
import psycopg
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Kubelab</title>
        </head>
        <body>
            <h1>Kubelab Customer Manager</h1>
            <p>Kubernetes is serving this page. Whoohoo!</p>
            <form id="customer-form">
                <label for="name">Name:</label>
                <input type="text" id="name" required>

                <label for="email">Email:</label>
                <input type="email" id="email" required>

                <button type="submit">Add Customer</button>
            </form>
            <h2>Customers</h2>
            <ul id="customer-list"></ul>
            <script>
                const form = document.getElementById("customer-form");
                                
                async function loadCustomers() {
                    const response = await fetch("/customers");
                    const customers = await response.json();
                    
                    const customerList = document.getElementById("customer-list");
                    customerList.innerHTML = "";
                    
                    customers.forEach(function(customer) {
                        const item = document.createElement("li");
                        item.textContent = `${customer.name} - ${customer.email}`;
                        customerList.appendChild(item);
                    });
                }
                form.addEventListener("submit", async function(event) {
                    event.preventDefault();

                    const name = document.getElementById("name").value;
                    const email = document.getElementById("email").value;

                    const response = await fetch("/customers", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            name: name,
                            email: email
                        })
                    });

                    const customer = await response.json();

                    console.log(customer);
                    await loadCustomers();
                    form.reset();
                });
                loadCustomers();
            </script>
        </body>
    </html>
    """
