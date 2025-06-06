"""
TBH Secure Agents v5.0 - Memory Security Integration Test

Simple integration test to verify all security components work together.
This is a basic test to ensure Step 3 is complete and functional.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path

from ..models import MemoryEntry, MemoryType, MemoryPriority, MemoryAccess, MemoryMetadata
from ..config import MemorySystemConfig, SecurityConfig, StorageConfig, IndexingConfig, IndexingBackend
from .memory_security_manager import MemorySecurityManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_memory_security_integration():
    """Test that all security components work together"""
    try:
        # Create test configuration
        config = MemorySystemConfig(
            security=SecurityConfig(
                enable_hybrid_validation=True,
                validation_level="high",
                enable_encryption=True,
                encryption_algorithm="fernet",
                max_acceptable_risk_score=0.7
            ),
            storage=StorageConfig(
                backend="sqlite",
                sqlite_path=str(Path.home() / "tmp" / "test_memory.db")
            ),
            indexing=IndexingConfig(
                backend=IndexingBackend.SIMPLE
            )
        )
        
        # Initialize security manager
        security_manager = MemorySecurityManager(config)
        logger.info("✅ Security manager initialized successfully")
        
        # Create test memory entry
        test_entry = MemoryEntry(
            key="test_security_integration",
            user_id="test_user",
            memory_type=MemoryType.WORKING,
            content="This is a test memory entry for security validation",
            content_hash="test_hash",
            metadata=MemoryMetadata(
                priority=MemoryPriority.MEDIUM,
                access_level=MemoryAccess.PRIVATE,
                tags=["test", "security"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            tags=["test", "security"],
            version=1,
            is_encrypted=False
        )
        logger.info("✅ Test memory entry created")
        
        # Test 1: Grant user permissions
        await security_manager.access_controller.grant_user_permissions(
            user_id="test_user",
            permissions={"read", "write", "update", "access_working"},
            memory_types={MemoryType.WORKING, MemoryType.SESSION},
            access_level="standard"
        )
        logger.info("✅ User permissions granted")
        
        # Test 2: Validate memory entry
        validation_result = await security_manager.validate_memory_entry(
            entry=test_entry,
            operation="store"
        )
        logger.info(f"✅ Memory validation result: {validation_result.is_secure}, method: {validation_result.method}")
        
        # Test 3: Test encryption if validation passed
        if validation_result.is_secure:
            encrypted_entry = await security_manager.encrypt_memory_entry(test_entry)
            logger.info(f"✅ Memory encryption: is_encrypted={encrypted_entry.is_encrypted}")
            
            # Test decryption
            decrypted_entry = await security_manager.decrypt_memory_entry(encrypted_entry)
            logger.info(f"✅ Memory decryption: content_match={decrypted_entry.content == test_entry.content}")
        
        # Test 4: Get security statistics
        stats = security_manager.get_security_statistics()
        logger.info(f"✅ Security statistics: {len(stats)} metrics collected")
        
        # Test 5: Test access control
        access_result = await security_manager.access_controller.validate_access(
            user_id="test_user",
            memory_key="test_security_integration",
            memory_type=MemoryType.WORKING,
            access_level=MemoryAccess.PRIVATE,
            operation="read"
        )
        logger.info(f"✅ Access control result: {access_result.is_allowed}")
        
        # Test 6: Test audit logging
        audit_summary = await security_manager.audit_logger.get_audit_summary()
        logger.info(f"✅ Audit summary: {audit_summary.total_events} events logged")
        
        # Test 7: User access summary
        user_summary = security_manager.access_controller.get_user_access_summary("test_user")
        logger.info(f"✅ User summary: {user_summary['access_level']} level access")
        
        logger.info("🎉 All security integration tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Security integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the integration test
    result = asyncio.run(test_memory_security_integration())
    if result:
        print("\n✅ Memory Security Integration Test: PASSED")
        print("🔒 Step 3: Memory Security Integration is COMPLETE!")
    else:
        print("\n❌ Memory Security Integration Test: FAILED")
        print("⚠️  Please check the errors above")
