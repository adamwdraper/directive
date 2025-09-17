# Impact Analysis — Reset Password Flow

## Modules/packages likely touched
- Web app: Login/Authentication UI  
- Backend: Auth service (password reset initiation, token validation)  
- Email service or provider integration  

## Contracts to update (APIs, events, schemas, migrations)
- POST `/auth/password-reset` to request reset  
- POST `/auth/password-reset/confirm` to set new password  
- Email template for reset link delivery  

## Risks
- Security: token leakage, replay attacks, enumeration of valid emails  
- Availability: email provider outages  
- Data integrity: token expiry and revocation edge cases  

## Observability needs
- Logs: reset requested, token issued, token validated, reset succeeded/failed  
- Metrics: requests count, success rate, token expiry rate, email send failures  
- Alerts: spike in failures or unusual volume  


