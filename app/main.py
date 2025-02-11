import logging
from typing import Dict, List

from fastapi import FastAPI, UploadFile, HTTPException
import heapq
from app.performance import profile_memory

app = FastAPI()
CHUNK_SIZE = 1024 * 1024  # Read 1MB chunks

@app.post("/top-ids/")
@profile_memory  # Apply memory profiling
async def get_top_ids(file: UploadFile, x: int) -> Dict[str, List[str]]:
    """
    Processes a dataset and returns the top X numerical IDs with the highest values.
    """
    if x <= 0:
        raise HTTPException(status_code=400, detail="X must be a positive integer")

    heap = []

    try:
        buffer = b''
        while chunk := await file.read(CHUNK_SIZE):
            buffer += chunk
            lines = buffer.split(b'\n')

            for line_bytes in lines[:-1]:
                line = line_bytes.decode().strip()
                if not line:
                    continue
                parts = line.split('_')
                if len(parts) != 2:
                    logging.warning(f"Ignoring invalid line: {line}")
                    continue
                id_part, value_part = parts
                try:
                    value = int(value_part)
                except ValueError:
                    logging.warning(f"Ignoring line with invalid value: {line}")
                    continue

                # Maintain min-heap of size X
                if len(heap) < x:
                    heapq.heappush(heap, (value, id_part))
                elif value > heap[0][0]:
                    heapq.heappushpop(heap, (value, id_part))

            buffer = lines[-1]

        if buffer:
            try:
                line = buffer.decode().strip()
                if line:
                    parts = line.split('_')
                    if len(parts) == 2:
                        id_part, value_part = parts
                        value = int(value_part)
                        if len(heap) < x:
                            heapq.heappush(heap, (value, id_part))
                        elif value > heap[0][0]:
                            heapq.heappushpop(heap, (value, id_part))
            except Exception:
                pass

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Error processing the file")

    return {"top_ids": [item[1] for item in heap]}