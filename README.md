# penn_jobs
This repostiory contains Dockerized Python scripts that use Selenium and Firefox to scrape Pennsylvania-based jobs of interest based on keywords and then emails the results.

<b>Instructions:</b>

1. Install Docker on your system.

2. Clone the repository.

3. Build the Docker image using the following command:
`docker build -t penn-jobs .`

4. Run the Docker container using the following command:
`docker run --name penn-jobs-container --env-file ./.env penn-jobs`

5. After initially running the Docker container, you can run the container using the following command:
`docker start -a penn-jobs-container`

<b>Sending Emails using Python</b>

GeeksforGeeks has <a href='https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/'>instructions</a> for sending emails using SMTP (Simple Mail Transfer Protocol). I store the sender, receiver, and sender password in a .env file on my system. Docker will read the .env file from the host machine and inject those variables into the container's environment before your Python scripts start.

<h2>Schedule Python Scripts to Run Daily</h2>

I have scheduled these Dockerized scripts to run daily on my system by running `docker start penn-jobs-containers` at a specific time. Please see <a href='https://www.geeksforgeeks.org/schedule-python-script-using-windows-scheduler/'>GeeksforGeeks instructions</a> for one way to do this.

<h2>Example Output</h2>

The user should receive an email with results similar to the below picture.
<img src="https://raw.githubusercontent.com/theapphiker/penn-jobs/refs/heads/main/example_output.png" alt="example output">

