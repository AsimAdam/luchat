import { useState, type FormEvent } from "react"
import { sendMessage, type ChatMessage } from "../api/api"

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [draft, setDraft] = useState("")
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const content = draft.trim()
    if (content.length === 0) {
      return
    }

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content }]
    setMessages(nextMessages)
    setDraft("")
    setError(null)

    try {
      const reply = await sendMessage(nextMessages)
      setMessages([...nextMessages, reply])
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "The chat request failed")
    }
  }

  return (
    <main>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>
            {message.role}: {message.content}
          </li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {error ? <p>{error}</p> : null}
    </main>
  )
}