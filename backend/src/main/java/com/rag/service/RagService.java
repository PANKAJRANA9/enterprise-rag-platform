package com.rag.service;
import com.rag.controller.dto.RagResponse;
public interface RagService {
    RagResponse ask(String source, String query);
    RagResponse askAll(String query);
}
