# Sample Output — Design: Place Order

This is an example of the kind of output an agent should produce after running OOPforge design for a place-order use case.

## Use case

Place an order for a customer using product IDs and quantities.

## Input command

```text
PlaceOrderCommand
- customerId
- lines: productId, quantity
```

## Application service

```text
PlaceOrderUseCase
- loads product price data through ProductCatalogPort
- creates an Order aggregate
- calls Order.place()
- saves through OrderRepositoryPort
- publishes OrderPlaced
```

## Ports

- `OrderRepositoryPort`
- `ProductCatalogPort`
- `DomainEventPublisherPort`

## Aggregate behavior

```text
Order.place(customerId, lines)
```

Rules:

- Reject empty order lines.
- Reject non-positive quantities.
- Calculate total from order lines.
- Mark status as placed.
- Record `OrderPlaced`.

## Tests to write first

- Place order with valid lines.
- Reject empty order.
- Reject zero or negative quantity.
- Published event contains order ID and customer ID.
- Application service saves through the repository port.
