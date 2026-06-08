package com.oopforge.example.calculator.adapter.web;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class CalculatorApiTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void commandCreatesThenQueryReturnsHistory() throws Exception {
        mvc.perform(post("/api/v1/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"operandA\":2,\"operator\":\"ADD\",\"operandB\":3}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.calculationId").exists());

        mvc.perform(get("/api/v1/calculations/history"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items[0].result").value(5.0))
                .andExpect(jsonPath("$.items[0].operator").value("add"));
    }
}
