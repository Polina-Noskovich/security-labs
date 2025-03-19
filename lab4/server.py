import asyncio
import random
import string

PROTECTION = True

MAX_SYN_CONN = 20
SYN_CONNECTIONS = set()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ipadress = writer.get_extra_info("peername")
    print(f"New connection: {ipadress}")

    if PROTECTION and len(SYN_CONNECTIONS) >= MAX_SYN_CONN:
        writer.write("Server is busy, please try again later.\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print(f"Connection cancelled for {ipadress} due to too many open handshakes.")
        return

    handshake_success = False
    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    if PROTECTION:
        try:
            SYN_CONNECTIONS.add(ipadress)
            writer.write(f"TOKEN: {token}\n".encode()) 
            await writer.drain()
            response = await asyncio.wait_for(reader.readline(), timeout=5.0)
            response = response.decode().strip() 

            if response == token: 
                handshake_success = True
                writer.write("Handshake successful.\n".encode())
                await writer.drain()
                print(f"Successful handshake with {ipadress}")
            else:
                writer.write("Handshake failed.\n".encode())
                await writer.drain()
                print(f"Handshake failed from {ipadress}")

        except asyncio.TimeoutError:  
            writer.write("Handshake timeout.\n".encode())
            await writer.drain()
            print(f"Handshake timeout for {ipadress}.")
        finally:
            SYN_CONNECTIONS.discard(ipadress)
    else:  
        handshake_success = True
        writer.write("Connection accepted. Protection is off.\n".encode())
        await writer.drain()
        print(f"Protection disabled: Connected {ipadress} without handshake.")

    if not handshake_success: 
        writer.close()
        await writer.wait_closed()
        print(f"Connection closed for {ipadress} (failed handshake).")
        return

    writer.write("Welcome to the server!\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()
    print(f"Connection closed for {ipadress}")


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8080)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    mode = "on" if PROTECTION else "off"
    print(f"Server running on {addrs} | Protection: {mode}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")