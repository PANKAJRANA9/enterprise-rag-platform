package com.rag.controller.dto;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
public record AskRequest(
    @NotBlank(message = "table is required") String table,
    @NotBlank(message = "text is required") @Size(max=500, message = "max 500 chars") String text
) {}
