package com.rag.controller;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record AskRequest(@NotBlank String table, @NotBlank @Size(max=500) String text) {}
