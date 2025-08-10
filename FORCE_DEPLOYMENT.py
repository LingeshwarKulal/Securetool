"""
🚨 EMERGENCY DEPLOYMENT FIX 🚨

This file forces Vercel to use the LATEST commit instead of the old cached version.

PROBLEM: Vercel is stuck on commit 92b7a7d (has tkinter-dev error)
SOLUTION: This commit bc765ae+ has CLEAN requirements.txt

CLEAN DEPENDENCIES (NO DESKTOP GUI):
✅ cryptography>=3.4.8
✅ Flask>=2.3.3  
✅ Werkzeug>=2.3.7

❌ REMOVED: tkinter-dev>=0.1.0 (causing the build failure)

This deployment should succeed!
"""

DEPLOYMENT_VERSION = "FIXED_v2.0"
EMERGENCY_TRIGGER = True
