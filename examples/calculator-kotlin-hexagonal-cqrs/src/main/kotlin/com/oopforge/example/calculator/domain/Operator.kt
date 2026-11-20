package com.oopforge.example.calculator.domain

enum class Operator {
    ADD {
        override fun apply(a: Double, b: Double): Double = TODO("Implement stage")
    },
    SUBTRACT {
        override fun apply(a: Double, b: Double): Double = TODO("Implement stage")
    },
    MULTIPLY {
        override fun apply(a: Double, b: Double): Double = TODO("Implement stage")
    },
    DIVIDE {
        override fun apply(a: Double, b: Double): Double = TODO("Implement stage")
    };

    abstract fun apply(a: Double, b: Double): Double
}
