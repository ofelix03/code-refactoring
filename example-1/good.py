def _parse_email(self, email):
    company_website = self.env.user.company_id.website
    company_domain = None

    if not company_website:
        # return email or maybe raise an exception
        return email

    # use semantic names, avoid generic, ambiguous and misinforming names
    url_protocols = ['https://www.', 'http://www.', 'https://', 'http://']

    for protocol in url_protocols:
        domain_split = company_website.split(protocol)
        if len(domain_split) == 2:
            company_domain = domain_split[1]

    return ''.join([email, '@', company_domain])


