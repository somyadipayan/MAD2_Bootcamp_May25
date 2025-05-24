from datetime import timedelta
from .workers import celery
from models import *
from .mailer import send_email
from flask import render_template
from celery.schedules import crontab

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, monthly.s(), name='test')
    # sender.add_periodic_task(crontab(hour=10,minute=0), send_daily_reminders.s(), name="send daily reminders at 10 am")
    # sender.add_periodic_task(crontab(day_of_month=1,hour=10,minute=0), monthly.s(), name="send monthly reminders at 10 am")



@celery.task
def add(a,b):
    return a+b

@celery.task()
def send_issue_email(issue_id):
    issue = IssueHistory.query.get_or_404(issue_id)
    # Send email to user
    to = issue.user.email
    subject = f"Your issue for {issue.book.name} has been accepted"
    user_name = issue.user.name
    book_name = issue.book.name
    issue_date = issue.issue_date.strftime("%Y-%m-%d %H:%M")
    return_by = (issue.issue_date + timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
    html = render_template("issue_accepted.html", user_name=user_name, book_name=book_name, issue_date=issue_date, return_date=return_by)
    send_email(to=to, subject=subject, html=html)
    return "Email sent successfully"

@celery.task()
def send_daily_reminders():
    """
    Sends a reminder via mail to all the users who haven't loggedin since past 24 hours
    """
    twenty_four_hours_ago = datetime.now() - timedelta(hours=10)
    users = User.query.filter_by(librarian=False).filter(User.last_login < twenty_four_hours_ago).all()
    for user in users:
        html = render_template("daily_reminder.html", user_name=user.name)
        send_email(to=user.email, subject="Reminder: Login to your account", html=html)
    return f"Reminders sent successfully to {len(users)} users"


@celery.task
def monthly():
    today = datetime.today()
    start_date = today - timedelta(days=30)
    end_date = today

    past_month_issues = IssueHistory.query.filter(
        IssueHistory.issue_date.between(start_date, end_date)
    ).all()

    user_issues = {}
    for issue in past_month_issues:
        print(issue.return_date)
        user_id = issue.user_id
        if user_id not in user_issues:
            user_issues[user_id] = []
        user_issues[user_id].append(issue)

    for user_id, issues in user_issues.items():
        user = User.query.get(user_id)
        user_email_content = render_template(
            'monthly.html',
            user_issues={user_id: issues},
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            total_issues=len(issues),
        )
        send_email(user.email, 'Monthly Issue Report', html=user_email_content)