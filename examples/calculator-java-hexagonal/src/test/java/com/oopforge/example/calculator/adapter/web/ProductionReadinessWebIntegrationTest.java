package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.adapter.audit.InMemoryAuditAdapter;
import com.oopforge.example.calculator.application.required.OutboxPort;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class ProductionReadinessWebIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private OutboxPort outbox;

    @Autowired
    private InMemoryAuditAdapter audit;

    @Test
    void rejectsInvalidInputWithSafeJson() throws Exception {
        MvcResult result = mockMvc.perform(post("/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"operandA":1,"operandB":2}
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(header().exists(CorrelationAuditFilter.CORRELATION_HEADER))
                .andExpect(jsonPath("$.code").value("invalid_request"))
                .andExpect(jsonPath("$.message").value("The request is invalid."))
                .andReturn();

        assertThat(result.getResponse().getContentAsString())
                .doesNotContain("MethodArgument", "operator");
    }

    @Test
    void replaysTheExactFirstResultWithoutAnotherOutboxRow() throws Exception {
        int initialOutboxRows = outbox.unpublished().size();
        String key = UUID.randomUUID().toString();
        String firstBody = """
                {"operandA":6,"operator":"DIVIDE","operandB":2}
                """;
        String normalizedSameBody = """
                {"operandB":2.0,"operator":"DIVIDE","operandA":6.0}
                """;

        MvcResult first = performCreated(key, firstBody);
        MvcResult duplicate = performCreated(key, normalizedSameBody);

        assertThat(duplicate.getResponse().getContentAsString())
                .isEqualTo(first.getResponse().getContentAsString());
        assertThat(outbox.unpublished()).hasSize(initialOutboxRows + 1);
    }

    @Test
    void rejectsAnIdempotencyKeyReusedForDifferentInput() throws Exception {
        int initialOutboxRows = outbox.unpublished().size();
        String key = UUID.randomUUID().toString();
        performCreated(key, """
                {"operandA":4,"operator":"ADD","operandB":2}
                """);

        mockMvc.perform(post("/calculations")
                        .header("Idempotency-Key", key)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"operandA":4,"operator":"MULTIPLY","operandB":2}
                                """))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("idempotency_conflict"))
                .andExpect(jsonPath("$.message").value(
                        "The idempotency key was already used for a different request."));

        assertThat(outbox.unpublished()).hasSize(initialOutboxRows + 1);
    }

    @Test
    void returnsASafeDomainErrorForDivisionByZero() throws Exception {
        int initialOutboxRows = outbox.unpublished().size();

        MvcResult result = mockMvc.perform(post("/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"operandA":1,"operator":"DIVIDE","operandB":0}
                                """))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.code").value("calculation_rejected"))
                .andExpect(jsonPath("$.message").value(
                        "The calculation could not be performed."))
                .andReturn();

        assertThat(result.getResponse().getContentAsString())
                .doesNotContain("division by zero", "IllegalArgumentException");
        assertThat(outbox.unpublished()).hasSize(initialOutboxRows);
    }

    @Test
    void generatesAndEchoesACorrelationId() throws Exception {
        MvcResult result = mockMvc.perform(validCalculation())
                .andExpect(status().isCreated())
                .andExpect(header().exists(CorrelationAuditFilter.CORRELATION_HEADER))
                .andReturn();

        String correlationId = result.getResponse()
                .getHeader(CorrelationAuditFilter.CORRELATION_HEADER);
        assertThatCodeIsUuid(correlationId);
    }

    @Test
    void echoesAProvidedCorrelationId() throws Exception {
        String correlationId = "client-request-123";

        mockMvc.perform(validCalculation()
                        .header(CorrelationAuditFilter.CORRELATION_HEADER, correlationId))
                .andExpect(status().isCreated())
                .andExpect(header().string(
                        CorrelationAuditFilter.CORRELATION_HEADER,
                        correlationId));
    }

    @Test
    void auditContainsOnlySafeFields() throws Exception {
        String correlationId = "safe-audit-" + UUID.randomUUID();

        mockMvc.perform(post("/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "operandA":2,
                                  "operator":"ADD",
                                  "operandB":3,
                                  "secret":"body-secret"
                                }
                                """)
                        .header(CorrelationAuditFilter.CORRELATION_HEADER, correlationId)
                        .header("Authorization", "Bearer authorization-secret")
                        .header("X-API-Key", "api-key-secret"))
                .andExpect(status().isCreated());

        InMemoryAuditAdapter.AuditEntry entry = audit.entries().stream()
                .filter(candidate -> candidate.correlationId().equals(correlationId))
                .findFirst()
                .orElseThrow();
        assertThat(entry.action()).isEqualTo("calculation.create");
        assertThat(entry.outcome()).isEqualTo("created");
        assertThat(entry.toString())
                .doesNotContain("authorization-secret", "api-key-secret", "body-secret");
        assertThat(InMemoryAuditAdapter.AuditEntry.class.getRecordComponents())
                .extracting(component -> component.getName())
                .containsExactly("correlationId", "action", "outcome");
    }

    private MvcResult performCreated(String key, String body) throws Exception {
        return mockMvc.perform(post("/calculations")
                        .header("Idempotency-Key", key)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isCreated())
                .andReturn();
    }

    private MockHttpServletRequestBuilder validCalculation() {
        return post("/calculations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"operandA":2,"operator":"ADD","operandB":3}
                        """);
    }

    private void assertThatCodeIsUuid(String value) {
        assertThat(value).isNotNull();
        assertThatCode(() -> UUID.fromString(value)).doesNotThrowAnyException();
    }
}
