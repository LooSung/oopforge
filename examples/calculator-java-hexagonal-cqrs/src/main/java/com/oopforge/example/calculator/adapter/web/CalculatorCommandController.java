package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.command.Calculate;
import com.oopforge.example.calculator.domain.CalculationId;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/calculations")
public class CalculatorCommandController {

    private final Calculate calculate;

    public CalculatorCommandController(Calculate calculate) {
        this.calculate = calculate;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CalculationCreatedResponse calculate(@RequestBody CalculateRequest request) {
        Calculate.CalculateCommand command = new Calculate.CalculateCommand(
                request.operandA(),
                request.operator(),
                request.operandB());
        CalculationId id = calculate.handle(command);
        return new CalculationCreatedResponse(id.value().toString());
    }
}
