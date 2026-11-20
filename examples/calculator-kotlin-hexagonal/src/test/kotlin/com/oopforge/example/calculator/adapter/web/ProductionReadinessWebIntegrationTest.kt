package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.adapter.audit.InMemoryAuditAdapter
import com.oopforge.example.calculator.application.required.OutboxPort
import org.assertj.core.api.Assertions.assertThat
import org.assertj.core.api.Assertions.assertThatCode
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.annotation.DirtiesContext
import org.springframework.test.web.servlet.MockHttpServletRequestDsl
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.MvcResult
import org.springframework.test.web.servlet.ResultActionsDsl
import org.springframework.test.web.servlet.post
import java.util.UUID
import kotlin.reflect.full.primaryConstructor

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class ProductionReadinessWebIntegrationTest(
    @Autowired private val mockMvc: MockMvc,
    @Autowired private val outbox: OutboxPort,
    @Autowired private val audit: InMemoryAuditAdapter,
) {

    @Test
    fun rejectsInvalidInputWithSafeJson() {
        val result = postCalculation("""{"operandA":1,"operandB":2}""").andExpect {
            status { isBadRequest() }
            header { exists(CorrelationAuditFilter.CORRELATION_HEADER) }
            jsonPath("$.code") { value("invalid_request") }
            jsonPath("$.message") { value("The request is invalid.") }
        }.andReturn()

        assertThat(result.response.contentAsString).doesNotContain("MethodArgument", "operator")
    }

    @Test
    fun replaysTheExactFirstResultWithoutAnotherOutboxRow() {
        val initialOutboxRows = outbox.unpublished().size
        val key = UUID.randomUUID().toString()
        val firstBody = """{"operandA":6,"operator":"DIVIDE","operandB":2}"""
        val normalizedSameBody = """{"operandB":2.0,"operator":"DIVIDE","operandA":6.0}"""

        val first = performCreated(key, firstBody)
        val duplicate = performCreated(key, normalizedSameBody)

        assertThat(duplicate.response.contentAsString).isEqualTo(first.response.contentAsString)
        assertThat(outbox.unpublished()).hasSize(initialOutboxRows + 1)
    }

    @Test
    fun rejectsAnIdempotencyKeyReusedForDifferentInput() {
        val initialOutboxRows = outbox.unpublished().size
        val key = UUID.randomUUID().toString()
        performCreated(key, """{"operandA":4,"operator":"ADD","operandB":2}""")

        postCalculation("""{"operandA":4,"operator":"MULTIPLY","operandB":2}""") {
            header("Idempotency-Key", key)
        }.andExpect {
            status { isConflict() }
            jsonPath("$.code") { value("idempotency_conflict") }
            jsonPath("$.message") { value("The idempotency key was already used for a different request.") }
        }

        assertThat(outbox.unpublished()).hasSize(initialOutboxRows + 1)
    }

    @Test
    fun returnsASafeDomainErrorForDivisionByZero() {
        val initialOutboxRows = outbox.unpublished().size

        val result = postCalculation("""{"operandA":1,"operator":"DIVIDE","operandB":0}""").andExpect {
            status { isUnprocessableEntity() }
            jsonPath("$.code") { value("calculation_rejected") }
            jsonPath("$.message") { value("The calculation could not be performed.") }
        }.andReturn()

        assertThat(result.response.contentAsString).doesNotContain("division by zero", "IllegalArgumentException")
        assertThat(outbox.unpublished()).hasSize(initialOutboxRows)
    }

    @Test
    fun generatesAndEchoesACorrelationId() {
        val result = postCalculation(VALID_CALCULATION).andExpect {
            status { isCreated() }
            header { exists(CorrelationAuditFilter.CORRELATION_HEADER) }
        }.andReturn()

        val correlationId = result.response.getHeader(CorrelationAuditFilter.CORRELATION_HEADER)
        assertThatCodeIsUuid(correlationId)
    }

    @Test
    fun echoesAProvidedCorrelationId() {
        val correlationId = "client-request-123"

        postCalculation(VALID_CALCULATION) {
            header(CorrelationAuditFilter.CORRELATION_HEADER, correlationId)
        }.andExpect {
            status { isCreated() }
            header { string(CorrelationAuditFilter.CORRELATION_HEADER, correlationId) }
        }
    }

    @Test
    fun auditContainsOnlySafeFields() {
        val correlationId = "safe-audit-${UUID.randomUUID()}"

        postCalculation(CALCULATION_WITH_SECRET) {
            header(CorrelationAuditFilter.CORRELATION_HEADER, correlationId)
            header("Authorization", "Bearer authorization-secret")
            header("X-API-Key", "api-key-secret")
        }.andExpect { status { isCreated() } }

        val entry = audit.entries().first { it.correlationId == correlationId }
        assertThat(entry.action).isEqualTo("calculation.create")
        assertThat(entry.outcome).isEqualTo("created")
        assertThat(entry.toString()).doesNotContain("authorization-secret", "api-key-secret", "body-secret")
        assertThat(InMemoryAuditAdapter.AuditEntry::class.primaryConstructor?.parameters?.map { it.name })
            .containsExactly("correlationId", "action", "outcome")
    }

    private fun performCreated(key: String, body: String): MvcResult =
        postCalculation(body) { header("Idempotency-Key", key) }
            .andExpect { status { isCreated() } }
            .andReturn()

    private fun postCalculation(
        body: String,
        headers: MockHttpServletRequestDsl.() -> Unit = {},
    ): ResultActionsDsl =
        mockMvc.post("/calculations") {
            contentType = MediaType.APPLICATION_JSON
            content = body
            headers()
        }

    private fun assertThatCodeIsUuid(value: String?) {
        assertThat(value).isNotNull()
        assertThatCode { UUID.fromString(value) }.doesNotThrowAnyException()
    }

    private companion object {
        const val VALID_CALCULATION = """{"operandA":2,"operator":"ADD","operandB":3}"""
        const val CALCULATION_WITH_SECRET =
            """{"operandA":2,"operator":"ADD","operandB":3,"secret":"body-secret"}"""
    }
}
