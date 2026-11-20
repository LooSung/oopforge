package com.oopforge.example.calculator.domain

enum class Operator {
    ADD {
        override fun apply(a: Double, b: Double): Double = a + b
    },
    SUBTRACT {
        override fun apply(a: Double, b: Double): Double = a - b
    },
    MULTIPLY {
        override fun apply(a: Double, b: Double): Double = a * b
    },
    DIVIDE {
        override fun apply(a: Double, b: Double): Double {
            require(b != 0.0) { "division by zero" }
            return a / b
        }
    };

    abstract fun apply(a: Double, b: Double): Double
}
