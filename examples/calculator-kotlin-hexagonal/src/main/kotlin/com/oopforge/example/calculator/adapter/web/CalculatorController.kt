package com.oopforge.example.calculator.adapter.web

import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/calculations")
class CalculatorController internal constructor(private val handler: IdempotentCalculationHandler) {

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun calculate(
        @Valid @RequestBody request: CalculateRequest,
        @RequestHeader(value = "Idempotency-Key", required = false) idempotencyKey: String?,
    ): CalculationResponse = handler.handle(request, idempotencyKey)
}
