package com.rag.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;
import java.util.stream.Collectors;

@Service
public class RagService {

    private final VectorStore vectorStore;
    private final ChatClient chatClient;

    public RagService(VectorStore vectorStore, ChatClient.Builder builder) {
        this.vectorStore = vectorStore;
        this.chatClient = builder.build();
    }

    public String ask(String query) {
        // 1. Search your pg_pinecone tables
        var docs = vectorStore.similaritySearch(
                SearchRequest.builder().query(query).topK(4).similarityThreshold(0.7).build()
        );

        if (docs.isEmpty()) {
            return chatClient.prompt().user(query).call().content();
        }

        // 2. Build context from docs
        String context = docs.stream()
                .map(Document::getText)
                .collect(Collectors.joining("\n---\n"));

        String sources = docs.stream()
                .map(d -> d.getMetadata().toString())
                .collect(Collectors.joining(", "));

        // 3. Call Ollama llama3.1:8b with context
        String answer = chatClient.prompt()
                .system("You are a helpful assistant. Use the following context to answer. If context is not relevant, say you don't know. Context:\n" + context)
                .user(query)
                .call()
                .content();

        return answer + "\n\n[Sources: " + sources + "]";
    }
}