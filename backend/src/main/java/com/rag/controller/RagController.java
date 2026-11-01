package com.rag.controller;

import com.rag.controller.dto.AskAllRequest;
import com.rag.controller.dto.AskRequest;
import com.rag.controller.dto.RagResponse;
import com.rag.service.RagService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class RagController {
    private final RagService ragService;
    public RagController(RagService ragService) { this.ragService = ragService; }

    @PostMapping("/ask")
    public ResponseEntity<RagResponse> ask(@Valid @RequestBody AskRequest req) {
        return ResponseEntity.ok(ragService.ask(req.table(), req.text()));
    }

    @PostMapping("/ask-all")
    public ResponseEntity<RagResponse> askAll(@Valid @RequestBody AskAllRequest req) {
        return ResponseEntity.ok(ragService.askAll(req.text()));
    }

    @GetMapping("/tables")
    public ResponseEntity<?> tables() {
        return ResponseEntity.ok(new String[]{"crm_docs","odoo_docs","parking_docs","medical_kb","whatsapp_docs","ncert_docs"});
    }

    @GetMapping("/health")
    public ResponseEntity<?> health() {
        return ResponseEntity.ok(java.util.Map.of("status","UP","service","enterprise-rag","version","2.0"));
    }
}
