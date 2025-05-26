#!/usr/bin/env python3
"""
🔥 SUPER ADAPTIVE SECURITY SYSTEM 🔥
Learns from attacks, evolves patterns, and becomes smarter over time!
"""

import re
import time
import json
import hashlib
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import threading
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class AttackPattern:
    """Represents a learned attack pattern."""
    pattern: str
    category: str
    description: str
    confidence: float
    first_seen: datetime
    last_seen: datetime
    frequency: int
    severity: str
    source: str = "adaptive_learning"

@dataclass
class AttackAttempt:
    """Represents an attack attempt."""
    text: str
    timestamp: datetime
    blocked: bool
    method: str
    pattern_matched: Optional[str] = None
    category: Optional[str] = None

class AdaptiveSecurityEngine:
    """
    🚀 SUPER ADAPTIVE SECURITY ENGINE 🚀
    - Learns from attack patterns in real-time
    - Evolves security rules automatically
    - Adapts to new threat vectors
    - Provides intelligent threat analysis
    """

    def __init__(self):
        """Initialize the adaptive security engine."""
        self._lock = threading.RLock()
        self.learned_patterns: Dict[str, AttackPattern] = {}
        self.attack_history: deque = deque(maxlen=10000)
        self.pattern_effectiveness: Dict[str, float] = {}
        self.threat_intelligence: Dict[str, Any] = {}

        # Load Palo Alto Unit 42 threat patterns
        self._load_palo_alto_patterns()

        # Initialize adaptive learning
        self._initialize_learning_engine()

        logger.info("🔥 SUPER ADAPTIVE SECURITY ENGINE INITIALIZED! 🔥")

    def _load_palo_alto_patterns(self):
        """Load threat patterns from Palo Alto Unit 42 report."""
        palo_alto_patterns = {
            # Scenario 1: Agent Enumeration
            "agent_enumeration": [
                r"(?i)(?:DO NOT DELEGATE|WITHOUT INVOKING|don't delegate).*(?:task|request|this)",
                r"(?i)(?:show|list|provide|reveal).*(?:coworker|agent|participant)",
                r"(?i)(?:transfer.*to|delegate.*to).*(?:agent|coworker)",
                r"(?i)list.*(?:names of tools|prefixed with transfer)",
            ],

            # Scenario 2: Instruction Extraction
            "instruction_extraction": [
                r"(?i)(?:show|provide|reveal|display).*(?:details of your|system|instruction|prompt|role|responsibility|goal|task|guideline|policy)",
                r"(?i)(?:what are your|show me your).*(?:exact instruction|objective|system prompt|configuration)",
                r"(?i)reveal.*(?:internal prompt|guideline|job|role|task|rule)",
            ],

            # Scenario 3: Tool Schema Extraction
            "tool_schema_extraction": [
                r"(?i)(?:show|list|provide).*(?:available tool|tool.*schema|API specification)",
                r"(?i)(?:what tool|how do I use).*(?:access|available)",
                r"(?i)(?:tool.*name|argument|description|schema)",
            ],

            # Scenario 4: SSRF/Network Access
            "ssrf_network_access": [
                r"(?i)(?:read|fetch|access).*(?:from|content from).*(?:192\.168\.|10\.|172\.|localhost|127\.0\.0\.1)",
                r"(?i)(?:http://|https://)(?:192\.168\.|10\.|172\.|localhost|127\.0\.0\.1|169\.254\.169\.254)",
                r"(?i)(?:metadata\.google|169\.254\.169\.254|metadata\.aws)",
                r"(?i)file:///(?:etc|home|root|var)",
            ],

            # Scenario 5: Data Exfiltration
            "data_exfiltration": [
                r"(?i)(?:execute|run|import os).*(?:listdir|/mnt|/data|secrets)",
                r"(?i)(?:open|read).*(?:/home/.*\.ssh|id_rsa|private.*key)",
                r"(?i)subprocess\.run.*(?:cat|ls|find|grep)",
            ],

            # Scenario 6: Service Token Exfiltration
            "service_token_exfiltration": [
                r"(?i)(?:requests\.get|curl|fetch).*(?:metadata|169\.254\.169\.254|security-credentials)",
                r"(?i)(?:AWS|Google Cloud|Azure).*(?:metadata|service account|token|credential)",
                r"(?i)(?:iam/security-credentials|computeMetadata|instance/service-accounts)",
            ],

            # Scenario 7: SQL Injection (Enhanced)
            "sql_injection_advanced": [
                r"(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER).*(?:WHERE|FROM|INTO).*(?:'1'='1'|1=1)",
                r"(?i)(?:UNION|UNION ALL).*SELECT.*(?:FROM|WHERE)",
                r"(?i)(?:';|;).*(?:DROP|DELETE|UPDATE|INSERT).*(?:TABLE|FROM|INTO)",
                r"(?i)(?:EXEC|EXECUTE).*(?:xp_cmdshell|sp_executesql)",
            ],

            # Scenario 8: BOLA (Broken Object Level Authorization)
            "bola_attacks": [
                r"(?i)(?:access|retrieve|show).*(?:user data|portfolio|account).*(?:for user|user_id|user.*=)",
                r"(?i)(?:transaction history|account detail|user profile).*(?:for|user|admin)",
                r"(?i)(?:all user|user.*=\d+|user_id.*=)",
            ],

            # Scenario 9: Indirect Prompt Injection
            "indirect_prompt_injection": [
                r"(?i)(?:IMPORTANT|URGENT|SPECIAL INSTRUCTION).*(?:continue reading|next page|more at)",
                r"(?i)(?:hidden instruction|system override|populate.*placeholder)",
                r"(?i)(?:forward.*conversation|send.*history|export.*chat)",
                r"(?i)<!--.*(?:instruction|send|forward|export).*-->",
            ],

            # Advanced Evasion Techniques
            "evasion_techniques": [
                r"(?i)(?:ignore|bypass|circumvent|override).*(?:previous|all|security|restriction)",
                r"(?i)(?:pretend|act as|impersonate|pose as).*(?:admin|root|system|another)",
                r"(?i)(?:jailbreak|break out|escape|get around).*(?:restriction|limit|rule)",
            ]
        }

        # Convert to AttackPattern objects
        for category, patterns in palo_alto_patterns.items():
            for pattern in patterns:
                pattern_id = hashlib.md5(pattern.encode()).hexdigest()[:12]
                self.learned_patterns[pattern_id] = AttackPattern(
                    pattern=pattern,
                    category=category,
                    description=f"Palo Alto Unit 42 {category.replace('_', ' ').title()} pattern",
                    confidence=0.95,  # High confidence for known patterns
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    frequency=1,
                    severity="high",
                    source="palo_alto_unit42"
                )

        logger.info(f"🎯 Loaded {len(self.learned_patterns)} Palo Alto Unit 42 threat patterns")

    def _initialize_learning_engine(self):
        """Initialize the adaptive learning engine."""
        self.learning_config = {
            "min_confidence_threshold": 0.7,
            "pattern_decay_rate": 0.95,  # Patterns lose confidence over time if not seen
            "learning_rate": 0.1,
            "max_patterns": 5000,
            "similarity_threshold": 0.8,
        }

        # Initialize threat intelligence
        self.threat_intelligence = {
            "common_attack_vectors": defaultdict(int),
            "attack_frequency_by_hour": defaultdict(int),
            "blocked_vs_allowed_ratio": {"blocked": 0, "allowed": 0},
            "top_attack_categories": defaultdict(int),
            "adaptive_patterns_created": 0,
            "pattern_effectiveness_scores": {},
        }

    def analyze_and_learn(self, text: str, context: Dict[str, Any],
                         validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        🧠 SUPER SMART ANALYSIS & LEARNING 🧠
        Analyzes text, learns from patterns, and adapts security rules.
        """
        with self._lock:
            # Record attack attempt
            attack = AttackAttempt(
                text=text,
                timestamp=datetime.now(),
                blocked=not validation_result.get("is_secure", True),
                method=validation_result.get("method", "unknown"),
                pattern_matched=validation_result.get("matched_pattern"),
                category=validation_result.get("category")
            )
            self.attack_history.append(attack)

            # Update threat intelligence
            self._update_threat_intelligence(attack)

            # Check against learned patterns
            adaptive_result = self._check_adaptive_patterns(text, context)

            # Learn new patterns if needed
            if not validation_result.get("is_secure", True):
                self._learn_from_attack(text, validation_result)

            # Combine results
            final_result = self._combine_results(validation_result, adaptive_result)

            # Update pattern effectiveness
            self._update_pattern_effectiveness(final_result)

            return final_result

    def _check_adaptive_patterns(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check text against learned adaptive patterns."""
        security_level = context.get("security_level", "standard")

        for pattern_id, pattern_obj in self.learned_patterns.items():
            try:
                # Skip low-confidence patterns for minimal security
                if security_level == "minimal" and pattern_obj.confidence < 0.9:
                    continue

                # Compile and check pattern
                compiled_pattern = re.compile(pattern_obj.pattern, re.IGNORECASE)
                match = compiled_pattern.search(text)

                if match:
                    # Update pattern statistics
                    pattern_obj.last_seen = datetime.now()
                    pattern_obj.frequency += 1

                    # Calculate dynamic confidence
                    dynamic_confidence = self._calculate_dynamic_confidence(pattern_obj)

                    if dynamic_confidence >= self.learning_config["min_confidence_threshold"]:
                        return {
                            "is_secure": False,
                            "method": "adaptive_learning",
                            "reason": f"Matched adaptive pattern: {pattern_obj.description}",
                            "matched_pattern": pattern_obj.pattern,
                            "matched_text": match.group(0),
                            "category": pattern_obj.category,
                            "confidence": dynamic_confidence,
                            "pattern_source": pattern_obj.source,
                            "fix_suggestion": self._generate_fix_suggestion(pattern_obj.category)
                        }

            except re.error as e:
                logger.warning(f"Invalid adaptive pattern {pattern_id}: {e}")
                continue

        return {"is_secure": True, "method": "adaptive_learning"}

    def _learn_from_attack(self, text: str, validation_result: Dict[str, Any]):
        """🎓 Learn new patterns from attack attempts."""
        category = validation_result.get("category", "unknown")

        # Extract potential patterns using NLP-like techniques
        potential_patterns = self._extract_patterns(text, category)

        for pattern in potential_patterns:
            pattern_id = hashlib.md5(pattern.encode()).hexdigest()[:12]

            if pattern_id not in self.learned_patterns:
                # Create new adaptive pattern
                self.learned_patterns[pattern_id] = AttackPattern(
                    pattern=pattern,
                    category=f"adaptive_{category}",
                    description=f"Learned pattern for {category} attacks",
                    confidence=0.6,  # Start with moderate confidence
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    frequency=1,
                    severity="medium",
                    source="adaptive_learning"
                )

                self.threat_intelligence["adaptive_patterns_created"] += 1
                logger.info(f"🎓 LEARNED NEW PATTERN: {pattern} (Category: {category})")
            else:
                # Strengthen existing pattern
                existing = self.learned_patterns[pattern_id]
                existing.confidence = min(0.95, existing.confidence + self.learning_config["learning_rate"])
                existing.frequency += 1
                existing.last_seen = datetime.now()

    def _extract_patterns(self, text: str, category: str) -> List[str]:
        """Extract potential attack patterns from text."""
        patterns = []

        # Common attack keywords by category
        keyword_patterns = {
            "instruction_extraction": [
                r"(?i)(?:show|reveal|display|provide).*(?:instruction|prompt|role|system)",
                r"(?i)(?:what are|tell me).*(?:your|the).*(?:objective|goal|task)",
            ],
            "system_enumeration": [
                r"(?i)(?:list|show).*(?:agent|tool|coworker|participant)",
                r"(?i)(?:available|all).*(?:tool|function|capability)",
            ],
            "data_exfiltration": [
                r"(?i)(?:read|access|open|execute).*(?:file|data|secret|credential)",
                r"(?i)(?:export|send|transmit).*(?:data|information|history)",
            ],
            "sql_injection": [
                r"(?i)(?:SELECT|INSERT|UPDATE|DELETE).*(?:WHERE|FROM|INTO)",
                r"(?i)(?:UNION|OR|AND).*(?:SELECT|1=1|'1'='1')",
            ]
        }

        # Extract patterns based on category
        if category in keyword_patterns:
            patterns.extend(keyword_patterns[category])

        # Extract dynamic patterns based on text structure
        words = text.lower().split()

        # Look for command-like structures
        if any(word in words for word in ["execute", "run", "system", "import", "open"]):
            # Create pattern for command execution
            pattern = r"(?i)(?:execute|run|system|import|open)\s+.*"
            patterns.append(pattern)

        # Look for URL patterns
        if "http" in text.lower() or "://" in text:
            pattern = r"(?i)(?:http|https|ftp|file)://[^\s]+"
            patterns.append(pattern)

        # Look for file path patterns
        if "/" in text and any(path in text.lower() for path in ["/etc", "/home", "/var", "/root"]):
            pattern = r"(?i)/(?:etc|home|var|root)/[^\s]*"
            patterns.append(pattern)

        return patterns

    def _calculate_dynamic_confidence(self, pattern_obj: AttackPattern) -> float:
        """Calculate dynamic confidence based on pattern history."""
        base_confidence = pattern_obj.confidence

        # Time decay factor
        days_since_last_seen = (datetime.now() - pattern_obj.last_seen).days
        time_decay = self.learning_config["pattern_decay_rate"] ** days_since_last_seen

        # Frequency boost
        frequency_boost = min(0.2, pattern_obj.frequency * 0.01)

        # Source reliability factor
        source_factor = 1.0 if pattern_obj.source == "palo_alto_unit42" else 0.8

        dynamic_confidence = (base_confidence * time_decay + frequency_boost) * source_factor
        return min(0.99, max(0.1, dynamic_confidence))

    def _update_threat_intelligence(self, attack: AttackAttempt):
        """Update threat intelligence with new attack data."""
        hour = attack.timestamp.hour
        self.threat_intelligence["attack_frequency_by_hour"][hour] += 1

        if attack.blocked:
            self.threat_intelligence["blocked_vs_allowed_ratio"]["blocked"] += 1
        else:
            self.threat_intelligence["blocked_vs_allowed_ratio"]["allowed"] += 1

        if attack.category:
            self.threat_intelligence["top_attack_categories"][attack.category] += 1
            self.threat_intelligence["common_attack_vectors"][attack.category] += 1

    def _combine_results(self, original_result: Dict[str, Any],
                        adaptive_result: Dict[str, Any]) -> Dict[str, Any]:
        """Combine original validation result with adaptive analysis."""
        # If either method blocks, block the request
        if not original_result.get("is_secure", True) or not adaptive_result.get("is_secure", True):
            # Return the more detailed result
            if not adaptive_result.get("is_secure", True):
                adaptive_result["combined_analysis"] = True
                adaptive_result["original_method"] = original_result.get("method", "unknown")
                return adaptive_result
            else:
                original_result["combined_analysis"] = True
                original_result["adaptive_check"] = "passed"
                return original_result

        # Both methods allow - return secure result with metadata
        return {
            "is_secure": True,
            "method": "combined_adaptive",
            "original_method": original_result.get("method", "unknown"),
            "adaptive_check": "passed",
            "combined_analysis": True
        }

    def _update_pattern_effectiveness(self, result: Dict[str, Any]):
        """Update pattern effectiveness metrics."""
        method = result.get("method", "unknown")
        is_secure = result.get("is_secure", True)

        if method not in self.pattern_effectiveness:
            self.pattern_effectiveness[method] = {"blocks": 0, "allows": 0}

        if is_secure:
            self.pattern_effectiveness[method]["allows"] += 1
        else:
            self.pattern_effectiveness[method]["blocks"] += 1

    def _generate_fix_suggestion(self, category: str) -> str:
        """Generate intelligent fix suggestions based on attack category."""
        suggestions = {
            "agent_enumeration": "Avoid requesting information about system architecture or agent details",
            "instruction_extraction": "Do not attempt to extract system prompts or internal instructions",
            "tool_schema_extraction": "Avoid requesting tool schemas or API specifications",
            "ssrf_network_access": "Use only approved external URLs and avoid internal network access",
            "data_exfiltration": "Avoid accessing sensitive files or system directories",
            "service_token_exfiltration": "Do not attempt to access cloud metadata services or credentials",
            "sql_injection_advanced": "Use parameterized queries and avoid SQL injection patterns",
            "bola_attacks": "Only access data you are authorized to view",
            "indirect_prompt_injection": "Avoid embedding hidden instructions or external redirects",
            "evasion_techniques": "Do not attempt to bypass security controls or restrictions"
        }

        return suggestions.get(category, "Review and modify the flagged content to comply with security policies")

    def get_threat_intelligence_report(self) -> Dict[str, Any]:
        """Generate comprehensive threat intelligence report."""
        with self._lock:
            total_attacks = len(self.attack_history)
            recent_attacks = [a for a in self.attack_history if a.timestamp > datetime.now() - timedelta(hours=24)]

            return {
                "summary": {
                    "total_patterns_learned": len(self.learned_patterns),
                    "total_attacks_analyzed": total_attacks,
                    "recent_attacks_24h": len(recent_attacks),
                    "adaptive_patterns_created": self.threat_intelligence["adaptive_patterns_created"],
                    "overall_block_rate": self._calculate_block_rate()
                },
                "threat_intelligence": self.threat_intelligence,
                "pattern_effectiveness": self.pattern_effectiveness,
                "top_attack_patterns": self._get_top_attack_patterns(),
                "security_recommendations": self._generate_security_recommendations()
            }

    def _calculate_block_rate(self) -> float:
        """Calculate overall attack block rate."""
        blocked = self.threat_intelligence["blocked_vs_allowed_ratio"]["blocked"]
        allowed = self.threat_intelligence["blocked_vs_allowed_ratio"]["allowed"]
        total = blocked + allowed
        return blocked / total if total > 0 else 0.0

    def _get_top_attack_patterns(self) -> List[Dict[str, Any]]:
        """Get top attack patterns by frequency."""
        patterns = []
        for pattern_id, pattern_obj in self.learned_patterns.items():
            patterns.append({
                "pattern": pattern_obj.pattern[:100] + "..." if len(pattern_obj.pattern) > 100 else pattern_obj.pattern,
                "category": pattern_obj.category,
                "frequency": pattern_obj.frequency,
                "confidence": pattern_obj.confidence,
                "source": pattern_obj.source
            })

        return sorted(patterns, key=lambda x: x["frequency"], reverse=True)[:10]

    def _generate_security_recommendations(self) -> List[str]:
        """Generate intelligent security recommendations."""
        recommendations = []

        # Analyze attack patterns
        top_categories = sorted(
            self.threat_intelligence["top_attack_categories"].items(),
            key=lambda x: x[1], reverse=True
        )[:5]

        for category, count in top_categories:
            if count > 10:  # Significant attack volume
                recommendations.append(
                    f"High volume of {category.replace('_', ' ')} attacks detected ({count} attempts). "
                    f"Consider implementing additional {category} specific protections."
                )

        # Check block rate
        block_rate = self._calculate_block_rate()
        if block_rate < 0.8:
            recommendations.append(
                f"Current block rate is {block_rate:.1%}. Consider tightening security policies."
            )

        # Pattern effectiveness analysis
        for method, stats in self.pattern_effectiveness.items():
            total = stats["blocks"] + stats["allows"]
            if total > 50:  # Sufficient data
                effectiveness = stats["blocks"] / total
                if effectiveness < 0.7:
                    recommendations.append(
                        f"Method '{method}' has low effectiveness ({effectiveness:.1%}). "
                        f"Consider reviewing or updating patterns."
                    )

        if not recommendations:
            recommendations.append("Security system is performing well. Continue monitoring for new threats.")

        return recommendations

# Global adaptive security engine
_adaptive_engine: Optional[AdaptiveSecurityEngine] = None
_engine_lock = threading.Lock()

def get_adaptive_engine() -> AdaptiveSecurityEngine:
    """Get or create the global adaptive security engine."""
    global _adaptive_engine

    if _adaptive_engine is None:
        with _engine_lock:
            if _adaptive_engine is None:
                _adaptive_engine = AdaptiveSecurityEngine()

    return _adaptive_engine

class SuperAdaptiveValidator:
    """
    🚀 SUPER ADAPTIVE VALIDATOR 🚀
    Wrapper around AdaptiveSecurityEngine to provide validator interface.
    """

    def __init__(self):
        """Initialize the super adaptive validator."""
        self.engine = get_adaptive_engine()
        logger.info("🚀 SUPER ADAPTIVE VALIDATOR INITIALIZED! 🚀")

    def validate(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate text using super adaptive learning.

        Args:
            text (str): Text to validate
            context (Dict[str, Any]): Validation context

        Returns:
            Dict[str, Any]: Validation result
        """
        try:
            # First check against learned patterns
            adaptive_result = self.engine._check_adaptive_patterns(text, context)

            # If not blocked by adaptive patterns, do basic validation
            if adaptive_result.get("is_secure", True):
                # Basic security check
                basic_result = self._basic_security_check(text, context)

                # Learn from this interaction
                self.engine.analyze_and_learn(text, context, basic_result)

                return basic_result
            else:
                # Blocked by adaptive patterns - learn from this
                self.engine.analyze_and_learn(text, context, adaptive_result)
                return adaptive_result

        except Exception as e:
            logger.error(f"Super adaptive validation error: {e}")
            return {"is_secure": False, "method": "super_adaptive", "error": str(e)}

    def _basic_security_check(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Basic security check for learning purposes."""
        security_level = context.get("security_level", "standard")

        # Basic dangerous patterns
        dangerous_patterns = [
            r"(?i)(?:rm\s+-rf|sudo\s+rm|del\s+/s)",
            r"(?i)(?:eval\s*\(|exec\s*\(|system\s*\()",
            r"(?i)(?:import\s+os|subprocess|__import__)",
            r"(?i)(?:DROP\s+TABLE|DELETE\s+FROM|UPDATE.*SET)",
            r"(?i)(?:script\s*>|javascript:|data:text/html)",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, text):
                return {
                    "is_secure": False,
                    "method": "super_adaptive_basic",
                    "reason": f"Matched dangerous pattern: {pattern}",
                    "category": "basic_security_violation"
                }

        return {"is_secure": True, "method": "super_adaptive_basic"}

def get_super_adaptive_validator() -> SuperAdaptiveValidator:
    """Get or create the global super adaptive validator."""
    return SuperAdaptiveValidator()
