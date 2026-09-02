import ollama
import json
from models import weather, chatRequest, chatResponse,WeatherAPIError
from prompts import SYSTEM_PROMPT
from tools import TOOLS
from fastapi import FastAPI, HTTPException


MODEL = "llama3.2"
app = FastAPI()


OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 300,
    "num_ctx": 4096,
}

class ChatBot:
   def __init__(self, model:str= MODEL, options: dict = OPTIONS):
      self.model = MODEL
      self.options = OPTIONS
      self.messages = [{"role": "system","content":SYSTEM_PROMPT}]


   def _call_model(self):
      return ollama.chat(
         model =self.model,
         messages = self.messages,
         tools= TOOLS,
         stream=True,
         options=self.options

      )

   def _consume_stream(self, stream):
        """Print content as it arrives; return (full_text, tool_calls|None)."""
        content = ""
        tool_calls = None
        for chunk in stream:
            msg = chunk["message"]
            if msg.get("tool_calls"):
                tool_calls = msg["tool_calls"]
            piece = msg.get("content")
            if piece:
                print(piece, end="", flush=True)
                content += piece
        return content, tool_calls

   def ask(self, user_input: str) -> str:
    self.messages.append({"role": "user", "content": user_input})
    print("Bot: ", end="", flush=True)
    content, tool_calls = self._consume_stream(self._call_model())

    if tool_calls:
        self.messages.append({"role": "assistant", "content": content, "tool_calls": tool_calls})
        for call in tool_calls:
            function = call["function"] if isinstance(call, dict) else call.function
            name = function["name"] if isinstance(function, dict) else function.name
            arguments = function["arguments"] if isinstance(function, dict) else function.arguments
            result = weather(arguments.get("city")) if name == "get_weather" else {"error": f"Unknown tool '{name}'"}
            self.messages.append({"role": "tool", "content": json.dumps(result)})

        final_content, _ = self._consume_stream(self._call_model())
        print()
        self.messages.append({"role": "assistant", "content": final_content})
        return final_content

    print()
    self.messages.append({"role": "assistant", "content": content})
    return content


@app.post("/Chat", response_model= chatResponse)
def askbot(payload: chatRequest):

    bot = ChatBot()
    try:
        reply = bot.ask(payload.user_input)    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return chatResponse(reply=reply)

def main():
   bot= ChatBot()
   print("AI chatbot (weather-aware).type 'exit' or 'quit' to stop\n")

   while True:
      user_input = input("you:").strip()
      if user_input.lower() in {"exit", "quit"}:
            print("BOT: GoodBye..!")
            break
      if not user_input:
         continue

      try:
         bot.ask(user_input)
         print()
      except Exception as exc:
         print(f"\n BOT: Sorry, Something went wrong: {exc}\n")   

if __name__ == "__main__":
   main()         



# @app.post('/help')
# def help():
#    return {'message': "nenu am cheyalo nake teliyakunda kaliga unte..nuv vachi help antav ..pakkaki pora pulka"}


# @app.post('/route')
# def route():
#    return {'route': 'route am ledu mingey ra '}

# @app.post('/chat')
# def askbot(User_input: str):
#    return {'message': 'inka am undile mawa'}


