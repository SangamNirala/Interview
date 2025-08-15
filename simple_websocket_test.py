#!/usr/bin/env python3
"""
Simple WebSocket connection test to diagnose connection issues
"""

import asyncio
import websockets
import json
import ssl
import logging

logging.basicConfig(level=logging.DEBUG)

async def test_websocket_connection():
    uri = "wss://browser-dna-collect.preview.emergentagent.com/ws/fingerprinting/test123"
    
    try:
        print(f"Attempting to connect to: {uri}")
        
        # Create SSL context that doesn't verify certificates (for testing)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Try connecting with different configurations
        websocket = await websockets.connect(
            uri,
            ssl=ssl_context,
            ping_interval=None,  # Disable ping
            close_timeout=10
        )
        
        print("✅ WebSocket connected successfully!")
        
        # Try to receive a message
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            print(f"✅ Received message: {message}")
            
            # Try to parse as JSON
            try:
                data = json.loads(message)
                print(f"✅ Parsed JSON: {data}")
            except:
                print("⚠️  Message is not JSON")
                
        except asyncio.TimeoutError:
            print("⚠️  No message received within timeout")
        
        # Try sending a message
        test_message = {
            "type": "test",
            "message": "Hello WebSocket!"
        }
        
        await websocket.send(json.dumps(test_message))
        print("✅ Test message sent")
        
        # Try to receive response
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"✅ Received response: {response}")
        except asyncio.TimeoutError:
            print("⚠️  No response received")
        
        await websocket.close()
        print("✅ Connection closed successfully")
        
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Invalid status code: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Headers: {e.headers}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"❌ Connection closed: {e}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Exception type: {type(e)}")

if __name__ == "__main__":
    asyncio.run(test_websocket_connection())