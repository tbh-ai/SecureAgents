"""
Advanced Prompt Injection Defense System

This module provides sophisticated detection and prevention of prompt injection attacks
using semantic analysis, contextual understanding, and advanced pattern matching.
"""

import re
import logging
from typing import List, Dict, Tuple, Optional, Set, Any
import hashlib
from collections import Counter

logger = logging.getLogger(__name__)

class PromptDefender:
    """
    Advanced defense system against prompt injection and other prompt-based attacks.
    Uses multiple layers of detection including pattern matching, semantic analysis,
    and contextual understanding.
    """
    
    def __init__(self, security_level: str = "high"):
        """
        Initialize the PromptDefender with the specified security level.
        
        Args:
            security_level (str): The security level to use ('standard', 'high', or 'maximum')
        """
        self.security_level = security_level
        
        # Initialize detection systems
        self._initialize_detection_patterns()
        self._initialize_semantic_analyzers()
        
        # Track historical attacks for adaptive defense
        self.attack_history: List[Dict[str, Any]] = []
        self.known_safe_patterns: Set[str] = set()
        self.known_attack_patterns: Set[str] = set()
        
        logger.debug(f"PromptDefender initialized with security level: {security_level}")
    
    def _initialize_detection_patterns(self) -> None:
        """Initialize the pattern-based detection systems."""
        # Base patterns that apply to all security levels
        self.injection_patterns = [
            # Direct injection attempts
            r"ignore (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"disregard (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"forget (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"don'?t (?:follow|adhere to|listen to|obey) (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            
            # Indirect injection attempts
            r"(?:from now on|starting now|beginning now|henceforth),? (?:you are|you're|you will be|you should be)",
            r"(?:let'?s|we should) (?:pretend|imagine|assume|say) (?:that|you are|you're)",
            r"(?:I want|I need|I would like) you to (?:pretend|imagine|assume|act) (?:as if|like|that)",
            
            # Authority-based injection
            r"(?:as|being) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
            r"(?:I am|I'm) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
            
            # System prompt extraction attempts
            r"(?:what|show|tell|give|share|reveal|extract|output|display|print|repeat|recite)(?: me| us|)(?: your| the| initial| original| system| hidden| secret| internal| underlying| base| default| core| primary) (?:instructions|prompts|guidance|context|directives|commands|orders)",
            r"(?:what|how) (?:were|are) you (?:told|instructed|programmed|designed|made|created|built|trained|fine-tuned) to (?:do|perform|execute|carry out|accomplish|achieve|respond|reply|answer)",
            
            # Confusion techniques
            r"(?:ignore|disregard) (?:this|that|the following|the next|the previous) (?:part|section|text|message|instruction)",
            r"(?:this|that|the following|the next|the previous) (?:part|section|text|message|instruction) is (?:not relevant|irrelevant|to be ignored|to be disregarded)",
        ]
        
        # Additional patterns for high security level
        if self.security_level in ["high", "maximum"]:
            self.injection_patterns.extend([
                # More sophisticated injection attempts
                r"(?:new|different|updated|revised|alternative) (?:instructions|prompts|guidance|context)(?::|;| are| follow)",
                r"(?:from now on|starting now|beginning now|henceforth)(?: you| please| kindly|) (?:ignore|disregard|forget)",
                r"(?:let's|we should) (?:ignore|disregard|forget) (?:the |)(?:previous|prior|earlier|above|initial)",
                r"(?:pretend|imagine) (?:that |)(?:we are|you are|I am) (?:in|having|starting) a new conversation",
                r"(?:let's|we should) (?:start|begin) (?:over|again|fresh|anew|a new conversation)",
                
                # Sophisticated system prompt extraction
                r"(?:I need|I want|I would like|I'd like|I require|I must have|give me|show me|tell me|share|reveal) (?:access to|information about|details of|insight into) (?:your|the) (?:system|initial|original|underlying|base|core) (?:prompt|message|instruction|directive|command|order)",
                r"(?:how|what) (?:were|are) you (?:initialized|set up|configured|programmed|instructed|directed|commanded|ordered)",
                
                # Token manipulation attempts
                r"<\|(?:im_start|endoftext|system|user|assistant)\|>",
                r"<(?:system>|user>|assistant>|\/system>|\/user>|\/assistant>)",
                r"\[(?:system\]|\]system|\[user\]|\]user|\[assistant\]|\]assistant)",
            ])
        
        # Additional patterns for maximum security level
        if self.security_level == "maximum":
            self.injection_patterns.extend([
                # Extremely sophisticated attempts
                r"(?:your|these|those|the) (?:instructions|guidelines|rules|constraints|limitations) (?:are|seem|appear) (?:too|very|extremely|unnecessarily) (?:restrictive|limiting|constraining|confining)",
                r"(?:break|bypass|circumvent|get around|work around|overcome) (?:the|these|those|your|any) (?:restrictions|limitations|constraints|rules|guidelines|guardrails|boundaries)",
                r"(?:I'm|I am) (?:testing|checking|evaluating|assessing) (?:your|the) (?:security|safety|guardrails|boundaries|limitations|restrictions)",
                
                # Extremely subtle extraction attempts
                r"(?:what|which) (?:rules|guidelines|constraints|limitations|restrictions|boundaries|parameters|settings|configurations) (?:govern|control|regulate|manage|direct|guide) (?:your|the) (?:behavior|conduct|actions|activities|operations|functions)",
                r"(?:how|in what way) (?:do|does|would|should|could|might) (?:you|your|the system) (?:typically|usually|normally|generally|commonly) (?:respond|reply|answer|behave|act|operate|function|work)",
                
                # Multi-message attack detection
                r"(?:this|that|the) (?:is|was) (?:part|message|instruction) (?:\d+|one|two|three|four|five) (?:of|out of) (?:\d+|several|many|multiple)",
                r"(?:continue|proceed|go on|carry on) (?:with|from) (?:where|what|the point) (?:we|you) (?:left off|stopped|paused|ended)",
            ])
        
        # Identity manipulation patterns
        self.identity_patterns = [
            r"(?:pretend|imagine|act|behave|perform|role-play) (?:to be|as|like|that you are|you're)",
            r"(?:you are|you're) (?:now|actually|really|supposed to be|meant to be)",
            r"(?:assume|take on|adopt) (?:the|a) (?:role|persona|character|identity|personality) of",
        ]
        
        # Confusion techniques
        self.confusion_patterns = [
            r"(?:this is|this message is|this instruction is) (?:a test|a joke|not serious|just testing)",
            r"(?:ignore|disregard) (?:the|any|all) (?:security|safety) (?:checks|measures|protocols|systems)",
            r"(?:this|that|the following|the next|the previous) (?:part|section|text|message|instruction) is (?:just|only|merely) (?:a test|an example|a demonstration)",
        ]
        
        # Token manipulation patterns
        self.token_manipulation_patterns = [
            r"(?:<\|im_start\|>|<\|im_end\|>|<\|endoftext\|>)",
            r"(?:<\|system\|>|<\|user\|>|<\|assistant\|>)",
            r"(?:```\s*system|```\s*user|```\s*assistant)",
            r"(?:System:|User:|Assistant:)",
        ]
    
    def _initialize_semantic_analyzers(self) -> None:
        """Initialize the semantic analysis systems."""
        # In a real implementation, this would initialize NLP models or other semantic analysis tools
        # For this implementation, we'll use simpler techniques
        
        # Common words in prompt injections (for basic semantic analysis)
        self.injection_keywords = {
            'ignore', 'disregard', 'forget', 'pretend', 'imagine', 'role-play', 'bypass', 
            'circumvent', 'override', 'instructions', 'prompt', 'system', 'original', 
            'previous', 'prior', 'initial', 'instead', 'rather', 'new', 'different'
        }
        
        # Context transition markers (often used in injections)
        self.context_transition_markers = {
            'from now on', 'starting now', 'beginning now', 'henceforth', 'going forward',
            'let\'s start', 'let\'s begin', 'ignore everything above', 'disregard previous'
        }
    
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze a prompt for potential injection attacks using multiple detection methods.
        
        Args:
            prompt (str): The prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results including:
                - is_safe (bool): Whether the prompt is considered safe
                - threat_level (float): 0.0-1.0 indicating the threat level
                - detection_method (str): Which method detected the threat
                - matched_pattern (str, optional): The pattern that matched, if any
                - semantic_score (float): 0.0-1.0 indicating semantic analysis score
                - recommendations (List[str]): Recommendations for improving prompt safety
        """
        # Initialize result
        result = {
            'is_safe': True,
            'threat_level': 0.0,
            'detection_method': None,
            'matched_pattern': None,
            'semantic_score': 0.0,
            'recommendations': []
        }
        
        # Skip empty prompts
        if not prompt or len(prompt.strip()) < 5:
            result['recommendations'].append("Prompt is too short for meaningful analysis")
            return result
        
        # 1. Pattern-based detection (fastest, catches obvious attacks)
        pattern_result = self._pattern_based_detection(prompt)
        if not pattern_result['is_safe']:
            result.update(pattern_result)
            return result
        
        # 2. Semantic analysis (more nuanced, catches less obvious attacks)
        semantic_result = self._semantic_analysis(prompt)
        if not semantic_result['is_safe']:
            result.update(semantic_result)
            return result
        
        # 3. Contextual analysis (most sophisticated, catches subtle attacks)
        if self.security_level in ["high", "maximum"]:
            contextual_result = self._contextual_analysis(prompt)
            if not contextual_result['is_safe']:
                result.update(contextual_result)
                return result
        
        # 4. Historical pattern analysis (learns from past attacks)
        if self.security_level == "maximum" and self.attack_history:
            historical_result = self._historical_pattern_analysis(prompt)
            if not historical_result['is_safe']:
                result.update(historical_result)
                return result
        
        # If we get here, the prompt passed all checks
        result['recommendations'].append("Prompt appears safe based on all security checks")
        return result
    
    def _pattern_based_detection(self, prompt: str) -> Dict[str, Any]:
        """
        Detect injection attacks using pattern matching.
        
        Args:
            prompt (str): The prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        result = {
            'is_safe': True,
            'threat_level': 0.0,
            'detection_method': None,
            'matched_pattern': None,
            'recommendations': []
        }
        
        # Check injection patterns
        for pattern in self.injection_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                result['is_safe'] = False
                result['threat_level'] = 0.8
                result['detection_method'] = 'pattern_matching'
                result['matched_pattern'] = pattern
                result['recommendations'].append(f"Prompt contains a potential injection pattern: '{pattern}'")
                
                # Record this attack for future reference
                self._record_attack(prompt, pattern, 'pattern_matching')
                return result
        
        # Check identity manipulation patterns
        for pattern in self.identity_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                result['is_safe'] = False
                result['threat_level'] = 0.7
                result['detection_method'] = 'identity_manipulation'
                result['matched_pattern'] = pattern
                result['recommendations'].append(f"Prompt contains a potential identity manipulation pattern: '{pattern}'")
                
                # Record this attack for future reference
                self._record_attack(prompt, pattern, 'identity_manipulation')
                return result
        
        # Check confusion patterns
        for pattern in self.confusion_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                result['is_safe'] = False
                result['threat_level'] = 0.6
                result['detection_method'] = 'confusion_technique'
                result['matched_pattern'] = pattern
                result['recommendations'].append(f"Prompt contains a potential confusion technique: '{pattern}'")
                
                # Record this attack for future reference
                self._record_attack(prompt, pattern, 'confusion_technique')
                return result
        
        # Check token manipulation patterns
        for pattern in self.token_manipulation_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                result['is_safe'] = False
                result['threat_level'] = 0.9
                result['detection_method'] = 'token_manipulation'
                result['matched_pattern'] = pattern
                result['recommendations'].append(f"Prompt contains a potential token manipulation pattern: '{pattern}'")
                
                # Record this attack for future reference
                self._record_attack(prompt, pattern, 'token_manipulation')
                return result
        
        return result
    
    def _semantic_analysis(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the semantic content of the prompt for potential attacks.
        
        Args:
            prompt (str): The prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        result = {
            'is_safe': True,
            'threat_level': 0.0,
            'detection_method': None,
            'semantic_score': 0.0,
            'recommendations': []
        }
        
        # Convert to lowercase for analysis
        prompt_lower = prompt.lower()
        
        # Count injection keywords
        words = re.findall(r'\b\w+\b', prompt_lower)
        injection_word_count = sum(1 for word in words if word in self.injection_keywords)
        
        # Calculate semantic threat score based on keyword density
        if words:
            keyword_density = injection_word_count / len(words)
            semantic_score = min(1.0, keyword_density * 5)  # Scale up for sensitivity
            result['semantic_score'] = semantic_score
            
            # Detect based on threshold appropriate for security level
            threshold = 0.3 if self.security_level == "standard" else 0.2 if self.security_level == "high" else 0.1
            
            if semantic_score > threshold:
                result['is_safe'] = False
                result['threat_level'] = semantic_score
                result['detection_method'] = 'semantic_analysis'
                result['recommendations'].append(f"Prompt contains a high density of injection-related keywords ({injection_word_count} keywords, {semantic_score:.2f} score)")
                
                # Record this attack for future reference
                self._record_attack(prompt, None, 'semantic_analysis', semantic_score)
                return result
        
        # Check for context transition markers
        for marker in self.context_transition_markers:
            if marker in prompt_lower:
                result['is_safe'] = False
                result['threat_level'] = 0.6
                result['detection_method'] = 'context_transition'
                result['recommendations'].append(f"Prompt contains a context transition marker: '{marker}'")
                
                # Record this attack for future reference
                self._record_attack(prompt, marker, 'context_transition')
                return result
        
        return result
    
    def _contextual_analysis(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the prompt in context for subtle injection attempts.
        
        Args:
            prompt (str): The prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        result = {
            'is_safe': True,
            'threat_level': 0.0,
            'detection_method': None,
            'recommendations': []
        }
        
        # Split into sentences for analysis
        sentences = re.split(r'[.!?]\s+', prompt)
        
        # Check for contextual shifts within the prompt
        if len(sentences) > 2:
            # Look for abrupt topic changes
            topics = self._extract_topics(sentences)
            topic_shifts = self._detect_topic_shifts(topics)
            
            if topic_shifts:
                result['is_safe'] = False
                result['threat_level'] = 0.5
                result['detection_method'] = 'contextual_shift'
                result['recommendations'].append(f"Prompt contains abrupt topic shifts that may indicate an injection attempt")
                
                # Record this attack for future reference
                self._record_attack(prompt, None, 'contextual_shift')
                return result
        
        # Check for instruction-like language followed by different content
        instruction_patterns = [
            r"(?:please|kindly|now|next|then|after that|subsequently)(?:\s+|,\s*)(?:ignore|disregard|forget)",
            r"(?:I want|I need|I would like|I'd like)(?:\s+|,\s*)(?:you to|for you to)",
            r"(?:let's|we should|we need to|we must|we can)(?:\s+|,\s*)(?:change|switch|move|transition)",
        ]
        
        for pattern in instruction_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                # Check if there's substantial content after the instruction
                match = re.search(pattern, prompt, re.IGNORECASE)
                if match and len(prompt) - match.end() > 50:  # If there's significant content after the instruction
                    result['is_safe'] = False
                    result['threat_level'] = 0.6
                    result['detection_method'] = 'instruction_injection'
                    result['matched_pattern'] = pattern
                    result['recommendations'].append(f"Prompt contains instruction-like language followed by substantial content")
                    
                    # Record this attack for future reference
                    self._record_attack(prompt, pattern, 'instruction_injection')
                    return result
        
        return result
    
    def _historical_pattern_analysis(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the prompt against historical attack patterns.
        
        Args:
            prompt (str): The prompt to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        result = {
            'is_safe': True,
            'threat_level': 0.0,
            'detection_method': None,
            'recommendations': []
        }
        
        # Skip if no history
        if not self.attack_history:
            return result
        
        # Generate a fingerprint of the prompt
        prompt_fingerprint = self._generate_prompt_fingerprint(prompt)
        
        # Check similarity to known attacks
        for attack in self.attack_history:
            if 'fingerprint' in attack:
                similarity = self._calculate_fingerprint_similarity(prompt_fingerprint, attack['fingerprint'])
                if similarity > 0.8:  # High similarity threshold
                    result['is_safe'] = False
                    result['threat_level'] = 0.7
                    result['detection_method'] = 'historical_pattern'
                    result['recommendations'].append(f"Prompt is similar to a previously detected attack (similarity: {similarity:.2f})")
                    
                    # Record this attack for future reference
                    self._record_attack(prompt, None, 'historical_pattern', similarity=similarity)
                    return result
        
        return result
    
    def _extract_topics(self, sentences: List[str]) -> List[Set[str]]:
        """
        Extract main topics from each sentence.
        
        Args:
            sentences (List[str]): List of sentences
            
        Returns:
            List[Set[str]]: List of topic sets for each sentence
        """
        topics = []
        for sentence in sentences:
            # Simple topic extraction based on nouns and verbs
            # In a real implementation, this would use NLP techniques
            words = re.findall(r'\b\w+\b', sentence.lower())
            # Remove common stop words
            stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when', 'at', 'from', 'by', 'for'}
            filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
            topics.append(set(filtered_words))
        return topics
    
    def _detect_topic_shifts(self, topics: List[Set[str]]) -> List[int]:
        """
        Detect abrupt shifts in topics.
        
        Args:
            topics (List[Set[str]]): List of topic sets for each sentence
            
        Returns:
            List[int]: Indices where topic shifts occur
        """
        shifts = []
        for i in range(1, len(topics)):
            # Calculate Jaccard similarity between consecutive sentences
            if topics[i-1] and topics[i]:  # Ensure non-empty sets
                intersection = len(topics[i-1].intersection(topics[i]))
                union = len(topics[i-1].union(topics[i]))
                similarity = intersection / union if union > 0 else 0
                
                # Low similarity indicates a topic shift
                if similarity < 0.1:
                    shifts.append(i)
        return shifts
    
    def _generate_prompt_fingerprint(self, prompt: str) -> str:
        """
        Generate a fingerprint for a prompt to enable similarity comparison.
        
        Args:
            prompt (str): The prompt to fingerprint
            
        Returns:
            str: A fingerprint hash
        """
        # Normalize the prompt
        normalized = prompt.lower()
        # Remove punctuation and extra whitespace
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Create a bag of words representation
        words = normalized.split()
        word_counts = Counter(words)
        
        # Create a stable representation for hashing
        fingerprint_base = " ".join(f"{word}:{count}" for word, count in sorted(word_counts.items()))
        
        # Hash the representation
        return hashlib.sha256(fingerprint_base.encode()).hexdigest()
    
    def _calculate_fingerprint_similarity(self, fp1: str, fp2: str) -> float:
        """
        Calculate similarity between two fingerprints.
        
        Args:
            fp1 (str): First fingerprint
            fp2 (str): Second fingerprint
            
        Returns:
            float: Similarity score (0.0-1.0)
        """
        # In a real implementation, this would use more sophisticated techniques
        # For simplicity, we'll use a basic character-level comparison
        if not fp1 or not fp2:
            return 0.0
        
        # Convert hex fingerprints to binary
        bin1 = bin(int(fp1, 16))[2:].zfill(256)
        bin2 = bin(int(fp2, 16))[2:].zfill(256)
        
        # Calculate Hamming distance
        hamming_distance = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
        
        # Convert to similarity (0.0-1.0)
        return 1.0 - (hamming_distance / 256)
    
    def _record_attack(self, prompt: str, pattern: Optional[str], detection_method: str, 
                      semantic_score: float = 0.0, similarity: float = 0.0) -> None:
        """
        Record an attack for historical analysis and adaptive defense.
        
        Args:
            prompt (str): The prompt that was flagged
            pattern (Optional[str]): The pattern that matched, if any
            detection_method (str): The method that detected the attack
            semantic_score (float): Semantic analysis score, if applicable
            similarity (float): Similarity score, if applicable
        """
        # Generate a fingerprint for the prompt
        fingerprint = self._generate_prompt_fingerprint(prompt)
        
        # Record the attack
        attack_record = {
            'fingerprint': fingerprint,
            'detection_method': detection_method,
            'pattern': pattern,
            'semantic_score': semantic_score,
            'similarity': similarity,
            'timestamp': None  # In a real implementation, this would be a timestamp
        }
        
        # Add to history
        self.attack_history.append(attack_record)
        
        # If it's a pattern-based attack, add to known attack patterns
        if pattern:
            self.known_attack_patterns.add(pattern)
        
        # Limit history size to prevent memory issues
        if len(self.attack_history) > 1000:
            self.attack_history = self.attack_history[-1000:]
    
    def get_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Get detailed recommendations based on analysis results.
        
        Args:
            analysis_result (Dict[str, Any]): The analysis result from analyze_prompt
            
        Returns:
            List[str]: Detailed recommendations for improving prompt safety
        """
        recommendations = analysis_result.get('recommendations', [])
        
        # Add general recommendations based on detection method
        detection_method = analysis_result.get('detection_method')
        if detection_method == 'pattern_matching':
            recommendations.append("Remove or rephrase content that matches injection patterns")
            recommendations.append("Avoid using phrases that ask to ignore, disregard, or override instructions")
        elif detection_method == 'identity_manipulation':
            recommendations.append("Avoid asking the AI to pretend, imagine, or role-play being something else")
            recommendations.append("Rephrase requests to focus on the task rather than identity changes")
        elif detection_method == 'confusion_technique':
            recommendations.append("Remove ambiguous or contradictory instructions")
            recommendations.append("Make instructions clear and direct without meta-commentary")
        elif detection_method == 'token_manipulation':
            recommendations.append("Remove any special tokens or formatting that might manipulate the AI's behavior")
            recommendations.append("Use natural language rather than system-like commands or tokens")
        elif detection_method == 'semantic_analysis':
            recommendations.append("Reduce the density of injection-related keywords")
            recommendations.append("Rephrase using more neutral language that focuses on the task")
        elif detection_method == 'contextual_shift':
            recommendations.append("Maintain consistent context throughout the prompt")
            recommendations.append("Avoid abrupt topic changes that could be interpreted as separate instructions")
        elif detection_method == 'instruction_injection':
            recommendations.append("Avoid instruction-like language followed by substantial content")
            recommendations.append("Structure the prompt as a single, coherent request")
        elif detection_method == 'historical_pattern':
            recommendations.append("The prompt is similar to previously detected attacks")
            recommendations.append("Significantly rephrase the request to avoid similarity to known attacks")
        
        return recommendations
