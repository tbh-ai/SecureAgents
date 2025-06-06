"""
TBH Secure Agents v5.0 - Memory Encryption Manager

Provides encryption and decryption services for sensitive memory content.
Integrates with the existing security infrastructure while providing
memory-specific encryption features.
"""

import base64
import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from ..models import MemoryEntry, MemoryType
from ..config import MemorySystemConfig


logger = logging.getLogger(__name__)


class EncryptionResult:
    """Result of encryption operation"""
    
    def __init__(
        self,
        success: bool,
        encrypted_data: Optional[str] = None,
        encryption_metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        self.success = success
        self.encrypted_data = encrypted_data
        self.encryption_metadata = encryption_metadata or {}
        self.error = error


class DecryptionResult:
    """Result of decryption operation"""
    
    def __init__(
        self,
        success: bool,
        decrypted_data: Optional[str] = None,
        error: Optional[str] = None
    ):
        self.success = success
        self.decrypted_data = decrypted_data
        self.error = error


class MemoryEncryptionManager:
    """
    Memory encryption manager that provides comprehensive encryption services
    for memory content with support for multiple encryption methods and
    key management.
    
    Features:
    - Symmetric encryption for bulk data (Fernet/AES)
    - Asymmetric encryption for high-security data (RSA)
    - Key derivation and management
    - Per-user encryption keys
    - Encryption metadata tracking
    - Key rotation support
    """
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        
        # Encryption settings
        self._master_key: Optional[bytes] = None
        self._user_keys: Dict[str, bytes] = {}
        self._encryption_cache: Dict[str, Fernet] = {}
        
        # Initialize master key
        self._initialize_master_key()
        
        # Key rotation tracking
        self._key_creation_times: Dict[str, datetime] = {}
        
        logger.info("MemoryEncryptionManager initialized")
    
    def _initialize_master_key(self):
        """Initialize or load the master encryption key"""
        try:
            # Try to load existing master key from environment or config
            master_key_b64 = os.environ.get('TBH_MEMORY_MASTER_KEY')
            
            if master_key_b64:
                try:
                    self._master_key = base64.urlsafe_b64decode(master_key_b64)
                    logger.info("Loaded master key from environment")
                    return
                except Exception as e:
                    logger.warning(f"Failed to load master key from environment: {e}")
            
            # Try to load from persistent file
            key_file_path = os.path.join(os.path.expanduser("~"), ".tbh_memory_key")
            if os.path.exists(key_file_path):
                try:
                    with open(key_file_path, 'r') as f:
                        master_key_b64 = f.read().strip()
                        self._master_key = base64.urlsafe_b64decode(master_key_b64)
                        logger.info("Loaded master key from persistent file")
                        return
                except Exception as e:
                    logger.warning(f"Failed to load master key from file: {e}")
            
            # Generate new master key if none exists
            self._master_key = Fernet.generate_key()
            logger.info("Generated new master key")
            
            # Save to persistent file for future use
            try:
                encoded_key = base64.urlsafe_b64encode(self._master_key).decode()
                with open(key_file_path, 'w') as f:
                    f.write(encoded_key)
                os.chmod(key_file_path, 0o600)  # Secure file permissions
                logger.info("Saved master key to persistent file")
            except Exception as e:
                logger.warning(f"Failed to save master key to file: {e}")
            
            # Optionally save to environment (for development)
            if self.config.environment == "development":
                encoded_key = base64.urlsafe_b64encode(self._master_key).decode()
                logger.info(f"Development master key: {encoded_key}")
                
        except Exception as e:
            logger.error(f"Failed to initialize master key: {e}")
            # Generate fallback key
            self._master_key = Fernet.generate_key()
    
    def _get_user_key(self, user_id: str) -> bytes:
        """Get or generate encryption key for a specific user"""
        if user_id not in self._user_keys:
            # Derive user-specific key from master key and user ID
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=user_id.encode(),
                iterations=100000,
            )
            self._user_keys[user_id] = kdf.derive(self._master_key)
            self._key_creation_times[user_id] = datetime.now()
            logger.debug(f"Generated encryption key for user: {user_id}")
        
        return self._user_keys[user_id]
    
    def _get_fernet_cipher(self, user_id: str) -> Fernet:
        """Get Fernet cipher for user"""
        if user_id not in self._encryption_cache:
            user_key = self._get_user_key(user_id)
            # Fernet requires a 32-byte URL-safe base64-encoded key
            fernet_key = base64.urlsafe_b64encode(user_key)
            self._encryption_cache[user_id] = Fernet(fernet_key)
        
        return self._encryption_cache[user_id]
    
    async def encrypt_entry(self, entry: MemoryEntry) -> MemoryEntry:
        """
        Encrypt a memory entry's content and return the encrypted entry.
        
        Args:
            entry: The memory entry to encrypt
            
        Returns:
            MemoryEntry with encrypted content
        """
        try:
            if not self.config.security.enable_encryption:
                return entry
            
            if entry.is_encrypted:
                logger.debug(f"Entry {entry.id} already encrypted")
                return entry
            
            # Determine encryption method based on memory type and security needs
            encryption_method = self._get_encryption_method(entry)
            
            if encryption_method == "symmetric":
                result = await self._encrypt_symmetric(entry.content, entry.user_id)
            elif encryption_method == "asymmetric":
                result = await self._encrypt_asymmetric(entry.content, entry.user_id)
            else:
                # No encryption needed
                return entry
            
            if not result.success:
                logger.error(f"Failed to encrypt entry {entry.id}: {result.error}")
                return entry
            
            # Create encrypted entry
            encrypted_entry = MemoryEntry(
                id=entry.id,
                user_id=entry.user_id,
                memory_type=entry.memory_type,
                key=entry.key,
                value=entry.value,  # Keep original value for reference
                content=result.encrypted_data,
                content_hash=entry.content_hash,  # Keep original hash
                tags=entry.tags,
                version=entry.version,
                is_encrypted=True,
                metadata=entry.metadata
            )
            
            # Add encryption metadata
            encrypted_entry.metadata.encryption_method = encryption_method
            encrypted_entry.metadata.encryption_timestamp = datetime.now()
            encrypted_entry.metadata.encryption_metadata = result.encryption_metadata
            
            logger.debug(f"Successfully encrypted entry {entry.id} using {encryption_method}")
            return encrypted_entry
            
        except Exception as e:
            logger.error(f"Error encrypting entry {entry.id}: {e}")
            return entry
    
    async def decrypt_entry(self, entry: MemoryEntry) -> MemoryEntry:
        """
        Decrypt a memory entry's content and return the decrypted entry.
        
        Args:
            entry: The encrypted memory entry
            
        Returns:
            MemoryEntry with decrypted content
        """
        try:
            if not entry.is_encrypted:
                logger.debug(f"Entry {entry.id} is not encrypted")
                return entry
            
            # Get encryption method from metadata
            encryption_method = getattr(entry.metadata, 'encryption_method', 'symmetric')
            
            if encryption_method == "symmetric":
                result = await self._decrypt_symmetric(entry.content, entry.user_id)
            elif encryption_method == "asymmetric":
                result = await self._decrypt_asymmetric(entry.content, entry.user_id)
            else:
                logger.error(f"Unknown encryption method: {encryption_method}")
                return entry
            
            if not result.success:
                logger.error(f"Failed to decrypt entry {entry.id}: {result.error}")
                return entry
            
            # Create decrypted entry
            decrypted_entry = MemoryEntry(
                id=entry.id,
                user_id=entry.user_id,
                memory_type=entry.memory_type,
                key=entry.key,
                value=entry.value,
                content=result.decrypted_data,
                content_hash=entry.content_hash,
                tags=entry.tags,
                version=entry.version,
                is_encrypted=False,
                metadata=entry.metadata
            )
            
            # Remove encryption metadata
            if hasattr(decrypted_entry.metadata, 'encryption_method'):
                delattr(decrypted_entry.metadata, 'encryption_method')
            if hasattr(decrypted_entry.metadata, 'encryption_timestamp'):
                delattr(decrypted_entry.metadata, 'encryption_timestamp')
            if hasattr(decrypted_entry.metadata, 'encryption_metadata'):
                delattr(decrypted_entry.metadata, 'encryption_metadata')
            
            logger.debug(f"Successfully decrypted entry {entry.id}")
            return decrypted_entry
            
        except Exception as e:
            logger.error(f"Error decrypting entry {entry.id}: {e}")
            return entry
    
    async def _encrypt_symmetric(self, content: str, user_id: str) -> EncryptionResult:
        """Encrypt content using symmetric encryption (Fernet/AES)"""
        try:
            cipher = self._get_fernet_cipher(user_id)
            content_bytes = content.encode('utf-8')
            encrypted_bytes = cipher.encrypt(content_bytes)
            encrypted_data = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
            
            return EncryptionResult(
                success=True,
                encrypted_data=encrypted_data,
                encryption_metadata={
                    "method": "symmetric",
                    "algorithm": "Fernet",
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            return EncryptionResult(
                success=False,
                error=f"Symmetric encryption failed: {str(e)}"
            )
    
    async def _decrypt_symmetric(self, encrypted_data: str, user_id: str) -> DecryptionResult:
        """Decrypt content using symmetric decryption (Fernet/AES)"""
        try:
            cipher = self._get_fernet_cipher(user_id)
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_bytes = cipher.decrypt(encrypted_bytes)
            decrypted_data = decrypted_bytes.decode('utf-8')
            
            return DecryptionResult(
                success=True,
                decrypted_data=decrypted_data
            )
        except Exception as e:
            return DecryptionResult(
                success=False,
                error=f"Symmetric decryption failed: {str(e)}"
            )
    
    async def _encrypt_asymmetric(self, content: str, user_id: str) -> EncryptionResult:
        """Encrypt content using asymmetric encryption (RSA)"""
        try:
            # For this prototype, we'll use a simplified approach
            # In production, you'd have proper key management with key pairs
            
            # Generate RSA key pair (in production, these would be managed separately)
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()
            
            # Encrypt with public key
            content_bytes = content.encode('utf-8')
            
            # RSA can only encrypt limited data, so for larger content,
            # we'd typically use hybrid encryption (RSA + AES)
            if len(content_bytes) > 190:  # RSA 2048 can encrypt ~190 bytes
                # Use hybrid encryption: generate AES key, encrypt content with AES,
                # encrypt AES key with RSA
                aes_key = Fernet.generate_key()
                fernet = Fernet(aes_key)
                
                # Encrypt content with AES
                encrypted_content = fernet.encrypt(content_bytes)
                
                # Encrypt AES key with RSA
                encrypted_aes_key = public_key.encrypt(
                    aes_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                # Combine encrypted key and content
                combined_data = {
                    "encrypted_key": base64.urlsafe_b64encode(encrypted_aes_key).decode('utf-8'),
                    "encrypted_content": base64.urlsafe_b64encode(encrypted_content).decode('utf-8'),
                    "private_key": base64.urlsafe_b64encode(
                        private_key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.NoEncryption()
                        )
                    ).decode('utf-8')
                }
                
                import json
                encrypted_data = base64.urlsafe_b64encode(
                    json.dumps(combined_data).encode('utf-8')
                ).decode('utf-8')
                
            else:
                # Direct RSA encryption for small content
                encrypted_bytes = public_key.encrypt(
                    content_bytes,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                # Store private key with encrypted data (in production, manage separately)
                combined_data = {
                    "encrypted_content": base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8'),
                    "private_key": base64.urlsafe_b64encode(
                        private_key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.NoEncryption()
                        )
                    ).decode('utf-8')
                }
                
                import json
                encrypted_data = base64.urlsafe_b64encode(
                    json.dumps(combined_data).encode('utf-8')
                ).decode('utf-8')
            
            return EncryptionResult(
                success=True,
                encrypted_data=encrypted_data,
                encryption_metadata={
                    "method": "asymmetric",
                    "algorithm": "RSA-2048",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return EncryptionResult(
                success=False,
                error=f"Asymmetric encryption failed: {str(e)}"
            )
    
    async def _decrypt_asymmetric(self, encrypted_data: str, user_id: str) -> DecryptionResult:
        """Decrypt content using asymmetric decryption (RSA)"""
        try:
            import json
            
            # Decode the combined data
            combined_data = json.loads(
                base64.urlsafe_b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
            )
            
            # Load private key
            private_key_bytes = base64.urlsafe_b64decode(
                combined_data["private_key"].encode('utf-8')
            )
            private_key = serialization.load_pem_private_key(
                private_key_bytes,
                password=None,
            )
            
            if "encrypted_key" in combined_data:
                # Hybrid decryption
                encrypted_aes_key = base64.urlsafe_b64decode(
                    combined_data["encrypted_key"].encode('utf-8')
                )
                encrypted_content = base64.urlsafe_b64decode(
                    combined_data["encrypted_content"].encode('utf-8')
                )
                
                # Decrypt AES key with RSA
                aes_key = private_key.decrypt(
                    encrypted_aes_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                # Decrypt content with AES
                fernet = Fernet(aes_key)
                decrypted_bytes = fernet.decrypt(encrypted_content)
                
            else:
                # Direct RSA decryption
                encrypted_content = base64.urlsafe_b64decode(
                    combined_data["encrypted_content"].encode('utf-8')
                )
                
                decrypted_bytes = private_key.decrypt(
                    encrypted_content,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            
            decrypted_data = decrypted_bytes.decode('utf-8')
            
            return DecryptionResult(
                success=True,
                decrypted_data=decrypted_data
            )
            
        except Exception as e:
            return DecryptionResult(
                success=False,
                error=f"Asymmetric decryption failed: {str(e)}"
            )
    
    def _get_encryption_method(self, entry: MemoryEntry) -> str:
        """Determine encryption method based on entry characteristics"""
        # High-security memory types use asymmetric encryption
        if entry.memory_type in [MemoryType.LONG_TERM, MemoryType.PATTERN]:
            if entry.metadata.priority.value in ["critical", "high"]:
                return "asymmetric"
        
        # Most memory uses symmetric encryption
        if entry.memory_type in [MemoryType.WORKING, MemoryType.PREFERENCE, MemoryType.LONG_TERM]:
            return "symmetric"
        
        # Session memory typically doesn't need encryption
        return "none"
    
    async def rotate_user_key(self, user_id: str) -> bool:
        """
        Rotate encryption key for a user.
        
        Note: This is a simplified implementation. In production,
        you'd need to re-encrypt all existing data with the new key.
        """
        try:
            # Remove old key
            if user_id in self._user_keys:
                del self._user_keys[user_id]
            if user_id in self._encryption_cache:
                del self._encryption_cache[user_id]
            if user_id in self._key_creation_times:
                del self._key_creation_times[user_id]
            
            # New key will be generated on next access
            logger.info(f"Rotated encryption key for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rotate key for user {user_id}: {e}")
            return False
    
    def should_rotate_key(self, user_id: str) -> bool:
        """Check if a user's key should be rotated based on age"""
        if user_id not in self._key_creation_times:
            return False
        
        key_age = datetime.now() - self._key_creation_times[user_id]
        rotation_interval = timedelta(days=self.config.security.encryption_key_rotation_days)
        
        return key_age > rotation_interval
    
    async def get_encryption_status(self, user_id: str) -> Dict[str, Any]:
        """Get encryption status for a user"""
        has_key = user_id in self._user_keys
        key_created = self._key_creation_times.get(user_id)
        needs_rotation = self.should_rotate_key(user_id) if has_key else False
        
        return {
            "user_id": user_id,
            "has_encryption_key": has_key,
            "key_created": key_created.isoformat() if key_created else None,
            "needs_key_rotation": needs_rotation,
            "encryption_enabled": self.config.security.enable_encryption,
            "key_age_days": (datetime.now() - key_created).days if key_created else None
        }
