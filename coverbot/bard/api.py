import asyncio
import re

from bardapi import Bard

from text import t
from utils import config


async def get_cover_letter_text(vacancy_details, user_details):
    prompt = t('main.cover_prompt', 'en').format(
        user_name=user_details.get('user_name') or '',
        years_of_experience=user_details.get('years_of_experience') or '<find necessary years of experience and paste it here>',
        last_position=user_details.get('last_position') or '',
        skills=user_details.get('skills') or '<find necessary skills in job text and paste them here comma-separated>',
        sphere_of_work=user_details.get('sphere_of_work') or '<find sphere of work in job text and paste it here>',
        vacancy_position=vacancy_details['role'],
        company_name=vacancy_details['company'],
        job_text=vacancy_details['text'],
    ).strip()
    # removing top level domain
    prompt = re.sub('([a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9])(\.[a-zA-Z]{2,})', '\\1', prompt)

    loop = asyncio.get_event_loop()
    bard = Bard(token=config.BARD_TOKEN)
    response = await loop.run_in_executor(None, bard.get_answer, prompt)
    return response.get('content')

