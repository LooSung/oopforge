package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.query.CalculationHistory;
import com.oopforge.example.calculator.domain.CalculationId;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/calculations")
public class CalculatorQueryController {

    private final CalculationHistory history;

    public CalculatorQueryController(CalculationHistory history) {
        this.history = history;
    }

    @GetMapping("/history")
    public HistoryListResponse listHistory(@RequestParam(defaultValue = "20") int limit) {
        List<HistoryEntryResponse> items = history.listRecent(limit).stream()
                .map(HistoryEntryResponse::from)
                .toList();
        return new HistoryListResponse(items);
    }

    @GetMapping("/{calculationId}")
    public ResponseEntity<HistoryEntryResponse> getCalculation(@PathVariable String calculationId) {
        return history.findById(CalculationId.of(calculationId))
                .map(summary -> ResponseEntity.ok(HistoryEntryResponse.from(summary)))
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}
