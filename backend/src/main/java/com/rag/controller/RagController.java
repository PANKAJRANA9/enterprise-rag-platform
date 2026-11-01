package com.rag.controller;
import com.rag.service.RagService;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class RagController {
    private final RagService ragService;
    public RagController(RagService ragService) { this.ragService = ragService; }

    @PostMapping("/ask")
    public Map<String,String> ask(@RequestBody Map<String,String> body) {
        String q = body.get("text");
        String ans = ragService.ask(q);
        return Map.of("query", q, "answer", ans, "source", "crm_docs + Ollama nomic-embed-text");
    }

    @PostMapping("/mock/whatsapp")
    public Map<String,Object> whatsapp(@RequestBody Map<String,String> body) {
        String q = body.get("text");
        String ans = ragService.ask(q);
        return Map.of("from", body.getOrDefault("from","+91 98765 43210"), "reply", ans, "mock", true);
    }
}