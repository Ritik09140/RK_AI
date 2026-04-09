import g4f
from g4f.client import Client

def main():
    try:
        from g4f.Provider import Blackbox, DuckDuckGo, FreeGpt
        
        for provider in [DuckDuckGo, Blackbox, FreeGpt]:
            try:
                print(f"Testing {provider.__name__}...")
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4o,
                    messages=[{"role": "user", "content": "Hi"}],
                    provider=provider
                )
                print(f"SUCCESS with {provider.__name__}: {response}")
                return
            except Exception as e:
                print(f"FAILED {provider.__name__}: {str(e)}")
    except Exception as e:
        print("FAIL MODULE", e)

if __name__ == "__main__":
    main()
