import re

import aiohttp
from bs4 import BeautifulSoup

from utils.log import log


async def get_vacancy_details(url):
    recommended_job_regex = 'https:\/\/www\.linkedin\.com\/jobs\/collections\/recommended\/\?currentJobId=(\d+)'
    search_job_regex = 'https:\/\/www\.linkedin\.com\/jobs\/search\/\?currentJobId=(\d+)&?(.*)'
    job_details_class = 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'
    role_and_company_class = 'welcome-back-sign-in-form__subline'
    if (job_id := re.findall(recommended_job_regex, url)) or (job_id := re.findall(search_job_regex, url)[0]):
        url = f'https://www.linkedin.com/jobs/view/{job_id[0]}'
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url,
        ) as response:
            log.info('get_vacancy_text response', response.status)
            soup = BeautifulSoup(await response.text())
            job_details = soup.find(class_=job_details_class)
            role = soup.find(class_=role_and_company_class).find_all('b')[0]
            company_name = soup.find(class_=role_and_company_class).find_all('b')[1]
            return {
                'text': job_details.get_text().strip(),
                'company': (
                        (
                            company_name.get_text().strip() if company_name else None
                        ) or '<find company name in job text and paste it here>'
                ).strip(),
                'role': (
                        (
                            role.get_text().strip() if role else None
                        )
                        or '<find role name in job text and paste it here>'
                ).strip()
            }

