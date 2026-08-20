package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.provided.Calculate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class UnexpectedFailureWebIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private Calculate calculate;

    @Test
    void hidesUnexpectedFailureDetails() throws Exception {
        given(calculate.handle(any())).willThrow(
                new IllegalStateException("forced internal detail"));

        MvcResult result = mockMvc.perform(post("/calculations")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"operandA":2,"operator":"ADD","operandB":3}
                                """))
                .andExpect(status().isInternalServerError())
                .andExpect(header().exists(CorrelationAuditFilter.CORRELATION_HEADER))
                .andExpect(jsonPath("$.code").value("internal_error"))
                .andExpect(jsonPath("$.message").value(
                        "The request could not be completed."))
                .andReturn();

        assertThat(result.getResponse().getContentAsString())
                .doesNotContain("forced internal detail", "IllegalStateException", "Calculate");
    }
}
