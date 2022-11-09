# Questionnnaire Data Analyses
Questionnaire data analyses code from ART piplot analyses

# Description

Questionnaire data analyses code from ART pilot analyses.

## Data
The data is stored as .csv.gz. format, which the I/O module reads and convert into a Spark DataFrame for further processing.

## Features
### QuestionnaireNotificationResponseLatency

The time it took for participants to start filling out the questionnaires after receiving the notification.
### QuestionnaireCompletionTime

The time it took for participants to finish the questionnaires after starting them.

## Output

The output is 2 csv files`questionnaire_completion_time.csv` and `questionnaire_notification_response_latency.csv`.