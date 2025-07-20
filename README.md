# 🏥 Patient Management System

A comprehensive FastAPI-based Patient Management System with **two different implementations** for managing patient data, appointments, and medical records with automatic BMI calculation and health assessment.

## 🔄 Two Implementation Approaches

This repository contains **two complete implementations** of the Patient Management System:

### 1. **Enhanced Version** (`project.py`) - *Recommended*
- Complete CRUD with advanced features
- Auto-generated Patient IDs
- Comprehensive statistics and analytics
- Professional error handling and validation

### 2. **Standard Version** (`main.py`) - *Educational*
- Manual ID management
- Computed fields with Pydantic
- Advanced sorting capabilities
- Direct JSON file operations

## 🌟 Common Features

- **Complete CRUD Operations** - Create, Read, Update, and Delete patient records
- **Automatic BMI Calculation** - Calculates BMI and provides health verdicts
- **Data Validation** - Uses Pydantic models for robust input validation
- **Professional API Documentation** - Auto-generated interactive docs
- **Error Handling** - Comprehensive error handling with proper HTTP status codes
- **JSON File Storage** - Persistent data storage in JSON format

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JawadAliAI/FastAPI-An-Introduction-to-Using-FastAPI.git
   cd FastAPI-An-Introduction-to-Using-FastAPI/HTTP_method
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn[standard] pydantic
   ```

3. **Choose and run your preferred implementation:**

   **For Enhanced Version (Recommended):**
   ```bash
   uvicorn project:app --reload
   ```

   **For Standard Version:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the application:**
   - **API**: http://127.0.0.1:8000
   - **Interactive Docs**: http://127.0.0.1:8000/docs
   - **Alternative Docs**: http://127.0.0.1:8000/redoc

## 📋 API Endpoints Comparison

### 🔹 Enhanced Version (`project.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome page with endpoint documentation |
| GET | `/about` | System information |
| GET | `/patients` | Retrieve all patients |
| GET | `/patients/{patient_id}` | Get specific patient |
| POST | `/patients` | Add new patient (auto-ID) |
| PUT | `/patients/{patient_id}` | Update patient |
| DELETE | `/patients/{patient_id}` | Delete patient |
| GET | `/patients/city/{city}` | Search by city |
| GET | `/patients/stats` | Comprehensive statistics |

### � Standard Version (`main.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/about` | System information |
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | Get specific patient |
| GET | `/sort` | Sort patients by height/weight/BMI |
| POST | `/create` | Add new patient (manual ID) |
| PUT | `/edit/{patient_id}` | Update patient |
| DELETE | `/delete/{patient_id}` | Delete patient |

## 🆚 Feature Comparison

| Feature | Enhanced Version | Standard Version |
|---------|-----------------|------------------|
| **ID Generation** | ✅ Auto-generated (P001, P002...) | ❌ Manual ID required |
| **Statistics** | ✅ Comprehensive analytics | ❌ Not available |
| **City Search** | ✅ Available | ❌ Not available |
| **Sorting** | ❌ Not available | ✅ Advanced sorting by height/weight/BMI |
| **Computed Fields** | ❌ Manual calculation | ✅ Pydantic computed fields |
| **File Path Handling** | ✅ Absolute paths | ❌ Relative paths |
| **Error Handling** | ✅ Professional HTTP responses | ✅ Basic error handling |
| **Data Models** | ✅ Separate create/update models | ✅ Advanced Pydantic models |

## 📊 Sample API Usage

### Enhanced Version Examples

**Adding a New Patient (Auto-ID):**
```bash
POST http://127.0.0.1:8000/patients
Content-Type: application/json

{
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

**Get Statistics:**
```bash
GET http://127.0.0.1:8000/patients/stats
```

### Standard Version Examples

**Adding a New Patient (Manual ID):**
```bash
POST http://127.0.0.1:8000/create
Content-Type: application/json

{
  "id": "P006",
  "name": "Jane Smith",
  "city": "Boston",
  "age": 28,
  "gender": "female", 
  "height": 1.65,
  "weight": 60
}
```

**Sort Patients by BMI:**
```bash
GET http://127.0.0.1:8000/sort?sort_by=bmi&order=desc
```

## 📈 BMI Calculation

Both versions automatically calculate BMI using:
```
BMI = weight (kg) / (height (m))²
```

### Health Verdicts:
- **Underweight**: BMI < 18.5
- **Normal**: 18.5 ≤ BMI < 25
- **Overweight**: 25 ≤ BMI < 30 *(Fixed in main.py)*
- **Obese**: BMI ≥ 30

## 🗂️ Project Structure

```
FastAPI/
├── HTTP_method/
│   ├── project.py          # Enhanced implementation (recommended)
│   ├── main.py            # Standard implementation with sorting
│   ├── patients.json       # Patient data storage
│   ├── app.py             # Additional FastAPI examples
│   └── ...
├── main.py                # Root level FastAPI example
├── pyproject.toml         # Project dependencies
└── README.md              # This documentation
```

## 📝 Data Models

### Enhanced Version (project.py)
```python
# Simple input model
{
  "name": "string",
  "city": "string", 
  "age": "integer",
  "gender": "string",
  "height": "float",
  "weight": "float"
}
# Auto-generates: id, bmi, verdict
```

### Standard Version (main.py)
```python
# Complete model with computed fields
{
  "id": "string (required)",
  "name": "string",
  "city": "string",
  "age": "integer (1-119)",
  "gender": "male|female|others",
  "height": "float (>0)",
  "weight": "float (>0)"
}
# Auto-computes: bmi, verdict
```

## 🎯 When to Use Which Version?

### Choose **Enhanced Version** (`project.py`) for:
- 🏢 **Production applications**
- 📊 **Analytics and reporting needs**
- 🔍 **Search functionality requirements**
- 🆔 **Automatic ID management**
- 🛡️ **Professional error handling**

### Choose **Standard Version** (`main.py`) for:
- 📚 **Learning Pydantic computed fields**
- 📈 **Advanced sorting requirements**
- 🎛️ **Manual control over IDs**
- 🔧 **Educational purposes**
- ⚡ **Lightweight implementations**

## 🔧 Bug Fixes Applied

✅ **Fixed BMI verdict logic in main.py:**
- Changed duplicate "Normal" verdict for BMI 25-30 range to "Overweight"

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Jawad Ali** - [JawadAliAI](https://github.com/JawadAliAI)

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Interactive documentation powered by [Swagger UI](https://swagger.io/tools/swagger-ui/)
- Data validation using [Pydantic](https://pydantic-docs.helpmanual.io/)
- Advanced field validation with Pydantic computed fields

---

⭐ **Star this repository if you found it helpful!**

Choose the implementation that best fits your needs and explore both to learn different FastAPI patterns and techniques!