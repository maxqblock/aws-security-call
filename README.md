Attribution: This code is provided by Maxwell Block and requires attribution in any derivative works or distributions. Please include the original author's name, copyright notice, and a link to the original project.

# Automated Security Alerts for GuardDuty

It is important that security teams are immediately informed when critical security events occur. High-severity alerts, such as HIGH GuardDuty findings, need direct and immediate communication with a security team member. This solution was developed to enhance security monitoring within AWS by ensuring that the right people are alerted quickly, which will improve compliance and responsiveness to significant security threats.

This AWS Lambda function processes GuardDuty alerts, sending notifications via email and outbound calls for critical findings. It utilizes Amazon SNS to dispatch email alerts and Amazon Connect to trigger outbound calls, ensuring prompt action on important GuardDuty findings. This solution can be deployed to any AWS environment through the YML file provided. PLEASE NOTE: This solution will only work in regions that Amazon Connect and other AWS services included are available in. Do not forget GuardDuty is a regional service.

## Prerequsities

### 1. Enable GuardDuty

Verify that GuardDuty is enabled in the region this solution will be deployed to. 

### 2. Enable Amazon Connect

While most of this solution is deployed through infrastructure as code, Amazon Connect needs to be enabled manually. Setup an Amazon Connect instance, contact flow with outbound access, and associate a phone number with this flow. Take note of the Connect instance ID, contact flow ID, and phone number as they are needed when deploying the IAC. These are parameters in the CloudFormation YAML template provided.