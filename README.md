# How to fake AWS locally with LocalStack

# Motivation:
I prefer to keep my local development environment as close as possible to how it's going to work in production. I can't think of a better away to achieve that than putting a bunch of S3 servers inside my computer.

# What will be covered:
This tutorial will cover setting up Localstack S3 and a simple python script to upload file to it. Localstack allows you to emulate a number of AWS services on your computer, but we're just going to use S3 in this example. Also, Localstack isn't specific to Python - so even if you aren't working in Python, a good portion of this tutorial will still be relevant. This also covers a little bit about Docker.

# A few benefits of this approach are:

	- You can work offline
	- You don't need a shared 'dev' bucket that everyone on your team uses
	- You can easily wipe & replace your local buckets
	- You don't need to worry about paying for AWS usage
	- You don't need to log into AWS 😛

# Initial Setup:
First, we'll need to install a few things.

Install Docker if you haven't already.
Install the AWS CLI. Even though we aren't going to be working with "real" AWS, we'll use this to talk to our local docker containers.
Install docker-compose
bash```
sudo pip install docker-compose
```
Make a few files. Create a new directory for your project, and within it:
bash```
touch docker-compose.yml && mkdir .localstack
```
Install boto3 lib:
bash```
sudo pip install boto3
```

# Docker Config:
You can run Localstack directly from the command line, but I like using Docker to keep it easy and clean. It's also nice because you don't need to worry about installing Localstack on your system. I prefer to use docker-compose to set this up. Here's the config:

```docker-compose.yml```

bash```
version: '3.2'
services:
  localstack:
    image: localstack/localstack:latest
    container_name: localstack_demo
    ports:
      - '4563-4584:4563-4584'
      - '8055:8080'
    environment:
      - SERVICES=s3
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
    volumes:
      - './.localstack:/tmp/localstack'
      - '/var/run/docker.sock:/var/run/docker.sock'
```

# Breaking some of these lines down:

image: localstack/localstack:latest
Use the latest Localstack image from Dockerhub

container_name: localstack_demo:
This gives our container a specific name that we can refer to later in the CLI.

ports: '4563-4584:4563-4584' and '8055:8080':
When your docker container starts, it will open up a few ports. The number on the left binds the port on your localhost to the port within the container, which is the number on the right. In most cases, these two numbers can be the same, i.e. 8080:8080. I often have some other things running on localhost:8080, so here, I've changed the default to 8055:8080. This means that when I connect to http://localhost:8055 within my app, it's going to talk to port 8080 on the container.

The line '4563-4584:4563-4584' does the same thing, but binds a whole range of ports. These particular port numbers are what Localstack uses as endpoints for the various APIs. We'll see more about this in a little bit.

```environment```
These are environment variables that are supplied to the container. Localstack will use these to set some things up internally:

SERVICES=s3: You can define a list of AWS services to emulate. In our case, we're just using S3, but you can include additional APIs, i.e. SERVICES=s3,lambda. There's more on this in the Localstack docs.
DEBUG=1: 🧻 Show me all of the logs!
DATA_DIR=/tmp/localstack/data: This is the directory where Localstack will save its data internally. More in this next:
volumes
'./.localstack:/tmp/localstack'

Remember when set up the DATA_DIR to be /tmp/localstack/data about 2 seconds ago? Just like the localhost:container syntax we used on the ports, this allows your containers to access a portion of your hard drive. Your computer's directory on the left, the container's on the right.

Here, we're telling the container to use our .localstack directory for its /tmp/localstack. It's like a symlink, or a magical portal, or something.

In our case, this makes sure that any data created by the container will still be present once the container restarts. Note that /tmp is cleared frequently and isn't a good place to store. If you want to put it in a more secure place

'/var/run/docker.sock:/var/run/docker.sock'
Starting our Container
Now that we have our docker-compose.yml in good shape, we can spin up the container: docker-compose up -d.

To make sure it's working, we can visit http://localhost:8055 to see Localstack's web UI. Right now it will look pretty empty

Similarly, our S3 endpoint http://localhost:4572 will show some basic AWS info

# Working with Localstack
AWS is now inside our computer and we have a local implementation of the S3 service.

Before we start uploading files, we need to create and configure a bucket. We'll do this using the AWS CLI that we installed earlier, using the ```--endpoint-url``` flag to talk to Localstack instead.

1. Create a bucket: ```aws --endpoint-url=http://localhost:4572 s3 mb s3://demo-bucket```
2. Attach an ACL to the bucket so it is readable: ```aws --endpoint-url=http://localhost:4572 s3api put-bucket-acl --bucket demo-bucket --acl public-read```

Now, when we visit the web UI(http://localhost:8055), we should see our bucket.


# Upload file to our bucket:
We will use the ```test-upload.jpg``` image for our demo

Execute the python script that will upload our test image:
```python s3_upload.py```

It will output tge URL of the uploaded image.
Copy the URL and paste it into your browser. The browser will immediately download the image.
