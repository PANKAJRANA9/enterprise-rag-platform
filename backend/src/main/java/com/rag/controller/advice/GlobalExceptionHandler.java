package com.rag.controller.advice;
import com.rag.controller.dto.ErrorResponse;
import com.rag.exception.InvalidSourceException;
import com.rag.exception.RagNotFoundException;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.time.Instant;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InvalidSourceException.class)
    public ResponseEntity<ErrorResponse> handleInvalid(InvalidSourceException ex) {
        return build(HttpStatus.BAD_REQUEST, "Invalid source", ex.getMessage(), null);
    }

    @ExceptionHandler(RagNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(RagNotFoundException ex) {
        return build(HttpStatus.NOT_FOUND, "Not found", ex.getMessage(), null);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        var field = ex.getBindingResult().getFieldErrors().stream().findFirst();
        String fieldName = field.map(f -> f.getField()).orElse("unknown");
        String msg = field.map(f -> f.getDefaultMessage()).orElse("validation failed");
        return build(HttpStatus.BAD_REQUEST, "Validation failed", msg, fieldName);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAll(Exception ex) {
        return build(HttpStatus.INTERNAL_SERVER_ERROR, "Internal error", ex.getMessage(), null);
    }

    private ResponseEntity<ErrorResponse> build(HttpStatus status, String error, String msg, String field) {
        String traceId = MDC.get("traceId") != null ? MDC.get("traceId") : "no-trace";
        var body = new ErrorResponse(Instant.now(), status.value(), error, msg, field, traceId);
        return ResponseEntity.status(status).body(body);
    }
}
