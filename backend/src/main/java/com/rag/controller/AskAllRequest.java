package com.rag.controller;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record AskAllRequest(@NotBlank @Size(max=500) String text) {}
