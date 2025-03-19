import asyncio

async def client_connect():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

        receive = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"CLIENT ---- Received {receive.decode().strip()}")

        if receive.decode().startswith("TOKEN"):
            token = receive.decode().split()[1]
            writer.write(f"{token}\n".encode())
            await writer.drain()

            handshake_result = await reader.readline()
            print(f"CLIENT ---- {handshake_result.decode().strip()}")
        else:
            print("No handshake, protection is off.")

        welcome = await reader.readline()
        print(f"{welcome.decode().strip()}")
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"CLIENT ---- ERROR: {e}")

if __name__ == '__main__':
    asyncio.run(client_connect())