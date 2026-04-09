from g4f.client import Client
import asyncio

async def test():
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hi"}],
        )
        print("G4F RESPONSE:", response.choices[0].message.content)
    except Exception as e:
        print("G4F ERROR:", str(e))

asyncio.run(test())
