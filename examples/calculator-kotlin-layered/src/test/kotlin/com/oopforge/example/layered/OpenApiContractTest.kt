package com.oopforge.example.layered

import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.get

@SpringBootTest
@AutoConfigureMockMvc
class OpenApiContractTest(@Autowired private val mockMvc: MockMvc) {

    @Test
    fun openApiDocsAvailable() {
        mockMvc.get("/v3/api-docs").andExpect {
            status { isOk() }
            jsonPath("$.openapi") { exists() }
            jsonPath("$.paths['/api/v1/calculations']") { exists() }
        }
    }
}
