import asyncio
import json
import subprocess
import time
import urllib.request
import websockets

async def measure_page_load(url="http://127.0.0.1:8080/", duration_sec=5.0):
    port = 9223
    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        f"--remote-debugging-port={port}",
        "--window-size=1440,900"
    ]
    proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(1.5)

    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=5)
        tabs = json.loads(req.read().decode())
        ws_url = tabs[0]["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url) as ws:
            # Enable Network
            await ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Page.navigate", "params": {"url": url}}))

            requests = {}
            responses = {}
            transferred = {}

            end_time = time.time() + duration_sec
            while time.time() < end_time:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    method = data.get("method")
                    params = data.get("params", {})

                    if method == "Network.requestWillBeSent":
                        req_id = params.get("requestId")
                        req_obj = params.get("request", {})
                        requests[req_id] = {
                            "url": req_obj.get("url"),
                            "method": req_obj.get("method"),
                            "type": params.get("type")
                        }

                    elif method == "Network.responseReceived":
                        req_id = params.get("requestId")
                        resp_obj = params.get("response", {})
                        responses[req_id] = {
                            "status": resp_obj.get("status"),
                            "mimeType": resp_obj.get("mimeType"),
                            "encodedDataLength": resp_obj.get("encodedDataLength", 0)
                        }

                    elif method == "Network.dataReceived":
                        req_id = params.get("requestId")
                        data_len = params.get("dataLength", 0)
                        encoded_len = params.get("encodedDataLength", 0)
                        transferred[req_id] = transferred.get(req_id, 0) + encoded_len

                    elif method == "Network.loadingFinished":
                        req_id = params.get("requestId")
                        enc_len = params.get("encodedDataLength", 0)
                        if enc_len > transferred.get(req_id, 0):
                            transferred[req_id] = enc_len

                except asyncio.TimeoutError:
                    continue

            # Summary
            total_requests = len(requests)
            total_bytes = sum(transferred.values())

            # Group by resource type
            by_type = {}
            req_details = []

            for r_id, r_info in requests.items():
                r_type = r_info.get("type", "Other")
                b_size = transferred.get(r_id, 0)
                by_type[r_type] = by_type.get(r_type, 0) + b_size

                req_details.append({
                    "url": r_info["url"],
                    "type": r_type,
                    "bytes": b_size,
                    "size_kb": round(b_size / 1024, 1)
                })

            req_details.sort(key=lambda x: x["bytes"], reverse=True)

            print(f"=== INITIAL PAGE LOAD RESULTS ({url}) ===")
            print(f"Total Requests: {total_requests}")
            print(f"Total Transferred: {round(total_bytes / (1024 * 1024), 2)} MB ({total_bytes} bytes)")
            print("\n--- By Resource Type ---")
            for t, sz in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
                print(f"  {t:<15}: {round(sz / (1024 * 1024), 2):>6.2f} MB ({round(sz/1024, 1):>8.1f} KB)")

            print("\n--- Top 15 Heaviest Requests ---")
            for r in req_details[:15]:
                print(f"  {r['size_kb']:>8.1f} KB | {r['type']:<10} | {r['url']}")

            return {
                "total_requests": total_requests,
                "total_bytes": total_bytes,
                "total_mb": round(total_bytes / (1024 * 1024), 2),
                "by_type": by_type,
                "requests": req_details
            }

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    res = asyncio.run(measure_page_load())
    with open("baseline_load_result.json", "w") as f:
        json.dump(res, f, indent=2)
