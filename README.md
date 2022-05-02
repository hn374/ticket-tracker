# ticket-tracker
A python script to run every 24 hours that sends me a text if I get any parking tickets in this Philadelphia area.

## Libraries and Languages Used
I used Selenium for the automation and web navigation, and Twilio in order to send me the texts. I used Python to develop the script.

## Reason:
I created this script because of an issue I had over quarantine. During the peak of the pandemic, I wasn't going outside much but one day I went outside to my car to find that I had 5 parking tickets from 5 consecutive days. I was angry because I thought I would get notified when I got the initial ticket, as I was not going outside at all so I wouldn't have known that I had tickets on my car. To solve this issue of not getting notified whenever I get a ticket, I created this Python script that inputs my license plate into the Philadelphia Parking Authority website to check if I have any outstanding tickets. Every time the script is run at midnight, I get a text indicating whether there are no tickets today or if I did get one.

Unfortunately, as of May 2022, the Philadelphia Parking Authority changed their website so that you need to input a citation number in order to check for tickets now instead of just the license plate.
