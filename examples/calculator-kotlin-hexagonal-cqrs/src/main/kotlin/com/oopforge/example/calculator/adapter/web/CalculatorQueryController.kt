package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.query.CalculationHistory
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/v1/calculations")
class CalculatorQueryController(private val history: CalculationHistory) {

    @GetMapping("/history")
    fun listHistory(@RequestParam(defaultValue = "20") limit: Int): HistoryListResponse = TODO("Implement stage")

    @GetMapping("/{calculationId}")
    fun getCalculation(@PathVariable calculationId: String): ResponseEntity<HistoryEntryResponse> =
        TODO("Implement stage")
}
