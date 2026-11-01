package com.rag.controller.dto;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
public record AskAllRequest(
    @NotBlank(message = "text is required") @Size(max=500, message = "max 500 chars") String text
) {}
