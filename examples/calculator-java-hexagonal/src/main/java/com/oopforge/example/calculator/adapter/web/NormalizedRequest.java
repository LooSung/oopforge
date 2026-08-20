package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.domain.Operator;

record NormalizedRequest(double operandA, Operator operator, double operandB) {

    static NormalizedRequest from(CalculateRequest request) {
        return new NormalizedRequest(
                normalizeZero(request.operandA()),
                request.operator(),
                normalizeZero(request.operandB()));
    }

    private static double normalizeZero(double value) {
        return value == 0.0 ? 0.0 : value;
    }
}
