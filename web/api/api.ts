export type ChatMessage = {
    role: "user" | "assistant";
    content: string
}

type ChatResponse = {
    role: "assistant"
    content:  string
}

function apiBaseUrl() {
    const url = import.meta.env.VITE_API_URL
    if (typeof url !== "string" || url.length === 0) {
        throw new Error("VITE_API_URL is missing")
    }
    return url
}

export async function sendMessage(messages: ChatMessage[]): Promise<ChatResponse> {
    const response = await fetch(`${apiBaseUrl()}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages}),
    })
    if (!response.ok) {
        throw new Error(`The chat request failed`)
    }
    return (await response.json()) as ChatResponse
}