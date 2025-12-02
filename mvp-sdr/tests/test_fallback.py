"""
Fallback Logic Test
Ensures the CSE handles missing data gracefully without crashing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from cse.engine import CSEEngine
from cse.schema import RawContext, BrightDataOutput, PainProfilerOutput, AngleRouterOutput

def test_missing_brightdata():
    """Test fallback when BrightData agent fails"""
    print("=" * 60)
    print("TEST: Missing BrightData")
    print("=" * 60)
    
    cse = CSEEngine()
    
    # Create context with missing BrightData
    raw_context = RawContext(
        lead_name="Test Lead",
        lead_company="Test Company",
        lead_title="CTO",
        brightdata=None,  # Missing!
        pain=PainProfilerOutput(
            pain_candidates=["execution friction"],
            primary_pain="execution friction",
            raw_fragments=[],
            pattern_matches={}
        ),
        angle=AngleRouterOutput(
            candidate_angles=["Execution Velocity"],
            selected_angle="Execution Velocity",
            rejected_angles=[],
            raw_patterns={}
        )
    )
    
    try:
        result = cse.process(raw_context)
        print(f"✅ Pipeline completed without crash")
        print(f"   Score: {result['lead_score']:.0f}")
        print(f"   Confidence: {result['avg_confidence']:.2f}")
        print(f"   Fallbacks: {len(result['trace']['fallbacks_applied'])}")
        
        # Verify fallback was applied
        assert len(result['trace']['fallbacks_applied']) > 0, "No fallback applied"
        assert result['avg_confidence'] < 1.0, "Confidence should be reduced"
        
        print("✅ PASS: Fallback applied correctly")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_missing_pain():
    """Test fallback when Pain Profiler fails"""
    print("\n" + "=" * 60)
    print("TEST: Missing Pain")
    print("=" * 60)
    
    cse = CSEEngine()
    
    # Create context with missing Pain
    raw_context = RawContext(
        lead_name="Test Lead",
        lead_company="Test Company",
        lead_title="CTO",
        brightdata=BrightDataOutput(
            raw_headcount=100,
            raw_open_roles=10
        ),
        pain=None,  # Missing!
        angle=AngleRouterOutput(
            candidate_angles=["Execution Velocity"],
            selected_angle="Execution Velocity",
            rejected_angles=[],
            raw_patterns={}
        )
    )
    
    try:
        result = cse.process(raw_context)
        print(f"✅ Pipeline completed without crash")
        print(f"   Score: {result['lead_score']:.0f}")
        print(f"   Fallbacks: {len(result['trace']['fallbacks_applied'])}")
        
        # Verify fallback was applied
        assert len(result['trace']['fallbacks_applied']) > 0, "No fallback applied"
        
        print("✅ PASS: Fallback applied correctly")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_all_missing():
    """Test fallback when ALL agents fail"""
    print("\n" + "=" * 60)
    print("TEST: All Agents Missing")
    print("=" * 60)
    
    cse = CSEEngine()
    
    # Create context with everything missing
    raw_context = RawContext(
        lead_name="Test Lead",
        lead_company="Test Company",
        lead_title="CTO",
        brightdata=None,
        pain=None,
        angle=None
    )
    
    try:
        result = cse.process(raw_context)
        print(f"✅ Pipeline completed without crash")
        print(f"   Score: {result['lead_score']:.0f}")
        print(f"   Confidence: {result['avg_confidence']:.2f}")
        print(f"   Fallbacks: {len(result['trace']['fallbacks_applied'])}")
        
        # Verify multiple fallbacks were applied
        assert len(result['trace']['fallbacks_applied']) >= 3, "Not all fallbacks applied"
        assert result['avg_confidence'] < 0.5, "Confidence should be very low"
        
        print("✅ PASS: All fallbacks applied correctly")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

if __name__ == "__main__":
    test1 = test_missing_brightdata()
    test2 = test_missing_pain()
    test3 = test_all_missing()
    
    print("\n" + "=" * 60)
    print("FALLBACK TEST SUMMARY")
    print("=" * 60)
    print(f"Missing BrightData: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Missing Pain:       {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"All Missing:        {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if test1 and test2 and test3:
        print("\n✅ ALL FALLBACK TESTS PASSED")
        exit(0)
    else:
        print("\n❌ SOME FALLBACK TESTS FAILED")
        exit(1)
