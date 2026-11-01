package com.rag.controller.dto;
import java.util.List;
public record RagResponse(String answer, List<String> sources, String traceId, long latencyMs) {}
