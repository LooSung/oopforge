package com.oopforge.example.layered.calculator.controller;

import com.oopforge.example.layered.calculator.controller.dto.CalculateRequest;
import com.oopforge.example.layered.calculator.controller.dto.CalculationResponse;
import com.oopforge.example.layered.calculator.service.CalculatorService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Calculator", description = "Arithmetic calculation (layered 3-tier)")
@RestController
@RequestMapping("/api/v1/calculations")
public class CalculatorController {

    private final CalculatorService calculatorService;

    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
    }

    @Operation(summary = "Perform a calculation")
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CalculationResponse calculate(@RequestBody CalculateRequest request) {
        CalculatorService.CalculateCommand command = new CalculatorService.CalculateCommand(
                request.operandA(),
                request.operator(),
                request.operandB());
        CalculatorService.CalculationResult result = calculatorService.calculate(command);
        return new CalculationResponse(
                result.calculationId(),
                result.operandA(),
                result.operator().name().toLowerCase(),
                result.operandB(),
                result.result());
    }
}
