from telegram.ext import (
    ContextTypes,
)


def remove_job_by_name(
    context: ContextTypes.DEFAULT_TYPE,
    job_name: str
) -> bool:
    '''Remove o job pelo nome.
    '''

    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    print('current_jobs', current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        print('JOB REMOVIDO:', job.name)
        job.schedule_removal()

    return True
