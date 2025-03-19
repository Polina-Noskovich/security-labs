import asyncio

async def syn_flood(i: int):
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 8080)

        receive = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"{i} Received: {receive.decode().strip()}")

        await asyncio.sleep(5)
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"ERROR {e}")


async def main():
    tasks = [asyncio.create_task(syn_flood(i)) for i in range(1000)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Syn flood attack immitation...")
    asyncio.run(main())