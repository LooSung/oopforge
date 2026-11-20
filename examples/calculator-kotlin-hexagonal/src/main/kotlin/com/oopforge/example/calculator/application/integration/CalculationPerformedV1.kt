package com.oopforge.example.calculator.application.integration

import java.time.Instant

data class CalculationPerformedV1(
    val schemaVersion: Int,
    val calculationId: String,
    val result: Double,
    val occurredAt: Instant,
) {
    companion object {
        const val SCHEMA_VERSION: Int = 1
    }
}
