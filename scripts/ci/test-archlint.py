#!/usr/bin/env python3
"""Self-test for archlint.py — proves it catches violations and clears clean code.

Builds throwaway fixtures in a temp dir, asserts expected pass/fail, then also
lints real examples in the repo. Pure stdlib; run in CI.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archlint  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FAILURES = []


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def expect(name, mode, root, want_violations):
    got = bool(archlint.lint(mode, root))
    ok = got == want_violations
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: violations={got} expected={want_violations}")
    if not ok:
        FAILURES.append(name)


def build_fixtures(base):
    for layer, cls in [("controller", "OrderController"), ("service", "OrderService"),
                       ("repository", "OrderRepository"), ("domain", "Order")]:
        write(f"{base}/good/order/{layer}/{cls}.java", f"package order.{layer}; public class {cls} {{}}")
    write(f"{base}/flat/order/OrderController.java",
          "package order; import order.OrderRepository; public class OrderController { OrderRepository r; }")
    write(f"{base}/flat/order/OrderService.java", "package order; public class OrderService {}")
    write(f"{base}/flat/order/OrderRepository.java", "package order; public interface OrderRepository {}")
    write(f"{base}/cqrs_good/order/service/OrderCommandService.java",
          "package order.service; public class OrderCommandService { public OrderId place(Req r){ return id; } }")
    write(f"{base}/cqrs_good/order/service/OrderQueryService.java",
          "package order.service; public class OrderQueryService { public OrderSummary get(String id){ return s; } }")
    write(f"{base}/cqrs_bad/order/service/OrderQueryService.java",
          "package order.service; public class OrderQueryService { public void save(OrderSummary s){} }")
    write(f"{base}/cqrs_bad/order/service/OrderCommandService.java",
          "package order.service; public class OrderCommandService { public OrderResponse place(Req r){ return resp; } }")
    write(f"{base}/py_good/calc/router/command_router.py", "from calc.service.command_service import S\n")
    write(f"{base}/py_good/calc/service/command_service.py",
          "class CalculateCommandService:\n    def calculate(self, a: float, b: float) -> str:\n        return 'id'\n")
    write(f"{base}/py_good/calc/service/query_service.py",
          "class HistoryQueryService:\n    def list_recent(self, limit: int) -> list:\n        return []\n")
    write(f"{base}/py_flat/calc/router.py", "from calc.repository import R\n")
    write(f"{base}/py_flat/calc/service.py", "class S: pass\n")
    write(f"{base}/py_cqrs_bad/calc/service/query_service.py",
          "class HistoryQueryService:\n    def bad(self):\n        self.repo.save(x)\n")
    write(f"{base}/py_cqrs_bad/calc/service/command_service.py",
          "class CalculateCommandService:\n    def calculate(self) -> HistorySummary:\n        return s\n")


def main():
    print("archlint self-test:")
    with tempfile.TemporaryDirectory() as base:
        build_fixtures(base)
        expect("layered-good clean", "layered", f"{base}/good", False)
        expect("flat-package violation", "layered", f"{base}/flat", True)
        expect("cqrs-good clean", "cqrs", f"{base}/cqrs_good", False)
        expect("cqrs-bad violation", "cqrs", f"{base}/cqrs_bad", True)
        expect("py-layered-good clean", "layered", f"{base}/py_good", False)
        expect("py-flat violation", "layered", f"{base}/py_flat", True)
        expect("py-cqrs-good clean", "cqrs", f"{base}/py_good", False)
        expect("py-cqrs-bad violation", "cqrs", f"{base}/py_cqrs_bad", True)

    java_layered = f"{REPO}/examples/calculator-java-layered/src/main/java/com/oopforge/example/layered/calculator"
    if os.path.isdir(java_layered):
        expect("real calculator-java-layered clean", "layered", java_layered, False)

    calc_layered = f"{REPO}/examples/calculator-python-layered/app/calculator"
    if os.path.isdir(calc_layered):
        expect("real calculator-layered clean", "layered", calc_layered, False)

    calc_cqrs = f"{REPO}/examples/calculator-python-hexagonal-cqrs/app"
    if os.path.isdir(calc_cqrs):
        expect("real calculator-hexagonal-cqrs cqrs clean", "cqrs", calc_cqrs, False)

    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
