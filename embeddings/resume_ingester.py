import re

experiences_text = """
Company: CodeBlossom  
Period: January 2024 to Present  
Skills: LLMs, Vision, Speech detection and Generation, Python SDKs  
Projects:  
- Created an applied AI curriculum empowering women across countries; developed hands-on modules for vision/audio AI applications using AI APIs.  
- Conducted weekly mentorship sessions on real-world AI implementation.  

---

Company: Amazon Music  
Period: December 2021 to January 2024  
Skills: Python, AWS (Data Pipeline, DynamoDB, S3, Athena, Lambda, IAM Permissions, Redshift, Data Lake), GDPR Policies, Audio Processing  
Projects:  
- Implemented on-demand deletion requests DB archival for querying, reducing issue triaging time by 90%.  
- Developed an Access Control Platform for Redshift, managing permissions for 9000 datasets on a petabyte-scale database.  
- Implemented a GDPR-compliant data deletion system, reducing legal risks by 40%.  
- Led a winning team in the Amazon Music AI hackathon, designing a stack that created real-time Karaoke tracks; conducted AI adoption sessions.  

---

Company: Amazon Music  
Period: March 2020 to November 2021  
Skills: Python, AWS Airflow, Big Data, DevOps, AWS Redshift, SQL  
Projects:  
- Enabled multi-team tenancy on the Airflow big data orchestration platform, saving 2 developer months annually for 3 teams.  
- Provided scripts automation for ETL jobs management, enabling 1-click migration for 20+ teams.  

---

Company: Amazon Music  
Period: August 2018 to December 2019  
Skills: Scala, Apache Spark, SQL, Big Data, Test-Driven Development, Data Modeling, Python, Django  
Projects:  
- Re-designed Alexa's music requests dataset on Scala Spark pipeline, transforming millions of events daily for reporting and analytics.  
- Introduced Python automations managing a petabyte-scale Redshift cluster, increasing operational maintainability by 80%.  
- Mentored interns, assisting in designing an ETL lineage tracker.  

---

Company: Amazon Music  
Period: January 2017 to August 2018  
Skills: AWS Services, Java, Python, DynamoDB, S3, Chromaprint, Coral Framework, AWS Lambda, Scala, Redshift  
Projects:  
- Back-end developer for Delivery service to Amazon's flagship project, Live Audio Platform.  
- Created an algorithm for live audio comparison, enabling 100% coverage for real-time audio transcoding QA.  
- Developed workflows in Python to route iOS subscription events, facilitating Amazon Music's launch of subscriptions on iOS.  

---

Company: Amazon Web Services  
Period: June 2016 to December 2016  
Skills: Ruby on Rails, Java Spring  
Projects:  
- Streamlined procurement system and reduced operational cost by implementing an email parser module.  

---

Company: Amazon Magazines  
Period: January 2015 to December 2016  
Skills: Serverless AWS architecture, Java  
Projects:  
- Enhanced operational efficiency and security through the "HTTPS Everywhere" initiative.  
- Migrated the Magazines Retail page from a legacy platform to a modern Java-based platform.  

---

Company: Ericsson Global India Ltd.  
Period: January 2012 to December 2015  
Skills: Automated solutions, Database monitoring  
Projects:  
- Developed automated solutions for monthly health checks and database monitoring, reducing costs and dependency on DB vendors.  

"""

# Split the experiences into segments
experience_segments = experiences_text.strip().split('---')

# Define a function to parse each segment
def parse_experience(segment):
    company = re.search(r'Company: (.+?)\n', segment)
    period = re.search(r'Period: (.+?)\n', segment)
    skills = re.search(r'Skills: (.+?)\n', segment)
    projects = re.findall(r'- (.+?)\n', segment)
    
    company = company.group(1).strip() if company else ''
    period = period.group(1).strip() if period else ''
    skills = skills.group(1).strip() if skills else ''
    
    return company, period, skills, projects

# Parse each experience and store in a formatted manner
parsed_experiences = []
for segment in experience_segments:
    company, period, skills, projects = parse_experience(segment)
    # Append each project as a separate line
    for project in projects:
        parsed_experiences.append(f'{company} | {period} | {skills} | {project}')

# Print out the results in pipe-separated format, with each project on a new line
for experience in parsed_experiences:
    print(experience)