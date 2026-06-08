package com.oopforge.example.layered.calculator.controller.dto;

public record CalculationResponse(String calculationId, double operandA, String operator, double operandB, double result) {}
