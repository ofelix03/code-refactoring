"""
Code Quality Issues:

-> unnecessary conditional checks
-> complex logic, it can be simplified to improve clarity
"""


def _parse_email(self, email):
    email_split = email.split("@")
    if len(email_split) == 1:
        company = self.env.user.company_id

    if all([company, company.website]):
        domain = company.website

    blacklist = ["https://www.", "http://www.", "https://", "http://"]
    for i in blacklist:
        domain_split = domain.split(i)
        if len(domain_split) == 2:
            domain = domain_split.pop()
            email = "".join([email, "@", domain])

        return email