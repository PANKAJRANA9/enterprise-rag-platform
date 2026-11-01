package com.rag.service.impl;

import com.rag.controller.dto.RagResponse;
import com.rag.exception.InvalidSourceException;
import com.rag.service.RagService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.filter.FilterExpressionBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Set;

@Service
public class RagServiceImpl implements RagService {
    private static final Logger log = LoggerFactory.getLogger(RagServiceImpl.class);
    private static final Set<String> ALLOWED = Set.of("crm_docs","odoo_docs","parking_docs","medical_kb","whatsapp_docs","ncert_docs");

    private final ChatClient chatClient;
    private final VectorStore vectorStore;
    private final int topK;
    private final int topKAll;

    public RagServiceImpl(ChatClient.Builder builder, VectorStore vectorStore,
                          @Value("${rag.top-k:4}") int topK,
                          @Value("${rag.top-k-all:6}") int topKAll) {
        this.chatClient = builder.build();
        this.vectorStore = vectorStore;
        this.topK = topK;
        this.topKAll = topKAll;
    }

    @Override
    public RagResponse ask(String source, String query) {
        long start = System.currentTimeMillis();
        String traceId = MDC.get("traceId");
        if (!ALLOWED.contains(source)) throw new InvalidSourceException("Invalid source: " + source);
        log.info("RAG ask source={} query={} traceId={}", source, query, traceId);

        FilterExpressionBuilder b = new FilterExpressionBuilder();
        var filter = b.eq("source", source).build();

        var docs = vectorStore.similaritySearch(SearchRequest.builder()
                .query(query)
                .topK(topK)
                .similarityThreshold(0.0)
                .filterExpression(filter)
                .build());

        log.info("Found {} docs for source={}", docs.size(), source);

        if (docs.isEmpty()) {
            return new RagResponse("Not found in " + source + " knowledge base. Try ask-all.", List.of(), traceId, System.currentTimeMillis()-start);
        }

        String ctx = docs.stream().map(Document::getText).collect(java.util.stream.Collectors.joining("\n\n"));
        String ans = chatClient.prompt().system("You are enterprise assistant. Use ONLY context. If not in context say not found.\nContext:\n" + ctx).user(query).call().content();
        List<String> sources = docs.stream().map(d -> d.getMetadata().get("source").toString()).distinct().toList();
        return new RagResponse(ans, sources, traceId, System.currentTimeMillis()-start);
    }

    @Override
    public RagResponse askAll(String query) {
        long start = System.currentTimeMillis();
        String traceId = MDC.get("traceId");
        var docs = vectorStore.similaritySearch(SearchRequest.builder().query(query).topK(topKAll).similarityThreshold(0.0).build());
        if (docs.isEmpty()) {
            return new RagResponse("Not found in knowledge base", List.of(), traceId, System.currentTimeMillis()-start);
        }
        String ctx = docs.stream().map(d -> "["+d.getMetadata().get("source")+"] "+d.getText()).collect(java.util.stream.Collectors.joining("\n\n"));
        String ans = chatClient.prompt().system("Context:\n"+ctx).user(query).call().content();
        List<String> sources = docs.stream().map(d -> d.getMetadata().get("source").toString()).distinct().toList();
        return new RagResponse(ans, sources, traceId, System.currentTimeMillis()-start);
    }
}