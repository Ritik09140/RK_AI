import sys
import os
import asyncio
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
asyncio.set_event_loop(asyncio.new_event_loop())

prompt = os.environ.get('RK_PROMPT', 'Hello')

try:
    from g4f.client import Client
    c = Client()
    r = c.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}]
    )
    print('AI:' + r.choices[0].message.content.strip())
except Exception as e:
    print('ERROR:' + str(e))
