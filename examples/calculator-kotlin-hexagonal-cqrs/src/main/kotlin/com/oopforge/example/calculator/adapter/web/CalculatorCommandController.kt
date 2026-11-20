package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.command.Calculate
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/v1/calculations")
class CalculatorCommandController(private val calculate: Calculate) {

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun calculate(@RequestBody request: CalculateRequest): CalculationCreatedResponse {
        val command = Calculate.CalculateCommand(
            request.operandA,
            request.operator,
            request.operandB,
        )
        val id = calculate.handle(command)
        return CalculationCreatedResponse(id.value.toString())
    }
}
