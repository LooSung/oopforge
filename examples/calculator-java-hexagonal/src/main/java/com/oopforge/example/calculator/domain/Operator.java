package com.oopforge.example.calculator.domain;

public enum Operator {
    ADD { public double apply(double a, double b) { return a + b; } },
    SUBTRACT { public double apply(double a, double b) { return a - b; } },
    MULTIPLY { public double apply(double a, double b) { return a * b; } },
    DIVIDE {
        public double apply(double a, double b) {
            if (b == 0) { throw new IllegalArgumentException("division by zero"); }
            return a / b;
        }
    };
    public abstract double apply(double a, double b);
}
