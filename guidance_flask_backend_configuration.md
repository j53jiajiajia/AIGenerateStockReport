## The first capstone is that while sending messages to the ec2 remote server(like http://13.229.141.204:5000/submit), it is successful to receive messages, run the program, and return messages.

This is the specific steps:
#### First Step: strat your instance aws ec2
1. Start a ec2 instance(remote server) in aws.
2. Set the Security Groups to open port 5000.

#### Second Step: deploy your code on the instance
1. Connect the ec2 remote server and upload your code to the ec2 remote server.
2. Write the app.py using flask to receive messages, run program, and return messages.
3. Execute command: python3 app.py to start the backend.

#### Thrid Step: test it using Postman app
1. choose "POST"
2. Input the ec2 remote server IP/route (e.g. http://13.229.141.204:5000/submit)
3. Choose "Body", then choose "raw", and then input the content that you want to send to the backend.
    This is an example:
    {
        "user_id": "jia",
        "service_id": "FIN-RP-GEN",
        "sent_time": "2024-03-01",
        "user_input": {"stock": "超级茅台"}
    }
4. Click "Send"

After that, if you succeed to receive the message and return the right content, you finished the first capstone.

## The second caspone is that while sending messages to the website(like http://report.bangbangday.com/submit), it is successful to receive messages, run the program, and return messages.

This is the specific steps:
#### First Step: create subdomain using Cloudflare
1. Log in to your Cloudflare account.
2. Select your domain.
3. Navigate to the "DNS" page.
4. Click on "Add record".
5. Choose the type as “A” record, enter the name as your desired subdomain (for example, "report"), and input your EC2 instance's public IPv4 address for the IPv4 address.
6. Save the record.

#### Second Step: configure an AWS EC2 instance to use HTTPS(install SSL certificate)
1. Set the Security Groups to open port 80, 443.
2. Connect to Your EC2 Instance: SSH into your EC2 instance.
3. Update Software Package List: sudo apt-get update 
4. Install Certbot and Required Packages: sudo apt-get install certbot python3-certbot-nginx to install Certbot along with the necessary Python packages.
5. Obtain and Install a Certificate: sudo certbot --nginx.

#### Third Step: use Nginx to transform ports
1. configure files under /etc/nginx/sites-available/ and /etc/nginx/sites-enabled to transform ports
2. Execute command: python3 app.py to start the backend.

#### Forth Step: test it using Postman app
1. choose "POST"
2. Input the URL (e.g. http://report.bangbangday.com/submit)
3. Choose "Body", then choose "raw", and then input the content that you want to send to the backend.
    This is an example:
    {
        "user_id": "jia",
        "service_id": "FIN-RP-GEN",
        "sent_time": "2024-03-01",
        "user_input": {"stock": "超级茅台"}
    }
4. Click "Send"

After that, if you succeed to receive the message and return the right content, you finished the second capstone.

## The third capstone: the right interaction between frontend and backend.
1. Add CORS in the app.py (e.g. cors = CORS(app, resources={r"/submit": {"origins": "https://bangbangday.com"}}))
2. Execute command: nohup python3 app.py &
3. Test it by sending messages through the frontend
