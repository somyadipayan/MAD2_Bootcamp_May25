from .workers import celery

@celery.task
def add(a,b):
    return a+b
