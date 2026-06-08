package com.oopforge.example.layered.calculator.controller.dto;

public record CalculateRequest(double operandA, com.oopforge.example.layered.calculator.domain.Operator operator, double operandB) {}
