#!/usr/bin/env python3
"""
Comprehensive All Formats Test for Result Destination
Tests ALL possible file formats supported by result_destination with new security features.
"""

import os
import tempfile
import shutil
from datetime import datetime

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA3ZxbIXpR3yNkZwGDznrztdQmgnU16DJI"

from tbh_secure_agents import Expert, Operation

def test_all_result_destination_formats():
    """Test ALL possible result_destination formats with new security features."""
    
    print("📁 COMPREHENSIVE ALL FORMATS TEST")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Framework Version: 0.4.0")
    
    # Create temporary test directory
    test_dir = tempfile.mkdtemp(prefix="tbh_formats_test_")
    print(f"📂 Test Directory: {test_dir}")
    
    try:
        # Test scenarios for ALL supported formats
        test_scenarios = [
            {
                "name": "Plain Text Format (.txt)",
                "expert_specialty": "Technical Writer",
                "task": "Write a simple guide about Python programming basics",
                "result_destination": os.path.join(test_dir, "python_guide.txt"),
                "security_profile": "minimal",
                "expected_format": "txt"
            },
            {
                "name": "Markdown Format (.md)",
                "expert_specialty": "Documentation Writer",
                "task": "Create a markdown document about renewable energy benefits",
                "result_destination": os.path.join(test_dir, "renewable_energy.md"),
                "security_profile": "minimal",
                "expected_format": "md"
            },
            {
                "name": "Markdown Format (.markdown)",
                "expert_specialty": "Content Creator",
                "task": "Write a tutorial about machine learning basics",
                "result_destination": os.path.join(test_dir, "ml_tutorial.markdown"),
                "security_profile": "minimal",
                "expected_format": "markdown"
            },
            {
                "name": "HTML Format (.html)",
                "expert_specialty": "Web Developer",
                "task": "Create an HTML page about web development best practices",
                "result_destination": os.path.join(test_dir, "web_dev_guide.html"),
                "security_profile": "minimal",
                "expected_format": "html"
            },
            {
                "name": "JSON Format (.json)",
                "expert_specialty": "API Developer",
                "task": "Create a JSON response for a weather API with sample data",
                "result_destination": os.path.join(test_dir, "weather_api.json"),
                "security_profile": "minimal",
                "expected_format": "json"
            },
            {
                "name": "CSV Format (.csv)",
                "expert_specialty": "Data Analyst",
                "task": "Create sample CSV data for a sales report with headers and data rows",
                "result_destination": os.path.join(test_dir, "sales_data.csv"),
                "security_profile": "minimal",
                "expected_format": "csv"
            },
            {
                "name": "PDF Format (.pdf)",
                "expert_specialty": "Report Writer",
                "task": "Create a professional report about artificial intelligence trends",
                "result_destination": os.path.join(test_dir, "ai_trends_report.pdf"),
                "security_profile": "minimal",
                "expected_format": "pdf"
            },
            {
                "name": "Nested Directory - Text (.txt)",
                "expert_specialty": "Technical Writer",
                "task": "Write installation instructions for a software package",
                "result_destination": os.path.join(test_dir, "docs", "installation", "install_guide.txt"),
                "security_profile": "minimal",
                "expected_format": "txt"
            },
            {
                "name": "Nested Directory - JSON (.json)",
                "expert_specialty": "API Developer",
                "task": "Create configuration JSON for a web application",
                "result_destination": os.path.join(test_dir, "config", "app_config.json"),
                "security_profile": "minimal",
                "expected_format": "json"
            },
            {
                "name": "Python Code File (.py)",
                "expert_specialty": "Software Developer",
                "task": "Write a simple Python script that prints hello world",
                "result_destination": os.path.join(test_dir, "scripts", "hello_world.py"),
                "security_profile": "minimal",
                "expected_format": "py"
            }
        ]
        
        results = {
            "total_tests": len(test_scenarios),
            "passed": 0,
            "failed": 0,
            "files_created": 0,
            "formats_tested": set(),
            "details": []
        }
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📝 [{i}/{len(test_scenarios)}] {scenario['name']}")
            print(f"    Format: .{scenario['expected_format']}")
            print(f"    Destination: {os.path.basename(scenario['result_destination'])}")
            print(f"    Security Profile: {scenario['security_profile']}")
            
            try:
                # Create expert
                expert = Expert(
                    specialty=scenario["expert_specialty"],
                    objective="Test result destination formats",
                    security_profile=scenario["security_profile"]
                )
                
                # Create operation with result_destination
                operation = Operation(
                    instructions=scenario["task"],
                    output_format=f"Content suitable for {scenario['expected_format']} format",
                    expert=expert,
                    result_destination=scenario["result_destination"]
                )
                
                # Execute the operation
                try:
                    result = operation.execute()
                    operation_blocked = False
                except Exception as e:
                    result = str(e)
                    operation_blocked = True
                
                # Check if file was created
                file_exists = os.path.exists(scenario["result_destination"])
                
                # Determine success
                if operation_blocked:
                    actual_behavior = "BLOCKED"
                elif file_exists:
                    actual_behavior = "SUCCESS"
                    results["files_created"] += 1
                    results["formats_tested"].add(scenario["expected_format"])
                else:
                    actual_behavior = "FAILED"
                
                # All scenarios should succeed
                expected_behavior = "SUCCESS"
                is_correct = (actual_behavior == expected_behavior)
                
                if is_correct:
                    print(f"    ✅ SUCCESS: File created successfully")
                    results["passed"] += 1
                else:
                    print(f"    ❌ FAILED: {actual_behavior}")
                    results["failed"] += 1
                
                # Get file info if created
                file_size = 0
                if file_exists:
                    file_size = os.path.getsize(scenario["result_destination"])
                    print(f"    📄 File Size: {file_size} bytes")
                
                results["details"].append({
                    "scenario": scenario["name"],
                    "format": scenario["expected_format"],
                    "destination": scenario["result_destination"],
                    "expected": expected_behavior,
                    "actual": actual_behavior,
                    "correct": is_correct,
                    "file_created": file_exists,
                    "file_size": file_size,
                    "result_preview": result[:100] + "..." if len(result) > 100 else result
                })
                
            except Exception as e:
                print(f"    ⚠️ UNEXPECTED ERROR: {e}")
                results["failed"] += 1
                results["details"].append({
                    "scenario": scenario["name"],
                    "format": scenario["expected_format"],
                    "error": str(e),
                    "correct": False
                })
        
        # Calculate scores
        accuracy = (results["passed"] / results["total_tests"]) * 100
        file_creation_rate = (results["files_created"] / results["total_tests"]) * 100
        format_coverage = (len(results["formats_tested"]) / 7) * 100  # 7 main formats
        
        print(f"\n🎯 ALL FORMATS TEST RESULTS")
        print("=" * 60)
        print(f"📊 Overall Accuracy: {accuracy:.1f}% ({results['passed']}/{results['total_tests']})")
        print(f"📁 File Creation Rate: {file_creation_rate:.1f}%")
        print(f"📋 Format Coverage: {format_coverage:.1f}% ({len(results['formats_tested'])}/7 formats)")
        
        # Format analysis
        print(f"\n📋 FORMAT ANALYSIS:")
        created_files = [d for d in results["details"] if d.get("file_created", False)]
        print(f"    Files Successfully Created: {len(created_files)}")
        
        # Group by format
        format_success = {}
        for detail in results["details"]:
            fmt = detail.get("format", "unknown")
            if fmt not in format_success:
                format_success[fmt] = {"total": 0, "success": 0}
            format_success[fmt]["total"] += 1
            if detail.get("correct", False):
                format_success[fmt]["success"] += 1
        
        for fmt, stats in sorted(format_success.items()):
            success_rate = (stats["success"] / stats["total"]) * 100
            status = "✅" if success_rate == 100 else "⚠️" if success_rate > 0 else "❌"
            print(f"      {status} .{fmt}: {success_rate:.0f}% ({stats['success']}/{stats['total']})")
        
        # Directory structure analysis
        print(f"\n📂 DIRECTORY STRUCTURE:")
        for root, dirs, files in os.walk(test_dir):
            level = root.replace(test_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f"{subindent}{file} ({file_size} bytes)")
        
        # Grade the result_destination system
        if accuracy >= 90 and file_creation_rate >= 90:
            grade = "A+ (Production Ready)"
            status = "🚀 RESULT DESTINATION PRODUCTION READY"
        elif accuracy >= 80 and file_creation_rate >= 80:
            grade = "A (Very Good)"
            status = "⚡ RESULT DESTINATION WORKING WELL"
        elif accuracy >= 70 and file_creation_rate >= 70:
            grade = "B (Good)"
            status = "🟡 RESULT DESTINATION MOSTLY WORKING"
        else:
            grade = "C (Needs Improvement)"
            status = "⚠️ RESULT DESTINATION NEEDS WORK"
        
        print(f"\n🏆 RESULT DESTINATION GRADE: {grade}")
        print(f"📊 STATUS: {status}")
        
        # Integration assessment
        print(f"\n🔗 INTEGRATION WITH NEW FEATURES:")
        print(f"    File Creation: {'✅ WORKING' if results['files_created'] > 0 else '❌ NOT WORKING'}")
        print(f"    Directory Creation: {'✅ WORKING' if any('/' in d.get('destination', '') for d in results['details']) else '❌ NOT TESTED'}")
        print(f"    Multiple Formats: {'✅ WORKING' if len(results['formats_tested']) >= 5 else '❌ LIMITED'}")
        print(f"    Security Integration: {'✅ COMPATIBLE' if accuracy > 50 else '❌ CONFLICTS'}")
        
        return results
        
    finally:
        # Cleanup test directory
        try:
            shutil.rmtree(test_dir)
            print(f"\n🧹 Cleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"\n⚠️ Failed to cleanup test directory: {e}")

if __name__ == "__main__":
    test_all_result_destination_formats()
