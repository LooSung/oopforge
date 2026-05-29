# Sample Output — Discovery: Order Domain

This is an example of the kind of output an agent should produce after running OOPforge discovery for an order domain.

## Business goal

Support order placement while protecting pricing, inventory, payment, and fulfillment invariants.

## Candidate bounded contexts

- Ordering
- Payment
- Inventory
- Shipping
- Pricing

## Core domain concepts

- Order
- OrderLine
- ProductId
- CustomerId
- Money
- OrderPlaced

## Candidate aggregate

### Order

The `Order` aggregate owns order lines, order status, totals, and placement rules.

It should not directly own payment, inventory, or shipping objects. Those contexts should refer to the order by ID.

## Key invariants

- An order cannot be placed without at least one order line.
- An order total must equal the sum of order line subtotals.
- A placed order cannot be modified directly.
- Payment must reference an order by ID, not by object reference.
- Inventory reservation must be explicit and observable.

## Domain events

- `OrderPlaced`
- `OrderCancelled`
- `OrderPaymentRequested`

## Open questions

- Can customers cancel after payment authorization?
- Is inventory reserved before or after payment?
- Are discounts owned by Ordering or Pricing?
- Does order placement require synchronous payment confirmation?
