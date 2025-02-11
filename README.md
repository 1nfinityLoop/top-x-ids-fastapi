# FastAPI Top X ID Extractor

This project extracts the top `X` numerical IDs from a dataset based on their numerical values.
---
## How It Works

### **1. File Upload and Endpoint**
The API accepts a file upload (`file`) via the `/top-ids/` POST endpoint and an integer (`x`) that specifies the number of top IDs to return. Example usage:
```bash
curl -X POST "http://127.0.0.1:8000/top-ids/?x=5" -F "file=@test_data.txt"
```

### **2. Validation**
- Ensures `x` is a positive integer. If not, a 400 HTTP error is returned.

### **3. Chunked File Reading**
- The file is read in **1MB chunks** (`CHUNK_SIZE` = 1024 * 1024) to minimize memory usage.
- Any incomplete lines at the end of a chunk are buffered for processing in the next chunk, ensuring no data is lost.

### **4. Line Processing**
Each line in the file is expected to follow the format:
```
<numerical_id>_<numerical_value>
```
- Example: `12345678_500`
- The line is split into two parts:
  - `numerical_id` (e.g., `12345678`)
  - `numerical_value` (e.g., `500`)

### **5. Handling Invalid Lines**
- Lines that do not conform to the format or have non-integer values are **skipped**.
- Warnings are logged for invalid lines (e.g., malformed entries).

### **6. Min-Heap for Top X Values**
- A **min-heap** is used to maintain the top `X` values efficiently:
  - If the heap has fewer than `X` elements, the current `(value, id)` is added.
  - If the heap has `X` elements and the current value is larger than the smallest value in the heap, the smallest value is replaced with the current one.
- This ensures that only the top `X` values are stored in memory.

### **7. Return Results**
- After processing all chunks, the IDs from the heap are extracted and returned in a JSON response:
```json
{
  "top_ids": ["98765432", "12345678", "87654321"]
}
```

---

## **Performance Overview**

### **Time Complexity**
- **File Reading**: `O(N)` (reads all lines in the file).
- **Heap Operations**: `O(N log X)` (insert/remove operations for `X` top values).
- **Total Complexity**: **`O(N log X)`**, where `N` is the number of lines in the file and `X` is the number of top IDs to track.

### **Space Complexity**
- **Heap**: `O(X)` (stores `X` top values in memory).
- **Buffer**: `O(CHUNK_SIZE)` (stores one chunk at a time).

---

## Example Workflow
### Input File:
```
11111111_500
22222222_1000
33333333_1500
44444444_250
55555555_2000
```
### Request:
```bash
curl -X POST "http://127.0.0.1:8000/top-ids/?x=3" -F "file=@test_data.txt"
```
### Response:
```json
{
  "top_ids": ["55555555", "33333333", "22222222"]
}
```

---

## 📌 Features
- Handles large datasets efficiently using a **min-heap**.
- Provides **Dockerized deployment** for easy setup.
- Includes **profiling tools** for performance analysis.
- Implements **unit tests** with `pytest`.

## 🚀 Installation & Setup

1️⃣ **Clone the repository**:
```bash
git clone <repo_url>
cd top-x-ids-fastapi
```

1️⃣ **Clone the repository**:
```bash
docker build -t fastapi-topx .
docker run -p 8000:8000 fastapi-topx
```

### **Run Tests Inside Docker**

1. **Access the running container**:

   ```bash
   docker exec -it <container_id> /bin/sh
   ```

   Replace `<container_id>` with your running container ID, which you can find by running:

   ```bash
   docker ps
   ```

2. **Run the tests inside the container**:

   ```bash
   pytest app/tests
   ```
3. Verify that all tests pass. Example output:
   ```
   ============================= test session starts =============================
   collected 2 items

   app/tests/test_main.py ..                                             [100%]

   ============================== 2 passed in 0.10s ===============================
   ```
   
4. **Exit the container**:

   ```bash
   exit
   ```

