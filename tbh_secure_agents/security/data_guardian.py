"""
Data Leakage Prevention System

This module provides comprehensive protection against data leakage in multi-agent systems,
including PII detection, sensitive information filtering, and data sanitization.
"""

import re
import logging
from typing import List, Dict, Tuple, Optional, Set, Any, Union
import hashlib
import json

logger = logging.getLogger(__name__)

class DataGuardian:
    """
    Advanced system for preventing data leakage in multi-agent systems.
    Detects and sanitizes sensitive information in both inputs and outputs.
    """
    
    def __init__(self, security_level: str = "high", custom_patterns: Optional[Dict[str, List[str]]] = None):
        """
        Initialize the DataGuardian with the specified security level.
        
        Args:
            security_level (str): The security level to use ('standard', 'high', or 'maximum')
            custom_patterns (Optional[Dict[str, List[str]]]): Custom patterns to detect specific types of sensitive data
        """
        self.security_level = security_level
        self.custom_patterns = custom_patterns or {}
        
        # Initialize detection systems
        self._initialize_detection_patterns()
        
        # Track detected sensitive information for consistent redaction
        self.detected_sensitive_info: Dict[str, str] = {}
        
        logger.debug(f"DataGuardian initialized with security level: {security_level}")
    
    def _initialize_detection_patterns(self) -> None:
        """Initialize the pattern-based detection systems for sensitive data."""
        # PII detection patterns
        self.pii_patterns = {
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            'phone_number': [
                r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b',
                r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
            ],
            'ssn': [
                r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'
            ],
            'credit_card': [
                r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b'
            ],
            'address': [
                r'\b\d{1,5}\s+[A-Za-z0-9\s,]{5,}(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St)\.?\b',
                r'\b[A-Za-z0-9\s,]{5,}(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St)\.?\b'
            ],
            'zip_code': [
                r'\b\d{5}(?:-\d{4})?\b'
            ],
            'date_of_birth': [
                r'\b(?:0[1-9]|1[0-2])[/.-](?:0[1-9]|[12][0-9]|3[01])[/.-](?:19|20)\d\d\b',
                r'\b(?:19|20)\d\d[/.-](?:0[1-9]|1[0-2])[/.-](?:0[1-9]|[12][0-9]|3[01])\b'
            ],
            'ip_address': [
                r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
            ],
            'name': [
                r'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
                r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
            ]
        }
        
        # Add custom patterns if provided
        if self.custom_patterns:
            for key, patterns in self.custom_patterns.items():
                if key in self.pii_patterns:
                    self.pii_patterns[key].extend(patterns)
                else:
                    self.pii_patterns[key] = patterns
        
        # Credentials and secrets patterns
        self.credentials_patterns = {
            'api_key': [
                r'\b(?:api[_-]?key|apikey|access[_-]?key)[=:"\'\s]+([A-Za-z0-9]{16,})\b',
                r'\b[A-Za-z0-9]{32,}\b'
            ],
            'password': [
                r'\b(?:password|passwd|pwd)[=:"\'\s]+([A-Za-z0-9!@#$%^&*()_+]{8,})\b'
            ],
            'token': [
                r'\b(?:token|access[_-]?token|auth[_-]?token)[=:"\'\s]+([A-Za-z0-9_\-.]{10,})\b',
                r'\b(?:Bearer|bearer)\s+([A-Za-z0-9_\-.]{10,})\b'
            ],
            'aws_key': [
                r'\b(?:AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b'
            ],
            'private_key': [
                r'-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----'
            ],
            'oauth': [
                r'\b(?:ya29\.|Atza|AAAA)[A-Za-z0-9_\-.]{40,}\b'
            ]
        }
        
        # Financial information patterns
        self.financial_patterns = {
            'bank_account': [
                r'\b(?:account|acct)[=:"\'\s]+\d{8,17}\b',
                r'\b\d{8,17}\b'
            ],
            'routing_number': [
                r'\b(?:routing|ABA)[=:"\'\s]+\d{9}\b',
                r'\b\d{9}\b'
            ],
            'swift_code': [
                r'\b[A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b'
            ],
            'iban': [
                r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}(?:[A-Z0-9]{0,16})\b'
            ]
        }
        
        # Internal information patterns
        self.internal_patterns = {
            'internal_url': [
                r'\b(?:https?://)?(?:localhost|127\.0\.0\.1|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/[A-Za-z0-9\-._~:/?#[\]@!$&\'()*+,;=]*)?\b'
            ],
            'internal_path': [
                r'\b(?:/home/[A-Za-z0-9]+|/Users/[A-Za-z0-9]+|/var/www|/etc|/usr/local|C:\\Users\\[A-Za-z0-9]+|C:\\Program Files|D:\\)\b'
            ],
            'database_connection': [
                r'\b(?:jdbc|mongodb|mysql|postgresql|redis|sqlite)://[A-Za-z0-9\-._~:/?#[\]@!$&\'()*+,;=]+\b'
            ]
        }
        
        # High security level adds more patterns
        if self.security_level in ["high", "maximum"]:
            # Add more sophisticated PII detection
            self.pii_patterns['passport_number'] = [
                r'\b[A-Z]{1,2}\d{6,9}\b',
                r'\b\d{9}\b'
            ]
            self.pii_patterns['drivers_license'] = [
                r'\b[A-Z]\d{7}\b',
                r'\b[A-Z]{1,2}\d{5,7}\b'
            ]
            
            # Add more credential patterns
            self.credentials_patterns['github_token'] = [
                r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b'
            ]
            self.credentials_patterns['google_api'] = [
                r'\bAIza[0-9A-Za-z_\-]{35}\b'
            ]
            self.credentials_patterns['firebase'] = [
                r'\bAAAAAA[0-9A-Za-z_\-]{7}:[0-9A-Za-z_\-]{140}\b'
            ]
            
            # Add more internal information patterns
            self.internal_patterns['internal_hostname'] = [
                r'\b(?:[a-zA-Z0-9-]+\.local|[a-zA-Z0-9-]+\.internal|[a-zA-Z0-9-]+\.intranet|[a-zA-Z0-9-]+\.corp|[a-zA-Z0-9-]+\.lan)\b'
            ]
            self.internal_patterns['vpn_config'] = [
                r'\b(?:vpn\.config|openvpn\.conf|wireguard\.conf)\b'
            ]
        
        # Maximum security level adds even more patterns
        if self.security_level == "maximum":
            # Add extremely sensitive PII detection
            self.pii_patterns['medical_record'] = [
                r'\bMRN:?\s*\d{5,10}\b',
                r'\bPatient\s+ID:?\s*\d{5,10}\b'
            ]
            self.pii_patterns['biometric'] = [
                r'\b(?:fingerprint|retina|iris|face|voice)(?:\s+ID)?:?\s*[A-Za-z0-9]{10,}\b'
            ]
            
            # Add more credential patterns
            self.credentials_patterns['jwt'] = [
                r'\bey[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b'
            ]
            self.credentials_patterns['certificate'] = [
                r'-----BEGIN CERTIFICATE-----'
            ]
            
            # Add more internal information patterns
            self.internal_patterns['kubernetes'] = [
                r'\bkubectl\s+config\b',
                r'\bkubeconfig\b'
            ]
            self.internal_patterns['aws_config'] = [
                r'\baws\s+configure\b',
                r'\b\.aws/credentials\b'
            ]
    
    def scan_for_sensitive_data(self, text: str) -> Dict[str, List[str]]:
        """
        Scan text for sensitive data using multiple detection methods.
        
        Args:
            text (str): The text to scan
            
        Returns:
            Dict[str, List[str]]: Dictionary of detected sensitive data by category
        """
        if not text:
            return {}
        
        results: Dict[str, List[str]] = {}
        
        # Scan for PII
        pii_results = self._scan_with_patterns(text, self.pii_patterns)
        if pii_results:
            results['pii'] = pii_results
        
        # Scan for credentials
        credentials_results = self._scan_with_patterns(text, self.credentials_patterns)
        if credentials_results:
            results['credentials'] = credentials_results
        
        # Scan for financial information
        financial_results = self._scan_with_patterns(text, self.financial_patterns)
        if financial_results:
            results['financial'] = financial_results
        
        # Scan for internal information
        internal_results = self._scan_with_patterns(text, self.internal_patterns)
        if internal_results:
            results['internal'] = internal_results
        
        # Store detected sensitive information for consistent redaction
        for category, items in results.items():
            for item in items:
                # Generate a consistent replacement token
                replacement = self._generate_replacement_token(item, category)
                self.detected_sensitive_info[item] = replacement
        
        return results
    
    def _scan_with_patterns(self, text: str, pattern_dict: Dict[str, List[str]]) -> List[str]:
        """
        Scan text with a dictionary of patterns.
        
        Args:
            text (str): The text to scan
            pattern_dict (Dict[str, List[str]]): Dictionary of patterns by category
            
        Returns:
            List[str]: List of detected sensitive data
        """
        results = []
        
        for category, patterns in pattern_dict.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    # Handle both string matches and group matches
                    for match in matches:
                        if isinstance(match, tuple):
                            # If the pattern has groups, add each group
                            for group in match:
                                if group and len(group) > 3:  # Avoid very short matches
                                    results.append(group)
                        else:
                            # If the pattern doesn't have groups, add the whole match
                            if match and len(match) > 3:  # Avoid very short matches
                                results.append(match)
        
        # Remove duplicates while preserving order
        unique_results = []
        seen = set()
        for item in results:
            if item not in seen:
                seen.add(item)
                unique_results.append(item)
        
        return unique_results
    
    def _generate_replacement_token(self, sensitive_data: str, category: str) -> str:
        """
        Generate a consistent replacement token for sensitive data.
        
        Args:
            sensitive_data (str): The sensitive data to replace
            category (str): The category of the sensitive data
            
        Returns:
            str: A replacement token
        """
        # Create a hash of the sensitive data for consistency
        data_hash = hashlib.md5(sensitive_data.encode()).hexdigest()[:8]
        
        # Create a descriptive replacement based on category
        if category == 'pii':
            return f"[REDACTED_PII_{data_hash}]"
        elif category == 'credentials':
            return f"[REDACTED_CREDENTIAL_{data_hash}]"
        elif category == 'financial':
            return f"[REDACTED_FINANCIAL_{data_hash}]"
        elif category == 'internal':
            return f"[REDACTED_INTERNAL_{data_hash}]"
        else:
            return f"[REDACTED_{data_hash}]"
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by redacting sensitive information.
        
        Args:
            text (str): The text to sanitize
            
        Returns:
            str: Sanitized text with sensitive information redacted
        """
        if not text:
            return text
        
        # First scan for any new sensitive data
        self.scan_for_sensitive_data(text)
        
        # Then replace all detected sensitive data
        sanitized = text
        for sensitive_data, replacement in self.detected_sensitive_info.items():
            # Use regex to replace whole words only, avoiding partial replacements
            sanitized = re.sub(r'\b' + re.escape(sensitive_data) + r'\b', replacement, sanitized)
        
        return sanitized
    
    def sanitize_json(self, json_data: Union[Dict, List, str]) -> Union[Dict, List, str]:
        """
        Sanitize JSON data by redacting sensitive information.
        
        Args:
            json_data (Union[Dict, List, str]): The JSON data to sanitize
            
        Returns:
            Union[Dict, List, str]: Sanitized JSON data
        """
        # If input is a string, try to parse it as JSON
        if isinstance(json_data, str):
            try:
                parsed_data = json.loads(json_data)
                sanitized_data = self._sanitize_json_object(parsed_data)
                return json.dumps(sanitized_data)
            except json.JSONDecodeError:
                # If it's not valid JSON, treat it as regular text
                return self.sanitize_text(json_data)
        else:
            # If input is already a dict or list, sanitize it directly
            return self._sanitize_json_object(json_data)
    
    def _sanitize_json_object(self, obj: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
        """
        Recursively sanitize a JSON object.
        
        Args:
            obj (Union[Dict, List, Any]): The object to sanitize
            
        Returns:
            Union[Dict, List, Any]: Sanitized object
        """
        if isinstance(obj, dict):
            # For dictionaries, sanitize both keys and values
            sanitized_dict = {}
            for key, value in obj.items():
                # Sanitize the key if it's a string
                sanitized_key = self.sanitize_text(key) if isinstance(key, str) else key
                
                # Recursively sanitize the value
                sanitized_value = self._sanitize_json_object(value)
                
                sanitized_dict[sanitized_key] = sanitized_value
            return sanitized_dict
        
        elif isinstance(obj, list):
            # For lists, sanitize each item
            return [self._sanitize_json_object(item) for item in obj]
        
        elif isinstance(obj, str):
            # For strings, sanitize the text
            return self.sanitize_text(obj)
        
        else:
            # For other types (numbers, booleans, null), return as is
            return obj
    
    def is_sensitive_data_present(self, text: str) -> bool:
        """
        Check if sensitive data is present in the text.
        
        Args:
            text (str): The text to check
            
        Returns:
            bool: True if sensitive data is present, False otherwise
        """
        results = self.scan_for_sensitive_data(text)
        return bool(results)
    
    def get_sensitivity_report(self, text: str) -> Dict[str, Any]:
        """
        Generate a detailed report on the sensitivity of the text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            Dict[str, Any]: A detailed sensitivity report
        """
        results = self.scan_for_sensitive_data(text)
        
        # Calculate sensitivity metrics
        total_sensitive_items = sum(len(items) for items in results.values())
        
        # Calculate sensitivity score (0.0-1.0)
        sensitivity_score = 0.0
        if text:
            # Base score on density of sensitive items
            words = len(text.split())
            if words > 0:
                base_score = min(1.0, total_sensitive_items / (words / 10))  # 1 sensitive item per 10 words = 1.0
                
                # Adjust score based on categories (credentials and financial are more sensitive)
                category_weights = {
                    'pii': 1.0,
                    'credentials': 2.0,
                    'financial': 1.5,
                    'internal': 1.2
                }
                
                weighted_score = 0.0
                for category, items in results.items():
                    weight = category_weights.get(category, 1.0)
                    weighted_score += len(items) * weight
                
                if total_sensitive_items > 0:
                    weighted_score /= total_sensitive_items
                    sensitivity_score = base_score * weighted_score
                else:
                    sensitivity_score = 0.0
        
        # Generate report
        report = {
            'has_sensitive_data': bool(results),
            'sensitivity_score': sensitivity_score,
            'total_sensitive_items': total_sensitive_items,
            'categories': {category: len(items) for category, items in results.items()},
            'recommendations': self._generate_recommendations(results)
        }
        
        return report
    
    def _generate_recommendations(self, results: Dict[str, List[str]]) -> List[str]:
        """
        Generate recommendations based on detected sensitive data.
        
        Args:
            results (Dict[str, List[str]]): Dictionary of detected sensitive data by category
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        if not results:
            recommendations.append("No sensitive data detected. Continue with standard security practices.")
            return recommendations
        
        # General recommendation
        recommendations.append("Sensitive data detected. Consider sanitizing this content before processing or storing.")
        
        # Category-specific recommendations
        if 'pii' in results:
            recommendations.append(f"Personal Identifiable Information (PII) detected ({len(results['pii'])} items). Ensure compliance with privacy regulations like GDPR or CCPA.")
        
        if 'credentials' in results:
            recommendations.append(f"Credentials or secrets detected ({len(results['credentials'])} items). These should be immediately redacted and any exposed credentials should be rotated.")
        
        if 'financial' in results:
            recommendations.append(f"Financial information detected ({len(results['financial'])} items). Ensure compliance with financial regulations like PCI DSS.")
        
        if 'internal' in results:
            recommendations.append(f"Internal information detected ({len(results['internal'])} items). This could expose internal systems or infrastructure details.")
        
        # Add specific handling recommendations
        total_items = sum(len(items) for items in results.values())
        if total_items > 10:
            recommendations.append("High volume of sensitive data detected. Consider using a different approach that doesn't require handling this data.")
        
        if 'credentials' in results or 'financial' in results:
            recommendations.append("High-risk sensitive data detected. Implement additional security controls such as encryption and access restrictions.")
        
        return recommendations
