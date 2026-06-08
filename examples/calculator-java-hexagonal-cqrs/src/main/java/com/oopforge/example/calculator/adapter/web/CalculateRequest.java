package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.domain.Operator;

public record CalculateRequest(double operandA, Operator operator, double operandB) {}
