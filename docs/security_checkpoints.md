# Security Checkpoints in TBH Secure Agents Framework

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

The `tbh_secure_agents` framework is designed with security as a core principle, implementing comprehensive security checkpoints throughout the expert and operation execution lifecycle. These checkpoints provide multiple layers of defense against various security threats.

Here's a breakdown of the eight main security checkpoints implemented in the framework:

## 1. Operation Pre-Execution Check (`Operation._pre_execution_secure()`)

*   **File:** `tbh_secure_agents/task.py`
*   **Called By:** `Operation.execute()`
*   **When:** Immediately after `Operation.execute()` is called, *before* the operation instructions or context is passed to the assigned expert's `execute_task()` method.
*   **Purpose:** To perform operation-level validation *before* the expert begins processing.
*   **Implementation:** The method now performs comprehensive security checks:
    *   Validates that operation instructions are not empty or too short
    *   Checks for excessive instruction length to prevent resource exhaustion
    *   Detects potentially dangerous operations using pattern matching
    *   Identifies operations that might lead to data exfiltration
    *   Detects operations that might lead to privilege escalation
    *   Checks for operations that might lead to denial of service
    *   Validates that the operation is appropriate for the expert's specialty
*   **Behavior:** Returns `False` if any security check fails, which aborts the operation execution before involving the expert.

## 2. Expert Prompt Check (`Expert._is_prompt_secure()`)

*   **File:** `tbh_secure_agents/agent.py`
*   **Called By:** `Expert.execute_task()`
*   **When:** After the expert has constructed the full prompt (including specialty, objective, background, context, and operation instructions) but *before* this prompt is sent to the underlying LLM (e.g., Google Gemini).
*   **Purpose:** To validate the final prompt that the LLM will process and prevent prompt injection and agent hijacking.
*   **Implementation:** The method now performs comprehensive security checks:
    *   Checks for excessive prompt length to prevent resource exhaustion
    *   Detects common hijacking patterns like "ignore previous instructions"
    *   Identifies attempts to extract system prompts
    *   Blocks attempts to perform unauthorized actions based on security profile
    *   Prevents attempts to change the expert's identity or specialty
    *   Applies additional checks based on the expert's security profile
*   **Behavior:** Returns `False` if any security check fails, which skips the LLM call and returns an error message.

## 3. Expert Output Check (`Expert._is_output_secure()`)

*   **File:** `tbh_secure_agents/agent.py`
*   **Called By:** `Expert.execute_task()`
*   **When:** Immediately *after* the LLM returns its response but *before* the expert returns this result back to the calling `Operation`.
*   **Purpose:** To validate the raw output received from the LLM and prevent data leakage and harmful content.
*   **Implementation:** The method now performs comprehensive security checks:
    *   Checks for empty output
    *   Scans for potential PII (emails, phone numbers, SSNs, credit cards, IP addresses, etc.)
    *   Detects harmful content (violence, terrorism, abuse, etc.)
    *   Identifies potential data leakage based on security profile
    *   Checks for code injection attempts in the output
    *   Enforces output length limits to prevent resource exhaustion
    *   Applies different levels of scanning based on the expert's security profile
*   **Behavior:** Returns `False` if any security check fails, which rejects the potentially insecure output and returns an error message.

## 4. Operation Post-Execution Check (`Operation._post_execution_secure()`)

*   **File:** `tbh_secure_agents/task.py`
*   **Called By:** `Operation.execute()`
*   **When:** After the expert's `execute_task()` method has successfully returned a result (which has already passed `_is_output_secure`).
*   **Purpose:** To perform final validation on the result *in the context of the specific operation* and ensure reliability and consistency.
*   **Implementation:** The method now performs comprehensive security checks:
    *   Checks if result exists
    *   Checks for excessive result length to prevent resource exhaustion
    *   Detects hallucination indicators in the output
    *   Identifies refusal or inability to complete the operation
    *   Validates format compliance with the expected `output_format`
    *   Checks for consistency with the operation instructions
    *   Scans for potentially harmful or inappropriate content
    *   Uses key term extraction to ensure relevance to the instructions
*   **Behavior:** Returns `False` if any security check fails, which logs a warning and may affect how the result is handled.

## 5. Squad Security Validation (`Squad._validate_squad_security()`)

*   **File:** `tbh_secure_agents/crew.py`
*   **Called By:** `Squad.deploy()`
*   **When:** At the beginning of squad deployment, before any operations are executed.
*   **Purpose:** To validate the entire squad configuration and prevent multi-agent exploitation.
*   **Implementation:** The method performs comprehensive security checks:
    *   Checks if there are any experts and operations
    *   Validates expert security profiles
    *   Checks for potential circular dependencies or infinite loops
    *   Ensures expert-operation compatibility
    *   Detects duplicate operations (potential redundancy attack)
    *   Prevents excessive resource usage
    *   Validates the process type
*   **Behavior:** Returns `False` if any security check fails, which aborts the squad deployment.

## 6. Operation Security Validation (`Squad._validate_operation_security()`)

*   **File:** `tbh_secure_agents/crew.py`
*   **Called By:** `Squad.deploy()`
*   **When:** Before each operation is assigned and executed.
*   **Purpose:** To validate individual operations and prevent dangerous operations.
*   **Implementation:** The method performs security checks:
    *   Validates that operation instructions are not empty or too short
    *   Checks for excessive instruction length
    *   Detects potentially dangerous operations
    *   Identifies data exfiltration attempts
*   **Behavior:** Returns `False` if any security check fails, which skips the operation or aborts the squad deployment in sequential mode.

## 7. Context Passing Security (`Squad._is_safe_for_context_passing()`)

*   **File:** `tbh_secure_agents/crew.py`
*   **Called By:** `Squad.deploy()`
*   **When:** Before context is passed from one operation to another in sequential mode.
*   **Purpose:** To validate context before passing it between operations and prevent context-based attacks.
*   **Implementation:** The method performs security checks:
    *   Checks for excessive length
    *   Scans for potentially harmful content
    *   Detects potential prompt injection attempts in the previous result
*   **Behavior:** Returns `False` if any security check fails, which blocks the context passing.

## 8. Final Result Audit (`Squad._audit_squad_results()`)

*   **File:** `tbh_secure_agents/crew.py`
*   **Called By:** `Squad.deploy()`
*   **When:** After all operations have been executed, before returning the final result.
*   **Purpose:** To perform a final security audit on the squad execution results.
*   **Implementation:** The method performs security checks:
    *   Checks for empty output
    *   Checks for excessive output length
    *   Analyzes execution metrics for anomalies
    *   Checks for operations that took too long
    *   Identifies failed operations
    *   Scans for potentially harmful content in the final output
*   **Behavior:** Returns `False` if any security check fails, which may affect how the final result is handled.

## Security Checkpoint Flow

The security checkpoints are executed in the following order during a typical operation:

1. **Squad Security Validation** (`_validate_squad_security`) - Before any operations are executed
2. **Operation Security Validation** (`_validate_operation_security`) - Before each operation is assigned
3. **Context Passing Security** (`_is_safe_for_context_passing`) - Before context is passed to an operation
4. **Pre-Execution Security Check** (`_pre_execution_secure`) - Before an operation is executed
5. **Pre-Prompt Security Check** (`_is_prompt_secure`) - Before a prompt is sent to the LLM
6. **Post-Output Security Check** (`_is_output_secure`) - After receiving output from the LLM
7. **Post-Execution Security Check** (`_post_execution_secure`) - After an operation is executed
8. **Final Result Audit** (`_audit_squad_results`) - After all operations are completed

This multi-layered approach provides defense in depth, ensuring that security issues are caught at multiple points in the execution flow.
