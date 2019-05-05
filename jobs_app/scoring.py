edu_score = {
    1: 0.2,
    2: 0.2,
    3: 0.3,
    4: 0.6,
    5: 0.9,
}

tier1_colleges = [
    'indian institute of technology',
    'national institute of technology',
    'birla institute of technology',
    'delhi technical university',
    'indian institute of information technology',
]

tier2_colleges = [
    'vellore institute of technology',
    'manipal universiy',
    'thapar',
]

def _college_score(education):
    if education.level > 2:
        if any(coll in education.college.lower() for coll in tier1_colleges):
            return 0.9
        elif any(coll in education.college.lower() for coll in tier2_colleges):
            return 0.6
        else:
            return 0.3
    return 0

def _percent_score(education):
    if education.level in [1,2]:
        if education.percent >=85:
            return 0.9
        elif 70 <= education.percent < 85:
            return 0.6
        elif 60 <= education.percent < 70:
            return 0.3
        return 0
    
    elif education.level in [3,4,5]:
        if education.percent >=75:
            return 0.9
        elif 65 <= education.percent < 75:
            return 0.6
        elif 60 <= education.percent < 65:
            return 0.3
        return 0
    
    return 0

def get_score_for_user_application(user, job_application):
    score = 0.0
    # score the maximum education level
    edu = None
    max_edu_lvl = 0
    for edu in user.education_set.all():
        if edu.level > max_edu_lvl:
            max_edu = edu
            max_edu_lvl = edu.level
    
    if edu:
        score += edu_score[edu.level]
        score += _percent_score(edu)
        score += _college_score(edu)
    
    # score the experience years

    exp_years = 0
    for exp in user.experience_set.all():
        exp_years += exp.experience_years
    
    if exp_years >= 5:
        score += 0.9
    elif 2 <= exp_years < 5:
        score += 0.6
    elif exp_years == 1:
        score += 0.3
    
    # score on number of skills in job application
    skills = job_application.skills.split(',')
    if len(skills)>5:
        score += 0.9
    elif 3 <= len(skills) <=5:
        score += 0.6
    elif 1 <= len(skills) <=2:
        score += 0.3
    
    # score on video
    if job_application.video_token:
        score += 0.9
    
    # score on country
    if user.candidateprofile.country.lower() == "india":
        score += 0.9
    
    return float("{0:.2f}".format(score))