# **AI-Powered Text Generation API**
🚀 **AI-Powered Text Generation API** allows users to generate AI-based text using OpenAI's API, store responses, and manage generated text securely.

---

## **📌 Features**
- ✅ **User Authentication** (JWT-based login & registration)
- ✅ **Generate AI Text** using OpenAI API
- ✅ **Store & Retrieve** generated texts
- ✅ **Update & Delete** stored texts
- ✅ **Secure API with JWT Authentication**
- ✅ **Dockerized Deployment**
- ✅ **Fully Tested API (Unit & Integration Tests)**

---

## **📋 Project Requirements**
Ensure you have the following installed:
- 🐍 **Python 3.10+**
- 🐘 **PostgreSQL 15+**
- 🐳 **Docker & Docker Compose** (for containerized deployment)
- 💾 **Redis (optional for caching)**

---

## **🛠️ Project Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Osaroigb/ai-text-generator-api.git
cd ai-text-generator-api
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv venv

source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## **🗄️ Database Setup**
### **1️⃣ Configure PostgreSQL**
Create a `.env` file in the project root:
```
# Flask Configuration
APP_PORT=8080
APP_HOST=0.0.0.0
APP_NAME="AI Text Generator"
APP_ENV=development
JWT_SECRET_KEY=mysecretkey
JWT_EXPIRY_IN_SECONDS=3600
OPENAI_API_KEY=your-openai-api-key

# PostgreSQL Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_db_name
```

---

## **🚀 Running the API Locally**
```sh
python run.py
```
The API will be available at:  
📍 **http://127.0.0.1:8080/api**

---

## **🐳 Running the API with Docker**
### **1️⃣ Build and Start Containers**
```sh
docker-compose up --build
```
### **2️⃣ Stop Containers**
```sh
docker-compose down
```
✅ The API is now running at **http://localhost:8080/api**.

---

## **🛠️ Running Tests**
Run unit and integration tests using **pytest**:
```sh
pytest tests/
```
To test inside Docker:
```sh
docker-compose exec app pytest tests/
```

---

## **📖 API Documentation**
### **1️⃣ Authentication**
#### **🔹 Register a User**
**Endpoint:** `POST /api/auth/register`  
**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "john_doe"
  }
}
```

#### **🔹 User Login**
**Endpoint:** `POST /api/auth/login`  
**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "jwt-token-here"
  }
}
```

---

### **2️⃣ Text Generation**
#### **🔹 Generate AI Text**
**Endpoint:** `POST /api/text/`  
**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
**Request:**
```json
{
  "prompt": "Write a poem about AI."
}
```
**Response:**
```json
{
  "success": true,
  "message": "Text generated successfully.",
  "data": {
    "id": 1,
    "user_id": 1,
    "prompt": "Write a poem about AI.",
    "response": "AI is the future...",
    "timestamp": "2024-03-01T12:00:00Z"
  }
}
```

#### **🔹 Get Generated Text by ID**
**Endpoint:** `GET /api/text/<id>`  
**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
**Response:**
```json
{
  "success": true,
  "message": "Generated text retrieved successfully.",
  "data": {
    "id": 1,
    "user_id": 1,
    "prompt": "Write a poem about AI.",
    "response": "AI is the future...",
    "timestamp": "2024-03-01T12:00:00Z"
  }
}
```

#### **🔹 Update Generated Text**
**Endpoint:** `PUT /api/text/<id>`  
**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
**Request:**
```json
{
  "response": "Updated AI text..."
}
```
**Response:**
```json
{
  "success": true,
  "message": "Generated text updated successfully.",
  "data": {
    "id": 1,
    "response": "Updated AI text..."
  }
}
```

#### **🔹 Delete Generated Text**
**Endpoint:** `DELETE /api/text/<id>`  
**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
**Response:**
```json
{
  "success": true,
  "message": "Generated text deleted successfully."
}
```

---

## **🔹 Additional Notes**
- 🔒 **All endpoints (except register/login) require JWT authentication.**
- 📝 **Store `JWT_TOKEN` from `/api/auth/login` and use it in requests.**
- 🚀 **Supports Dockerized deployment for easy setup.**