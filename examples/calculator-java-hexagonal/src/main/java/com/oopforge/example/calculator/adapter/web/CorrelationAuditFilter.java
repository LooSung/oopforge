package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.adapter.audit.InMemoryAuditAdapter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.UUID;
import java.util.regex.Pattern;

@Component
final class CorrelationAuditFilter extends OncePerRequestFilter {

    static final String CORRELATION_HEADER = "X-Correlation-Id";
    private static final String CORRELATION_MDC_KEY = "correlationId";
    private static final Pattern SAFE_CORRELATION_ID =
            Pattern.compile("[A-Za-z0-9._:-]{1,128}");

    private final InMemoryAuditAdapter audit;

    CorrelationAuditFilter(InMemoryAuditAdapter audit) {
        this.audit = audit;
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        String correlationId = correlationId(request.getHeader(CORRELATION_HEADER));
        response.setHeader(CORRELATION_HEADER, correlationId);
        MDC.put(CORRELATION_MDC_KEY, correlationId);
        try {
            filterChain.doFilter(request, response);
        } finally {
            auditCalculation(request, response, correlationId);
            MDC.remove(CORRELATION_MDC_KEY);
        }
    }

    private String correlationId(String provided) {
        if (provided == null) {
            return UUID.randomUUID().toString();
        }
        String candidate = provided.strip();
        return isValid(candidate) ? candidate : UUID.randomUUID().toString();
    }

    private boolean isValid(String candidate) {
        return SAFE_CORRELATION_ID.matcher(candidate).matches();
    }

    private void auditCalculation(
            HttpServletRequest request,
            HttpServletResponse response,
            String correlationId) {
        if (request.getMethod().equals("POST")
                && request.getRequestURI().equals(request.getContextPath() + "/calculations")) {
            audit.record(correlationId, "calculation.create", outcome(response.getStatus()));
        }
    }

    private String outcome(int status) {
        return switch (status) {
            case 201 -> "created";
            case 400 -> "invalid_request";
            case 409 -> "idempotency_conflict";
            case 422 -> "calculation_rejected";
            default -> status >= 500 ? "failed" : "completed";
        };
    }
}
