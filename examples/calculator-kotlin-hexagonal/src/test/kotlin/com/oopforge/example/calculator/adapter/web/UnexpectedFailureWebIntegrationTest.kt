package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.provided.Calculate
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.mockito.ArgumentMatchers
import org.mockito.BDDMockito.given
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.context.bean.override.mockito.MockitoBean
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.post

@SpringBootTest
@AutoConfigureMockMvc
class UnexpectedFailureWebIntegrationTest(@Autowired private val mockMvc: MockMvc) {

    @MockitoBean
    private lateinit var calculate: Calculate

    @Test
    fun hidesUnexpectedFailureDetails() {
        given(calculate.handle(anyValue())).willThrow(IllegalStateException("forced internal detail"))

        val result = mockMvc.post("/calculations") {
            contentType = MediaType.APPLICATION_JSON
            content = """{"operandA":2,"operator":"ADD","operandB":3}"""
        }.andExpect {
            status { isInternalServerError() }
            header { exists(CorrelationAuditFilter.CORRELATION_HEADER) }
            jsonPath("$.code") { value("internal_error") }
            jsonPath("$.message") { value("The request could not be completed.") }
        }.andReturn()

        assertThat(result.response.contentAsString)
            .doesNotContain("forced internal detail", "IllegalStateException", "Calculate")
    }

    // ArgumentMatchers.any() returns null. Kotlin null-checks that result when it is passed
    // straight to the non-null `handle` parameter, but not when it is returned as a generic T.
    private fun <T> anyValue(): T = ArgumentMatchers.any()
}
