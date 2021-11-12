# ClamNotif: A tool to send you ClamAV notifications

*ClamNotif*, a.k.a *ClamAV Notification*, is a handy and simple tool written in Python, which is able to forward notifications to different recipients categorised by two severity levels of the regular health reports produced by `clamscan` bundled with the [ClamAV](https://www.clamav.net/) antivirus engine.

## What challenge we had faced

We, [PiSoft Company Ltd.](http://www.pisoft.com.mo/), is a software company based in [Macao S.A.R](https://www.gov.mo/en/). For more than a decade, we have been developing , operating and maintaining software systems for many clients. For system security, we use ClamAV to scan the server regularly.

Usually, that is done in the form of a daily heath check on the server. Because ClamAV is an antivirus engine __only__, in order to make our operation as automatic as possible, we have to find a solution to forward those health reports automatically.

As part of our daily operations, if ClamAV doesn't find any thing infected, a health report should be forwarded to our maintenance team as a __heart-beating__ signal. This is quite important, especially during the __pilot period__, which is the very beginning of a new system running in Production.

On the other hand, if ClamAV finds some files infected, the health report shall be forwarded to our maintenance team as well as the *representative* of our client as an __alert__.

We googled for a solution with no luck, only some pieces of bash scripts cooperating with `mailx` available. Perhaps, building a tool ourselves for our requirement seems *unavoidable*.

## Installation

First of all, we can install ClamNotif by

```console
$ pip3 install clamnotif
```

let's check if it works properly

```console
$ python3 -m clamnotif
```

We should see

```console
$ python3 -m clamnotif
Welcome for using ClamNotif v0.1.0 brought to you by PiSoft Company Ltd.
Usage: python3 -m clamnotif [--test-smtp|--check-report]
```

## Configuration

### Prepare Our Configurations
The configuration file of ClamNotif is an *ini* file designed with intuitive variable names. Please make sure to save the configuration file as `~/.clamnotif/clamnotif.cfg`.

ClamNotif *always* reads all configurations under the home folder of the current user. Thus the __read permission__ of the configuration file needs to be granted to ClamNotif, which should be the default in most cases.

Once our configuration completes, please make sure the *ClamAVReportFolder* as well as the files inside the folder can be read by the current user. In the following case, we have to check the directory `~/.ClamAV/daily/`.

When the system is getting more and more stable, a daily notification would not be necessary. We can fine-tune how often a heart-beat is sent by setting *HeartbeatDayGap*. In the following example, suppose ClamNotif forwarded a heart-beat on 17/Apr, the next heart-beat would be sent on 19/Apr, i.e., __2 days__ later. This value has no impact on the sending of alerts. Once an alert is detected, it will be sent to the recipients immediately.

```ini
[SMTP]
SMTPServerHost = smtp.gmail.com
SMTPServerPort = 465
SMTPTLSEnabled = false

[Notification]
SenderAddress = foo@gmail.com
SenderPasswd = $@SendPwd
AlertSubject = My System Antivirus Notification - Alert !!!
AlertReceiverAddresses = alice@gmail.com,robert@gmail.com,sysadmin@gmail.com
HeartbeatSubject = My System Antivirus Heartbeating Notification
HeartbeatReceiverAddresses = sysadmin@gmail.com
HeartbeatDayGap = 2

[ClamAV]
ClamAVReportFolder = ~/.ClamAV/daily/
```
### Test Our Configurations
Let's send a testing email to all recipients defined in the configuration file above by turning on the flag `--test-smtp`. Check our email box to see if we can receive the email for testing.

```console
$ python3 -m clamnotif --test-smtp
Successfully sent a testing email with title 'ClamNotif Testing' to foo@gmail.com and alice@gmail.com,robert@gmail.com,sysadmin@gmail.com.
```
If it works, we can go further. The flag `--check-report` tells ClamNotif to check the *ClamAVReportFolder* and to send a notification to the appropriate recipients.
```console
$ python3 -m clamnotif --check-report
[clamnotif] 2021-11-12 19:39:47 looking up reports from /Users/developer/.clamnotif/ClamAV/daily/ ..
.
[clamnotif] 2021-11-12 19:39:47 no files infected. Try sending a heartbeat...
[clamnotif] 2021-11-12 19:39:47 no heartbeat send. should wait for 1 more day(s).
[clamnotif] 2021-11-12 19:39:47 done.
```
`python3 -m clamnotif --check-report` is the most common usage of ClamNotif.

## Run ClamNotif Daily
We are able to run `clamnotif` regularly by registering it as a schedule job with `crontab`.

Here is an article [Complete Beginners Tutorial](https://linuxhint.com/cron_jobs_complete_beginners_tutorial/) for your reference.

## Bash Scripts

There are some handy *bash* scripts which we use to wrap `clamscan` and `clamnotif` under the `bash` folder. Just see if they are helpful.

## Acknowledgement

We built this tool in memory of *Mr Brain Iu*, who was a visionary in the field of software development and had been promoting the Python Programming Language in Macao long before it became all the rage .

Hope you find it useful. Drop me a line if you like it!
