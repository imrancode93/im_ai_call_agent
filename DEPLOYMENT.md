# Deployment Guide

This guide provides step-by-step instructions for deploying the AI Sales Call Assistant on Render and AWS.

## Prerequisites

- GitHub account
- Render account (for Render deployment)
- AWS account (for AWS deployment)
- Docker installed locally (for testing)

## Deploying to Render

1. **Create a New Web Service**
   - Log in to Render
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository

2. **Configure the Service**
   - Name: `ai-sales-call-assistant`
   - Environment: `Docker`
   - Region: Choose closest to your users
   - Branch: `main`
   - Build Command: `docker build -t ai-sales-call-assistant .`
   - Start Command: `docker run -p 8501:8501 --env-file .env ai-sales-call-assistant`

3. **Add Environment Variables**
   - Click "Environment" tab
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_api_key_here
     DEBUG=False
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build and deployment to complete
   - Your app will be available at `https://ai-sales-call-assistant.onrender.com`

## Deploying to AWS EC2

1. **Launch EC2 Instance**
   - Log in to AWS Console
   - Go to EC2 Dashboard
   - Click "Launch Instance"
   - Choose Amazon Linux 2023
   - Select t2.micro (free tier) or larger
   - Configure security group to allow port 8501
   - Launch and download key pair

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install Docker**
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

4. **Clone Repository**
   ```bash
   git clone your-repository-url
   cd ai-sales-call-assistant
   ```

5. **Create Environment File**
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "DEBUG=False" >> .env
   ```

6. **Build and Run**
   ```bash
   docker build -t ai-sales-call-assistant .
   docker run -d -p 8501:8501 --env-file .env ai-sales-call-assistant
   ```

7. **Access Application**
   - Open `http://your-instance-ip:8501` in your browser

## Monitoring and Maintenance

### Render
- Monitor logs in Render dashboard
- Set up automatic deployments from GitHub
- Configure alerts for errors

### AWS
- Use CloudWatch for monitoring
- Set up auto-scaling if needed
- Configure security groups properly

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   - Check environment variables
   - Verify port 8501 is open
   - Check Docker logs

2. **API Key Issues**
   - Verify OPENAI_API_KEY is set correctly
   - Check API key permissions

3. **Memory Issues**
   - Increase instance size if needed
   - Monitor memory usage

## Security Considerations

1. **API Keys**
   - Never commit .env files
   - Rotate keys regularly
   - Use environment variables

2. **Network Security**
   - Use HTTPS
   - Configure firewalls
   - Limit access to necessary ports

3. **Data Security**
   - Implement user authentication
   - Encrypt sensitive data
   - Regular security audits 