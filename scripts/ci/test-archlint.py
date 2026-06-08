#!/usr/bin/env python3
"""Self-test for archlint.py — proves it catches violations and clears clean code.

Builds throwaway fixtures in a temp dir, asserts expected pass/fail, then also
lints the real layered example in the repo. Pure stdlib; run in CI.
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
    open(path, "w").write(text)


def expect(name, mode, root, want_violations):
    got = bool(archlint.lint(mode, root))
    ok = got == want_violations
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: violations={got} expected={want_violations}")
    if not ok:
        FAILURES.append(name)


def build_fixtures(base):
    # layered-good
    for layer, cls in [("controller", "OrderController"), ("service", "OrderService"),
                       ("repository", "OrderRepository"), ("domain", "Order")]:
        write(f"{base}/good/order/{layer}/{cls}.java", f"package order.{layer}; public class {cls} {{}}")
    # layered-flat (one folder, mixed suffixes, controller hits repository)
    write(f"{base}/flat/order/OrderController.java",
          "package order; import order.OrderRepository; public class OrderController { OrderRepository r; }")
    write(f"{base}/flat/order/OrderService.java", "package order; public class OrderService {}")
    write(f"{base}/flat/order/OrderRepository.java", "package order; public interface OrderRepository {}")
    # cqrs-good
    write(f"{base}/cqrs_good/order/service/OrderCommandService.java",
          "package order.service; public class OrderCommandService { public OrderId place(Req r){ return id; } }")
    write(f"{base}/cqrs_good/order/service/OrderQueryService.java",
          "package order.service; public class OrderQueryService { public OrderSummary get(String id){ return s; } }")
    # cqrs-bad (query mutates, command returns read-shaped)
    write(f"{base}/cqrs_bad/order/service/OrderQueryService.java",
          "package order.service; public class OrderQueryService { public void save(OrderSummary s){} }")
    write(f"{base}/cqrs_bad/order/service/OrderCommandService.java",
          "package order.service; public class OrderCommandService { public OrderResponse place(Req r){ return resp; } }")


def main():
    print("archlint self-test:")
    with tempfile.TemporaryDirectory() as base:
        build_fixtures(base)
        expect("layered-good clean",       "layered", f"{base}/good", False)
        expect("flat-package violation",   "layered", f"{base}/flat", True)
        expect("cqrs-good clean",          "cqrs",    f"{base}/cqrs_good", False)
        expect("cqrs-bad violation",       "cqrs",    f"{base}/cqrs_bad", True)

    real = f"{REPO}/examples/order-java-layered/src/main/java/com/oopforge/example/layered/order"
    if os.path.isdir(real):
        expect("real order-java-layered clean", "layered", real, False)

    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
