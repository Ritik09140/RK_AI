import g4f
try:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": "Hi"}],
    )
    print("G4F RESPONSE:", response)
except Exception as e:
    import traceback
    traceback.print_exc()
