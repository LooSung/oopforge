package com.oopforge.example.calculator.adapter.web

import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.web.servlet.MockMvc

@SpringBootTest
@AutoConfigureMockMvc
class CalculatorApiTest(@Autowired private val mvc: MockMvc) {

    @Test
    fun commandCreatesThenQueryReturnsHistory() {
        TODO("Implement stage: port from Java")
    }
}
