package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.provided.Calculate;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/calculations")
public class CalculatorController {

    private final Calculate calculate;

    public CalculatorController(Calculate calculate) {
        this.calculate = calculate;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CalculationResponse calculate(@RequestBody CalculateRequest request) {
        Calculate.CalculateCommand command = new Calculate.CalculateCommand(
                request.operandA(),
                request.operator(),
                request.operandB());
        Calculate.CalculationResult result = calculate.handle(command);
        return new CalculationResponse(
                result.calculationId(),
                result.operandA(),
                result.operator().name().toLowerCase(),
                result.operandB(),
                result.result());
    }
}
