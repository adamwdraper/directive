# Spec Card (per PR)

**Feature name**: Reset Password Flow  
**One-line summary**: Allow users to reset their password securely via email.  

---

## Problem
Users forget their passwords and currently need admin help to regain access. This creates friction and support overhead.  

## Goal
Users can initiate and complete a password reset without admin involvement.  

## Success Criteria
- [ ] 90% of reset attempts succeed without support intervention  
- [ ] Reset process takes < 5 minutes end-to-end  

## User Story
As a returning user who forgot my password, I want to reset it myself, so that I can log back in quickly without contacting support.  

## Flow / States
- User clicks “Forgot password” link on login page  
- User enters email → system sends reset link  
- User clicks link → sets new password → redirected to login  
- Edge case: expired link → show “link expired” message and option to resend  

## UX Links
Links to designs, copy, or prototypes (e.g., Figma files, screenshots, docs).  
- Designs: <link>  
- Prototype: <link>  
- Copy/Content: <link>  

## Requirements
- Must send a secure, time-limited reset link  
- Must handle expired/invalid tokens gracefully  
- Must not expose whether an email exists in the system  
*(plain English, no tech detail)*  

## Acceptance Criteria
- Given a valid user email, when they request a reset, then an email with a reset link is delivered  
- Given an expired reset link, when clicked, then the user sees an error and can request a new one  
- Negative: Given an email not in the system, when entered, then show generic success message (no data leak)  

## Non-Goals
- Social login reset flows (Google, GitHub) are out of scope  
- Multi-factor reset is not included in this iteration  


