package com.oopforge.example.layered.calculator.controller

import com.oopforge.example.layered.calculator.controller.dto.CalculateRequest
import com.oopforge.example.layered.calculator.controller.dto.CalculationResponse
import com.oopforge.example.layered.calculator.service.CalculatorService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestController

@Tag(name = "Calculator", description = "Arithmetic calculation (layered 3-tier)")
@RestController
@RequestMapping("/api/v1/calculations")
class CalculatorController(private val calculatorService: CalculatorService) {

    @Operation(summary = "Perform a calculation")
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun calculate(@RequestBody request: CalculateRequest): CalculationResponse {
        val command = CalculatorService.CalculateCommand(
            request.operandA,
            request.operator,
            request.operandB,
        )
        val result = calculatorService.calculate(command)
        return CalculationResponse(
            result.calculationId,
            result.operandA,
            result.operator.name.lowercase(),
            result.operandB,
            result.result,
        )
    }
}
