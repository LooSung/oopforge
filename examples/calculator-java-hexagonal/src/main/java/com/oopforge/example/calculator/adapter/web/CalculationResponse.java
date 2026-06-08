package com.oopforge.example.calculator.adapter.web;

public record CalculationResponse(String calculationId, double operandA, String operator, double operandB, double result) {}
