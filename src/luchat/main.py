from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from luchat.llm import complete
from luchat.schemas import ChatRequest, ChatResponse

def create_app() -> FastAPI:
    app = FastAPI(title="Luchat", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["Content-Type"],
    )
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/chat", response_model=ChatResponse)
    def chat(body: ChatRequest) -> ChatResponse:
        reply = complete(body.messages)
        return ChatResponse(role="assistant", content=reply)  

    return app


app = create_app()