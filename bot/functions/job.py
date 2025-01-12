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
    print('CURRENT_JOBS:', current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        print('JOB REMOVIDO:', job.name)
        job.schedule_removal()

    return True


def job_exists(context: ContextTypes.DEFAULT_TYPE, job_name: str) -> bool:
    '''Verifica se o job existe.
    Retorna True se o job existir, False caso contrário.
    '''

    current_jobs = context.job_queue.get_jobs_by_name(job_name)

    return bool(current_jobs)
