"""
Code Quality Improvements:

-> removed unnecessary coditional checks
-> simplified logic, by resorting to using a library suitable for the job (regex)
"""

import re


def _parse_email(self, email):
    """
    Simplified further by taking some time and effort to use regular expressions (re):
    """
    company_website = self.env.user.company_id.website
    company_domain = None

    if not company_website:  # we can remove this and code will still work just fine
        return email  # return email or maybe raise an exception here

    company_website_split = re.split('^https://w+.', company_website)
    if len(company_website_split) == 2:
        company_domain = company_website_split[1]

    return "".join([email, '@', company_domain])