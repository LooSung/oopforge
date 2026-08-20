package com.oopforge.example.calculator;

import com.oopforge.example.calculator.adapter.messaging.CalculationPerformedConsumer;
import com.oopforge.example.calculator.adapter.messaging.OutboxRelay;
import com.oopforge.example.calculator.application.integration.CalculationPerformedV1;
import com.oopforge.example.calculator.application.required.OutboxMessage;
import com.oopforge.example.calculator.application.required.OutboxPort;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class DomainEventIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private OutboxPort outbox;

    @Autowired
    private OutboxRelay relay;

    @Autowired
    private CalculationPerformedConsumer consumer;

    @Test
    void relaysVersionOnePayloadAndDeduplicatesDuplicateDelivery() throws Exception {
        performCalculation();

        OutboxMessage message = outbox.unpublished().getFirst();
        CalculationPerformedV1 payload = (CalculationPerformedV1) message.payload();
        assertThat(payload.schemaVersion()).isEqualTo(1);
        assertThat(payload.result()).isEqualTo(32.0);

        relay.relay();
        consumer.consume(message);

        assertThat(consumer.effects()).containsExactly(payload);
        assertThat(outbox.publishedAt(message.id())).isPresent();
    }

    private void performCalculation() throws Exception {
        mockMvc.perform(post("/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"operandA":8,"operator":"MULTIPLY","operandB":4}
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.operator").value("multiply"))
                .andExpect(jsonPath("$.result").value(32.0));
    }
}
