package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.adapter.audit.InMemoryAuditAdapter
import jakarta.servlet.FilterChain
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.slf4j.MDC
import org.springframework.stereotype.Component
import org.springframework.web.filter.OncePerRequestFilter
import java.util.UUID

@Component
internal class CorrelationAuditFilter(private val audit: InMemoryAuditAdapter) : OncePerRequestFilter() {

    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain,
    ) {
        val correlationId = correlationId(request.getHeader(CORRELATION_HEADER))
        response.setHeader(CORRELATION_HEADER, correlationId)
        MDC.put(CORRELATION_MDC_KEY, correlationId)
        try {
            filterChain.doFilter(request, response)
        } finally {
            auditCalculation(request, response, correlationId)
            MDC.remove(CORRELATION_MDC_KEY)
        }
    }

    private fun correlationId(provided: String?): String =
        provided?.trim(Character::isWhitespace)
            ?.takeIf { SAFE_CORRELATION_ID.matches(it) }
            ?: UUID.randomUUID().toString()

    private fun auditCalculation(
        request: HttpServletRequest,
        response: HttpServletResponse,
        correlationId: String,
    ) {
        if (request.method == "POST" && request.requestURI == request.contextPath + "/calculations") {
            audit.record(correlationId, "calculation.create", outcome(response.status))
        }
    }

    private fun outcome(status: Int): String =
        when (status) {
            201 -> "created"
            400 -> "invalid_request"
            409 -> "idempotency_conflict"
            422 -> "calculation_rejected"
            else -> if (status >= 500) "failed" else "completed"
        }

    companion object {
        const val CORRELATION_HEADER: String = "X-Correlation-Id"
        private const val CORRELATION_MDC_KEY: String = "correlationId"
        private val SAFE_CORRELATION_ID: Regex = Regex("[A-Za-z0-9._:-]{1,128}")
    }
}
