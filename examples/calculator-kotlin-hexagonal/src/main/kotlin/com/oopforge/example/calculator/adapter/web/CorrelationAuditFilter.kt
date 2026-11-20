package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.adapter.audit.InMemoryAuditAdapter
import jakarta.servlet.FilterChain
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.stereotype.Component
import org.springframework.web.filter.OncePerRequestFilter

@Component
internal class CorrelationAuditFilter(private val audit: InMemoryAuditAdapter) : OncePerRequestFilter() {

    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain,
    ) {
        TODO("Implement stage")
    }

    companion object {
        const val CORRELATION_HEADER: String = "X-Correlation-Id"
        private const val CORRELATION_MDC_KEY: String = "correlationId"
        private val SAFE_CORRELATION_ID: Regex = Regex("[A-Za-z0-9._:-]{1,128}")
    }
}
