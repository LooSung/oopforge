// The domain's counterpart of Java's IllegalArgumentException: the web adapter
// maps it, and only it, to 422 calculation_rejected.
export class DomainRuleViolation extends Error {
  override readonly name = 'DomainRuleViolation';
}
