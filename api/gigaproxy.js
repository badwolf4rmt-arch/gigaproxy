import https from "https";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  try {
    const { messages, systemPrompt, context, apiKey } = req.body;

    if (!apiKey) {
      return res.status(400).json({ error: "Missing GigaChat API key" });
    }

    // Формируем system prompt
    let fullSystemPrompt = systemPrompt || "You are a helpful assistant.";
    if (context && context.trim()) {
      fullSystemPrompt += `\n\nAdditional context:\n${context}`;
    }

    const apiMessages = [{ role: "system", content: fullSystemPrompt }, ...messages];

    // Создаём агент, который игнорирует проверку SSL
    const agent = new https.Agent({
      rejectUnauthorized: false,
    });

    const response = await fetch(
      "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: "GigaChat-2-Max",
          scope: "GIGACHAT_API_CORP",
          messages: apiMessages,
          max_tokens: 4096,
        }),
        agent,
      }
    );

    if (!response.ok) {
      const text = await response.text();
      console.error("⚠️ GigaChat error:", response.status, text);
      res.status(response.status).send(text);
      return;
    }

    const data = await response.json();
    res.status(200).json({
      content: data.choices?.[0]?.message?.content ?? "No content",
      model: "GigaChat-2-Max",
    });
  } catch (err) {
    console.error("🔥 Proxy error:", err);
    res.status(500).json({ error: err.message });
  }
}
