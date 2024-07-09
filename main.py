import multiprocessing
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

def foo(process_name):
    name = multiprocessing.current_process().name
    print(f"Starting {name}\n")
    results = []
    if process_name == 'background_process':
        for i in range(0, 5):
            results.append(f'---> starting {i}')
            print(f'---> starting {i}\n')
            time.sleep(1)
    else:
        for i in range(5, 10):
            results.append(f'---> background {i}')
            print(f'---> background {i}\n')
            time.sleep(1)
    print(f"Exiting {name}\n")
    return {"name": name, "results": results}

@app.get("/run/{process_name}")
async def run_process(process_name: str):
    if process_name not in ['background_process', 'NO_background_process']:
        raise HTTPException(status_code=400, detail="Invalid process name")

    if process_name == 'background_process':
        background_process = multiprocessing.Process(name='background_process', target=foo, args=(process_name,))
        background_process.daemon = True
        background_process.start()
        return JSONResponse(content={"message": f"{process_name} started", "daemon": True})
    elif process_name == 'NO_background_process':
        NO_background_process = multiprocessing.Process(name='NO_background_process', target=foo, args=(process_name,))
        NO_background_process.daemon = False
        NO_background_process.start()
        return JSONResponse(content={"message": f"{process_name} started", "daemon": False})

@app.get("/start/{process_name}")
async def start_process(process_name: str):
    if process_name not in ['background_process', 'NO_background_process']:
        raise HTTPException(status_code=400, detail="Invalid process name")

    if process_name == 'background_process':
        background_process = multiprocessing.Process(name='background_process', target=foo, args=(process_name,))
        background_process.daemon = True
        background_process.start()
        return {"message": "Background process started."}
    elif process_name == 'NO_background_process':
        NO_background_process = multiprocessing.Process(name='NO_background_process', target=foo, args=(process_name,))
        NO_background_process.daemon = False
        NO_background_process.start()
        return {"message": "NO_background_process started."}
    else:
        return {"error": "Invalid process name."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
