---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Use OOPforge review on this pasted diff of a FastAPI service. Do not edit any files.

```diff
--- a/app/adapter/inbound/web/loan_controller.py
+++ b/app/adapter/inbound/web/loan_controller.py
@@ -10,3 +10,17 @@ router = APIRouter(prefix="/loans")
+@router.post("/{loan_id}/return")
+def return_loan(loan_id: str, repo: LoanRepository = Depends(get_loan_repository)):
+    loan = repo.find(loan_id)
+    if loan is None:
+        return {"status": "ok"}
+    if loan.returned_at is not None:
+        raise HTTPException(status_code=500, detail="already returned")
+    loan.returned_at = datetime.now()
+    overdue_days = max(0, (datetime.now() - loan.due_at).days)
+    loan.member.penalty += overdue_days * 100
+    repo.save(loan)
+    repo.save_member(loan.member)
+    return {"status": "ok"}
```
