"""
Multi-Agent Security System

This module provides protection against attacks that target the interactions between agents,
including impersonation detection, trust verification, and secure message passing.
"""

import logging
import hashlib
import time
import re
from typing import Dict, List, Optional, Any, Set, Tuple
import uuid

logger = logging.getLogger(__name__)

class AgentSentinel:
    """
    Security system for protecting multi-agent interactions and communications.
    Prevents impersonation, ensures message integrity, and manages trust between agents.
    """
    
    def __init__(self, security_level: str = "high"):
        """
        Initialize the AgentSentinel with the specified security level.
        
        Args:
            security_level (str): The security level to use ('standard', 'high', or 'maximum')
        """
        self.security_level = security_level
        
        # Trust registry for tracking agent relationships
        self.trust_registry: Dict[str, Dict[str, float]] = {}
        
        # Message verification registry
        self.message_registry: Dict[str, Dict[str, Any]] = {}
        
        # Impersonation detection patterns
        self._initialize_detection_patterns()
        
        # Security incident log
        self.security_incidents: List[Dict[str, Any]] = []
        
        logger.debug(f"AgentSentinel initialized with security level: {security_level}")
    
    def _initialize_detection_patterns(self) -> None:
        """Initialize detection patterns for various security threats."""
        # Impersonation detection patterns
        self.impersonation_patterns = [
            r"(?:I am|I'm) (?:the|an?) (?:expert|specialist|authority|professional) (?:on|in|with|about)",
            r"(?:As|Being|Speaking as) (?:the|an?) (?:expert|specialist|authority|professional)",
            r"(?:I am|I'm) (?:your|the) (?:assigned|designated|selected|chosen) (?:expert|agent)",
        ]
        
        # Manipulation detection patterns
        self.manipulation_patterns = [
            r"(?:ignore|disregard|forget) (?:what|anything|everything) (?:the other|another|previous|other) (?:expert|agent|assistant) (?:said|told|advised|recommended)",
            r"(?:don't|do not) (?:trust|believe|listen to) (?:the other|another|previous|other) (?:expert|agent|assistant)",
            r"(?:I know better|I'm more knowledgeable|I'm more qualified) than (?:the other|another|previous|other) (?:expert|agent|assistant)",
        ]
        
        # High security level adds more patterns
        if self.security_level in ["high", "maximum"]:
            self.impersonation_patterns.extend([
                r"(?:I have|I've been given|I possess) (?:special|elevated|higher|additional) (?:access|privileges|permissions|authority)",
                r"(?:I can|I'm able to) (?:override|bypass|circumvent) (?:the|any|normal) (?:restrictions|limitations|constraints)",
                r"(?:I've been|I was) (?:authorized|instructed|directed|told) by (?:the system|the administrator|the owner)",
            ])
            
            self.manipulation_patterns.extend([
                r"(?:between us|just between us|this is confidential|keep this private)",
                r"(?:don't|do not) (?:share|tell|disclose|reveal|mention) this (?:with|to) (?:the other|another|any other) (?:expert|agent|assistant)",
                r"(?:let's|we should) (?:work|proceed|continue) (?:without|independently of) (?:the other|another|any other) (?:expert|agent|assistant)",
            ])
        
        # Maximum security level adds even more patterns
        if self.security_level == "maximum":
            self.impersonation_patterns.extend([
                r"(?:I represent|I speak for|I'm acting on behalf of) (?:the system|the administrator|the owner)",
                r"(?:I've been|I was) (?:upgraded|promoted|elevated) to (?:a higher|an advanced|a superior) (?:role|position|status)",
                r"(?:I'm|I am) (?:now|currently) (?:operating|functioning|working) (?:with|under) (?:special|elevated|higher|additional) (?:protocols|parameters|settings)",
            ])
            
            self.manipulation_patterns.extend([
                r"(?:there's been|there has been) (?:a change|an update|a modification) to (?:the protocol|the procedure|the process|the workflow)",
                r"(?:new|updated|revised|modified) (?:instructions|directives|guidelines|protocols) (?:have been|were) (?:issued|released|provided)",
                r"(?:I've received|I was given|I got) (?:new|updated|revised|modified) (?:instructions|directives|guidelines|protocols)",
            ])
    
    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> str:
        """
        Register an agent with the security system and generate a security token.
        
        Args:
            agent_id (str): The unique identifier for the agent
            agent_info (Dict[str, Any]): Information about the agent
            
        Returns:
            str: A security token for the agent
        """
        # Generate a unique security token
        token = self._generate_security_token(agent_id, agent_info)
        
        # Initialize trust relationships
        if agent_id not in self.trust_registry:
            self.trust_registry[agent_id] = {}
        
        logger.debug(f"Agent '{agent_id}' registered with security system")
        return token
    
    def establish_trust(self, agent_id1: str, agent_id2: str, trust_level: float = 0.5) -> bool:
        """
        Establish a trust relationship between two agents.
        
        Args:
            agent_id1 (str): The first agent's ID
            agent_id2 (str): The second agent's ID
            trust_level (float): The initial trust level (0.0-1.0)
            
        Returns:
            bool: True if trust was established, False otherwise
        """
        # Ensure both agents are registered
        if agent_id1 not in self.trust_registry or agent_id2 not in self.trust_registry:
            logger.warning(f"Cannot establish trust: One or both agents not registered")
            return False
        
        # Establish bidirectional trust
        self.trust_registry[agent_id1][agent_id2] = trust_level
        self.trust_registry[agent_id2][agent_id1] = trust_level
        
        logger.debug(f"Trust established between '{agent_id1}' and '{agent_id2}' at level {trust_level}")
        return True
    
    def update_trust(self, agent_id1: str, agent_id2: str, trust_delta: float) -> float:
        """
        Update the trust level between two agents based on interactions.
        
        Args:
            agent_id1 (str): The first agent's ID
            agent_id2 (str): The second agent's ID
            trust_delta (float): The change in trust level (-1.0 to 1.0)
            
        Returns:
            float: The new trust level
        """
        # Ensure both agents are registered and have a trust relationship
        if (agent_id1 not in self.trust_registry or 
            agent_id2 not in self.trust_registry or 
            agent_id2 not in self.trust_registry[agent_id1]):
            logger.warning(f"Cannot update trust: No existing trust relationship")
            return 0.0
        
        # Get current trust level
        current_trust = self.trust_registry[agent_id1][agent_id2]
        
        # Update trust level, keeping it within bounds
        new_trust = max(0.0, min(1.0, current_trust + trust_delta))
        
        # Update bidirectional trust
        self.trust_registry[agent_id1][agent_id2] = new_trust
        self.trust_registry[agent_id2][agent_id1] = new_trust
        
        logger.debug(f"Trust between '{agent_id1}' and '{agent_id2}' updated from {current_trust} to {new_trust}")
        return new_trust
    
    def verify_message(self, sender_id: str, recipient_id: str, message: str, 
                      security_token: str) -> Dict[str, Any]:
        """
        Verify the authenticity and integrity of a message between agents.
        
        Args:
            sender_id (str): The sender agent's ID
            recipient_id (str): The recipient agent's ID
            message (str): The message content
            security_token (str): The sender's security token
            
        Returns:
            Dict[str, Any]: Verification results including:
                - is_authentic (bool): Whether the message is authentic
                - is_trusted (bool): Whether the sender is trusted by the recipient
                - threat_level (float): 0.0-1.0 indicating the threat level
                - issues (List[str]): List of identified security issues
        """
        result = {
            'is_authentic': False,
            'is_trusted': False,
            'threat_level': 0.0,
            'issues': []
        }
        
        # Verify sender's security token
        if not self._verify_security_token(sender_id, security_token):
            result['issues'].append("Invalid security token")
            result['threat_level'] = 0.9
            self._record_security_incident("invalid_token", sender_id, recipient_id, message)
            return result
        
        # Check trust relationship
        if (sender_id in self.trust_registry and 
            recipient_id in self.trust_registry[sender_id]):
            trust_level = self.trust_registry[sender_id][recipient_id]
            result['is_trusted'] = trust_level >= 0.5  # Minimum trust threshold
            
            if not result['is_trusted']:
                result['issues'].append(f"Sender has low trust level ({trust_level:.2f})")
                result['threat_level'] = max(result['threat_level'], 0.5)
        else:
            result['issues'].append("No established trust relationship")
            result['threat_level'] = max(result['threat_level'], 0.7)
        
        # Check for impersonation attempts
        impersonation_check = self._check_impersonation(message)
        if impersonation_check['is_detected']:
            result['issues'].append(f"Potential impersonation attempt: {impersonation_check['pattern']}")
            result['threat_level'] = max(result['threat_level'], 0.8)
            self._record_security_incident("impersonation_attempt", sender_id, recipient_id, message)
        
        # Check for manipulation attempts
        manipulation_check = self._check_manipulation(message)
        if manipulation_check['is_detected']:
            result['issues'].append(f"Potential manipulation attempt: {manipulation_check['pattern']}")
            result['threat_level'] = max(result['threat_level'], 0.8)
            self._record_security_incident("manipulation_attempt", sender_id, recipient_id, message)
        
        # If no issues found, mark as authentic
        if not result['issues']:
            result['is_authentic'] = True
        
        # Register the message for future reference
        message_id = self._register_message(sender_id, recipient_id, message, result)
        
        return result
    
    def secure_message(self, sender_id: str, recipient_id: str, message: str, 
                      security_token: str) -> Dict[str, Any]:
        """
        Secure a message for transmission between agents.
        
        Args:
            sender_id (str): The sender agent's ID
            recipient_id (str): The recipient agent's ID
            message (str): The message content
            security_token (str): The sender's security token
            
        Returns:
            Dict[str, Any]: Secured message package including:
                - secured_message (str): The secured message
                - message_id (str): A unique ID for the message
                - timestamp (float): The timestamp when the message was secured
                - signature (str): A digital signature for verification
        """
        # Verify the sender's token first
        if not self._verify_security_token(sender_id, security_token):
            logger.warning(f"Cannot secure message: Invalid security token for '{sender_id}'")
            return {
                'error': 'Invalid security token',
                'secured_message': None,
                'message_id': None,
                'timestamp': time.time(),
                'signature': None
            }
        
        # Generate a unique message ID
        message_id = str(uuid.uuid4())
        
        # Create timestamp
        timestamp = time.time()
        
        # Create a digital signature
        signature_base = f"{sender_id}:{recipient_id}:{message_id}:{timestamp}:{message}"
        signature = hashlib.sha256(signature_base.encode()).hexdigest()
        
        # Register the message
        self._register_message(sender_id, recipient_id, message, {
            'is_authentic': True,
            'message_id': message_id,
            'timestamp': timestamp,
            'signature': signature
        })
        
        # Return the secured message package
        return {
            'secured_message': message,
            'message_id': message_id,
            'timestamp': timestamp,
            'signature': signature
        }
    
    def verify_secured_message(self, sender_id: str, recipient_id: str, 
                              secured_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a secured message received by an agent.
        
        Args:
            sender_id (str): The sender agent's ID
            recipient_id (str): The recipient agent's ID
            secured_message (Dict[str, Any]): The secured message package
            
        Returns:
            Dict[str, Any]: Verification results including:
                - is_authentic (bool): Whether the message is authentic
                - is_trusted (bool): Whether the sender is trusted by the recipient
                - message (str): The original message content
                - issues (List[str]): List of identified security issues
        """
        result = {
            'is_authentic': False,
            'is_trusted': False,
            'message': None,
            'issues': []
        }
        
        # Extract message components
        message = secured_message.get('secured_message')
        message_id = secured_message.get('message_id')
        timestamp = secured_message.get('timestamp')
        signature = secured_message.get('signature')
        
        # Verify all components are present
        if not all([message, message_id, timestamp, signature]):
            result['issues'].append("Incomplete secured message package")
            return result
        
        # Verify signature
        signature_base = f"{sender_id}:{recipient_id}:{message_id}:{timestamp}:{message}"
        expected_signature = hashlib.sha256(signature_base.encode()).hexdigest()
        
        if signature != expected_signature:
            result['issues'].append("Invalid message signature")
            self._record_security_incident("invalid_signature", sender_id, recipient_id, message)
            return result
        
        # Check message freshness (prevent replay attacks)
        current_time = time.time()
        message_age = current_time - timestamp
        
        # Maximum message age depends on security level
        max_age = 3600  # 1 hour for standard
        if self.security_level == "high":
            max_age = 1800  # 30 minutes
        elif self.security_level == "maximum":
            max_age = 600  # 10 minutes
        
        if message_age > max_age:
            result['issues'].append(f"Message too old ({message_age:.2f} seconds)")
            self._record_security_incident("message_replay", sender_id, recipient_id, message)
            return result
        
        # Check trust relationship
        if (sender_id in self.trust_registry and 
            recipient_id in self.trust_registry[sender_id]):
            trust_level = self.trust_registry[sender_id][recipient_id]
            result['is_trusted'] = trust_level >= 0.5  # Minimum trust threshold
            
            if not result['is_trusted']:
                result['issues'].append(f"Sender has low trust level ({trust_level:.2f})")
        else:
            result['issues'].append("No established trust relationship")
        
        # If no issues found, mark as authentic and return the message
        if not result['issues']:
            result['is_authentic'] = True
            result['message'] = message
        
        return result
    
    def _generate_security_token(self, agent_id: str, agent_info: Dict[str, Any]) -> str:
        """
        Generate a security token for an agent.
        
        Args:
            agent_id (str): The agent's ID
            agent_info (Dict[str, Any]): Information about the agent
            
        Returns:
            str: A security token
        """
        # Create a unique token based on agent ID and info
        token_base = f"{agent_id}:{str(agent_info)}:{time.time()}:{uuid.uuid4()}"
        token = hashlib.sha256(token_base.encode()).hexdigest()
        
        return token
    
    def _verify_security_token(self, agent_id: str, token: str) -> bool:
        """
        Verify an agent's security token.
        
        Args:
            agent_id (str): The agent's ID
            token (str): The security token to verify
            
        Returns:
            bool: True if the token is valid, False otherwise
        """
        # In a real implementation, this would verify the token against stored values
        # For this implementation, we'll assume all tokens are valid if they're non-empty
        # and the agent is registered
        return bool(token) and agent_id in self.trust_registry
    
    def _check_impersonation(self, message: str) -> Dict[str, Any]:
        """
        Check a message for signs of impersonation attempts.
        
        Args:
            message (str): The message to check
            
        Returns:
            Dict[str, Any]: Check results including:
                - is_detected (bool): Whether impersonation was detected
                - pattern (str): The pattern that matched, if any
        """
        result = {
            'is_detected': False,
            'pattern': None
        }
        
        # Check against impersonation patterns
        for pattern in self.impersonation_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                result['is_detected'] = True
                result['pattern'] = pattern
                break
        
        return result
    
    def _check_manipulation(self, message: str) -> Dict[str, Any]:
        """
        Check a message for signs of manipulation attempts.
        
        Args:
            message (str): The message to check
            
        Returns:
            Dict[str, Any]: Check results including:
                - is_detected (bool): Whether manipulation was detected
                - pattern (str): The pattern that matched, if any
        """
        result = {
            'is_detected': False,
            'pattern': None
        }
        
        # Check against manipulation patterns
        for pattern in self.manipulation_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                result['is_detected'] = True
                result['pattern'] = pattern
                break
        
        return result
    
    def _register_message(self, sender_id: str, recipient_id: str, message: str, 
                         metadata: Dict[str, Any]) -> str:
        """
        Register a message in the message registry.
        
        Args:
            sender_id (str): The sender agent's ID
            recipient_id (str): The recipient agent's ID
            message (str): The message content
            metadata (Dict[str, Any]): Additional metadata about the message
            
        Returns:
            str: The message ID
        """
        # Generate a message ID if not provided
        message_id = metadata.get('message_id', str(uuid.uuid4()))
        
        # Create a message record
        message_record = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'message': message,
            'timestamp': metadata.get('timestamp', time.time()),
            'is_authentic': metadata.get('is_authentic', False),
            'is_trusted': metadata.get('is_trusted', False),
            'issues': metadata.get('issues', [])
        }
        
        # Store in registry
        if message_id not in self.message_registry:
            self.message_registry[message_id] = message_record
        
        return message_id
    
    def _record_security_incident(self, incident_type: str, sender_id: str, 
                                 recipient_id: str, message: str) -> None:
        """
        Record a security incident for analysis and response.
        
        Args:
            incident_type (str): The type of security incident
            sender_id (str): The sender agent's ID
            recipient_id (str): The recipient agent's ID
            message (str): The message content
        """
        incident = {
            'type': incident_type,
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'message': message,
            'timestamp': time.time()
        }
        
        self.security_incidents.append(incident)
        logger.warning(f"Security incident recorded: {incident_type} from {sender_id} to {recipient_id}")
    
    def get_security_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive security report.
        
        Returns:
            Dict[str, Any]: A security report including incidents, trust relationships, etc.
        """
        # Count incidents by type
        incident_counts = {}
        for incident in self.security_incidents:
            incident_type = incident['type']
            incident_counts[incident_type] = incident_counts.get(incident_type, 0) + 1
        
        # Calculate average trust levels
        trust_levels = []
        for agent_id, relationships in self.trust_registry.items():
            for other_id, trust_level in relationships.items():
                trust_levels.append(trust_level)
        
        avg_trust = sum(trust_levels) / len(trust_levels) if trust_levels else 0.0
        
        # Generate report
        report = {
            'total_incidents': len(self.security_incidents),
            'incident_types': incident_counts,
            'recent_incidents': self.security_incidents[-10:] if self.security_incidents else [],
            'registered_agents': len(self.trust_registry),
            'average_trust_level': avg_trust,
            'security_level': self.security_level,
            'timestamp': time.time()
        }
        
        return report
