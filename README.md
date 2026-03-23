# Auto Scaling EC2 using AWS Lambda

##  Overview

This project implements an automated scaling solution using AWS Lambda, CloudWatch, EC2, and SNS.

##  Technologies Used

* AWS Lambda
* EC2
* CloudWatch
* SNS
* Boto3 (Python)

##  Features

* Automatically scales EC2 instances based on CPU load
* Sends alerts via SNS
* Runs every 5 minutes using EventBridge

##  Architecture

CloudWatch → Lambda → EC2 → SNS

##  Setup Steps

1. Create EC2 + Load Balancer
2. Setup SNS topic
3. Create IAM Role
4. Deploy Lambda function
5. Configure EventBridge

##  Screenshots

(Add here)

## 📈 Outcome

* Reduced manual scaling effort
* Improved system availability
