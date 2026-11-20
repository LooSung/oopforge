package com.oopforge.example.calculator.domain

import java.util.UUID

data class CalculationId(val value: UUID) {
    companion object {
        fun generate(): CalculationId = CalculationId(UUID.randomUUID())

        fun of(raw: String): CalculationId = CalculationId(UUID.fromString(raw))
    }
}
