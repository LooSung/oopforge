package com.oopforge.example.calculator.adapter.web

import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.get
import org.springframework.test.web.servlet.post

@SpringBootTest
@AutoConfigureMockMvc
class CalculatorApiTest(@Autowired private val mvc: MockMvc) {

    @Test
    fun commandCreatesThenQueryReturnsHistory() {
        mvc.post("/api/v1/calculations") {
            contentType = MediaType.APPLICATION_JSON
            content = """{"operandA":2,"operator":"ADD","operandB":3}"""
        }.andExpect {
            status { isCreated() }
            jsonPath("$.calculationId") { exists() }
        }

        mvc.get("/api/v1/calculations/history").andExpect {
            status { isOk() }
            jsonPath("$.items[0].result") { value(5.0) }
            jsonPath("$.items[0].operator") { value("add") }
        }
    }
}
