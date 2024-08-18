Attribution: This code is provided by Maxwell Block and requires attribution in any derivative works or distributions. Please include the original author's name, copyright notice, and a link to the original project.

# Automated Security Alerts for GuardDuty

It is important that security teams are immediately informed when critical security events occur. High-severity alerts, such as HIGH GuardDuty findings, need direct and immediate communication with a security team member. This solution was developed to enhance security monitoring within AWS by ensuring that the right people are alerted quickly, which will improve compliance and responsiveness to significant security threats.

This AWS Lambda function processes GuardDuty alerts, sending notifications via email and outbound calls for critical findings. It utilizes Amazon SNS to dispatch email alerts and Amazon Polly to synthesize speech for voice notifications. The function triggers an outbound call through Amazon Connect, ensuring prompt action on important GuardDuty findings. All key parameters, including SNS Topic ARN, S3 Bucket Name, and Amazon Connect details, are managed via environment variables for flexibility and ease of deployment.

## Initial Steps

- Verify GuardDuty is enabled in the region and account you are deploying to (this solution will work best in the account containing the GuardDuty delegated administrator)
- Setup Amazon Connect (shown below)