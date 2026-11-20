#!/usr/bin/env python3
"""Self-test for archlint.py using isolated passing and failing fixtures."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archlint  # noqa: E402

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


def build_kotlin_layered_fixtures(base):
    for layer, cls in [("controller", "OrderController"), ("service", "OrderService"),
                       ("repository", "OrderRepository"), ("domain", "Order")]:
        write(f"{base}/kt_good/order/{layer}/{cls}.kt", f"package order.{layer}\n\nclass {cls}\n")
    write(f"{base}/kt_flat/order/OrderController.kt",
          "package order\n\nclass OrderController(private val repository: OrderRepository)\n")
    write(f"{base}/kt_flat/order/OrderService.kt", "package order\n\nclass OrderService\n")
    write(f"{base}/kt_flat/order/OrderRepository.kt", "package order\n\ninterface OrderRepository\n")
    write(f"{base}/kt_controller_repo/order/controller/OrderController.kt",
          "package order.controller\n\nclass OrderController(private val orders: Repository<Order, Long>)\n")


def build_kotlin_cqrs_fixtures(base):
    write(f"{base}/kt_cqrs_good/order/service/OrderCommandService.kt",
          "class OrderCommandService {\n    fun place(r: Req): OrderId {\n        return id\n    }\n\n"
          "    private fun helper() = 1\n}\n")
    write(f"{base}/kt_cqrs_good/order/service/OrderQueryService.kt",
          "class OrderQueryService {\n    fun get(id: String): OrderSummary = repo.find(id)\n}\n")
    write(f"{base}/kt_cqrs_bad_query/order/service/OrderQueryService.kt",
          "class OrderQueryService {\n    fun get(s: OrderSummary) {\n        repo.save(s)\n    }\n}\n")
    write(f"{base}/kt_cqrs_bad_command/order/service/OrderCommandService.kt",
          "class OrderCommandService {\n    fun place(r: Req): List<OrderSummary> {\n        return s\n    }\n}\n")
    write(f"{base}/kt_cqrs_implicit/order/service/OrderCommandService.kt",
          "class OrderCommandService {\n    fun place(r: Req) = repo.next()\n}\n")


def build_mixed_fixtures(base):
    for layer, cls in [("controller", "OrderController"), ("service", "OrderService")]:
        write(f"{base}/mixed_good/order/{layer}/{cls}.java", f"package order.{layer}; public class {cls} {{}}")
        write(f"{base}/mixed_good/billing/{layer}/Bill{cls[5:]}.kt", f"package billing.{layer}\n\nclass Bill{cls[5:]}\n")
    write(f"{base}/mixed_bad/order/controller/OrderController.java",
          "package order.controller; public class OrderController {}")
    write(f"{base}/mixed_bad/billing/BillController.kt", "package billing\n\nclass BillController\n")
    write(f"{base}/mixed_bad/billing/BillService.kt", "package billing\n\nclass BillService\n")


CASES = [
    ("layered-good clean", "layered", "good", False),
    ("flat-package violation", "layered", "flat", True),
    ("cqrs-good clean", "cqrs", "cqrs_good", False),
    ("cqrs-bad violation", "cqrs", "cqrs_bad", True),
    ("py-layered-good clean", "layered", "py_good", False),
    ("py-flat violation", "layered", "py_flat", True),
    ("py-cqrs-good clean", "cqrs", "py_good", False),
    ("py-cqrs-bad violation", "cqrs", "py_cqrs_bad", True),
    ("kt-layered-good clean", "layered", "kt_good", False),
    ("kt-flat violation", "layered", "kt_flat", True),
    ("kt-controller-repository violation", "layered", "kt_controller_repo", True),
    ("kt-cqrs-good clean", "cqrs", "kt_cqrs_good", False),
    ("kt-cqrs-query-mutation violation", "cqrs", "kt_cqrs_bad_query", True),
    ("kt-cqrs-command-returns-read violation", "cqrs", "kt_cqrs_bad_command", True),
    ("kt-cqrs-implicit-return violation", "cqrs", "kt_cqrs_implicit", True),
    ("mixed-java-kotlin-good clean", "layered", "mixed_good", False),
    ("mixed-java-kotlin-flat violation", "layered", "mixed_bad", True),
]


def main():
    print("archlint self-test:")
    with tempfile.TemporaryDirectory() as base:
        for build in (build_fixtures, build_kotlin_layered_fixtures,
                      build_kotlin_cqrs_fixtures, build_mixed_fixtures):
            build(base)
        for name, mode, folder, want in CASES:
            expect(name, mode, f"{base}/{folder}", want)

    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
