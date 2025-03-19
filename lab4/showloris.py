import asyncio

async def slowloris():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

        receive = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"Received {receive.decode().strip()}")

        token = receive.decode().strip().split()[1]
        response = f"{token}\n"
        print("Sending slow responce...")
        
        await asyncio.sleep(10)
        writer.write(response.encode())
        await writer.drain()

        handshake_result = await reader.readline()
        print(f"{handshake_result.decode().strip()}")

        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"ERROR {e}")

if __name__ == '__main__':
    print("Slowloris attack immitation...")
    asyncio.run(slowloris())