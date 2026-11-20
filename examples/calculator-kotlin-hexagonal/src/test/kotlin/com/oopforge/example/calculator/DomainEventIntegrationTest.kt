package com.oopforge.example.calculator

import com.oopforge.example.calculator.adapter.messaging.CalculationPerformedConsumer
import com.oopforge.example.calculator.adapter.messaging.OutboxRelay
import com.oopforge.example.calculator.application.integration.CalculationPerformedV1
import com.oopforge.example.calculator.application.required.OutboxPort
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.post

@SpringBootTest
@AutoConfigureMockMvc
class DomainEventIntegrationTest(
    @Autowired private val mockMvc: MockMvc,
    @Autowired private val outbox: OutboxPort,
    @Autowired private val relay: OutboxRelay,
    @Autowired private val consumer: CalculationPerformedConsumer,
) {

    @Test
    fun relaysVersionOnePayloadAndDeduplicatesDuplicateDelivery() {
        performCalculation()

        val message = outbox.unpublished().first()
        val payload = message.payload as CalculationPerformedV1
        assertThat(payload.schemaVersion).isEqualTo(1)
        assertThat(payload.result).isEqualTo(32.0)

        relay.relay()
        consumer.consume(message)

        assertThat(consumer.effects()).containsExactly(payload)
        assertThat(outbox.publishedAt(message.id)).isNotNull()
    }

    private fun performCalculation() {
        mockMvc.post("/calculations") {
            contentType = MediaType.APPLICATION_JSON
            content = """{"operandA":8,"operator":"MULTIPLY","operandB":4}"""
        }.andExpect {
            status { isCreated() }
            jsonPath("$.operator") { value("multiply") }
            jsonPath("$.result") { value(32.0) }
        }
    }
}
