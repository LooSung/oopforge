package com.oopforge.example.calculator.domain

import java.util.UUID

data class CalculationId(val value: UUID) {
    companion object {
        fun generate(): CalculationId = TODO("Implement stage")

        fun of(raw: String): CalculationId = TODO("Implement stage")
    }
}
